import urllib2, ast
from flask import Flask
app = Flask(__name__)

def numIngredients(ingredients):
    ingredients_list = ingredients.split(",")
    if (ingredients_list[0] == ''):
        return 0
    else:
        return len(ingredients_list)

def removeIngredient(ingredients):
    ingredients_list = ingredients.split(",")
    if (ingredients_list[0] == ''): # No ingredients
        return ingredients
    else:
        ingredients_list.pop(0)
        return ','.join(ingredients_list)

@app.route("/user/<string:ingredients>")
#@app.route("/user/")
def getRecipe(ingredients):
    content = urllib2.urlopen("http://food2fork.com/api/search?key=8ded784ee30fccebd50438b3e1db5866&q=" + ingredients).read()
    contentDict = ast.literal_eval(content)
    recipes = contentDict["recipes"]

    while ((len(recipes) == 0) and (numIngredients(ingredients) > 1)):
        print("Retrying")
        ingredients = removeIngredient(ingredients)
        print(ingredients)
        content = urllib2.urlopen("http://food2fork.com/api/search?key=8ded784ee30fccebd50438b3e1db5866&q=" + ingredients).read()
        contentDict = ast.literal_eval(content)
        recipes = contentDict["recipes"]

    if (len(recipes) == 0):
        return "NO RECIPES FOUND"
    else:
        return (str(recipes[0]))

if __name__ == "__main__":
    app.run()
