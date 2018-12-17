# -*- coding:utf-8 -*-

import json
import sys
import re
from aliyunsdkcore import client
from aliyunsdkcore.request import CommonRequest


# from aliyunsdkcms.request.v20180308 import QueryMetricListRequest

# 安装架包：aliyun-python-sdk-core
# sudo pip install aliyun-python-sdk-core

class MemcacheMonitor:
    def __init__(self, _ak, _secret, _region_id, _instanceId):
        self.region_id = _region_id
        self.ak = _ak
        self.instanceId = _instanceId
        self.clt = client.AcsClient(
            ak=_ak,
            secret=_secret,
            region_id=_region_id
        )

    def getInformation(self, Metric):
        if Metric == 'help':
            print u"""
            更多监控项请查看：https://help.aliyun.com/document_detail/28619.html?spm=a2c4g.11186623.6.676.ddaefx#h2--memcache-6
            """
            return
        try:
            _domian = "metrics.%s.aliyuncs.com" % self.region_id
            request = CommonRequest(domain=_domian, version='2018-03-08', action_name='QueryMetricList')
            request.add_query_param('Project', 'acs_memcache')
            request.add_query_param('Metric', Metric)
            request.add_query_param('Dimensions', "{'instanceId':'" + self.instanceId + "'}")
            response = json.loads(self.clt.do_action_with_exception(request))
            #print response  # 查看返回的结果
            if response['Datapoints'] != u'[]':
                restr = "\"Average\":(\\d+(\\.\\d+)?)"
                regex = re.compile(restr, re.IGNORECASE)
                mylist = regex.findall(response['Datapoints'])
                # print mylist   查看正则匹配的数值和小数
                if Metric == 'UsedMemory':
                    print mylist[-1][0] + "E7"
                else:
                    print mylist[-1][0]
            else:
                print u'暂无返回结果'


        except Exception as e:
            print u"""
无法获取：%s

更多Metric监控项请查看：
https://help.aliyun.com/document_detail/28619.html?spm=a2c4g.11186623.6.676.ddaefx#h2--memcache-6""" % str(e)


if __name__ == '__main__':
    MemcacheMonitor("ak", "aks", "region",
                    "instanceId").getInformation(sys.argv[1])
