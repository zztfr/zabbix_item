#!/bin/bash
# 用户名
MYSQL_USER='用户名'
# 密码
MYSQL_PWD='密码'
# 主机地址/IP
MYSQL_HOST='主机ip'
# 端口
MYSQL_PORT='端口'
#数据连接
MYSQL_CONN="mysqladmin(命令实际路径) -u${MYSQL_USER} -p${MYSQL_PWD} -P${MYSQL_PORT}"
#数据库查询
MYSQL_CON="mysql(命令实际路径) -u${MYSQL_USER} -p${MYSQL_PWD} -P${MYSQL_PORT}"
# 参数是否正确
if [ $# -ne "1" ] ;then
echo "arg error!"
fi
# 获取数据
case $1 in
Uptime)
result=`${MYSQL_CONN} status|cut -f2 -d":"|cut -f1 -d"T"`
echo $result
;;
Com_update)
result=`${MYSQL_CONN} extended-status |grep -w "Com_update"|cut -d"|" -f3`
echo $result
;;
Slow_queries)
result=`${MYSQL_CONN} status |cut -f5 -d":"|cut -f1 -d"O"`
echo $result
;;
Com_select)
result=`${MYSQL_CONN} extended-status |grep -w "Com_select"|cut -d"|" -f3`
echo $result
;;
Com_rollback)
result=`${MYSQL_CONN} extended-status |grep -w "Com_rollback"|cut -d"|" -f3`
echo $result
;;
Questions)
result=`${MYSQL_CONN} status|cut -f4 -d":"|cut -f1 -d"S"`
echo $result
;;
Com_insert)
result=`${MYSQL_CONN} extended-status |grep -w "Com_insert"|cut -d"|" -f3`
echo $result
;;
Com_delete)
result=`${MYSQL_CONN} extended-status |grep -w "Com_delete"|cut -d"|" -f3`
echo $result
;;
Com_commit)
result=`${MYSQL_CONN} extended-status |grep -w "Com_commit"|cut -d"|" -f3`
echo $result
;;
Bytes_sent)
result=`${MYSQL_CONN} extended-status |grep -w "Bytes_sent" |cut -d"|" -f3`
echo $result
;;
Bytes_received)
result=`${MYSQL_CONN} extended-status |grep -w "Bytes_received" |cut -d"|" -f3`
echo $result
;;
Com_begin)
result=`${MYSQL_CONN} extended-status |grep -w "Com_begin"|cut -d"|" -f3`
echo $result
;;
Ping)
result=`${MYSQL_CONN} ping|grep -c alive`
echo $result
;;
Version)
result=`/usr/bin/mysql -V | cut -f6 -d" " | sed 's/,//'`
echo $result
;;
Process)
result=`${MYSQL_CON} -e "show processlist" 2>/dev/null|wc -l`
echo $result
;;
Seconds_Behind_Master)
result=`${MYSQL_CON} -e 'show slave status\G' | grep 'Seconds_Behind_Master'|cut -f2 -d":"`
echo $result
;;
Slave_IO_Running)
result=`${MYSQL_CON} -e 'show slave status\G'|grep 'Slave_IO_Running'|cut -f2 -d":"|grep -i Yes|wc -l`
echo $result
;;
Slave_SQL_Running)
result=`${MYSQL_CON} -e 'show slave status\G'|grep 'Slave_SQL_Running'|cut -f2 -d":"|grep -i Yes|wc -l`
echo $result
;;
*)
echo "Usage:$0(Uptime|Com_update|Slow_queries|Com_select|Com_rollback|Questions|Com_insert|Com_delete|Com_commit|Bytes_sent|Bytes_received|Com_begin|Ping|Process|Seconds_Behind_Master|Slave_IO_Running|Slave_SQL_Running)"
;;
esac
