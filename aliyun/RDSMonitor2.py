# -*- coding:utf-8 -*-
# if the python sdk is not install using 'sudo pip install aliyun-python-sdk-rds'
# if the python sdk is not install using 'sudo pip install aliyun-python-sdk-cms'

# if the python sdk is install using 'sudo pip install --upgrade aliyun-python-sdk-rds'
# if the python sdk is install using 'sudo pip install --upgrade aliyun-python-sdk-cms'

# make sure the sdk version is 2.1.2, you can use command 'pip show aliyun-python-sdk-rds' to check
# make sure the sdk version is 6.0.5, you can use command 'pip show aliyun-python-sdk-cms' to check

# !/usr/bin/env python
# coding=utf-8
import datetime
import json
import sys, time
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeDBInstancePerformanceRequest, DescribeDBInstanceAttributeRequest
from aliyunsdkcms.request.v20180308 import QueryMetricListRequest

PERFORMANCELIST = "CpuUsage,DiskUsage,IOPSUsage,ConnectionUsage,MySQL_NetworkTraffic,MySQL_QPSTPS,MySQL_Sessions,MySQL_InnoDBBufferRatio,\
MySQL_InnoDBDataReadWriten,MySQL_InnoDBLogRequests,MySQL_InnoDBLogWrites,MySQL_TempDiskTableCreates,\
MySQL_MyISAMKeyBufferRatio,MySQL_MyISAMKeyReadWrites,MySQL_COMDML,MySQL_RowDML,MySQL_MemCpuUsage,\
MySQL_IOPS,MySQL_DetailedSpaceUsage,slavestat,SQLServer_Transactions,SQLServer_Sessions,\
SQLServer_BufferHit,SQLServer_FullScans,SQLServer_SQLCompilations,SQLServer_CheckPoint,\
SQLServer_Logins,SQLServer_LockTimeout,SQLServer_Deadlock,SQLServer_LockWaits,SQLServer_NetworkTraffic,\
SQLServer_QPS,SQLServer_InstanceCPUUsage,SQLServer_IOPS,SQLServer_DetailedSpaceUsage"


def getRegionTime(region):
    if region == 'eu-central-1':
        hours = 7
    elif region == 'us-east-1':
        hours = 8
    else:
        hours = 8
    getTime = []
    getTime.append((datetime.datetime.now() - datetime.timedelta(minutes=10, hours=hours)).strftime("%Y-%m-%dT%H:%MZ"))
    getTime.append((datetime.datetime.now() - datetime.timedelta(minutes=0, hours=hours)).strftime('%Y-%m-%dT%H:%MZ'))
    return getTime


