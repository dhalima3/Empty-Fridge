import urllib2, ast
from flask import Flask
app = Flask(__name__)

@app.route("/user/<string:ingredient>/")
#@app.route("/user/")
def hello(ingredient):
    url = "http://food2fork.com/api/search?key=8ded784ee30fccebd50438b3e1db5866&q=paneer"
    content = urllib2.urlopen("http://food2fork.com/api/search?key=8ded784ee30fccebd50438b3e1db5866&q=" + ingredient).read()
    contentDict = ast.literal_eval(content)
    recipes = contentDict["recipes"]
    return str(recipes[0])

if __name__ == "__main__":
    app.run()


