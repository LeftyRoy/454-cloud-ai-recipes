import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', password='food', db='Recipes')
cur = conn.cursor()
name = ""

def login(user):
    cur.execute("SELECT * FROM Users WHERE Name=%s", user)
    userData=cur.fetchone()
    return userData

def getAllUsers():
    cur.execute("SELECT Name FROM Users")
    userList = cur.fetchall()
    return userList

def insert_name(nm):
    name = str(nm)
    cur.execute("SELECT * FROM Users WHERE Name=%s", name)
    if(cur.fetchone()!=None):
        return False
    users_insert_query = "INSERT INTO Users (Name) VALUES (%s);"
    cur.execute(users_insert_query, name)
    conn.commit()
    return True

def remove_name(nm):
    users_delete_query = "DELETE FROM Users WHERE Name=%s"
    cur.execute(users_delete_query, str(nm))
    conn.commit()
    return True
	
	
def get_recipes():
    ingredients = []

    n = int(input("Enter number of ingredients: "))
    print("Enter those ingredients: \n")
	
    for i in range (0, n):
        ingredient = str(input())
        ingredients.append(ingredient)
	
    get_recipes_query = "SELECT Title FROM recipes WHERE"
	
    counter = 0
    for i in ingredients:
        if counter is len(ingredients) - 1:
            get_recipes_query += " Ingredients LIKE '%" + str(i) + "%'"
            print(get_recipes_query)
            break
        get_recipes_query += " Ingredients LIKE '%" + str(i) + "%' OR"
        counter += 1

    cur.execute(get_recipes_query)
	
    result = cur.fetchall()
	
    return result