#!/usr/bin/env python
import os
import simplejson as json 
t=os.popen("""cat /usr/local/zabbix-proxy/monitor_scripts/slb_port.txt""")
ports = []
for port in t.readlines():
        r = os.path.basename(port.strip())
        ports += [{'{#SLB_PORT}':r}]
print json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))
