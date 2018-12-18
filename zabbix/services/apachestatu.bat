@echo off
for /f "delims=: tokens=2" %%i in ('C:\zabbix-agent\bin\win64\wget --quiet -O - http://127.0.0.1/server-status?auto | find /i "%1"') do (echo %%i)