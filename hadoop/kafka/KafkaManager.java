package org.apache.spark.streaming.kafka  
  
import kafka.common.TopicAndPartition  
import kafka.message.MessageAndMetadata  
import kafka.serializer.Decoder  
import org.apache.spark.SparkException  
import org.apache.spark.rdd.RDD  
import org.apache.spark.streaming.StreamingContext  
import org.apache.spark.streaming.dstream.InputDStream  
import org.apache.spark.streaming.kafka.KafkaCluster.{LeaderOffset}  
  
import scala.reflect.ClassTag  
  
/** 
 * Created by knowpigxia on 15-8-5. 
 */  
class KafkaManager(val kafkaParams: Map[String, String]) extends Serializable {  
  
  private val kc = new KafkaCluster(kafkaParams)  
  
  /** 
   * ���������� 
   * @param ssc 
   * @param kafkaParams 
   * @param topics 
   * @tparam K 
   * @tparam V 
   * @tparam KD 
   * @tparam VD 
   * @return 
   */  
  def createDirectStream[K: ClassTag, V: ClassTag, KD <: Decoder[K]: ClassTag, VD <: Decoder[V]: ClassTag](  
                                                                                                            ssc: StreamingContext, kafkaParams: Map[String, String], topics: Set[String]): InputDStream[(K, V)] =  {  
    val groupId = kafkaParams.get("group.id").get  
    // ��zookeeper�϶�ȡoffsetsǰ�ȸ���ʵ���������offsets  
    setOrUpdateOffsets(topics, groupId)  
  
    //��zookeeper�϶�ȡoffset��ʼ����message  
    val messages = {  
      val partitionsE = kc.getPartitions(topics)  
      if (partitionsE.isLeft)  
        throw new SparkException(s"get kafka partition failed: ${partitionsE.left.get}")  
      val partitions = partitionsE.right.get  
      val consumerOffsetsE = kc.getConsumerOffsets(groupId, partitions)  
      if (consumerOffsetsE.isLeft)  
        throw new SparkException(s"get kafka consumer offsets failed: ${consumerOffsetsE.left.get}")  
      val consumerOffsets = consumerOffsetsE.right.get  
      KafkaUtils.createDirectStream[K, V, KD, VD, (K, V)](  
        ssc, kafkaParams, consumerOffsets, (mmd: MessageAndMetadata[K, V]) => (mmd.key, mmd.message))  
    }  
    messages  
  }  
  
  /** 
   * ����������ǰ������ʵ�����������������offsets 
   * @param topics 
   * @param groupId 
   */  
  private def setOrUpdateOffsets(topics: Set[String], groupId: String): Unit = {  
    topics.foreach(topic => {  
      var hasConsumed = true  
      val partitionsE = kc.getPartitions(Set(topic))  
      if (partitionsE.isLeft)  
        throw new SparkException(s"get kafka partition failed: ${partitionsE.left.get}")  
      val partitions = partitionsE.right.get  
      val consumerOffsetsE = kc.getConsumerOffsets(groupId, partitions)  
      if (consumerOffsetsE.isLeft) hasConsumed = false  
      if (hasConsumed) {// ���ѹ�  
        /** 
         * ���streaming����ִ�е�ʱ�����kafka.common.OffsetOutOfRangeException�� 
         * ˵��zk�ϱ����offsets�Ѿ���ʱ�ˣ���kafka�Ķ�ʱ��������Ѿ���������offsets���ļ�ɾ���� 
         * ������������ֻҪ�ж�һ��zk�ϵ�consumerOffsets��earliestLeaderOffsets�Ĵ�С�� 
         * ���consumerOffsets��earliestLeaderOffsets��С�Ļ���˵��consumerOffsets�ѹ�ʱ, 
         * ��ʱ��consumerOffsets����ΪearliestLeaderOffsets 
         */  
        val earliestLeaderOffsetsE = kc.getEarliestLeaderOffsets(partitions)  
        if (earliestLeaderOffsetsE.isLeft)  
          throw new SparkException(s"get earliest leader offsets failed: ${earliestLeaderOffsetsE.left.get}")  
        val earliestLeaderOffsets = earliestLeaderOffsetsE.right.get  
        val consumerOffsets = consumerOffsetsE.right.get  
  
        // ����ֻ�Ǵ��ڲ��ַ���consumerOffsets��ʱ������ֻ���¹�ʱ������consumerOffsetsΪearliestLeaderOffsets  
        var offsets: Map[TopicAndPartition, Long] = Map()  
        consumerOffsets.foreach({ case(tp, n) =>  
          val earliestLeaderOffset = earliestLeaderOffsets(tp).offset  
          if (n < earliestLeaderOffset) {  
            println("consumer group:" + groupId + ",topic:" + tp.topic + ",partition:" + tp.partition +  
              " offsets�Ѿ���ʱ������Ϊ" + earliestLeaderOffset)  
            offsets += (tp -> earliestLeaderOffset)  
          }  
        })  
        if (!offsets.isEmpty) {  
          kc.setConsumerOffsets(groupId, offsets)  
        }  
      } else {// û�����ѹ�  
      val reset = kafkaParams.get("auto.offset.reset").map(_.toLowerCase)  
        var leaderOffsets: Map[TopicAndPartition, LeaderOffset] = null  
        if (reset == Some("smallest")) {  
          val leaderOffsetsE = kc.getEarliestLeaderOffsets(partitions)  
          if (leaderOffsetsE.isLeft)  
            throw new SparkException(s"get earliest leader offsets failed: ${leaderOffsetsE.left.get}")  
          leaderOffsets = leaderOffsetsE.right.get  
        } else {  
          val leaderOffsetsE = kc.getLatestLeaderOffsets(partitions)  
          if (leaderOffsetsE.isLeft)  
            throw new SparkException(s"get latest leader offsets failed: ${leaderOffsetsE.left.get}")  
          leaderOffsets = leaderOffsetsE.right.get  
        }  
        val offsets = leaderOffsets.map {  
          case (tp, offset) => (tp, offset.offset)  
        }  
        kc.setConsumerOffsets(groupId, offsets)  
      }  
    })  
  }  
  
  /** 
   * ����zookeeper�ϵ�����offsets 
   * @param rdd 
   */  
  def updateZKOffsets(rdd: RDD[(String, String)]) : Unit = {  
    val groupId = kafkaParams.get("group.id").get  
    val offsetsList = rdd.asInstanceOf[HasOffsetRanges].offsetRanges  
  
    for (offsets <- offsetsList) {  
      val topicAndPartition = TopicAndPartition(offsets.topic, offsets.partition)  
      val o = kc.setConsumerOffsets(groupId, Map((topicAndPartition, offsets.untilOffset)))  
      if (o.isLeft) {  
        println(s"Error updating the offset to Kafka cluster: ${o.left.get}")  
      }  
    }  
  }  
}