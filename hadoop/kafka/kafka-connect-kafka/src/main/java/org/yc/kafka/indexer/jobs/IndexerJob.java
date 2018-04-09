package org.yc.kafka.indexer.jobs;

import java.nio.ByteBuffer;
import java.util.Iterator;
import java.util.concurrent.Callable;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.yc.kafka.indexer.FailedEventsLogger;
import org.yc.kafka.indexer.exception.IndexerESNotRecoverableException;
import org.yc.kafka.indexer.exception.IndexerESRecoverableException;
import org.yc.kafka.indexer.exception.KafkaClientNotRecoverableException;
import org.yc.kafka.indexer.exception.KafkaClientRecoverableException;
import org.yc.kafka.indexer.service.IMessageHandler;
import org.yc.kafka.indexer.service.KafkaClientService;

import kafka.common.ErrorMapping;
import kafka.javaapi.FetchResponse;
import kafka.javaapi.message.ByteBufferMessageSet;
import kafka.message.Message;
import kafka.message.MessageAndOffset;

public class IndexerJob implements Callable<IndexerJobStatus> {

    private static final Logger logger = LoggerFactory.getLogger(IndexerJob.class);
    private IMessageHandler messageHandlerService;
	public KafkaClientService kafkaClient;
    private long offsetForThisRound;
    private long nextOffsetToProcess;
    private boolean isStartingFirstTime;
    private final int currentPartition;
    private final String currentTopic;
    private IndexerJobStatus indexerJobStatus;
    private volatile boolean shutdownRequested = false;
    private int consumerSleepBetweenFetchsMs;
    // this property can be set to TRUE to enable logging timings of the event processing
    private boolean isPerfReportingEnabled = false;
    // this property can be set to TRUE to skip indexing into ES
    private boolean isDryRun = false;
   
    public IndexerJob(String topic, IMessageHandler messageHandlerService,
                      KafkaClientService kafkaClient, int partition, int consumerSleepBetweenFetchsMs)
            throws Exception {
        this.currentPartition = partition;
        this.currentTopic = topic;
        this.messageHandlerService = messageHandlerService;
        indexerJobStatus = new IndexerJobStatus(-1L, IndexerJobStatusEnum.Created, partition);
        isStartingFirstTime = true;
        this.consumerSleepBetweenFetchsMs = consumerSleepBetweenFetchsMs;
        this.kafkaClient = kafkaClient;
        indexerJobStatus.setJobStatus(IndexerJobStatusEnum.Initialized);
        logger.info("Created IndexerJob for topic={}, partition={};  messageHandlerService={}; kafkaClient={}",
                currentTopic, partition, messageHandlerService, kafkaClient);
    }

    // a hook to be used by the Manager app to request a graceful shutdown of the job
    public void requestShutdown() {
        shutdownRequested = true;
    }

    public IndexerJobStatus call() {
        indexerJobStatus.setJobStatus(IndexerJobStatusEnum.Started);
        while (!shutdownRequested) {
            try {
                if (Thread.currentThread().isInterrupted()) {
                    Thread.currentThread().interrupt();
                    throw new InterruptedException(
                            "Caught interrupted event in IndexerJob for partition=" + currentPartition + " - stopping");
                }
                logger.debug("******* Starting a new batch of events from Kafka for partition {} ...", currentPartition);
                processMessagesFromKafka();
                indexerJobStatus.setJobStatus(IndexerJobStatusEnum.InProgress);
                Thread.sleep(consumerSleepBetweenFetchsMs);
                logger.debug("Completed a round of indexing into ES for partition {}", currentPartition);
            } catch (IndexerESNotRecoverableException | KafkaClientNotRecoverableException e) {
                indexerJobStatus.setJobStatus(IndexerJobStatusEnum.Failed);
                stopClients();
                break;
            } catch (InterruptedException e) {
                indexerJobStatus.setJobStatus(IndexerJobStatusEnum.Stopped);
                stopClients();
                break;
            } catch (Exception e) {
                if (!reinitKafkaSucessful(e)) {
                    break;
                }

            }
        }
        logger.warn("******* Indexing job was stopped, indexerJobStatus={} - exiting", indexerJobStatus);
        return indexerJobStatus;
    }

