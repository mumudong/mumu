/**
  * @author marinapopova
  * Feb 24, 2016
 */
package org.yc.kafka.indexer.service.impl.examples;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.yc.kafka.indexer.service.IMessageHandler;
import org.yc.kafka.indexer.service.KafkaProducerService;
import org.yc.kafka.indexer.utils.JoinerUtils;
import org.yc.kafka.indexer.utils.JsonUtils;

import com.google.common.collect.Lists;
import com.google.common.collect.Maps;

import kafka.producer.KeyedMessage;

/**
 * 
 *
 */
public class DispatchDetailInfoHandlerImpl implements IMessageHandler {
	private static final Logger logger = LoggerFactory.getLogger(DispatchDetailInfoHandlerImpl.class);
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
		String parsedMessage = parseToLine(new String(inputMessage));
		long num = counter.get();
		KeyedMessage<Integer, String> data = new KeyedMessage<Integer, String>(TOPIC,
				(int)(num % numOfPartitions), parsedMessage);
		msgCache.add(data);
	}

	@Override
	public boolean postToKafka() throws InterruptedException{
		try {
			kafkaProducerService.postEventBatchToKafka(msgCache);
			return true;
		} catch (Exception e) {
			logger.error("error while post Batch " + counter.get() + " to Kafka", e);
			return false;
		} finally {
			msgCache = Lists.newArrayList();
			counter.incrementAndGet();
		}
	}
	
	public static final String[] fieldNames = new String[]{"datetime","null1","service_order_id","round","batch","flag","driver_id","distance","dispatch_time","dispatch_lat","dispatch_lng","dispatch_total_rate","dispatch_snapshot","response_time","accept_status","response_lat","response_lng","response_distance","response_time_length","decision_time","decision_total_rate","decision_result","decision_failure_reason","decision_msg_snapshot","subtract_amount","add_price_set","response_snapshot","is_assigned","route_distance","route_time_length","distance_time_length"};
	public static String parseToLine(String line) throws IOException {
		String[] results = new String[fieldNames.length];
		//log分割成13份, 取出前12个字段
		String[] fields = line.split(" ",13);
		for(int i=0; i< 12; i++){
			results[i] = fields[i];
		}
		//继续将第13份分割成2份,取出 dispatch_snapshot(第13个)字段
		fields = fields[12].split("} ", 2);
		results[12] = fields[0]+"}";
		//继续分割剩下的字段
		fields = fields[1].split(" ", -1);
		for(int i=0; i< fields.length; i++){
			results[i+13] = fields[i];
		}
		return JoinerUtils.LOG_JOINER.join(results);
	}
	
	public static String parseToJson(String line) throws IOException{
		Map<String , String> jsonBuild = Maps.newHashMap();
		
		//log分割成13份, 取出前12个字段
		String[] fields = line.split(" ",13);
		for(int i=0; i< 12; i++){
			jsonBuild.put(fieldNames[i],fields[i]);
		}
		//继续将第13份分割成2份,取出 dispatch_snapshot(第13个)字段
		fields = fields[12].split("} ", 2);
		jsonBuild.put(fieldNames[12],fields[0]+"}");
		//继续分割剩下的字段
		fields = fields[1].split(" ", -1);
		for(int i=0; i< fields.length; i++){
			jsonBuild.put(fieldNames[i+13],fields[i]);
		}
		return JsonUtils.toJson(jsonBuild);
	}
	
	public static void main(String[] args) throws IOException {
		String log="2016-11-02_00:00:02  6348030299416648265 1 1 0 3241685 1697 1478015980 29.671300455729 91.146075032552 9700 {\"is_self_employed\":0,\"country\":\"CN\",\"driver_id\":\"3241685\",\"flag\":61450,\"base_score\":20,\"driver_type\":5,\"color\":2,\"distance\":1697,\"city\":\"lasa\",\"latitude\":29.671300455729,\"total_rate\":9700,\"device_type\":\"2\",\"audit_status\":20,\"has_logistics\":0,\"discount_rate\":100,\"distance_time_length\":509.1,\"contribution_rate\":24,\"last_position_time\":1478015972,\"surpport_face_pay\":1,\"evaluation\":1000,\"evaluation_rate\":100,\"has_qualified\":0,\"contribution\":18000,\"cellphone\":\"13219867012\",\"silence_end_at\":0,\"work_status\":0,\"car_id\":3375494,\"brand\":\"\\u5e7f\\u6c7d\\u4f20\\u797aGA3\",\"seat_num\":4,\"route_distance\":0,\"longitude\":91.146075032552,\"car_type_id\":37,\"route_time_length\":0,\"device_id\":24694855613539879,\"base_score_rate\":20,\"good_comment_rate\":100,\"driver_level\":1,\"version\":\"204\",\"car_brand_id\":40,\"car_model_id\":467,\"vehicle_number\":\"\\u5dddFQP012\",\"name\":\"\\u5218\\u52c7\",\"imei\":\"e069929597d9c4c9c2ae656353378cc1\",\"distance_rate\":97,\"is_assigned\":0,\"add_price_set\":{\"add_price_redispatch\":0,\"add_price_rate\":0,\"add_price_max_amount\":10000000,\"add_price_type\":0,\"add_price_vip\":0,\"strategy_id\":0,\"add_total_amount\":0,\"total_add_price_rate\":0,\"bidding_id\":\"6348030297090432167\",\"total_magnification\":0,\"bidding_price\":0,\"add_amount_str\":\"\",\"add_amount_str_full\":\"\"}} 0 0 0 0 0 0 0 0 0 0 - 0 {\"add_price_redispatch\":0,\"add_price_rate\":0,\"add_price_max_amount\":10000000,\"add_price_type\":0,\"add_price_vip\":0,\"strategy_id\":0,\"add_total_amount\":0,\"total_add_price_rate\":0,\"bidding_id\":\"6348030297090432167\",\"total_magnification\":0,\"bidding_price\":0,\"add_amount_str\":\"\",\"add_amount_str_full\":\"\"} - 0 0 0 509.1";
		
		System.out.println(parseToJson(log));
		System.out.println(parseToLine(log));
	}
}
