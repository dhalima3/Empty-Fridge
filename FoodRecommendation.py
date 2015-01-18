import urllib2, ast
from flask import Flask
app = Flask(__name__)

API_KEY = "8ded784ee30fccebd50438b3e1db5866"
BASE_SEARCH = "http://food2fork.com/api/search?key="
BASE_GET = "http://food2fork.com/api/get?key="

BASE_RESULT = {"Name" : "",
               "URL" : "",
               "Ingredients" : "",
               "Image_Url" : ""}

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
@app.route("/user/<string:ingredients>/")
def getRecipe(ingredients):
    if (ingredients == ""):
        return str(BASE_RESULT)
    searchRequest = BASE_SEARCH + API_KEY
    params = ""
    ingredients = "&q=" + ingredients
    searchRequest = searchRequest + ingredients
    try:
        content = urllib2.urlopen(searchRequest).read()
        contentDict = ast.literal_eval(content)
        count = contentDict["count"]

        while ((count == 0) and (numIngredients(ingredients) > 1)):
            ingredients = removeIngredient(ingredients)
            content = urllib2.urlopen(BASE_SEARCH + API_KEY + "&q=" + ingredients).read()
            contentDict = ast.literal_eval(content)
            count = contentDict["count"]

        if (count == 0):
            return str(BASE_RESULT)
        else:
            finalDict = contentDict["recipes"][0]
            searchGet = BASE_GET + API_KEY + "&rId=" + finalDict["recipe_id"]
            finalContentDictStr = urllib2.urlopen(searchGet).read()
            finalContentDict = ast.literal_eval(finalContentDictStr)
            completeDict = {"Name" : "",
                            "URL" : "",
                            "Ingredients" : "",
                            "Image_Url" : ""}
            completeDict["Name"] = finalContentDict["recipe"]["title"]
            completeDict["URL"] = finalContentDict["recipe"]["source_url"]
            completeDict["Ingredients"] = str(finalContentDict["recipe"]["ingredients"])
            completeDict["Image_Url"] = finalContentDict["recipe"]["image_url"]
            return str(completeDict)
    except:
        return str(BASE_RESULT)

if __name__ == "__main__":
    app.run()
