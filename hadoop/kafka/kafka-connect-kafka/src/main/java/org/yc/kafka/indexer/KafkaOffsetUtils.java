package org.yc.kafka.indexer;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.springframework.stereotype.Service;

import com.google.common.collect.ImmutableMap;

import kafka.api.PartitionOffsetRequestInfo;
import kafka.cluster.Broker;
import kafka.common.TopicAndPartition;
import kafka.javaapi.OffsetRequest;
import kafka.javaapi.OffsetResponse;
import kafka.javaapi.PartitionMetadata;
import kafka.javaapi.TopicMetadata;
import kafka.javaapi.TopicMetadataRequest;
import kafka.javaapi.TopicMetadataResponse;
import kafka.javaapi.consumer.SimpleConsumer;

@Service
public class KafkaOffsetUtils {
	private static final Logger logger = LoggerFactory.getLogger(KafkaOffsetUtils.class);
	    
    @Autowired
    private ApplicationContext indexerContext;
    @Value("${consumer.topic:my_log_topic}")
    private String topic;
    @Value("${kafkaBrokersList:localhost:9092}")
    private String kafkaBrokersList;
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

	public void processAllThreads() throws Exception{
		logger.info("================TopicMetadataResponse: ===================\n{}",getTopicOffsets(kafkaBrokersList, topic));
//        try {
//            for (int partition=firstPartition; partition<=lastPartition; partition++){
//                KafkaClientService kafkaClientService = (KafkaClientService)indexerContext.getBean("kafkaClientService", partition);
//                logger.info("topic: {}, partition: {}, offset: {}", topic, partition, kafkaClientService.fetchCurrentOffsetFromKafka());
//            }
//        } catch (Exception e) {
//            logger.error("ERROR: Failure creating a consumer job, exiting: ", e);
//            throw e;
//        }
    }

	public static Map<TopicAndPartition, Long> getTopicOffsets(String brokers, String topic) {
		Map<TopicAndPartition, Long> retVals = new HashMap<TopicAndPartition, Long>();

		for (String broker : brokers.split(",")) {
			SimpleConsumer simpleConsumer = new SimpleConsumer(broker.split(":")[0], Integer.valueOf(broker.split(":")[1]), 10000, 1024, "consumer");
			TopicMetadataRequest topicMetadataRequest = new TopicMetadataRequest(Arrays.asList(topic));
			TopicMetadataResponse topicMetadataResponse = simpleConsumer.send(topicMetadataRequest);

			for (TopicMetadata metadata : topicMetadataResponse.topicsMetadata()) {
				for (PartitionMetadata part : metadata.partitionsMetadata()) {
					Broker leader = part.leader();
					if (leader != null) {
						TopicAndPartition topicAndPartition = new TopicAndPartition(topic, part.partitionId());
						PartitionOffsetRequestInfo partitionOffsetRequestInfo = new PartitionOffsetRequestInfo(kafka.api.OffsetRequest.LatestTime(), 10000);
						OffsetRequest offsetRequest = new OffsetRequest(ImmutableMap.of(topicAndPartition, partitionOffsetRequestInfo),
								kafka.api.OffsetRequest.CurrentVersion(), simpleConsumer.clientId());
						OffsetResponse offsetResponse = simpleConsumer.getOffsetsBefore(offsetRequest);

						if (!offsetResponse.hasError()) {
							long[] offsets = offsetResponse.offsets(topic, part.partitionId());
							retVals.put(topicAndPartition, offsets[0]);
						}
					}
				}
			}
			simpleConsumer.close();
		}
		return retVals;
	}
	
    public static void main(String[] args) throws Exception {
        logger.info("Starting KafkaOffsetUtils");
        String confFileName = System.getProperty("spring.conf", "classpath:conf/kafka-context-public.xml");
        @SuppressWarnings("resource")
		ClassPathXmlApplicationContext indexerContext = new ClassPathXmlApplicationContext(confFileName);
        indexerContext.registerShutdownHook();
        indexerContext.getBean(KafkaOffsetUtils.class).processAllThreads();
        logger.info("KafkaOffsetUtils is finished OK");
    }

}
