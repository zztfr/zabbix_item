# analysis_binlog

#### 介绍
分析binlog工具，现有功能：

- 1、基于业务表分析统计各个表的dml的次数。
- 2、各个业务表的最后访问时间。
- 3、各dml总的dml。
- 4、该binlog的事务总数。
- 5、其他功能敬请期待。

> git 连接：https://gitee.com/mo-shan/analysis_binlog



工具介绍
```
root /data/git/analysis_binlog/bin >> bash analysis_binlog -h


Usage: bash analysis_binlog [OPTION]...

--type=value or -t=value          The value=detail | simple
                                  For example: --type=detail,-t=detail,-t=simple,-t=simple,
                                  The "detail": The results displayed are more detailed, but also take more time.
                                  The "simple": The results shown are simple, but save time
                                  The default value is "simple". 

--binlog-dir or -bdir             Specify a directory for the binlog dir.
                                  For example: --binlog-dir=/mysql_binlog_dir,-bdir=/mysql_binlog_dir
                                  If the input is a relative path, it will be automatically modified to an absolute path.
                                  The default value is "Current path". 

--binlog-file or -bfile           Specify a file for the binlog file, multiple files separated by ",".
                                  For example: --binlog-file=/path/mysql_binlog_file,-bfile=/path/mysql_binlog_file
                                               --b-file=/path/mysql_binlog_file1,/path/mysql_binlog_file1
                                  If the input is a relative path, it will be automatically modified to an absolute path.
                                  If this parameter is used, the "--binlog-dir or -bdir" parameter will be invalid.

--sort or -s                      Sort the results for "INSERT | UPDATE | DELETE"
                                  The value=insert | update | delete
                                  The default value is "insert".

--threads or -w                   Decompress/compress the number of concurrent. For example:--threads=8
                                  This parameter works only when there are multiple files.
                                  If you use this parameter, specify a valid integer, and the default value is "1".

--help or -h                      Display this help and exit.

```



使用例子：

1、克隆项目
```
git clone https://gitee.com/mo-shan/analysis_binlog.git
```
进入analysis_binlog的家目录

2、更改路径(第一次使用需要配置)

(1)更改mysqlbinlog路径
```
sed -i 's/mysqlbinlog=.*/mysqlbinlog=\"/mysqlbinlog_path\"/g' bin/analysis_binlog #将这里的mysqlbinlog_path改成mysqlbinlog工具的绝对路径,否则可能会因版本太低导致错误
```

(2)更改analysis_binlog家目录路径
```
sed -i 's/work_dir=.*/work_dir=\"/analysis_binlog_path\"/g' bin/analysis_binlog #将这里的analysis_binlog_path改成analysis_binlog的家目录的绝对路径
```

3、为analysis_binlog配置环境变量(选做)
```
chmod +x bin/analysis_binlog 
echo "export PATH=$(pwd)/bin:${PATH}" >> ${HOME}/.bashrc
```

4、根据需求执行
- -bfile: 指定binlog文件, 支持多个文件并行分析, 多个文件用逗号相隔, 需要并行分析时请结合-w参数使用
- -w    : 指定并行数, 当需要分析多个binlog文件时该参数有效, 默认是1
- -t    : 指定显示结果的格式/内容, 供选选项有"detail|simple". 当指定detail的时候结果较为详细, 会打印详细的分析过程, 消耗时间也不直观, simple只做了统计工作
- -s    : 指定排序规则, 供选选项有"insert|update|delete". 默认会把统计结果做一个排序, 按照表的维度统计出insert update delete的次数, 并按照次数大小排序(默认insert)
>注: 其他参数使用请参见帮助手册 bash analysis_binlog -h

(1)配置了环境变量
```
analysis_binlog -bfile=/data/mysql/binlog/3306/mysql-bin.000798,/data/mysql/binlog/3306/mysql-bin.000799 -w=2 -t=simple -s=update  
```
(2)未配置环境变量
```
bash bin/analysis_binlog -bfile=/data/mysql/binlog/3306/mysql-bin.000798,/data/mysql/binlog/3306/mysql-bin.000799 -w=2 -t=simple -s=update  
```

