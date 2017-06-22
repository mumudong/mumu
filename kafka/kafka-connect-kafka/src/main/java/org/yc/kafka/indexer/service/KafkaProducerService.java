package org.yc.kafka.indexer.service;

import java.io.FileInputStream;
import java.util.List;
import java.util.Properties;

import javax.annotation.PostConstruct;

import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.config.BeanDefinition;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Service;

import kafka.javaapi.producer.Producer;
import kafka.producer.KeyedMessage;
import kafka.producer.ProducerConfig;

//async方式单Producer
@Service
@Scope(value = BeanDefinition.SCOPE_SINGLETON)
public class KafkaProducerService {
	private static final Logger logger = LoggerFactory.getLogger(KafkaProducerService.class);
	//Producer配置
	protected final Properties producer_props = new Properties();
	
	private Producer<Integer, String> producer;
	
	private KafkaProducerService() {
		registerExitEvent();
	}

	@PostConstruct
	private void init() {
		try {
			String conf = System.getProperty("kafka.producer.conf", "kafka-producer-conf.properties");
			if (conf.startsWith("classpath:")) {
				conf = StringUtils.substringAfter(conf, "classpath:");
				producer_props.load(KafkaProducerService.class.getClassLoader().getResourceAsStream(conf));
			} else {
				producer_props.load(new FileInputStream(conf));
			}
			ProducerConfig config = new ProducerConfig(producer_props);
			producer = new Producer<Integer, String>(config);
		} catch (Exception e) {
			logger.error("init client error!", e);
		}
	}

	/*
	 * 添加回调方法，关闭producer
	 */
	private void registerExitEvent() {
		Runtime.getRuntime().addShutdownHook(new Thread() {
			public void run() {
				if (producer != null) {
					producer.close();
				}
			}
		});
	}

	public void close(){
		if (producer != null) {
			producer.close();
		}
	}
	public void postEventBatchToKafka(List<KeyedMessage<Integer, String>> msgCache) {
			producer.send(msgCache);
	}
	
}
