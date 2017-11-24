#!/bin/bash
#!/usr/bin/expect
# uninstall ambari automatic

if [ $# -ne 1 ]; then
    echo "Usage:"
    echo "$0  hostsFile"
    exit 1
fi
 

#取得集群的所有主机名，这里需要注意：/etc/hosts配置的IP和主机名只能用一个空格分割
 
hostList=$1

#定义ambari组件所在目录对应的变量
yumReposDir=/etc/yum.repos.d/
alterNativesDir=/etc/alternatives/
hdpDir=/usr/hdp/
usrBinDir=/usr/bin/
etcDir=/etc/
varLogDir=/var/log/
varRunDir=/var/run/


#ping主机的次数
pingCount=5

#Log日志开头
logPre=UNINSTALL

#输入ambari主机名称
read -p "Please input your master hostname: " master
master=${master:-"master"}
ssh $master "ambari-server stop"



for host in `cat  $hostList`
do
    yum clean all
	yum makecache
	
	
	
	#关闭agent
	
	ssh $host "ambari-agent stop"
	
	

    echo "$logPre======>$host deleting... \n"

    
    #删除HDP相关的安装包
    ssh $host "yum remove -y  *sqoop*"
	ssh $host "yum remove -y  *ranger*"
	ssh $host "yum remove -y  *spark*"
	ssh $host "yum remove -y  *storm*"
    ssh $host "yum remove -y  *lzo-devel.x86_64"
    ssh $host "yum remove -y  *hadoop-libhdfs.x86_64"
    ssh $host "yum remove -y  *rrdtool.x86_64"
    ssh $host "yum remove -y  *hbase*"
    ssh $host "yum remove -y  *pig.noarch"
    ssh $host "yum remove -y  *lzo.x86_64" 
    ssh $host "yum remove -y  *ambari-log4j.noarch"
    ssh $host "yum remove -y  *oozie.noarch"
    ssh $host "yum remove -y  *oozie-client.noarch"
    ssh $host "yum remove -y  *gweb.noarch"
    ssh $host "yum remove -y  *snappy-devel.x86_64"
    ssh $host "yum remove -y  *hcatalog.noarch"
    ssh $host "yum remove -y  *python-rrdtool.x86_64"
    ssh $host "yum remove -y  *nagios.x86_64"
    ssh $host "yum remove -y  *webhcat-tar-pig.noarch"
    ssh $host "yum remove -y  *snappy.x86_64"
    ssh $host "yum remove -y  *libconfuse.x86_64"
    ssh $host "yum remove -y  *webhcat-tar-hive.noarch"
    ssh $host "yum remove -y  *ganglia-gmetad.x86_64"
    ssh $host "yum remove -y  *extjs.noarch"
    ssh $host "yum remove -y  *hive.noarch"
    ssh $host "yum remove -y  *hadoop*"
    ssh $host "yum remove -y  *nagios-plugins.x86_64"
    ssh $host "yum remove -y  *hadoop.x86_64"
    ssh $host "yum remove -y  *zookeeper*"   
    ssh $host "yum remove -y  *hadoop-sbin.x86_64"
    ssh $host "yum remove -y  *ganglia-gmond.x86_64"
    ssh $host "yum remove -y  *libganglia.x86_64"
    ssh $host "yum remove -y  *perl-rrdtool.x86_64"
    ssh $host "yum remove -y  *epel-release.noarch"
    ssh $host "yum remove -y  *compat-readline5*"
    ssh $host "yum remove -y  *fping.x86_64"
    ssh $host "yum remove -y  *perl-Crypt-DES.x86_64"
    ssh $host "yum remove -y  *exim.x86_64"
    ssh $host "yum remove -y *ganglia-web.noarch"
    ssh $host "yum remove -y *perl-Digest-HMAC.noarch"
    ssh $host "yum remove -y *perl-Digest-SHA1.x86_64"
    ssh $host "yum remove -y *bigtop-jsvc.x86_64"
    
    #删除快捷方式
    ssh $host "cd $alterNativesDir"
    ssh $host "rm -rf hadoop-etc" 
    ssh $host "rm -rf zookeeper-conf"
    ssh $host "rm -rf hbase-conf" 
    ssh $host "rm -rf hadoop-log" 
    ssh $host "rm -rf hadoop-lib"
    ssh $host "rm -rf hadoop-default" 
    ssh $host "rm -rf oozie-conf"
    ssh $host "rm -rf hcatalog-conf" 
    ssh $host "rm -rf hive-conf"
    ssh $host "rm -rf hadoop-man"
    ssh $host "rm -rf sqoop-conf"
    ssh $host "rm -rf hadoop-confone"

    #删除用户
    ssh $host "userdel -rf nagios"
    ssh $host "userdel -rf hive"
    ssh $host "userdel -rf ambari-qa"
    ssh $host "userdel -rf hbase"
    ssh $host "userdel -rf oozie"
    ssh $host "userdel -rf hcat"
    ssh $host "userdel -rf mapred"
    ssh $host "userdel -rf hdfs"
    ssh $host "userdel -rf rrdcached"
    ssh $host "userdel -rf zookeeper"
    ssh $host "userdel -rf sqoop"
    ssh $host "userdel -rf puppet"
    ssh $host "userdel -rf flume"
    ssh $host "userdel -rf tez"
    ssh $host "userdel -rf yarn"
	
	ssh $host "userdel -rf knox"
    ssh $host "userdel -rf storm"
    ssh $host "userdel -rf spark"
    ssh $host "userdel -rf kafka"
    ssh $host "userdel -rf ams"
    ssh $host "userdel -rf falcon"
    ssh $host "userdel -rf kms"
    ssh $host "userdel -rf ranger"
	

    #删除文件夹
    ssh $host "rm -rf /hadoop"
    ssh $host "rm -rf /etc/hadoop" 
    ssh $host "rm -rf /etc/hbase"
    ssh $host "rm -rf /etc/hcatalog" 
    ssh $host "rm -rf /etc/hive"
    ssh $host "rm -rf /etc/ganglia" 
    ssh $host "rm -rf /etc/nagios"
    ssh $host "rm -rf /etc/oozie"
    ssh $host "rm -rf /etc/sqoop"
    ssh $host "rm -rf /etc/zookeeper" 
	ssh $host "rm -rf /etc/hive2"
	ssh $host "rm -rf /etc/hive-hcatalog"
	ssh $host "rm -rf /etc/hive-webhcat"
	ssh $host "rm -rf /etc/knox"
	ssh $host "rm -rf /etc/livy2"
	ssh $host "rm -rf /etc/phoenix"
	ssh $host "rm -rf /etc/pig"
	ssh $host "rm -rf /etc/smartsense-activity"
	ssh $host "rm -rf /etc/spark2"
	ssh $host "rm -rf /etc/storm*"
	ssh $host "rm -rf /etc/tez"
	ssh $host "rm -rf /etc/tez_hive2"
	ssh $host "rm -rf /etc/falcon"
	ssh $host "rm -rf /etc/slider"
	ssh $host "rm -rf /etc/ranger"
	ssh $host "rm -rf /var/lib/hdfs"
	ssh $host "rm -rf /var/lib/knox"
	ssh $host "rm -rf /var/lib/slider"
	ssh $host "rm -rf /var/lib/ranger"
	ssh $host "rm -rf /var/lib/hdfs"
	ssh $host "rm -rf /var/lib/hadoop*" 
    ssh $host "rm -rf /var/run/hadoop" 
    ssh $host "rm -rf /var/run/hbase"
    ssh $host "rm -rf /var/run/hive"
    ssh $host "rm -rf /var/run/ganglia" 
    ssh $host "rm -rf /var/run/nagios"
    ssh $host "rm -rf /var/run/oozie"
    ssh $host "rm -rf /var/run/zookeeper"
    ssh $host "rm -rf /var/run/falcon" 
    ssh $host "rm -rf /var/run/ambari-agent"
    ssh $host "rm -rf /var/run/ambari-infra-solr"
    ssh $host "rm -rf /var/run/ambari-metrics-grafana"	
	ssh $host "rm -rf /var/run/ambari-server"	
	ssh $host "rm -rf /var/run/hadoop-mapreduce"	
	ssh $host "rm -rf /var/run/hadoop-yarn"	
	ssh $host "rm -rf /var/run/hive2"	
	ssh $host "rm -rf /var/run/storm"	
	ssh $host "rm -rf /var/log/storm"	
	ssh $host "rm -rf /etc/flume"	
	ssh $host "rm -rf /var/run/flume"	
	ssh $host "rm -rf /var/run/hive2"	
	
	ssh $host "rm -rf /var/lib/flume"	
	ssh $host "rm -rf /etc/kafka"	
	ssh $host "rm -rf /var/run/kafka"	
	ssh $host "rm -rf /var/log/kafka"	
	ssh $host "rm -rf /kafka-logs"	 
	
	ssh $host "rm -rf /var/run/hive-hcatalog"
	ssh $host "rm -rf /var/run/knox"
	ssh $host "rm -rf /var/run/ranger"
	ssh $host "rm -rf /var/run/ranger_kms"
	ssh $host "rm -rf /var/run/smartsense-activity-analyzer"
	ssh $host "rm -rf /var/run/smartsense-activity-explorer"
	ssh $host "rm -rf /var/run/spark"
	ssh $host "rm -rf /var/run/spark2"
	ssh $host "rm -rf /var/run/sqoop"
	ssh $host "rm -rf /var/run/webhcat"
    ssh $host "rm -rf /var/log/hadoop"
    ssh $host "rm -rf /var/log/hbase"
    ssh $host "rm -rf /var/log/hive"
    ssh $host "rm -rf /var/log/nagios" 
    ssh $host "rm -rf /var/log/oozie"
    ssh $host "rm -rf /var/log/zookeeper" 
    ssh $host "rm -rf /var/log/falcon" 
    ssh $host "rm -rf /var/log/ambari-agent"
    ssh $host "rm -rf /var/log/ambari-infra-solr"
    ssh $host "rm -rf /var/log/ambari-metrics-grafana"	
	ssh $host "rm -rf /var/log/ambari-server"	
	ssh $host "rm -rf /var/log/hadoop-mapreduce"	
	ssh $host "rm -rf /var/log/hadoop-yarn"	
	ssh $host "rm -rf /var/log/hive2"	
	ssh $host "rm -rf /var/log/hive-hcatalog"
	ssh $host "rm -rf /var/log/knox"
	ssh $host "rm -rf /var/log/ranger"
	ssh $host "rm -rf /var/log/ranger_kms"
	ssh $host "rm -rf /var/log/smartsense-activity-analyzer"
	ssh $host "rm -rf /var/log/smartsense-activity-explorer"
	ssh $host "rm -rf /var/log/spark"
	ssh $host "rm -rf /var/log/spark2"
	ssh $host "rm -rf /var/log/sqoop"
	ssh $host "rm -rf /var/log/webhcat"	 
    ssh $host "rm -rf /usr/lib/hadoop"
    ssh $host "rm -rf /usr/lib/hbase"
    ssh $host "rm -rf /usr/lib/hcatalog" 
    ssh $host "rm -rf /usr/lib/hive"
    ssh $host "rm -rf /usr/lib/oozie"
    ssh $host "rm -rf /usr/lib/sqoop"
    ssh $host "rm -rf /usr/lib/zookeeper" 
    ssh $host "rm -rf /var/lib/hive"
    ssh $host "rm -rf /var/lib/ganglia" 
    ssh $host "rm -rf /var/lib/oozie"
    ssh $host "rm -rf /var/lib/zookeeper" 
    ssh $host "rm -rf /usr/lib/ambari-*"
    ssh $host "rm -rf /usr/lib/flume"
    ssh $host "rm -rf /usr/lib/storm"  
    ssh $host "rm -rf /var/tmp/oozie"
    ssh $host "rm -rf /tmp/hadoop-hdfs"	
	ssh $host "rm -rf /var/tmp/oozie"
	ssh $host "rm -rf /var/tmp/oozie"
	ssh $host "rm -rf /var/tmp/oozie"
	ssh $host "rm -rf /var/tmp/oozie"
	ssh $host "rm -rf /var/tmp/sqoop" 
    ssh $host "rm -rf /tmp/hive"
    ssh $host "rm -rf /tmp/nagios" 
    ssh $host "rm -rf /tmp/ambari-qa" 
    ssh $host "rm -rf /tmp/sqoop-ambari-qa"
    ssh $host "rm -rf /var/nagios"
    ssh $host "rm -rf /hadoop/oozie"
    ssh $host "rm -rf /hadoop/zookeeper"
    ssh $host "rm -rf /hadoop/mapred"
    ssh $host "rm -rf /hadoop/hdfs"
    ssh $host "rm -rf /tmp/hadoop-hive" 
    ssh $host "rm -rf /tmp/hadoop-nagios" 
    ssh $host "rm -rf /tmp/hadoop-hcat"
    ssh $host "rm -rf /tmp/hadoop-ambari-qa" 
    ssh $host "rm -rf /tmp/hsperfdata_hbase"
    ssh $host "rm -rf /tmp/hsperfdata_hive"
    ssh $host "rm -rf /tmp/hsperfdata_nagios"
    ssh $host "rm -rf /tmp/hsperfdata_oozie"
    ssh $host "rm -rf /tmp/hsperfdata_zookeeper"
    ssh $host "rm -rf /tmp/hsperfdata_mapred"
    ssh $host "rm -rf /tmp/hsperfdata_hdfs"
    ssh $host "rm -rf /tmp/hsperfdata_hcat"
    ssh $host "rm -rf /tmp/hsperfdata_ambari-qa"


    #删除ambari相关包
    ssh $host "yum remove -y ambari-*"
    ssh $host "yum remove -y postgresql"
    ssh $host "rm -rf /var/lib/ambari*"
    ssh $host "rm -rf /var/log/ambari*"
    ssh $host "rm -rf /etc/ambari*"
	    #1.)删除hdp.repo、HDP.repo、HDP-UTILS.repo和ambari.repo
    #ssh $host "cd $yumReposDir"
    #ssh $host "rm -rf $yumReposDir/hdp.repo"
    #ssh $host "rm -rf $yumReposDir/HDP*" 

    echo "$logPre======>$host is done! \n"
done
