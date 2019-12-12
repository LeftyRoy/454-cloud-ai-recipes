#!/bin/bash

apt-get install python3-pip
pip install pymysql
snap install google-cloud-sdk --classic
gcloud config set account mutexstudios@gmail.com
gcloud config set project project-food-257404
