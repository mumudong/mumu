/**
  * @author marinapopova
  * Feb 24, 2016
 */
package org.yc.kafka.indexer.service.impl.examples;

import com.google.common.collect.Lists;
import com.google.common.collect.Maps;
import kafka.producer.KeyedMessage;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.yc.kafka.indexer.service.IMessageHandler;
import org.yc.kafka.indexer.service.KafkaProducerService;
import org.yc.kafka.indexer.utils.JoinerUtils;
import org.yc.kafka.indexer.utils.JsonUtils;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

/**
 * 
 *
 */
public class DispatchInfoHandlerImpl implements IMessageHandler {
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
		String parsedMessage = parseToLine(new String(inputMessage));
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
	
	public static final String[] fieldNames = new String[] { "datetime", "null", "service_order_id", "dispatch_count",
			"response_count", "accept_count", "flag", "dispatch_time", "decision_time", "contribution",
			"expect_decision_time", "dispatch_template_id", "template_snapshot", "status", "dispatch_type",
			"decision_type", "round", "batch", "create_time", "update_time", "estimate_time", "can_dispatch_count",
			"user_id", "user_level", "user_name", "user_gender", "add_price_redispatch", "add_price_info",
			"decision_driver_id", "decision_car_type_id", "bidding_id", "bidding_rate" };

	public static String parseToLine(String line) throws IOException {
		String[] results = new String[fieldNames.length];
				
		// log分割成13份, 取出前12个字段
		String[] fields = line.split(" ", 13);
		for (int i = 0; i < 12; i++) {
			results[i]=fields[i];
		}
		line =  fields[12];
		// 继续将第13份分割成2份,先取出 dispatch_snapshot(第13个)字段
		if(line.charAt(0) == ' '){
			line="{} "+line.substring(1);
		}
		fields = line.split("} ", 2);
		results[12]=fields[0] + "}";
		//将dispatch_snapshot之后的内容分成12份,取出前11(第14-24)个字段
		fields = fields[1].split(" ", 12);
		for (int i = 0; i < 11; i++) {
			results[i + 13] = fields[i];
		}
		//取出剩下的8(第25-32)个字段,注要先从后向前取7个,剩下的都是user_name
		fields = fields[11].split(" ", -1);
		int extra = fields.length - 8; //理论上fields.length一定大于等于8
		for(int i=7;i > 0; i--){
			results[i + 24] = fields[i + extra];
		}
		//把user_name拼接起来
		String user_name = StringUtils.join(fields, " ", 0, extra+1);
		results[24] = user_name;
		return JoinerUtils.LOG_JOINER.join(results);
	}
	
	public static String parseToJson(String line) throws IOException {
		Map<String, String> jsonBuild = Maps.newHashMap();
		
		// log分割成13份, 取出前12个字段
		String[] fields = line.split(" ", 13);
		for (int i = 0; i < 12; i++) {
			jsonBuild.put(fieldNames[i], fields[i]);
		}
		line =  fields[12];
		// 继续将第13份分割成2份,先取出 dispatch_snapshot(第13个)字段
		if(line.charAt(0) == ' '){
			line="{} "+line.substring(1);
		}
		fields = line.split("} ", 2);
		jsonBuild.put(fieldNames[12], fields[0] + "}");
		//将dispatch_snapshot之后的内容分成12份,取出前11(第14-24)个字段
		fields = fields[1].split(" ", 12);
		for (int i = 0; i < 11; i++) {
			jsonBuild.put(fieldNames[i + 13], fields[i]);
		}
		//取出剩下的8(第25-32)个字段,注要先从后向前取7个,剩下的都是user_name
		fields = fields[11].split(" ", -1);
		int extra = fields.length - 8; //理论上fields.length一定大于等于8
		for(int i=7;i > 0; i--){
			jsonBuild.put(fieldNames[i + 24], fields[i + extra]);
		}
		//把user_name拼接起来
		String user_name = StringUtils.join(fields, " ", 0, extra+1);
		jsonBuild.put(fieldNames[24], user_name);
//		System.out.println(jsonBuild.size());
		return JsonUtils.toJson(jsonBuild);
	}
	
	public static void main(String[] args) throws IOException {
		String log="2016-11-08_08:59:11  6327625331092013788 19 0 0 512 1473265103 0 400 1473265140 25 {\"dispatch_template_id\":\"25\",\"city\":\"sh\",\"code\":\"asap\",\"name\":\"ASAP\",\"is_rush_hour\":\"0\",\"dispatch_params\":\"{\\\"ASSIGN_MAX_RANGE\\\":2000,\\\"DISTANCE\\\":100,\\\"CONTRIBUTION\\\":0,\\\"MONTHBASE\\\":0,\\\"EVALUATION\\\":0,\\\"DESTWISH\\\":0,\\\"MAX_RANGE\\\":4000,\\\"MAX_DRIVER_COUNT\\\":300,\\\"MAX_ACCEPT_COUNT\\\":2,\\\"BATCH_INTERVAL\\\":10,\\\"DRIVER_DEADLINE\\\":20,\\\"BATCH_DRIVER_COUNT\\\":40,\\\"SECOND_SORT_BY\\\":\\\"DISTANCE\\\"}\",\"decision_params\":\"{\\\"DISTANCE\\\":100,\\\"CONTRIBUTION\\\":0,\\\"MONTHBASE\\\":0,\\\"EVALUATION\\\":0,\\\"DESTWISH\\\":0,\\\"USER_DEADLINE\\\":70,\\\"SECOND_SORT_BY\\\":\\\"DISTANCE\\\"}\",\"operator\":\"lvshaowei\",\"remark\":\"及时用车，默认时段的规则\",\"create_time\":\"1420911046\",\"update_time\":\"1472523848\"} 40 1 0 1 1 1473265078 1473265103 1473 19 3615235 3 白珊 - 0 - 0 0 -1 0.00";
		
		System.out.println(parseToJson(log));
		System.out.println(parseToLine(log));

	}
}
