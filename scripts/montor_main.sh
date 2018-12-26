#!/usr/bin/bash
#获取目录下所有脚本信息，并进行排序输出

resettem=$(tput sgr0)
declare -A ssharray
i=0
numbers=""
for scripts_file in $(ls -I "montor_main.sh" ./)
do
	echo -e "\e[1;35m" "The Scripts:" ${i} '==>' ${resettem} ${scripts_file}
	#grep -E "^\#Program function" ${scripts_file}
	ssharray[$i]=${scripts_file}
	numbers="$numbers | ${i}"
	i=$((i+1))
done
while true
do
	read -p "Please input a number [ ${numbers} ]:" execshell
	if [[ ! ${execshell} =~  ^[0-9]+ ]];then
		exit 
	fi
	/usr/bin/bash ./${ssharray[$execshell]}
done
