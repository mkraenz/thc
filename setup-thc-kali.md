# Setup for THC Kali

## aliases and default setups

```bash
alias ..='cd ..'
alias ~='cd ~'
alias r='cd /'
alias johnrock='sudo john --wordlist=/usr/share/wordlists/rockyou.txt'
alias www='python3 -m http.server'
alias o='xdg-open .'
# gunzip /usr/share/wordlists/rockyou.txt.gz
```

## one-time

Note: assumes you're running root. If not, add some sudo's as needed.

### VSCode

```bash
apt update
apt install snapd -y
systemctl enable --now snapd apparmor
systemctl start snapd
snap install --classic code

mkdir ~/vs-code-user-data
alias code="/snap/bin/code --user-data-dir ~/vs-code-user-data"
code
```

### XClip

```bash
sudo apt install xclip
source /usr/bin/xclip
alias xclip='xclip -selection clipboard'
```

### Seclists

`sudo apt update && sudo apt install seclists`

### Feroxbuster

[on github](https://github.com/epi052/feroxbuster#default-values)

```shell
sudo apt update && sudo apt install seclists
sudo apt install -y feroxbuster
```

usage:
`feroxbuster -u http://10.10.80.188 --no-recursion -vv`
