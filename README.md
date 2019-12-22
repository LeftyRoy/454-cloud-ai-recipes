# 454-cloud-ai-recipes

Mitchell Norseth: mitchell2124@csu.fullerton.edu
Vijay Duggirala: vduggirala@csu.fullerton.edu

GCloudSQL.py - Contains all of our SQL query functions and connects to the database the Google Cloud SQL Proxy is running.

Reciple.py - Contains our class for a Recipe object

Application.py - Contains the UI made with the tkinter python library as well as the classes and functions that make it work.

cloud_sql_proxy.exe - Executable used when starting the proxy.

fridge.txt - example list of ingredients within a 'fridge' used to showcase our program.

db-recipes.json - The raw recipe list before converted to sql with the script we've made.

main.py - This is the script you want to run once the CLoud SQL Proxy is up and running.

mySQL.sql - result of our script converting the db-recipes.json format to sql.

jsontosql.py - the script to convert json files to sql files.

setup.py - installs python3, gcloud, and the google cloud sdk to the user's device.

start.sh - Starts up the Google Cloud SQL Proxy.

------------------------------------------------------------------------------------------------------------------------------------------

Steps: 
1. run setup.py to install the necessary tools
2. run start.sh to initialize the proxy
3. run main.py