    /**
     * Try to re-init Kafka connection first - in case the leader for this partition
     * has changed due to a Kafka node restart and/or leader re-election
     * TODO decide if we want to re-try forever or fail here
     * TODO introduce another JobStatus to indicate that the job is in the REINIT state - if this state can take awhile
     * If Exception is thrown dureing reinit stop the job and fix the issue manually,
     * It is better to monitor the job externally
     * via Zabbix or the likes - rather then keep failing [potentially] forever
     * @param e
     * @return
     */
    protected boolean reinitKafkaSucessful(Exception e) {
        // we will treat all other Exceptions as recoverable for now
        logger.error("Exception when starting a new round of kafka Indexer job for partition {} - will try to re-init Kafka ",
                currentPartition, e);
        try {
            kafkaClient.reInitKafka();
            return true;
        } catch (Exception e2) {
            logger.error("Exception when starting a new round of kafka Indexer job, partition {}, exiting: "
                    + e2.getMessage(), currentPartition);
            indexerJobStatus.setJobStatus(IndexerJobStatusEnum.Failed);
            stopClients();
            return false;
        }
    }

    /**
     * save nextOffsetToProcess in temporary field,and save it after successful execution of indexIntoESWithRetries method
     * @throws KafkaClientRecoverableException 
     * @throws IndexerESNotRecoverableException 
     * @throws InterruptedException 
     * @throws KafkaClientNotRecoverableException 
     * @throws Exception
     */
    public void processMessagesFromKafka() throws KafkaClientRecoverableException, InterruptedException, IndexerESNotRecoverableException, KafkaClientNotRecoverableException {
        long jobStartTime = System.currentTimeMillis();
        determineOffsetForThisRound();
        ByteBufferMessageSet byteBufferMsgSet = getMessageAndOffsets(jobStartTime);
        if (byteBufferMsgSet == null) 
        	return;

        logger.debug("Starting to process messages from the current batch for partition {}", currentPartition);
        BatchCreationResult batchCreationResult = addMessagesToBatch(jobStartTime, byteBufferMsgSet);
        long proposedNextOffsetToProcess = batchCreationResult.getOffsetOfNextBatch();
        boolean batchCreationSuccessful = batchCreationResult.isBatchCreationSuccessful();
        if (!batchCreationSuccessful) {
        	// this is the case when ALL messages in the batch failed to be added to the ES 
        	// index builders due to parsing/mapping/Mongo issues - skip the whole batch
            nextOffsetToProcess = proposedNextOffsetToProcess;
        	commitOffSet(jobStartTime);
        	return;
        }
        if (isDryRun) {
            logger.info("**** This is a dry run, NOT committing the offset in Kafka nor posting to ES for partition {}****", currentPartition);
            return;
        }
        boolean moveToNextBatch = postBatchToKafka(proposedNextOffsetToProcess);
        if (moveToNextBatch) {
            nextOffsetToProcess = proposedNextOffsetToProcess;
            commitOffSet(jobStartTime);
        }
    }

    /**
     * 1) Do not handle exceptions here - throw them out to the call() method which will decide if re-init
     * @param jobStartTime
     * @throws KafkaClientRecoverableException
     */
    private void commitOffSet(long jobStartTime) throws KafkaClientRecoverableException {
        if (isPerfReportingEnabled) {
            long timeAfterEsPost = System.currentTimeMillis();
            logger.debug("Approx time to post of ElasticSearch: {} ms for partition {}",
                    (timeAfterEsPost - jobStartTime), currentPartition);
        }
        logger.info("Committing offset={} for partition={}", nextOffsetToProcess, currentPartition);
        try {
            kafkaClient.saveOffsetInKafka(nextOffsetToProcess, ErrorMapping.NoError());
        } catch (Exception e) {
            logger.error("Failed to commit nextOffsetToProcess={} after processing and posting to ES for partition={}: ",
                    nextOffsetToProcess, currentPartition, e);
            throw new KafkaClientRecoverableException("Failed to commit nextOffsetToProcess=" + nextOffsetToProcess +
                    " after processing and posting to ES; partition=" + currentPartition + "; error: " + e.getMessage(), e);
        }

        if (isPerfReportingEnabled) {
            long timeAtEndOfJob = System.currentTimeMillis();
            logger.info("*** This round of IndexerJob took about {} ms for partition {} ",
                    (timeAtEndOfJob - jobStartTime), currentPartition);
        }
        logger.info("*** Finished current round of IndexerJob, processed messages with offsets [{}-{}] for partition {} ****",
                offsetForThisRound, nextOffsetToProcess, currentPartition);
    }

