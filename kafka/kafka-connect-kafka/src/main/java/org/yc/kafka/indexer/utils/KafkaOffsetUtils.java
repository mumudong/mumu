package org.yc.kafka.indexer.utils;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.retry.RetryUntilElapsed;
import org.codehaus.jackson.map.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

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

public class KafkaOffsetUtils {
	private static final Logger logger =  LoggerFactory.getLogger(KafkaOffsetUtils.class);
	private static ObjectMapper objectMapper = new ObjectMapper();
	
	//zk path to save kafka offset ,eg: "/consumers/[groupId]/offsets/[topic]/[partitionId]" => long (offset)
	public static final String OFFSET_ZK_PATH = "/consumers/%s/offsets/%s";
	
    public static Map<TopicAndPartition,Long> getConsumerOffsets(String zkServers, String groupID, String topic) { 
        Map<TopicAndPartition,Long> retVals = new HashMap<TopicAndPartition,Long>();

        CuratorFramework  curatorFramework = CuratorFrameworkFactory.builder()
                .connectString(zkServers).connectionTimeoutMs(1000)
                .sessionTimeoutMs(10000).retryPolicy(new RetryUntilElapsed(5000, 1000)).build();
        curatorFramework.start();
        try{
        String nodePath = String.format(OFFSET_ZK_PATH, groupID, topic);
        if(curatorFramework.checkExists().forPath(nodePath)!=null){
            List<String> partitions=curatorFramework.getChildren().forPath(nodePath);
            for(String partiton:partitions){
                int partitionL=Integer.valueOf(partiton);
                Long offset=objectMapper.readValue(curatorFramework.getData().forPath(nodePath+"/"+partiton),Long.class);
                TopicAndPartition topicAndPartition=new TopicAndPartition(topic,partitionL);
                retVals.put(topicAndPartition, offset);
            }
        }
        }catch(Exception e){
            logger.error(String.format("get offsets error,topic:%s, group:%s",topic,groupID),e);
        }
        curatorFramework.close();
        return retVals;
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
    
//	  import org.apache.spark.streaming.kafka.OffsetRange;
//    public static void saveOffsets(String zkServers, String topic, String group, OffsetRange[] offsetRanges) { 
//    	 ObjectMapper objectMapper = new ObjectMapper();
//    	 CuratorFramework  curatorFramework = null;
//         try{
//        	 curatorFramework = CuratorFrameworkFactory.builder()
//                     .connectString(zkServers).connectionTimeoutMs(1000)
//                     .sessionTimeoutMs(10000).retryPolicy(new RetryUntilElapsed(5000, 1000)).build();
//
//             curatorFramework.start();
//         }catch (Exception e) {
//			logger.error("connect to zk error",e);
//			return;
//		}
//         for (OffsetRange offsetRange : offsetRanges) {
//        	 try {
//	        	 byte[] offsetBytes = objectMapper.writeValueAsBytes(offsetRange.untilOffset());
//				String nodePath = String.format(OFFSET_ZK_PATH, group, topic)+ "/" + offsetRange.partition();
//	             if(curatorFramework.checkExists().forPath(nodePath)!=null){
//	                     curatorFramework.setData().forPath(nodePath,offsetBytes);
//	             }else{
//	            	 curatorFramework.create().creatingParentsIfNeeded().forPath(nodePath, offsetBytes);
//	             }
//        	 }catch (Exception e) {
//        		 String msg = String.format("save offset error,topic:%s,group:%s,partition:%s,offset:%s", topic,group,offsetRange.partition(),offsetRange.untilOffset());
// 				logger.error(msg,e);
// 			}
//         }
//         curatorFramework.close();
//    } 
    
}
