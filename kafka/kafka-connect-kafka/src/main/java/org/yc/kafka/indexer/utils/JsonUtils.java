package org.yc.kafka.indexer.utils;

import java.io.IOException;
import java.text.SimpleDateFormat;

import org.codehaus.jackson.JsonGenerationException;
import org.codehaus.jackson.JsonParser;
import org.codehaus.jackson.map.DeserializationConfig;
import org.codehaus.jackson.map.JsonMappingException;
import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.map.SerializationConfig;
import org.codehaus.jackson.map.annotate.JsonSerialize;
import org.codehaus.jackson.type.TypeReference;

public class JsonUtils {
	private static ObjectMapper objectMapper = new ObjectMapper();
	static {
		objectMapper.setSerializationInclusion(JsonSerialize.Inclusion.NON_NULL); 
		objectMapper.configure(SerializationConfig.Feature.WRITE_DATES_AS_TIMESTAMPS, false);
		objectMapper.getDeserializationConfig().withDateFormat(new SimpleDateFormat("yyyy-MM-dd"));
		objectMapper.getSerializationConfig().withDateFormat(new SimpleDateFormat("yyyy-MM-dd"));
		objectMapper.configure(DeserializationConfig.Feature.FAIL_ON_UNKNOWN_PROPERTIES, false);
		objectMapper.configure(JsonParser.Feature.ALLOW_UNQUOTED_FIELD_NAMES, true);
		objectMapper.configure(JsonParser.Feature.ALLOW_SINGLE_QUOTES, true);
		objectMapper.configure(JsonParser.Feature.ALLOW_UNQUOTED_CONTROL_CHARS, true);
		objectMapper.configure(SerializationConfig.Feature.FAIL_ON_EMPTY_BEANS, false);
	}

	/**
	 * 格式化输出，性能有损耗
	 */
	public static <T> String toJsonForDisplay(T t) {
		try {
			String jsonStr = objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(t);
			return jsonStr;
		} catch (JsonGenerationException e) {
			throw new RuntimeException("JsonGenerationException", e);
		} catch (JsonMappingException e) {
			throw new RuntimeException("JsonMappingException", e);
		} catch (IOException e) {
			throw new RuntimeException("IOException", e);
		}
	}

	public static <T> String toJson(T t) {
		try {
			String jsonStr = objectMapper.writeValueAsString(t);
			return jsonStr;
		} catch (JsonGenerationException e) {
			throw new RuntimeException("JsonGenerationException", e);
		} catch (JsonMappingException e) {
			throw new RuntimeException("JsonMappingException", e);
		} catch (IOException e) {
			throw new RuntimeException("IOException", e);
		}
	}

	public static <T> T fromJSON(String jsonString, Class<T> clazz) {

		T object = null;
		try {
			object = objectMapper.readValue(jsonString, clazz);
		} catch (JsonGenerationException e) {
			throw new RuntimeException("JsonGenerationException", e);
		} catch (JsonMappingException e) {
			throw new RuntimeException("JsonMappingException", e);
		} catch (IOException e) {
			throw new RuntimeException("IOException", e);
		}
		return object;
	}

	public static <T> T fromJSON(String jsonString, TypeReference<T> typeReference) {

		T object = null;
		try {
			object = objectMapper.readValue(jsonString, typeReference);
		} catch (JsonGenerationException e) {
			throw new RuntimeException("JsonGenerationException", e);
		} catch (JsonMappingException e) {
			throw new RuntimeException("JsonMappingException", e);
		} catch (IOException e) {
			throw new RuntimeException("IOException", e);
		}
		return object;
	}

	public static byte[] writeValueAsBytes(Object value) throws IOException{
			return objectMapper.writeValueAsBytes(value);
	}
	
	public static long readValue(byte[] value) throws IOException{
		return objectMapper.readValue(objectMapper.writeValueAsBytes(value), long.class);
	}
}
