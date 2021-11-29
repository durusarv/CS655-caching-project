#!/bin/bash

git clone https://git-wip-us.apache.org/repos/asf/trafficserver.git
cd trafficserver/
autoreconf -if

# Remove comment from the below 2 lines if install fails with configure error: cannot find pcre library
#sudo apt-get update
#sudo apt-get install libpcre3 libpcre3-dev

./configure --with-included-apr
make
sudo make install

