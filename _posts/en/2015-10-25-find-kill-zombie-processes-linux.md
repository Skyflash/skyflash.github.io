---
title: Find and kill zombie processes on Linux with a bash script
layout: post
date: '2015-10-25'
description: A simple bash script to find zombie processes on a Linux server and clean them up, by hand or from cron, with a log of what was killed
intro: "On Unix and Unix-like operating systems, a zombie or defunct process is a process that has finished running but still has an entry in the process table, so that its parent can read its exit status"
lang: en_US
image: "/static/assets/img/blog/zombiesign.jpg"
keywords: linux,script,bash,process,kill,zombie,defunct,server,cron
categories:
- Infrastructure & Systems
permalink: "/en/blog/infrastructure/:title/"
translation_key: linux-zombie-processes
tags:
- linux
- scripting
- process
- security
- script
icon: fa-linux
---

Recently I had to do some tuning on a Linux server that was often overrun by zombie processes, pushing its load very high. From Wikipedia:

>On Unix and Unix-like computer operating systems, a zombie process or defunct process is a process that has completed execution but still has an entry in the process table: this entry is still needed to allow the parent process to read its child's exit status.

While looking around for something useful, I came across a good script to copy onto your servers: it finds zombies, cleans them up and keeps a record in a dedicated log file.

* TOC 
{:toc}

## The kill-zombies script

First, as root, create a new file called kill-zombies

```bash
cd /root
vi kill-zombies
```

Then copy the following code and paste it into the file you just created

```bash
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
```

Now make it executable and move it to /usr/bin

```bash
chmod +x kill-zombies
mv kill-zombies /usr/bin
```

### How it works

A zombie is already dead, so it can't be killed: the script sends `kill -9` to its parent process (the fourth column of `ps l`, the PPID), and once the parent is gone init adopts the zombies and reaps them. Use it knowing which service you're about to stop.

The script is called with a flag that changes its behaviour:

```bash
kill-zombies --admin
```

This one runs by hand. If zombie processes are found, you're shown the list and asked to confirm before anything is killed

```bash
kill-zombies --cron
```

This one is meant **to go in the crontab**, so the server runs it at regular intervals. Processes are killed automatically and each run is logged in /var/log/zombies.log

### Adding it to the crontab

Open the crontab editor with this command

```bash
crontab -e
```

And add this line:

```bash
*/10 * * * * /usr/bin/kill-zombies --cron
```

This way the script runs every 10 minutes. To change the interval, just replace */10 with, say, */5 (for 5 minutes)

[Download kill-zombies.sh](/static/assets/files/blog/process-zombie-linux/kill-zombies.sh)

References:

* [CronHowTo](https://help.ubuntu.com/community/CronHowto)
