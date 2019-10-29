import json, codecs
from Recipe import Recipe

with open("db-recipes.json") as jfile:
	data = json.load(jfile)

RecipeList = list()

for key,value in data.items():
	RecipeList.append(Recipe(value))

f = codecs.open("mySQL.sql", mode="a", encoding="utf-8")

f.write("USE 6Vm97vzJ6U;\n\n")
f.write("CREATE TABLE recipes(\nID VARCHAR(50) NOT NULL PRIMARY KEY,\nTitle VARCHAR(50) NOT NULL,\nInstructions TEXT,\nIngredients TEXT,\nTags TEXT,\nCalories INT,\nServings TEXT );\n\n")
f.write("INSERT INTO recipes (ID, Title, Instructions, Ingredients, Tags, Calories, Servings)\nVALUES\n")

for r in RecipeList:
	tempr = r.getDict()
	tempr["instructions"] = tempr["instructions"].replace("[", "")
	tempr["instructions"] = tempr["instructions"].replace("]", "")
	tempr["instructions"] = tempr["instructions"].replace("'", "")
	tempr["instructions"] = tempr["instructions"].replace('"', "")
	tempr["tags"] = str(tempr["tags"]).replace("[", "")
	tempr["tags"] = str(tempr["tags"]).replace("]", "")
	tempr["tags"] = str(tempr["tags"]).replace("'", "")
	tempr["ingredients"] = str(tempr["ingredients"]).replace("[", "")
	tempr["ingredients"] = str(tempr["ingredients"]).replace("]", "")
	tempr["ingredients"] = str(tempr["ingredients"]).replace("'", "")
	tempr["ingredients"] = str(tempr["ingredients"]).replace('"', "")
	f.write('\t("%s", "%s", "%s", "%s", "%s", %d, %d),\n' % (tempr["id"], str(tempr["name"]), str(tempr["instructions"]), str(tempr["ingredients"]), str(tempr["tags"]), tempr["calories"], tempr["servings"]))

f.close()
