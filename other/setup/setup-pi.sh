# What has/needs to be installed for a new headless pi

wd=$(pwd)
alias ins='sudo apt install' # ease

sudo apt-get update
ins tmux # Terminal multiplexing!
ins python3-pip --fix-missing # pip!
ins git # git!
ins sense-hat
ins rpi.gpio

# USB Relay
ins usbrelay
ins libhidapi-dev
ins libhidapi-hidraw0
ins python3-dev
ins python3.5-dev
mkdir ~/Documents/programs
git clone https://github.com/darrylb123/usbrelay ~/Documents/programs/usbrelay_git
cd ~/Documents/programs/usbrelay_git
make python
sudo make install_py


# XBee
pip3 install digi-xbee
pip3 install psutil


cd $wd
python3 welcome.py

