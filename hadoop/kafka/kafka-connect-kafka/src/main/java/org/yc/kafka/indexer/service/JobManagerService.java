package org.yc.kafka.indexer.service;

import com.google.common.util.concurrent.ThreadFactoryBuilder;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Service;
import org.yc.kafka.indexer.jobs.IndexerJob;
import org.yc.kafka.indexer.jobs.IndexerJobStatus;

import javax.annotation.PreDestroy;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

/**
 * Created by dhyan on 1/28/16.
 */
@Service
public class JobManagerService {
    private static final Logger logger = LoggerFactory.getLogger(JobManagerService.class);
    private static final String KAFKA_CONSUMER_STREAM_POOL_NAME_FORMAT = "kafka-indexer-thread-%d";
    
    @Autowired
    private ApplicationContext indexerContext;
    private ExecutorService executorService;
    @Value("${consumer.topic:my_log_topic}")
    private String topic;

    private int numOfPartitions;
    @Value("${firstPartition:0}")
    private int firstPartition;
    @Value("${lastPartition:3}")
    private int lastPartition;
    // Wait time in MS between consumer job rounds
    @Value("${consumerSleepBetweenFetchsMs:100}")
    private int consumerSleepBetweenFetchsMs;
    //timeout in seconds before force-stopping Indexer app and all indexer jobs
    @Value("${appStopTimeoutSeconds:10}")
    private int appStopTimeoutSeconds;
    // if set to TRUE - enable logging timings of the event processing
    @Value("${isPerfReportingEnabled:false}")
    private boolean isPerfReportingEnabled;
    // if set to TRUE - skip indexing into ES
    @Value("${isDryRun:false}")
   private boolean isDryRun;

    private ConcurrentHashMap<Integer, IndexerJob> indexerJobs;
    @SuppressWarnings("unused")
	private List<Future<IndexerJobStatus>> indexerJobFutures;



    public void processAllThreads() throws Exception{
        numOfPartitions =(lastPartition-firstPartition)+1;
        ThreadFactory threadFactory = new ThreadFactoryBuilder().setNameFormat(KAFKA_CONSUMER_STREAM_POOL_NAME_FORMAT).build();
        executorService = Executors.newFixedThreadPool(numOfPartitions, threadFactory);
        indexerJobs = new ConcurrentHashMap<>();
        // create as many IndexerJobs as there are partitions in the events topic
        // first create all jobs without starting them - to make sure they can init all resources OK
        try {
            for (int partition=firstPartition; partition<=lastPartition; partition++){
                logger.info("Creating IndexerJob for partition={}", partition);
                IMessageHandler messageHandlerService = (IMessageHandler)indexerContext.getBean("messageHandler");                
                KafkaClientService kafkaClientService = (KafkaClientService)indexerContext.getBean("kafkaClientService", partition);
                IndexerJob pIndexerJob = new IndexerJob(
                	topic, messageHandlerService, kafkaClientService, partition, consumerSleepBetweenFetchsMs);
                pIndexerJob.setDryRun(isDryRun);
                pIndexerJob.setPerfReportingEnabled(isPerfReportingEnabled);
                indexerJobs.put(partition, pIndexerJob);
            }
        } catch (Exception e) {
            logger.error("ERROR: Failure creating a consumer job, exiting: ", e);
            // if any job startup fails - abort;
            throw e;
        }
        // now start them all
        indexerJobFutures = executorService.invokeAll(indexerJobs.values());
    }

    public List<IndexerJobStatus> getJobStatuses(){
        List <IndexerJobStatus> indexerJobStatuses = new ArrayList<IndexerJobStatus>();
        for (IndexerJob indexerJob: indexerJobs.values()){
            indexerJobStatuses.add(indexerJob.getIndexerJobStatus());
        }
        return indexerJobStatuses;
    }

    @PreDestroy
    public void stop() {
        logger.info("About to stop all consumer jobs ...");
        if (executorService != null && !executorService.isTerminated()) {
            try {
                executorService.awaitTermination(appStopTimeoutSeconds, TimeUnit.SECONDS);
                logger.info("executorService threads stopped ");
            } catch (InterruptedException e) {
                logger.error("ERROR: failed to stop all consumer jobs due to InterruptedException: ", e);
            }
        }
        logger.info("Stop() finished");
    }

}
