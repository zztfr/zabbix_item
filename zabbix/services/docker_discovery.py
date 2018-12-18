#!/usr/bin/env python
import os
import simplejson as json 
t=os.popen("""sudo docker ps |grep -v "CONTAINER ID" |  awk '{print $NF}'|egrep -Ev "r-ip|r-n|r-h|r-s" """)
containers = []
for container in  t.readlines():
        r = os.path.basename(container.strip())
        containers += [{'{#CONTAINERNAME}':r}]
print json.dumps({'data':containers},sort_keys=True,indent=4,separators=(',',':'))

