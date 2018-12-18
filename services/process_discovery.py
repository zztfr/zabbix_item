#!/usr/bin/env python
import os
import simplejson as json 
t=os.popen("""netstat -tlnp|grep -Ev 'PID|Active'|awk '{print $4" "$7}'|awk -F'/' '{print $NF}'|sort -u|awk -F':' '{print $1}' """)
processs = []
for process in  t.readlines():
        r = os.path.basename(process.strip())
        processs += [{'{#PROCESS_STATUS}':r}]
print json.dumps({'data':processs},sort_keys=True,indent=4,separators=(',',':'))
