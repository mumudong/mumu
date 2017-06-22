package org.yc.kafka.indexer.utils;

import kafka.producer.Partitioner;
import kafka.utils.VerifiableProperties;

public class HashPartitioin implements Partitioner
{
    public int partition(Object key, int numPartitions)
    {
    	try{
    		long longVal = Long.parseLong(key.toString());
    		return (int)(longVal % numPartitions);
    	}catch (Exception e) {
    		return key.hashCode() % numPartitions;
		}
    }

    public HashPartitioin(VerifiableProperties props)
    {
    }
}
