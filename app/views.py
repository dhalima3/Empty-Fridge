from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    recipes = [  # fake array of recipes
        { 
            'name': 'BBQ Chicken', 
            'ingredients': ['salt',' pepper',' chicken'] 
        },
        { 
            'name': 'Goldfish', 
            'ingredients': ['salt','pepper'] 
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           recipes=recipes)
