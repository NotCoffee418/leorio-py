
## Drivers
```bash
git clone https://github.com/seeed-studio-projects/seeed-voicecard.git
cd seeed-voicecard
./install.sh
```

## Volume
Recording volume should be set to max in UI if any after drivers installed.

```bash
alsamixer
```
Set capture device volume to max white (dont peak it in red)


## Device IP
Not required, but logging for reference. Adjust as needed or skip.
```bash
sudo nano /etc/network/interfaces
```
append:
```
auto wlan0
iface wlan0 inet static
address 192.168.0.101
netmask 255.255.255.0
gateway 192.168.0.1
dns-nameservers 192.168.0.100
```

# Swap file 
creates 2G swap file
```bash
sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
sudo sysctl vm.swappiness=10
sudo sysctl -p
free -h
```

# Git
```bash
git config --global user.name "NotCoffee418"
git config --global user.email "9306304+NotCoffee418@users.noreply.github.com"
ssh-keygen -t ed25519 -C "9306304+NotCoffee418@users.noreply.github.com" -f ~/.ssh/id_github_ed25519
cat ~/.ssh/id_github_ed25519.pub # add this key to github
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_github_ed25519
ssh -T git@github.com
```


# Essentials
Needed for mycroft
```bash
# for numpy
sudo apt-get install libatlas-base-dev libjack0 libportaudio2 libopenblas-dev libhdf5-dev portaudio19-dev
```

# Setup environment
No venv or conda because rasp.

```bash
git clone https://github.com/NotCoffee418/leorio.git
cd leorio
pip3 install -r requirements.txt
```

# Set up .env
Copy .env.example to .env and fill in the blanks