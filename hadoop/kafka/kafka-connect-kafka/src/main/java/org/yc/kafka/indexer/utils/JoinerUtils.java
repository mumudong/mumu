package org.yc.kafka.indexer.utils;

import com.google.common.base.Joiner;

public class JoinerUtils {
	public static Joiner LOG_JOINER = Joiner.on("\001").useForNull("");
}
