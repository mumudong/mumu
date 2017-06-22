package org.yc.kafka.indexer.utils;

public class UnicodeUtils {

	public static String convertUnicode(String utfString){  
	    StringBuilder sb = new StringBuilder();  
	    int i = -1;  
	    int pos = 0;  
	      
	    while((i=utfString.indexOf("\\u", pos)) != -1){  
	        sb.append(utfString.substring(pos, i));  
	        if(i+5 < utfString.length()){  
	            pos = i+6;  
	            sb.append((char)Integer.parseInt(utfString.substring(i+2, i+6), 16));  
	        }  
	    }  
	    sb.append(utfString.substring(pos));  
	    return sb.toString();  
	} 
	
	public static String convertUnicode(byte[] utfBytes){  
		StringBuilder sb = new StringBuilder();  
		int i = -1;  
		int pos = 0;  
		String utfString = new String(utfBytes);
		while((i=utfString.indexOf("\\u", pos)) != -1){  
			sb.append(utfString.substring(pos, i));  
			if(i+5 < utfString.length()){  
				pos = i+6;  
				sb.append((char)Integer.parseInt(utfString.substring(i+2, i+6), 16));  
			}  
		}  
		sb.append(utfString.substring(pos));  
		return sb.toString();  
	} 
	
}
