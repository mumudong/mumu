#!/bin/sh

if [[ "X$1" == "X" ]] ; then
        echo "usage:$0 conf_basename"
        exit 1
fi

conf_basename=$1

# Setup variables
# CHANGE FOR YOUR ENV: absolute path of the indexer installation dir
INDEXER_HOME=$(cd dirname $0/..;pwd)

cd $INDEXER_HOME || exit 1
# CHANGE FOR YOUR ENV: JDK 8 installation dir - you can skip it if your JAVA_HOME env variable is set
#JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_25.jdk/Contents/Home

# CHANGE FOR YOUR ENV: absolute path of the logback config file
LOGBACK_CONFIG_FILE=$INDEXER_HOME/conf/$conf_basename/logback.xml

# CHANGE FOR YOUR ENV: absolute path of the indexer properties file
INDEXER_PROPERTIES_FILE=$INDEXER_HOME/conf/$conf_basename/kafka-indexer.properties

PRODUCER_PROPERTIES_FILE=$INDEXER_HOME/conf/$conf_basename/kafka-producer-conf.properties

SPRING_CONF_FILE=file:$INDEXER_HOME/conf/$conf_basename/kafka-context-public.xml

# DO NOT CHANGE ANYTHING BELOW THIS POINT (unless you know what you are doing :) )!
echo "Starting Kafka ES Indexer app ..."
echo "INDEXER_HOME=$INDEXER_HOME"
echo "JAVA_HOME=$JAVA_HOME"
echo "LOGBACK_CONFIG_FILE=$LOGBACK_CONFIG_FILE"
echo "INDEXER_PROPERTIES_FILE=$INDEXER_PROPERTIES_FILE"

# add all dependent jars to the classpath
for file in $INDEXER_HOME/lib/*.jar;
do
  CLASS_PATH=$CLASS_PATH:$file
done
echo "CLASS_PATH=$CLASS_PATH"

if [[ ! -e "logs/$conf_basename" ]]; then 
	mkdir -p logs/$conf_basename
fi

JAVA_OPTS="-server -Xms1g -Xmx3g -Xloggc:logs/gc.log -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=logs -XX:+PrintGC -XX:+PrintGCApplicationStoppedTime -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:MaxTenuringThreshold=15 -XX:+CMSClassUnloadingEnabled -XX:+CMSParallelRemarkEnabled -XX:+UseCMSInitiatingOccupancyOnly -XX:+DisableExplicitGC -XX:-OmitStackTraceInFastThrow"

JAVA_OPTS=" $JAVA_OPTS -Djava.net.preferIPv4Stack=true -Dfile.encoding=UTF-8"

$JAVA_HOME/bin/java $JAVA_OPTS -cp $CLASS_PATH -DappName=${conf_basename} -Dspring.conf=$SPRING_CONF_FILE -Dindexer.properties=$INDEXER_PROPERTIES_FILE -Dkafka.producer.conf=$PRODUCER_PROPERTIES_FILE -Dlogback.configurationFile=$LOGBACK_CONFIG_FILE org.yc.kafka.indexer.KafkaIndexerProcess >>logs/$conf_basename/start.log 2>&1 &
if [[ $? == 0 ]]; then 
	echo $! > bin/${conf_basename}.pid
fi
