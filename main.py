import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='food', db='Recipes')

cur = conn.cursor()

name = ""

def insert_name():

	name = input("Enter your name: ")
	print("Wecome " + name + "!")

	users_insert_query = "INSERT INTO Users (Name) VALUES (%s); "
					  
	cur.execute(users_insert_query, name)
	
	conn.commit()
	
	print("Name inserted successfully into Users table")

def remove_name():

	name = input("Select the name you wish to delete: ")

	users_delete_query = "DELETE FROM Users WHERE Name=%s"
	
	cur.execute(users_delete_query, name)
	
	conn.commit()

	print("Name deleted successfully from Users table")

# insert_name()
# remove_name()