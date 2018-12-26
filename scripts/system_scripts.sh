#!/usr/bin/bash
#系统初始化脚本
#检测是否为root用户
if [ `whoami` != "root" ];then
echo " only root can run it"
exit 1
fi
#1.配置yum源,安装基础软件

Rep(){
rm -rf /etc/yum.repos.d/*.repo
wget -O /etc/yum.repos.d/Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
yum clean all && yum makecache
yum install vim nc iotop iftop glances dstat telnet wget curl curl-devel bash-completion lsof iotop iostat unzip bzip2 bzip2-devel  -y
yum install -y gcc gcc-c++ make cmake autoconf openssl-devel openssl-perl net-tools
#yum update && rm -rf /etc/yum.repos.d/CentOS*
}
#2.调整文件描述符
limit(){
cat > /etc/security/limits.d/20-nproc.conf<<-EOF
	* soft nproc 65535
	* hard nproc 65535
	* soft nofile 65535
	* hard nofile 65535
	EOF
}
#3.调整基本配置
Mod(){
	#调整时区
	test -f /etc/localtime && rm -f /etc/localtime
	ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
	#调整语言
	sed -i 's#LANG=.*#LANG="en_US.UTF-8"#g' /etc/locale.conf
	#关闭ipv6
	cd /etc/modprobe.d/ && touch ipv6.conf
	cat >/etc/modprobe.d/ipv6.conf <<-EOF
		alias net-pf-10 off
		alias ipv6 off
	EOF
	#调整历史命令
	sed -i '/HISTSIZE=/cHISTSIZE=100000' /etc/profile
	grep -q 'HISTTIMEFORMAT' /etc/profile
	if [ $? -eq 0 ];then
    	     sed -i 's/^HISTTIMEFORMAT=.*$/HISTTIMEFORMAT="%F %T"/' /etc/profile
	else
		echo 'HISTTIMEFORMAT="%F %T "' >> /etc/profile
	fi
}
#4.调整防火墙与Selinux
Firewalld(){
	#Selinux
	sed -i '/SELINUX=/cSELINUX=disabled' /etc/selinux/config
	#Firewalld
	systemctl disable firewalld
	systemctl stop firewalld
}
#5.调整内核参数
Kernel(){
cat >/etc/sysctl.conf <<-EOF
net.ipv4.tcp_tw_reuse=1
net.ipv4.tcp_tw_recycle=0

#开启ICMP错误消息保护
net.ipv4.icmp_echo_ignore_broadcasts=1
net.ipv4.icmp_ignore_bogus_error_responses=1

#处理无缘路由包
net.ipv4.conf.all.accept_source_route=0
net.ipv4.conf.default.accept_source_route=0

#防止简单的DOS攻击
net.ipv4.tcp_max_orphans = 3276800

net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1

vm.swappiness = 0
net.ipv4.neigh.default.gc_stale_time=120


# see details in https://help.aliyun.com/knowledge_detail/39428.html
net.ipv4.conf.all.rp_filter=0
net.ipv4.conf.default.rp_filter=0
net.ipv4.conf.default.arp_announce = 2
net.ipv4.conf.lo.arp_announce=2
net.ipv4.conf.all.arp_announce=2


# see details in https://help.aliyun.com/knowledge_detail/41334.html
net.ipv4.tcp_max_tw_buckets = 5000
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 1024
net.ipv4.tcp_synack_retries = 2
kernel.sysrq = 1

net.ipv4.ip_forward=1

EOF
}

#6.调整ssh参数
#注意:慎用
#Ssh(){
#/usr/bin/cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
#sed -i 's/\#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
#sed -i 's/\#PermitEmptyPasswords no/PermitEmptyPasswords no/' /etc/ssh/sshd_config
#sed -i 's/\#UseDNS yes/UseDNS no/' /etc/ssh/sshd_config
#}

main(){
Rep;
limit;
Mod;
Firewalld;
Kernel;
#Ssh;
/sbin/sysctl -p
}
main
