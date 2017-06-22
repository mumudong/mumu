/**
  * @author marinapopova
  * Feb 24, 2016
 */
package org.yc.kafka.indexer.service.impl.examples;

import java.io.IOException;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;

import kafka.producer.KeyedMessage;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.yc.kafka.indexer.service.IMessageHandler;
import org.yc.kafka.indexer.service.KafkaProducerService;

import com.google.common.collect.Lists;

/**
 * 
 *
 */
public class SimpleHandlerImpl implements IMessageHandler {
	private static final Logger logger = LoggerFactory.getLogger(DispatchInfoHandlerImpl.class);
	@Autowired
	private KafkaProducerService kafkaProducerService = null;
	@Value("${producer.topic:producer_topic}")
	private String TOPIC;
	@Value("${producer.partition.num:100}")
	private int numOfPartitions;
	private AtomicLong counter = new AtomicLong(0);
	private List<KeyedMessage<Integer, String>> msgCache = Lists.newArrayList();

	@Override
	public byte[] transformMessage(byte[] inputMessage, Long offset) throws Exception {
		// do not do any transformations for this scenario - just return the message as is
		return inputMessage;
	}

	@Override
	public void addMessageToBatch(byte[] inputMessage, Long offset) throws Exception {
		String parsedMessage = new String(inputMessage);
		long num = counter.get();
		KeyedMessage<Integer, String> data = new KeyedMessage<Integer, String>(TOPIC,
				(int)(num % numOfPartitions), parsedMessage);
		msgCache.add(data);
	}

	@Override
	public boolean postToKafka(){
		try {
			kafkaProducerService.postEventBatchToKafka(msgCache);
			return true;
		} catch (Exception e) {
			logger.error("error while post Batch " + counter.get() + " to Kafka", e);
		} finally {
			msgCache = Lists.newArrayList();
			counter.incrementAndGet();
		}
		return false;
	}
	
	
	public static void main(String[] args) throws IOException {

	}
}
