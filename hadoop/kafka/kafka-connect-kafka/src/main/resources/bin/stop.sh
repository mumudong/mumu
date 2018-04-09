#!/bin/sh


if [[ "X$1" == "X" ]] ; then
        echo "usage:$0 basename"
        exit 1
fi

base=$(cd dirname $0/..;pwd)

appName=$1

pidfile=$base/bin/${appName}.pid
if [ ! -f "$pidfile" ];then
        echo "$appName is not running. exit."
        exit
fi

get_pid() {
    STR=$1
    PID=$2

    if [ ! -z "$PID" ]; then
                JAVA_PID=`ps -C java -f --width 1000|grep "$STR"|grep "$PID"|grep -v grep|awk '{print $2}'`
    else 
                JAVA_PID=`ps -C java -f --width 1000|grep "$STR"|grep -v grep|awk '{print $2}'`
    fi
    echo $JAVA_PID;
}

pid=`cat $pidfile`
if [ "$pid" == "" ] ; then
    pid=`get_pid "appName=${appName}"`
fi

echo -e "`hostname`: stopping canal $pid ... "

if [[ "X$PID" != " X" ]]; then
    kill $pid
fi

LOOPS=0
while (( $LOOPS < 10 )) ;
do
    gpid=`get_pid "appName=${appName}" "$pid"`
    if [ "$gpid" == "" ] ; then
        echo "Oook! cost:$LOOPS"
        `rm $pidfile`
        break;
    fi
    let LOOPS=LOOPS+1
    sleep 1
done

if [[ "X$gpid" != "X" ]]; then
    echo "kill -9 $gpid"
    kill -9 $gpid
    exit 1
fi

