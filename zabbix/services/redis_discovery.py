#!/usr/bin/env python
import os
import simplejson as json 
t=os.popen("""sudo netstat -tlpn |grep redis-server|grep 0.0.0.0|awk '{print $4}'|awk -F: '{print $2}' """)
ports = []
for port in  t.readlines():
        r = os.path.basename(port.strip())
        ports += [{'{#REDIS_PORT}':r}]
print json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))