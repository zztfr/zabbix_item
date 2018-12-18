#!/usr/bin/env python
import os
import simplejson as json 
t=os.popen("""export PGPASSWORD='密码' && psql命令路径 -h 主机 -p 端口 postgres 用户名 -t -c "select datname from pg_database" |grep -v '^$' |grep -v 'template' """)
instances = []
for instance in  t.readlines():
        r = os.path.basename(instance.strip())
        instances += [{'{#PGSQL_INSTANCE}':r}]
print json.dumps({'data':instances},sort_keys=True,indent=4,separators=(',',':'))