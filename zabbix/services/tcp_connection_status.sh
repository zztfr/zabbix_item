#!/bin/bash
#author: 范俊、陆逸
#获取非established连接数
non_established_cont(){
    netstat -an | awk '/^tcp/ {a[$NF]++} END {for (b in a) print b,a[b]}'|grep -v ESTABLISHED |cut -d ' ' -f 2|awk '{sum+=$1}END{print sum}'
}

#获取established连接数
established_cont(){
    netstat -an | awk '/^tcp/ {a[$NF]++} END {for (b in a) print b,a[b]}'|grep ESTABLISHED |cut -d ' ' -f 2|awk '{sum+=$1}END{print sum}'
}

#获取TCP连接总数
tcp_total_cont(){
    netstat -an | awk '/^tcp/ {a[$NF]++} END {for (b in a) print b,a[b]}'|cut -d ' ' -f 2|awk '{sum+=$1}END{print sum}'
}


case $1 in
   established_cont)
       established_cont
   ;;
   non_established_cont)
       non_established_cont
   ;;
   tcp_total_cont)
       tcp_total_cont
   ;;
  *)
       echo 'Please check $1 in established_cont,non_established_cont or tcp_total_cont'
   ;;
esac
