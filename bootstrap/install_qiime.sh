#!/bin/sh

# Install qiime (and dependencies) directly into path (and galaxy virtualenv)

sudo apt-get install -y pkg-config
sudo apt-get install -y libfreetype6-dev
sudo apt-get install -y libpng12-dev
sudo apt-get install -y libblas-dev
sudo apt-get install -y liblapack-dev

. galaxy/.venv/bin/activate
pip install numpy
pip install qiime

# "Install" qiime-galaxy scripts and libraries
git clone https://github.com/qiime/qiime-galaxy.git
ln -s ${HOME}/qiime-galaxy/scripts/* galaxy/.venv/local/bin/
ln -s ${HOME}/qiime-galaxy/lib/* galaxy/.venv/local/lib/python2.7/
