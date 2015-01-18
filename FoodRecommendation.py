import urllib2, ast
from flask import Flask
app = Flask(__name__)

API_KEY = "8ded784ee30fccebd50438b3e1db5866"

def numIngredients(ingredients):
    if (ingredients == ""):
        return 0
    ingredients_list = ingredients.split(",")
    return len(ingredients_list)

def removeIngredient(ingredients):
    ingredients_list = ingredients.split(",")
    if (ingredients_list[0] == ''): # No ingredients
        return ingredients
    else:
        ingredients_list.pop(0)
        return ','.join(ingredients_list)

@app.route("/user/<string:ingredients>")
def getRecipe(ingredients):
    if (ingredients == ""):
        return "NO INGREDIENTS SPECIFIED"
    searchRequest = "http://food2fork.com/api/search?key=" + API_KEY
    params = ""
    if (ingredients != ""):
        ingredients = "&q=" + ingredients
    searchRequest = searchRequest + ingredients
    try:
        content = urllib2.urlopen(searchRequest).read()
        contentDict = ast.literal_eval(content)
        #recipes = contentDict["recipes"]
        count = contentDict["count"]

        while ((count == 0) and (numIngredients(ingredients) > 1)):
            print("Retrying")
            ingredients = removeIngredient(ingredients)
            print(ingredients)
            content = urllib2.urlopen("http://food2fork.com/api/search?key=" + API_KEY + "&q=" + ingredients).read()
            contentDict = ast.literal_eval(content)
            #recipes = contentDict["recipes"]
            count = contentDict["count"]

        if (count == 0):
            return "NO RECIPES FOUND"
        else:
            #return (str(recipes[0]))
            return str(contentDict["recipes"][0])
    except:
        print "Error"

if __name__ == "__main__":
    app.run()
