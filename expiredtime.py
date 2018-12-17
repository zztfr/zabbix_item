# -*- coding:utf-8 -*-

# pip install aliyun-python-sdk-core
# python2
# pip install -U aliyun-python-sdk-core

# python3
# pip3 install -U aliyun-python-sdk-core-v3
from aliyunsdkcore import client
from aliyunsdkcore.request import CommonRequest
from multiprocessing import Process, Manager
import json, datetime, time, sys

reload(sys)
sys.setdefaultencoding('utf-8')

ecs = {'domain': 'ecs.aliyuncs.com', 'version': '2014-05-26', "action_name": 'DescribeInstances', 'PageSize': 100}
rds = {'domain': 'rds.aliyuncs.com', 'version': '2014-08-15', 'action_name': 'DescribeDBInstances', 'PageSize': 100}
redis = {'domain': 'r-kvstore.aliyuncs.com', 'version': '2015-01-01', 'action_name': 'DescribeInstances',
         'PageSize': 50}
mongodb = {'domain': 'mongodb.aliyuncs.com', 'version': '2015-12-01', 'action_name': 'DescribeDBInstances',
           'PageSize': 100}


class instance:
    def __init__(self, ak, aks):
        self.ak = ak
        self.aks = aks
        self.timeRange = 3
        self.error = False
        self.ecs = True
        self.rds = True
        self.redis = True
        self.mongodb = True

    def get_region(self, ali_type, action_name='DescribeRegions'):
        try:
            clt = client.AcsClient(self.ak, self.aks)
            request = CommonRequest(domain=ali_type['domain'], version=ali_type['version'], action_name=action_name)
            response = json.loads(clt.do_action_with_exception(request))
            # print response
            return response
        except Exception as e:
            if self.error:
                print str(e)
            print '连接失败,阿里云的地域都无法获得。可能ak等配置有误；或服务器连接失败啦'
            return

    def get_instance(self, ali_type, region_id):
        try:
            clt = client.AcsClient(self.ak, self.aks, region_id)
            request = CommonRequest(domain=ali_type['domain'], version=ali_type['version'],
                                    action_name=ali_type['action_name'])
            request.add_query_param('PageSize', ali_type['PageSize'])
            request.add_query_param('PageNumber', '1')
            response = json.loads(clt.do_action_with_exception(request))
            # print response
            return response
        except Exception as e:
            if self.error:
                print str(e)
            return []

    @staticmethod
    def hasdays(str):
        try:
            gettimes = str.split("-")
            day = gettimes[2].split("T")
            d1 = datetime.date(int(gettimes[0]), int(gettimes[1]), int(day[0]))
            str2 = time.strftime("%Y-%m-%d")
            nowtimes = str2.split("-")
            d2 = datetime.date(int(nowtimes[0]), int(nowtimes[1]), int(nowtimes[2]))
            return (d1 - d2).days
        except:
            return -9999

    def ecs_expiredtime(self, d):
        if self.ecs == False:
            return
        try:
            region = self.get_region(ecs)['Regions']['Region']
            for i in region:
                instance_result = self.get_instance(ecs, i['RegionId'])
                if instance_result == []:
                    continue
                else:
                    instances = instance_result['Instances']['Instance']
                    if instances == []: continue
                    for j in range(0, len(instances)):
                        if instances[j]["InstanceChargeType"] == "PrePaid":
                            daysi = instances[j]['ExpiredTime']
                            days = self.hasdays(daysi)
                            if days <= self.timeRange and days >= 0:
                                d[0] = 1
                                print "ECS will be expired after %s days,deadline:%s,instance-id:%s" % (
                                    days, daysi.replace('T', ' ').replace('Z', ''),
                                    instances[j]["InstanceId"])
                        elif instances[j]["InstanceChargeType"] == "PostPaid":
                            daysi = instances[j]['ExpiredTime']
                            days = self.hasdays(daysi)
                            if days <= self.timeRange and days >= 0:
                                d[0] = 1
                                print "ECS's InstanceChargeType is PostPaid，but you have released it  %s days later,deadline:%s,instance-id:%s" % (
                                    days, daysi.replace('T', ' ').replace('Z', ''),
                                    instances[j]["InstanceId"])
        except Exception as e:
            if self.error:
                print str(e)
            print "ecs获取失败"

    def rds_expiredtime(self, d):
        if self.rds == False:
            return
        try:
            regionlist = self.get_region(rds)['Regions']['RDSRegion']
            region = []
            for i in regionlist:
                region.append(i['RegionId'])
            region = list(set(region))
            for i in region:
                instance_result = self.get_instance(rds, i)
                if instance_result == []:
                    continue
                else:
                    instances = instance_result['Items']['DBInstance']
                    if instances == []: continue
                    for i in range(0, len(instances)):
                        if instances[i]["PayType"] == "Prepaid" and \
                                instances[i]["DBInstanceType"] == "Primary":
                            daysi = instances[i]["ExpireTime"]
                            days = self.hasdays(daysi)
                            if days <= self.timeRange and days >= 0:
                                d[0] = 1
                                print "RDS will be expired after %s days,deadline:%s,instance-id:%s" % (
                                    days, daysi.replace('T', ' ').replace('Z', ''),
                                    instances[i]["DBInstanceId"])
                        elif instances[i]["PayType"] == "PostPaid" and \
                                instances[i]["DBInstanceType"] == "Primary":
                            daysi = instances[i]["ExpireTime"]
                            days = self.hasdays(daysi)
                            if days <= self.timeRange and days >= 0:
                                d[0] = 1
                                print "RDS's InstanceChargeType is PostPaid，but you have released it %s days later,deadline:%s,instance-id:%s" % (
                                    days, daysi.replace('T', ' ').replace('Z', ''),
                                    instances[i]["DBInstanceId"])
        except Exception as e:
            if self.error:
                print str(e)
            print "rds获取失败"

    def redis_expiredtime(self,d):
        if self.redis == False:
            return
        try:
            regionlist = self.get_region(rds)['Regions']['RDSRegion']
            region = []
            for i in regionlist:
                region.append(i['RegionId'])
            region = list(set(region))
            for i in region:
                instance_result = self.get_instance(redis, i)
                if instance_result == []:
                    continue
                else:
                    instances = instance_result['Instances']['KVStoreInstance']
                    if instances == []: continue
                    for i in range(0, len(instances)):
                        if instances[i]['ChargeType'] != 'PrePaid': continue
                        EndTime = instances[i]['EndTime']
                        days = self.hasdays(EndTime)
                        if days <= self.timeRange and days >= 0:
                            d[0] = 1
                            print "Redis will be expired after %s days,deadline:%s,instance-id:%s" % (
                                days, EndTime.replace('T', ' ').replace('Z', ''),
                                instances[i]['UserName'])
        except Exception as e:
            if self.error:
                print str(e)
            print "redis获取失败"

    def mongodb_expiredtime(self,d):
        if self.mongodb == False:
            return
        try:
            regionlist = self.get_region(mongodb)['Regions']['DdsRegion']
            region = []
            for i in regionlist:
                region.append(i['RegionId'])
            region = list(set(region))
            for i in region:
                instance_result = self.get_instance(mongodb, i)
                if instance_result == []:
                    continue
                else:
                    instances = instance_result['DBInstances']['DBInstance']
                    if instances == []: continue
                    for i in range(0, len(instances)):
                        if instances[i]['ChargeType'] != 'PrePaid': continue
                        ExpireTime = instances[i]['ExpireTime']
                        days = self.hasdays(ExpireTime)
                        if days <= self.timeRange and days >= 0:
                            d[0] = 1
                            print "MongoDB will be expired after %s days,deadline:%s,instance-id:%s" % (
                                days, ExpireTime.replace('T', ' ').replace('Z', ''),
                                instances[i]['DBInstanceId'])
        except Exception as e:
            if self.error:
                print str(e)
            print "mongoDB获取失败"

    def main(self):

        m = Manager()
        d = m.dict()
        d[0]=0  # 为0表示所有产品运行正常
        p_ecs = Process(target=i.ecs_expiredtime, args=(d,))
        p_rds = Process(target=i.rds_expiredtime, args=(d,))
        p_redis = Process(target=i.redis_expiredtime, args=(d,))
        p_mongodb = Process(target=i.mongodb_expiredtime, args=(d,))

        p_ecs.start()
        p_rds.start()
        p_redis.start()
        p_mongodb.start()

        p_ecs.join()
        p_rds.join()
        p_redis.join()
        p_mongodb.join()

        if d[0] != 1:
            print "All products run normally"


if __name__ == '__main__':
    i = instance("ak", "aks")
    i.timeRange = 10  # 设置到期时间范围（天）／支持'ecs'、'rds' 按量在此时间范围内释放（按量付费默认到期365000天内）

    # i.error=False       #更新脚本报错防敏感信息泄露功能。True用于查看脚本报错，默认运行设置为False

    i.ecs = True  # ecs到期时间范围内的实例
    i.rds = True  # rds到期时间范围内的实例
    i.redis = True  # redis到期时间范围内的实例
    i.mongodb = True  # mongodb到期时间范围内的实例

    i.main()