    /**
     * TODO: we are loosing the ability to set Job's status to HANGING in case ES is unreachable and
     * re-connect to ES takes awhile ... See if it is possible to re-introduce it in another way;
     * ElasticsearchException handling:
     *      we are assuming that these exceptions are data-specific - continue and commit the offset,
     *      but be aware that ALL messages from this batch are NOT indexed into ES
     * IndexerESException handling:
     * 		we are assuming that these exceptions are transient , and the batch processing can be re-tried
     * 
     * @param proposedNextOffsetToProcess
     * @return
     * @throws IndexerESNotRecoverableException 
     * @throws InterruptedException 
     * @throws Exception
     */
	protected boolean postBatchToKafka(long proposedNextOffsetToProcess) throws InterruptedException, IndexerESNotRecoverableException  {
    	boolean moveToNextBatch = true;
        try {
            logger.info("About to post messages to ElasticSearch for partition={}, offsets {}-->{} ",
                    currentPartition, offsetForThisRound, proposedNextOffsetToProcess - 1);
            messageHandlerService.postToKafka();
        } catch (IndexerESRecoverableException e) {
            logger.error("Error posting messages to Elastic Search for offsets {}-->{} " +
                            " in partition={} - will re-try processing the batch; error: {}",
                    offsetForThisRound, proposedNextOffsetToProcess - 1, currentPartition, e.getMessage());
            moveToNextBatch = false;
        } 
        return moveToNextBatch;
    }

	protected BatchCreationResult addMessagesToBatch(long jobStartTime, ByteBufferMessageSet byteBufferMsgSet){
        int numProcessedMessages = 0;
        int numSkippedIndexingMessages = 0;
        int numMessagesInBatch = 0;
        long offsetOfNextBatch = 0;
        boolean batchCreationSuccessful = true;
        Iterator<MessageAndOffset> messageAndOffsetIterator = byteBufferMsgSet.iterator();

        while (messageAndOffsetIterator.hasNext()) {
            numMessagesInBatch++;
            MessageAndOffset messageAndOffset = messageAndOffsetIterator.next();
            offsetOfNextBatch = messageAndOffset.nextOffset();
            Message message = messageAndOffset.message();
            long thisMessageOffset = messageAndOffset.offset();
            ByteBuffer payload = message.payload();
            byte[] bytesMessage = new byte[payload.limit()];
            payload.get(bytesMessage);
            try {
                byte[] transformedMessage = messageHandlerService.transformMessage(bytesMessage, thisMessageOffset);
                messageHandlerService.addMessageToBatch(transformedMessage, thisMessageOffset);
                numProcessedMessages++;
            } catch (Exception e) {
                numSkippedIndexingMessages++;
                String msgStr = new String(bytesMessage);
                logger.error("ERROR processing message at offset={} - skipping it: {}", thisMessageOffset, msgStr, e);
                FailedEventsLogger.logFailedToTransformEvent(thisMessageOffset, e.getMessage(), msgStr);
            }
        }
        logger.info("Total # of messages in this batch: {}; " +
                        "# of successfully transformed : {}; # of skipped : {}; offsetOfNextBatch: {}; for partition={}",
                numMessagesInBatch, numProcessedMessages, numSkippedIndexingMessages, offsetOfNextBatch, currentPartition);

        if (isPerfReportingEnabled) {
            long timeAtPrepareES = System.currentTimeMillis();
            logger.debug("Completed preparing for post to ElasticSearch. Approx time taken: {}ms for partition {}",
                    (timeAtPrepareES - jobStartTime), currentPartition);
        }
        if (numMessagesInBatch > 0 && numProcessedMessages == 0 ) {
        	logger.error("All messages in the batch failed to be added to the index builders - skip this batch");
        	batchCreationSuccessful = false;
        }
        return new BatchCreationResult(offsetOfNextBatch, batchCreationSuccessful);
    }

