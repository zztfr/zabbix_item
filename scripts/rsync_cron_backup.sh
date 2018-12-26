#Mkdir Directory
#client端备份推送脚本
#注意：需要写入定时任务


Client_Dir=/backup
Client_Hostname=$(hostname)
Client_IP=$(/usr/sbin/ifconfig ens32|awk 'NR==2'|awk '{print $2}')
Client_date=$(date +%F)
Client_Dest_Dir="$Client_Dir"/"$Client_Hostname"_"$Client_IP"_"$Client_date"

[ ! -d $"$Client_Dest_Dir" ] && mkdir -p "$Client_Dest_Dir"

##setup2 copy configure, conf,log
/bin/tar czf "$Client_Dest_Dir"/conf_"$Client_date".tar.gz -C /  var/spool/cron/ etc/rc.local etc/fstab  etc/hosts && \
##log
/bin/tar czf "$Client_Dest_Dir"/system_log_"$Client_date".tar.gz -C / var/log/ && \

##scripts
/bin/tar czf "$Client_Dest_Dir"/scripts_"$Client_date".tar.gz  -C / soft/scripts && \
##rsync
/bin/tar czf "$Client_Dest_Dir"/rsync_config_"$Client_date".tar.gz -C / etc/rsyncd.conf etc/rsync.password
##md5sum
/usr/bin/md5sum "$Client_Dest_Dir"/*_"$Client_date".tar.gz > "$Client_Dest_Dir/flag_"$Client_date".md5"

###setup3 rsync push data
Server_User=rsync_backup
Server_IP=192.168.56.21
Server_Mode=backup/
Server_Pass=/etc/rsync.pass
/usr/bin/rsync -avz $Client_Dir/ $Server_User@$Server_IP::$Server_Mode --password-file=$Server_Pass

##setup4 find time out 30
/usr/bin/find $Client_Dir -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \;
