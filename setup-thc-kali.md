# Setup for THC Kali

## aliases

```bash
alias ..='cd ..'
alias ~='cd ~'
alias r='cd /'

```

## one-time

Note: assumes you're running root. If not, add some sudo's as needed.

### Install VSCode (as root)

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
