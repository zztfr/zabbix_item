# -*- coding:utf-8 -*-
import json,sys,time
from aliyunsdkcore import client
from aliyunsdkcore.request import CommonRequest

def cms_EIP(ak,aks,region,instanceID,metric):
    clt = client.AcsClient(ak,aks,region)
    request = CommonRequest(domain='metrics.cn-shanghai.aliyuncs.com', version='2017-03-01', action_name='QueryMetricList')

    request.add_query_param('Project','acs_vpc_eip')
    request.add_query_param('Dimensions',"{'instanceId':'"+instanceID+"'}")
    request.add_query_param('Metric',metric)

    request.add_query_param('StartTime', int(time.time()) * 1000 - 60 * 2000)
    response = json.loads(clt.do_action_with_exception(request))
    print response['Datapoints'][len(response['Datapoints']) - 1]['Value']

if __name__ == '__main__':
    if len(sys.argv)<2:
        print "没有参数"
    else:
        ak="ak"
        aks="aks"
        region="region"
        instanceID = "instanceID"
        metric=sys.argv[1]
        cms_EIP(ak,aks,region,instanceID,metric)

