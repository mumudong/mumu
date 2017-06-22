package org.yc.kafka.indexer.service.jmx;

import org.yc.kafka.indexer.jobs.IndexerJobStatusEnum;

public interface IndexerJobStatusMBean {
	long getLastCommittedOffset();
	IndexerJobStatusEnum getJobStatus();
	int getPartition();
}
