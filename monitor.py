#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#	Raspberry Pi monitorization functions
#
#	Mostly stolen from this page:
#
#		 https://alteageek.com/2016/09/17/raspberry-carga-del-procesador-temperatura-memoria-libre-direccion-ip-y-uptime/
#
#	and some other random searches
#

import datetime
import psutil
import subprocess
from datetime import timedelta

from gpiozero import CPUTemperature
cpu = CPUTemperature()

def get_gputemp_from_gpiozero():
    return cpu.temperature

def get_uptime_line():
    return subprocess.getoutput('uptime')


def get_cpuload():
    cpuload = psutil.cpu_percent(interval=1, percpu=False)
    return str(cpuload)

def get_ram():
    san = subprocess.check_output(['free','-m']).decode('utf-8')
    lines = san.split('\n')
    return ( int(lines[1].split()[1]), int(lines[2].split()[3]) )

def get_cpu_temp():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000

def get_gpu_temp():
    gpu_temp = subprocess.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace('temp=','').replace('\'C','')
    return float(gpu_temp)

def get_connections():
    san = subprocess.check_output(['netstat','-tun'])
    return len([x for x in san.split() if x == 'ESTABLISHED'])

def get_ipaddress():
    arg='ip route list'
    ip=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = ip.communicate()
    split_data = data[0].decode('utf-8').split()
    ipaddr = split_data[split_data.index('src')+1]
    return ipaddr

def get_uptime():
    with open('/proc/uptime', 'r') as f:
     uptime_seconds = float(f.readline().split()[0])
     uptime = (timedelta(seconds = uptime_seconds))
     return str(uptime)


if __name__ == "__main__":
  print("CPU load: ", get_cpuload())
  print("RAM: ", get_ram())
  print("CPU temp: ", get_cpu_temp())
  print("GPU temp: ", get_gpu_temp())
  print("Connections: ", get_connections())
  print("IP address: ", get_ipaddress())
  print("Uptime: ", get_uptime())

