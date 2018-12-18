#!/usr/bin/env python
import os
import simplejson as json 
t=os.popen("""netstat -tnlp|awk {'print $4'}|awk -F':' '{if ($NF~/^[0-9]*$/) print $NF}'|sort|uniq """)
ports = []
for port in  t.readlines():
        r = os.path.basename(port.strip())
        ports += [{'{#TCP_PORT}':r}]
print json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))
