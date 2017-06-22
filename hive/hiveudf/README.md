#hiveudf

## 编译方法
mvn clean

mvn package
## 身份证转换函数

com.asiainfo.dacp.platform.hive.udf.generic.UDFIDTrans

- 15位转18位
- 如果18位最后一位为x，则将x转换10拼接在最后
- 其他输出为字符错误信息“is error”信息

## 使用方法
1. 编译后的jar包上传到hive主机某个目录，如我上传的/root/dacpudf目录
2. 进入hive shell环境
2. 增加jar包如下

```
add jar /root/dacpudf/datasec-hive-udf-2.1.0.jar

create temporary function transid as 'com.asiainfo.dacp.platform.hive.udf.generic.UDFIDTrans';

select transid('510214910624174') FROM tf_a_payrelation limit 1;

```
3. 输出信息为510214199106241740


## 异常处理
### java版本异常
```
Caused by: java.lang.UnsupportedClassVersionError: 
com/asiainfo/dacp/platform/hive/udf/generic/UDFIDTrans : Unsupported major.minor version 52.0
```

这个情况是我们使用的0.12.0-cdh5.1.0版本貌似内核是1.6编译的，因此在eclipse设置重新编译输出版本为1.6重新上传即可
