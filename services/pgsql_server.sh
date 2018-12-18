#!/bin/sh


    export PGPASSWORD='密码'

    zapostver="1.0"
    rval=0
    sql=""
    case $1 in
    'totalsize')
            # 查数据库总大小(占用磁盘空间)
            sql="select sum(pg_database_size(datid)*0.001) as total_size from pg_stat_database"
            ;;
 
     'start_time')
            # 查数据库启动时间
            sql="select pg_postmaster_start_time()"
            ;;
    'server_processes')
         #数据库所有连接数
        sql="select sum(numbackends) from pg_stat_database"
        ;;
    'max_connections')
            # 最大连接数
        sql="show max_connections"
        ;;
    'zapostver')
           #
            echo "$zapostver"
        exit $rval
            ;;
 
    *)
        echo " 参数错误......."
            exit $rval
            ;;
    esac
    if [ "$sql" != "" ]; then
        if [ "$sql" == "version" ]; then
            psql命令路径 --version|head -n1
            rval=$?
        else
            psql命令路径 -h 主机 -p 端口 postgres 用户名 -t -c "$sql"
            rval=$?
        fi
    fi
 
    if [ "$rval" -ne 0 ]; then
          echo "错误"
fi
exit $rval
