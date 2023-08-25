
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