def RDSMonitor(ak, aks, region, DBInstanceId):
    gpus = ""
    if len(sys.argv) > 1:
        gpus = sys.argv[1]
        if gpus != "MaxConnections" and gpus != "MaxIOPS" and gpus != "DBInstanceStorage" and gpus != "MemoryUsage" and gpus != "DBInstanceMemory":
            if gpus.find("_") == -1:
                print "参数有误，必须包含\"_\"。如:MySQL_NetworkTraffic"
                return

    RDS = {}

    if gpus == "MySQL_MemoryUsage":
        # 查询该实例云监控内存使用率的平均值
        try:
            clt = client.AcsClient(ak, aks, region)
            request3 = QueryMetricListRequest.QueryMetricListRequest()
            request3.set_accept_format('json')
            request3.set_Project('acs_rds_dashboard')
            start_time = (datetime.datetime.now() - datetime.timedelta(minutes=8)).strftime('%Y-%m-%d %H:%M:%S')
            timestamp_start = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))) * 1000
            request3.set_StartTime(timestamp_start)
            request3.set_Metric('MemoryUsage')
            request3.set_Dimensions("{'instanceId':'" + DBInstanceId + "'}")
            request3.set_Period('300')
            result = json.loads(clt.do_action_with_exception(request3))
            print result['Datapoints'][-1]['Average']
        except Exception as e:
            print str(e)
        finally:
            return

    try:
        clt = client.AcsClient(ak, aks, region)
        request = DescribeDBInstancePerformanceRequest.DescribeDBInstancePerformanceRequest()
        request.set_DBInstanceId(DBInstanceId)
        request.set_Key(PERFORMANCELIST)
        request.set_StartTime(getRegionTime(region)[0])
        request.set_EndTime(getRegionTime(region)[1])

        response = clt.do_action_with_exception(request)
        response_dir = json.loads(response)
    except:
        print "ak,aks,地域或者实例ID配置有误"
    if response_dir['PerformanceKeys']['PerformanceKey'][0]['Values']['PerformanceValue'] == []:
        print  "还没有最新数据"
        return

    Engine = str(response_dir['Engine'])

    if Engine == 'MySQL':
        for i in range(len(response_dir['PerformanceKeys']['PerformanceKey'])):
            MySQL_key_head = str(response_dir['PerformanceKeys']['PerformanceKey'][i]['Key'])
            if MySQL_key_head == 'slavestat':
                continue
            MySQL_key_bodyList = str(response_dir['PerformanceKeys']['PerformanceKey'][i]['ValueFormat']).split('&')
            MySQL_valueList = str(
                response_dir['PerformanceKeys']['PerformanceKey'][i]['Values']['PerformanceValue'][-1]['Value']).split(
                '&')
            for i in range(len(MySQL_key_bodyList)):
                RDS[MySQL_key_head + "_" + MySQL_key_bodyList[i]] = MySQL_valueList[i]

    elif Engine == 'SQLServer':

        for i in range(len(response_dir['PerformanceKeys']['PerformanceKey'])):
            SQLServer_key = str(response_dir['PerformanceKeys']['PerformanceKey'][i]['Key'])
            if SQLServer_key == 'SQLServer_NetworkTraffic' or 'SQLServer_DetailedSpaceUsage':
                SQLServer_key_bodyList = str(response_dir['PerformanceKeys']['PerformanceKey'][i]['ValueFormat']).split(
                    '&')
                SQLServer_valueList = str(
                    response_dir['PerformanceKeys']['PerformanceKey'][i]['Values']['PerformanceValue'][-1][
                        'Value']).split('&')
                for i in range(len(SQLServer_key_bodyList)):
                    RDS[SQLServer_key + "_" + SQLServer_key_bodyList[i]] = SQLServer_valueList[i]

            else:
                SQLServer_value = str(
                    response_dir['PerformanceKeys']['PerformanceKey'][i]['Values']['PerformanceValue'][-1]['Value'])
                RDS[SQLServer_key] = SQLServer_value

    # 查询该实例的最大连接数，最大iops数
    request2 = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
    request2.set_DBInstanceId(DBInstanceId)
    request2.set_accept_format('json')
    response2 = clt.do_action_with_exception(request2)
    response_dir2 = json.loads(response2)
    try:
        RDS['MaxConnections'] = str(response_dir2['Items']['DBInstanceAttribute'][0]['MaxConnections'])
        RDS['MaxIOPS'] = str(response_dir2['Items']['DBInstanceAttribute'][0]['MaxIOPS'])
        RDS['DBInstanceStorage'] = str(response_dir2['Items']['DBInstanceAttribute'][0]['DBInstanceStorage'])
        RDS['DBInstanceMemory'] = str(response_dir2['Items']['DBInstanceAttribute'][0]['DBInstanceMemory'])
    except:
        pass

    if gpus != "":
        try:
            print RDS[gpus]
        except:
            print "参数有误，或此数据库应为%s类型，应以\"%s_\"开头" % (Engine, Engine)
    else:
        print json.dumps(RDS, indent=4)


if __name__ == '__main__':
    RDSMonitor('ak', 'aks', 'region','instanceid')  # mysql或sqlserver

