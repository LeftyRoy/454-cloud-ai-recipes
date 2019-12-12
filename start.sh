#!/bin/bash
echo "Initializing Google Cloud Proxy..."
gcloud services enable sqladmin
./cloud_sql_proxy -instances="project-food-257404:us-west2:fword"=tcp:3306 &
sleep 5
python3 main.py
