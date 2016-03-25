#!/bin/bash

sudo easy_install pip
sudo pip install yelp
sudo pip install requests
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install libxml2
brew install libxslt
brew link libxml2 --force
brew link libxslt --force
sudo pip install lxml
