#!/bin/bash
sudo apt update
sudo apt install nginx
sudo nginx -s stop
sudo cp -a nginx.conf /etc/nginx/nginx.conf
sudo nginx
sudo nginx -s reload
sudo apt install python-pip
pip install pandas