5、结果查询

分析完毕会在analysis_binlog家目录下的res目录下保存一个[binlog_file_name.res]文件，使用文本工具打开即可, 建议使用cat, tail, more, 如下结果展示, 会按照表的维度做个统计, 然后按照update的次数排序, Last Time表示该表的最后一次操作
```
root /data/git/analysis_binlog/res >> cat mysql-bin.000798.res
Table                                                       Last Time                     Insert(s)      Update(s)      Delete(s)      
moshan.flush_                                               190311 9:28:54                0              3475           0              
ultrax.dis_common_syscache                                  190312 11:31:53               0              231            0              
ultrax.dis_common_cron                                      190312 11:31:53               0              194            0              
ultrax.dis_common_session                                   190312 10:38:56               6              170            5              
ultrax.dis_forum_forum                                      190312 9:19:10                0              129            0              
moshan.money                                                190311 9:28:37                29             80             0              
ultrax.dis_common_onlinetime                                190312 10:38:42               0              48             0              
ultrax.dis_forum_thread                                     190312 10:38:56               4              47             0              
ultrax.dis_common_member_count                              190312 10:38:53               0              47             0              
ultrax.dis_common_credit_rule_log                           190312 10:38:53               0              38             0              
ultrax.dis_forum_post                                       190312 9:24:30                4              34             0              
ultrax.dis_common_member_status                             190312 9:04:42                0              20             0              
moshan.history_                                             190308 9:28:25                0              10             0              
ice_db.server_setting_tmp                                   190304 10:34:19               564            8              0              
ultrax.dis_common_process                                   190312 11:31:53               201            7              201            
ultrax.dis_common_setting                                   190312 9:04:42                0              7              0              
moshan.tmp_table                                            190304 17:17:21               0              7              0              
ultrax.dis_ucenter_failedlogins                             190306 10:07:11               0              4              0              
ultrax.dis_common_member_field_home                         190311 14:54:47               0              4              0              
ultrax.dis_forum_threadcalendar                             190312 9:09:56                2              2              0              
ultrax.dis_forum_attachment                                 190306 11:46:56               2              2              0              
moshan.use_date                                             190304 17:12:22               0              1              0              
ultrax.dis_forum_threadhot                                  190312 9:09:56                4              0              0              
ultrax.dis_forum_threaddisablepos                           190311 14:54:47               1              0              0              
ultrax.dis_forum_statlog                                    190312 9:04:42                304            0              0              
ultrax.dis_forum_sofa                                       190311 14:54:47               4              0              0              
ultrax.dis_forum_post_tableid                               190311 14:54:47               4              0              0              
ultrax.dis_forum_newthread                                  190311 14:54:47               4              0              6              
ultrax.dis_forum_attachment_unused                          190306 11:46:56               2              0              2              
ultrax.dis_forum_attachment_8                               190306 11:46:56               1              0              0              
ultrax.dis_forum_attachment_0                               190306 11:46:29               1              0              0              
ultrax.dis_common_statuser                                  190311 11:40:44               4              0              4              
ultrax.dis_common_searchindex                               190312 10:38:53               28             0              0              
ultrax.dis_common_member_action_log                         190311 14:54:47               4              0              4              
test.ttt                                                    190303 11:43:36               2              0              0              
test.t_test                                                 190308 16:52:35               4              0              0              
test.t_message_list                                         190313 9:30:16                307544         0              0              
test.t_message_content_lately                               190313 9:30:16                307544         0              0              
test.admin_user                                             190308 11:51:50               3              0              3              


Trans(total)                                                Insert(s)                     Update(s)      Delete(s)      
312619                                                      616270                        4565           225            
root /data/git/analysis_binlog/res >> 
```
