# What has/needs to be installed for a new headless pi
sudo apt-get update
alias ins='sudo apt install' # ease
ins tmux # Terminal multiplexing!
ins python3-pip --fix-missing # pip!
ins git # git!
ins sense-hat
ins rpi.gpio


pip3 install digi-xbee
pip3 install psutil


python3 welcome.py

