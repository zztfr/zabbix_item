#!/usr/bin/bash
#Install Nginx

#1.判断网络
ping -c1 www.baidu.com &>/dev/null
if [ $? -ne 0 ];then
        echo "请检查你的网络."
        exit 1
fi
yum install -y openssl-devel pcre-devel zlib-devel gcc gcc-c++ autoconf automake &>/dev/null

Path=/soft/src
Edition=nginx-1.14.2
Path1=/soft

mkdir $Path -p
wget -P $Path http://nginx.org/download/$Edition.tar.gz
sleep 5
tar xf $Path/$Edition.tar.gz
groupadd nginx
useradd -g nginx -s /sbin/nologin nginx
cd $Path/$Edition
./configure --prefix=/soft/$Edition --user=nginx --group=nginx --with-http_ssl_module --with-http_stub_status_module --with-pcre &>/dev/null
if [ $? -ne 0 ]; then
   echo "编译参数错误"
else
   make && make install
fi

ln -s $Path1/$Edition/sbin/nginx /usr/local/bin/nginx
ln -s $Path1/$Edition $Path1/nginx

