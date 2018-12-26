#!/bin/bash
#阿里云检测DHCP地址池租期脚本

datetime=$(date +%Y%m%d-%H:%M:%S)
log_file=/tmp/dhcp_fix_${datetime}.log
do_fix=false
lft_threshold=252288000 # 8 years secs

function log_info() {
    local msg=$1
	echo -e "\033[1;32;40m[INFO]\033[0m [`date +'%Y-%m-%d %H:%M:%S'`] $msg" | tee -a $log_file
    return 0
}

function log_warn() {
    local msg=$1
	echo -e "\033[1;31;40m[WARN]\033[0m [`date +'%Y-%m-%d %H:%M:%S'`] $msg" | tee -a $log_file
    return 1
}

function check_dhclient() {
    # dhclient is running -> 0
    # otherwise -> 1
    local interface=$1
    if   ps aux | grep -v grep | grep -q "dhclient -v" ; then # by dhclient -v
        return 0
    elif ps aux | grep -v grep | grep -q "dhclient $interface\$" ; then # by dhclient ethX
        return 0
    elif ps aux | grep -v grep | grep '/sbin/dhclient' | grep -q "$interface\$" ; then # by ifup ethX
        return 0
    fi
    return 1
}

function check_interface() {
    # don't need fix -> 0
    # need fix -> 1
    local interface=$1
    local ifcfg=/etc/sysconfig/network-scripts/ifcfg-$interface
    log_info "start checking $interface"

    if ! grep -q "up" /sys/class/net/$interface/operstate ; then
        log_info "no need fix, $interface link stat is not set up"
        return 0
    elif [[ ! -f $ifcfg ]]; then
        log_info "no need fix, $interface is not configured"
        return 0
    elif grep -q "BOOTPROTO=static" $ifcfg ; then
        log_info "no need fix, $interface is configured statically"
        return 0
    elif check_dhclient $interface ; then
        log_info "no need fix, dhclient $interface is running"
        return 0
    fi

    valid_lft=$(ip a show dev $interface | awk '/valid_lft/ {print $2}')
    valid_lft=${valid_lft%sec}
    if [[ $valid_lft -gt $lft_threshold || $valid_lft == forever ]]; then
        log_info "no need fix, $interface valid_lft $valid_lft"
        return 0
    fi

    log_warn "need fixing $interface"
    return 1
}

function fix_interface() {
    # fixed ok -> 0
    # fixed error -> 1
    local interface=$1
    log_info "start fixing $interface"
    ip a show dev $interface >> $log_file

    local ifcfg=/etc/sysconfig/network-scripts/ifcfg-$interface
    if [[ $interface != eth0 ]] && ! grep -q 'DEFROUTE=no' $ifcfg ; then
        log_warn "$interface is set as linked to default route, skip it"
        return 0
    fi

    /usr/sbin/ifup $interface
    ip a show dev $interface >> $log_file

    if check_dhclient $interface ; then
        log_info "ok, dhclient $interface is running now"
        return 0
    else
        log_warn "dhclient $interface still not running !"
        return 1
    fi
}

function work() {
    local interface=
    local ret=0
    for i in /sys/class/net/eth* ; do
        interface=${i#/sys/class/net/}
        if ! check_interface $interface ; then
            if $do_fix ; then
                if ! fix_interface $interface ; then
                    ret=1
                fi
            else
                ret=1
            fi
        fi
    done
    return $ret
}

function check_eni_utils() {
    # centos7 with eni_utils
    if [[ -f /etc/eni_utils/net.hotplug ]] && \
       [[ -d /var/run/systemd/ ]]; then
        return 0
    fi
    return 1
}

function main() {
    if ! check_eni_utils ; then
        log_info "no need fix"
        return 0
    fi

    if [[ $1 == fix ]] ; then
        do_fix=true
        action="check and fix"
    else
        do_fix=false
        action="check"
    fi

    log_info "start $action"
    if work ; then
        log_info "$action success"
        return 0
    else
        log_warn "$action failed"
        return 1
    fi
}

main $@
