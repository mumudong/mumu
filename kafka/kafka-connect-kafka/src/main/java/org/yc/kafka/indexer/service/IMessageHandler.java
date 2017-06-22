package org.yc.kafka.indexer.service;

import org.yc.kafka.indexer.exception.IndexerESNotRecoverableException;
import org.yc.kafka.indexer.exception.IndexerESRecoverableException;

/**
 * Created by dhyan on 1/28/16.
 */
public interface IMessageHandler {

    /**
     * Add messages to Batch
     * @param inputMessage
     * @param offset
     * @throws Exception
     */
    public void addMessageToBatch(byte[] inputMessage, Long offset) throws Exception;

    public byte[] transformMessage(byte[] inputMessage, Long offset) throws Exception;
    
    /**
     * In most cases - do not customize this method, just delegate to the BasicMessageHandler implementation
     * @return
     * @throws Exception
     */
    public boolean postToKafka() throws InterruptedException, IndexerESRecoverableException, IndexerESNotRecoverableException;
    


}
