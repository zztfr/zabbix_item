#!/usr/bin/bash
#获取web访问日志脚本

resettem=$(tput sgr0)
#需要分析的日志路径
Logfile=/soft/scripts/log/log.bjstack.log
Nginx_Status_code=( $(cat $Logfile |egrep -io "HTTP/1\.[0|1]\"[[:blank:]][0-9]{3}"|awk -F "[ ]+" '{
	if($2>=100 && $2<200) 
		{i++} 
	else if($2>=200 && $2<300) 
		{j++} 
	else if($2>=300 && $2<400) 
		{k++} 
	else if($2>=400 && $2<500) 
		{n++} 
	else if($2<500) 
		{p++}
	}END{ print i?i:0,j?j:0,k?k:0,n?n:0,p?p:0,i+j+k+n+p}'
		))

echo -e "\e[1;35m" "Http Status[100+]: ""${resettem} ${Nginx_Status_code[0]}"
echo -e "\e[1;35m" "Http Status[200+]: ""${resettem} ${Nginx_Status_code[1]}"
echo -e "\e[1;35m" "Http Status[300+]: ""${resettem} ${Nginx_Status_code[2]}"
echo -e "\e[1;35m" "Http Status[400+]:""${resettem} ${Nginx_Status_code[3]}"
echo -e "\e[1;35m" "Http Status[500+]:""${resettem} ${Nginx_Status_code[4]}"
echo -e "\e[1;35m" "Http Status[Total]:""${resettem} ${Nginx_Status_code[5]}"


