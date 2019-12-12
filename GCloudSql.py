import pymysql
import json

conn = pymysql.connect(host='127.0.0.1', user='root', password='food', db='Recipes')
cur = conn.cursor()
name = ""

def login(user):
    cur.execute("SELECT * FROM Users WHERE Name=%s", user)
    userData=cur.fetchone()
    return userData

def addScore(user, tag, amount):
    cur.execute("SELECT Scores FROM Users WHERE Name=%s", user)
    scores = cur.fetchone()
    if(scores[0] == None):
        scores = {}
    else:
        scores = str(scores[0])
        scores = json.loads(scores)
    
    if tag in scores:
        scores[tag] += amount
    else:
        scores[tag] = amount
    scores = json.dumps(scores)
    query = str("UPDATE Users SET Scores = '"+scores+"' WHERE Name='" + user + "'")
    cur.execute(query)
    conn.commit()

def getScore(user, tag):
    cur.execute("SELECT Scores FROM Users WHERE Name=%s", user)
    scores = cur.fetchone()
    scores = str(scores[0])
    scores = json.loads(scores)
    if tag in scores:
        return scores[tag]
    return 0


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

def getRecipeByName(name):
    cur.execute("SELECT * FROM recipes WHERE Title="+name)
    recipe = cur.fetchone()
    return recipe
	
def get_recipes():
    ingredients = []
    with open('fridge.txt') as f:
        for ingredient in f:
            ingredients.append(ingredient)

    get_recipes_query = "SELECT * FROM recipes WHERE"
	
    counter = 0
    for i in ingredients:
        if counter is len(ingredients) - 1:
            get_recipes_query += " Ingredients LIKE '%" + str(i) + "%'"
            break
        get_recipes_query += " Ingredients LIKE '%" + str(i) + "%' OR"
        counter += 1

    cur.execute(get_recipes_query)
	
    result = cur.fetchall()

    print("found " + str(len(result)) + " recipes you can make with " + str(len(ingredients)) + " ingredients in the fridge")
	
    return result

def filterResults(user, recipes):
    recipeList = list()
    for r in recipes:
        r=list(r)
        rscore = 0
        tags = str(r[4])
        tags = tags.split(',')
        for tag in tags:
            rscore += getScore(user, tag)
        r[0] = rscore
        recipeList.append(r)
    recipeList.sort(reverse=True, key=lambda x: x[0])
    return recipeList