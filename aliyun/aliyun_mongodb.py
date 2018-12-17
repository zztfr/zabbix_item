#!/usr/bin/env python
#coding: utf-8
from aliyunsdkcore import client
from aliyunsdkcms.request.v20180308 import QueryMetricListRequest
import time,datetime,sys,json

def getTime():
    return (datetime.datetime.now()-datetime.timedelta(minutes=6)).strftime("%Y-%m-%d %H:%M:%S")

def getResult(ak,aks,region,instanceId,role,userId):
    clt = client.AcsClient(ak,aks,region)
    request = QueryMetricListRequest.QueryMetricListRequest()
    request.set_accept_format('json')
    request.set_Project('acs_mongodb')
    request.set_Metric(sys.argv[1])
    start_time = str(getTime())
    timestamp_start = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))) * 1000
    request.set_Dimensions("{'instanceId':'"+instanceId+"','role':'"+role+"','userId':'"+userId}")
    request.set_Period('300')
    request.set_StartTime(timestamp_start)
    result = clt.do_action_with_exception(request)
    result_value = json.loads(result)
    #print result_value
    print eval(result_value['Datapoints'])[-1][sys.argv[2]]


if __name__ == "__main__":
    getResult('ak', 'aks', 'region','instanceid','role','userId')
