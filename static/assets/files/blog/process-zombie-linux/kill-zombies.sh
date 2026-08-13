#! /bin/bash
#
# Zombie processes killing script. Must be run under root.

case "$1" in
--admin)
stat=`ps ax | awk '{print $1}' | grep -v "PID" | xargs -n 1 ps lOp | grep -v "UID" | awk '{print"pid: "$3" *** parent_pid: "$4" *** status: "$10" *** process: "$13}' | grep ": Z"`

if ((${#stat} > 0));then
echo zombie processes found:
echo .
ps ax | awk '{print $1}' | grep -v "PID" | xargs -n 1 ps lOp | grep -v "UID" | awk '{print"pid: "$3" *** parent_pid: "$4" *** status: "$10" *** process: "$13}' | grep ": Z"
echo -n "Kill zombies? [y/n]: "
read keyb
if [ $keyb == 'y' ];then
echo killing zombies..
ps ax | awk '{print $1}' | grep -v "PID" | xargs -n 1 ps lOp | grep -v "UID" | awk '{print$4" status:"$10}' | grep "status:Z" | awk '{print $1}' | xargs -n 1 kill -9
fi
else
echo no zombies found!
fi
;;
--cron)
stat=`ps ax | awk '{print $1}' | grep -v "PID" | xargs -n 1 ps lOp | grep -v "UID" | awk '{print"pid: "$3" *** parent_pid: "$4" *** status: "$10" *** process: "$13}' | grep ": Z"`
if ((${#stat} > 0));then
ps ax | awk '{print $1}' | grep -v "PID" | xargs -n 1 ps lOp | grep -v "UID" | awk '{print$4" status:"$10}' | grep "status:Z" | awk '{print $1}' | xargs -n 1 kill -9
echo `date`": killed some zombie processes!" >> /var/log/zombies.log
fi
;;
*) echo 'usage: kill-zombies {--cron|--admin}'
;;
esac
exit 0
