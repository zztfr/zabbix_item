#!/bin/bash
#校验MD5值，并邮件返回校验结果

Path=/backup/
Date=$(date +%F)
MileFile=/tmp/mail.txt
Mail_Title=rsync_backup_$Date
Mail_User=1393233384@qq.com

# check md5
find $Path -type f -iname "flag_$Date*"|xargs md5sum -c > $MileFile

# Send mail
/usr/bin/mail -s "$Mail_Title" $Mail_User < $MileFile

# Find Mtime 180
find $Path -type d -mtime +180|sed 1d| xargs rm -rf