    /**
     * 1) Exceptions will be taken care of in the computeOffset() and thrown to call()method
     *      which will decide if re-init
     * 2) Roll back to the earliest offset in the case of OffsetOutOfRange
     * CORNER CASE :
     * TODO re-review this logic
     *  check a corner case when consumer did not read any events form Kafka from the last current offset -
     *  but the latestOffset reported by Kafka is higher than what consumer is trying to read from;
     * @param jobStartTime
     * @return
     * @throws KafkaClientRecoverableException 
     * @throws KafkaClientNotRecoverableException 
     * @throws Exception
     */
    protected ByteBufferMessageSet getMessageAndOffsets(long jobStartTime) throws KafkaClientRecoverableException, KafkaClientNotRecoverableException {
        FetchResponse fetchResponse = kafkaClient.getMessagesFromKafka(offsetForThisRound);
        ByteBufferMessageSet byteBufferMsgSet = null;
        if (fetchResponse.hasError()) {
            short errorCode = fetchResponse.errorCode(currentTopic, currentPartition);
            Long newNextOffsetToProcess = kafkaClient.handleErrorFromFetchMessages(errorCode, offsetForThisRound);
            if (newNextOffsetToProcess != null) {
                nextOffsetToProcess = newNextOffsetToProcess;
            }
            return null;
        }

        byteBufferMsgSet = fetchResponse.messageSet(currentTopic, currentPartition);
        if (isPerfReportingEnabled) {
            long timeAfterKafkaFetch = System.currentTimeMillis();
            logger.debug("Completed MsgSet fetch from Kafka. Approx time taken is {} ms for partition {}",
                    (timeAfterKafkaFetch - jobStartTime), currentPartition);
        }
        if (byteBufferMsgSet.validBytes() <= 0) {
            logger.debug("No events were read from Kafka - finishing this round of reads from Kafka for partition {}", currentPartition);
            long latestOffset = kafkaClient.getLastestOffset();
            if (latestOffset != offsetForThisRound) {
                logger.warn("latestOffset={} for partition={} is not the same as the offsetForThisRound for this run: {}" +
                                " - returning; will try reading messages form this offset again ",
                        latestOffset, currentPartition, offsetForThisRound);
                // TODO decide if we really need to do anything here - for now:
            }
            byteBufferMsgSet = null;
        }
        return byteBufferMsgSet;
    }

    /**
     * 1) Do not read offset from Kafka after each run - instead from memory
     * 2) Do not handle exceptions here - they will be taken care of in the computeOffset()
     *     If this is the only thread that is processing data from this partition
     * TODO  see if we are doing this too early - before we actually commit the offset
     * @throws KafkaClientNotRecoverableException 
     * @throws KafkaClientRecoverableException 
     * @throws Exception
     */
    protected void determineOffsetForThisRound() throws KafkaClientRecoverableException, KafkaClientNotRecoverableException {

        if (!isStartingFirstTime) {
            offsetForThisRound = nextOffsetToProcess;
        } else {
            indexerJobStatus.setJobStatus(IndexerJobStatusEnum.InProgress);
            offsetForThisRound = kafkaClient.computeInitialOffset();
            isStartingFirstTime = false;
            nextOffsetToProcess = offsetForThisRound;
        }
        indexerJobStatus.setLastCommittedOffset(offsetForThisRound);
        return;
    }

    public void stopClients() {
        logger.info("About to stop Kafka client for topic {}, partition {}", currentTopic, currentPartition);
        if (kafkaClient != null)
            kafkaClient.close();
        logger.info("Stopped Kafka client for topic {}, partition {}", currentTopic, currentPartition);
    }

    public IndexerJobStatus getIndexerJobStatus() {
        return indexerJobStatus;
    }

	public void setPerfReportingEnabled(boolean isPerfReportingEnabled) {
		this.isPerfReportingEnabled = isPerfReportingEnabled;
	}

	public void setDryRun(boolean isDryRun) {
		this.isDryRun = isDryRun;
	}
	
	public class BatchCreationResult {
		private long offsetOfNextBatch;
		private boolean batchCreationSuccessful;
		
		public BatchCreationResult(long offsetOfNextBatch, boolean batchCreationSuccessful){
			this.offsetOfNextBatch = offsetOfNextBatch;
			this.batchCreationSuccessful = batchCreationSuccessful;
		}

		public long getOffsetOfNextBatch() {
			return offsetOfNextBatch;
		}

		public boolean isBatchCreationSuccessful() {
			return batchCreationSuccessful;
		}
		
	}

   public void setOffsetForThisRound(long offsetForThisRound) {
		this.offsetForThisRound = offsetForThisRound;
	}

	public void setNextOffsetToProcess(long nextOffsetToProcess) {
		this.nextOffsetToProcess = nextOffsetToProcess;
	}

	
}
