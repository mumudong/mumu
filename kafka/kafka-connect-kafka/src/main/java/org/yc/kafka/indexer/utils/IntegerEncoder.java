package org.yc.kafka.indexer.utils;

import kafka.utils.VerifiableProperties;

public class IntegerEncoder implements kafka.serializer.Encoder<Integer>{

	public IntegerEncoder(VerifiableProperties verifiableProperties) {
	}
	
	
	@Override
	public byte[] toBytes(Integer arg0) {
		return int2byte(arg0);
	}
	
	public static byte[] int2byte(int res) {  
		byte[] targets = new byte[4];  
		  
		targets[0] = (byte) (res & 0xff);// 最低位   
		targets[1] = (byte) ((res >> 8) & 0xff);// 次低位   
		targets[2] = (byte) ((res >> 16) & 0xff);// 次高位   
		targets[3] = (byte) (res >>> 24);// 最高位,无符号右移。   
		return targets;   
		}   
}
