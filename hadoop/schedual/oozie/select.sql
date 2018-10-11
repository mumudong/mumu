insert overwrite directory '/test/oozie/test' ROW format delimited fields terminated by ',' select id,name from default.import_from_mysql_testtt;
