package org.yc.kafka.indexer.service;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

import org.apache.curator.framework.CuratorFramework;
import org.apache.curator.framework.CuratorFrameworkFactory;
import org.apache.curator.retry.ExponentialBackoffRetry;
import org.apache.curator.utils.CloseableUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.yc.kafka.indexer.utils.JsonUtils;

public class KafkaOffsetService {
	private static final Logger logger =  LoggerFactory.getLogger(KafkaOffsetService.class);
	
	//zk path to save kafka offset ,eg: "/consumers/[groupId]/offsets/[topic]/[partitionId]" => long (offset)
	public static final String OFFSET_ZK_PATH = "/consumers/%s/offsets/%s/%s";
   
	@Value("${kafkaZookeeperList:localhost:2181}")
    private String kafkaZookeeperList;
    
    @Value("${zkSessionTimeoutMs:30000}")
    private int zkSessionTimeoutMs;
     
    @Value("${zkConnectionTimeoutMs:10000}")
    private int zkConnectionTimeoutMs;
    
    @Value("${zkCuratorRetryTimes:3}")
    private int zkCuratorRetryTimes;
    
    @Value("${zkCuratorRetryDelayMs:2000}")
    private int zkCuratorRetryDelayMs;
	
    private CuratorFramework zkClient = null;
    
    @PostConstruct
    public void init(){
	    CuratorFrameworkFactory.Builder builder = CuratorFrameworkFactory.builder();
	    zkClient = builder.connectString(kafkaZookeeperList).sessionTimeoutMs(zkSessionTimeoutMs)
				.connectionTimeoutMs(zkConnectionTimeoutMs).retryPolicy(new ExponentialBackoffRetry(1000, zkCuratorRetryTimes)).defaultData(null)
				.build();
	    zkClient.start();
    }

    public boolean commitOffset(String consumerGroup, String topic, int partition, long value) throws Exception{
    	  final byte[] offsetBytes = JsonUtils.writeValueAsBytes(value);
          String nodePath = String.format(OFFSET_ZK_PATH,consumerGroup,topic, partition);
          if(zkClient.checkExists().forPath(nodePath)!=null){
        	  zkClient.setData().forPath(nodePath,offsetBytes);
          }else{
        	  zkClient.create().creatingParentsIfNeeded().forPath(nodePath, offsetBytes);
          }
          return true;
    }
    
    public long getOffset(String consumerGroup, String topic, int partition, long defaultValue) {
        String nodePath = String.format(OFFSET_ZK_PATH,consumerGroup,topic, partition);
        try {
			if(zkClient.checkExists().forPath(nodePath)!=null){
				byte[] value = zkClient.getData().forPath(nodePath);
				if(value == null){
					return defaultValue;
				}
				return JsonUtils.readValue(value);
			}else{
				return defaultValue;
			}
		} catch (Exception e) {
			logger.error("getOffset error", e);
		}
        return defaultValue;
  }
    
    @PreDestroy
    public void close(){
    	CloseableUtils.closeQuietly(zkClient);
    }
}
