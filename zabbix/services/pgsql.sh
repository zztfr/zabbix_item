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
 
    'db_cache')
            # 缓存
            if [ ! -z $2 ]; then
            shift
                sql="select cast(blks_hit/(blks_read+blks_hit+0.000001)*100.0 as numeric(5,2)) as cache from pg_stat_database where datname = '$1'"
        fi
            ;;
 
    'db_success')
            # 成功率
        if [ ! -z $2 ]; then
            shift
                   sql="select cast(xact_commit/(xact_rollback+xact_commit+0.000001)*100.0 as numeric(5,2)) as success from pg_stat_database where datname = '$1'"
        fi
        ;;
 
    'server_processes')
         #数据库所有连接数
        sql="select sum(numbackends) from pg_stat_database"
        ;;
 
    'tx_commited')
         #提交数
        sql="select sum(xact_commit) from pg_stat_database;"
        ;;
 
    'tx_rolledback')
         #回滚数
        sql="select sum(xact_rollback) from pg_stat_database"
        ;;
 
    'db_size')
        # 查数据库总大小(占用磁盘空间)
            if [ ! -z $2 ]; then
            shift
            sql="select pg_database_size('$1')" #as size"
        fi
        ;;
 
    'db_connections')
            # 当前连接数 
            if [ ! -z $2 ]; then
            shift
                sql="select numbackends from pg_stat_database where datname = '$1'"
        fi
        ;;
    'max_connections')
            # 最大连接数
            if [ ! -z $2 ]; then
            shift
                sql="show max_connections"
        fi
        ;;
    'db_returned')
        # 呈现这些数据要返回给客户的端的行数 
            if [ ! -z $2 ]; then
            shift
            sql="select tup_returned from pg_stat_database where datname = '$1'"
        fi
        ;;
 
    'db_fetched')
            # 呈现给用户的行数
            if [ ! -z $2 ]; then
            shift
                sql="select tup_fetched from pg_stat_database where datname = '$1'"
        fi
        ;;
 
    'db_inserted')
        # 插入记录数
            if [ ! -z $2 ]; then
                shift
                sql="select tup_inserted from pg_stat_database where datname = '$1'"
        fi
            ;;
 
    'db_updated')
        # 更新记录数
            if [ ! -z $2 ]; then
                shift
                sql="select tup_updated from pg_stat_database where datname = '$1'"
        fi
            ;;
 
    'db_deleted')
        # 删除记录数
            if [ ! -z $2 ]; then
                shift
                sql="select tup_deleted from pg_stat_database where datname = '$1'"
        fi
            ;;
 
    'db_commited')
        # 提交记录数
            if [ ! -z $2 ]; then
                shift
            sql="select xact_commit from pg_stat_database where datname = '$1'"
        fi
        ;;
 
    'db_rolled')
        # 回滚记录数
        if [ ! -z $2 ]; then
                shift
            sql="select xact_rollback from pg_stat_database where datname = '$1'"
        fi
        ;;
 
    'version')
         #数据库版本
        sql="version"
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
