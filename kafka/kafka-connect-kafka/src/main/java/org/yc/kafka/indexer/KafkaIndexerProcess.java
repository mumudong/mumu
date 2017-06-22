package org.yc.kafka.indexer;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import org.yc.kafka.indexer.service.JobManagerService;

/**
 * Created by dhyan on 1/28/16.
 */
public class KafkaIndexerProcess {
    private static final Logger logger = LoggerFactory.getLogger(KafkaIndexerProcess.class);
    public static void main(String[] args) throws Exception {
        logger.info("Starting KafkaIndexerProcess  ");
        String confFileName = System.getProperty("spring.conf", "classpath:conf/kafka-context-public.xml");
        @SuppressWarnings("resource")
		ClassPathXmlApplicationContext indexerContext = new ClassPathXmlApplicationContext(confFileName);
        indexerContext.registerShutdownHook();
        indexerContext.getBean(JobManagerService.class).processAllThreads();
        logger.info("KafkaIndexerProcess is started OK");

    }
}
