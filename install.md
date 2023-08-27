
## Drivers
```bash
git clone https://github.com/seeed-studio-projects/seeed-voicecard.git
cd seeed-voicecard
./install.sh
```

# Git
```bash
git config --global user.name "NotCoffee418"
git config --global user.email "9306304+NotCoffee418@users.noreply.github.com"
ssh-keygen -t ed25519 -C "9306304+NotCoffee418@users.noreply.github.com" -f ~/.ssh/id_github_ed25519
cat ~/.ssh/id_github_ed25519 # add this key to github
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_github_ed25519
ssh -T git@github.com
```

```bash
cd Desktop
git clone https://github.com/NotCoffee418/leorio.git
```

# Rust
Needed for mycroft build
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

sudo reboot
```

# delet this:
<!-- # Mycroft core
This is slow. It will warn pip upgrade and appear to do nothing. It is doing something.
```bash
cd ~/
git clone https://github.com/MycroftAI/mycroft-core.git
cd mycroft-core
bash dev_setup.sh
# Y, Y, N, Y, Y, ENTER, ENTER,
``` -->

# Precise engine
```
cd ~/
wget https://github.com/MycroftAI/precise-data/raw/dist/armv7l/precise-engine.tar.gz
tar xvf precise-engine.tar.gz
```