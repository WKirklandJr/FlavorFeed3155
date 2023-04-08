from flask import Flask, redirect, render_template, request, abort

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/recipes')
def recipes():
    return render_template('recipes.html')

@app.get('/recipes/<id>')
def get_recipe():
    return()

@app.get('/recipes/new')
def new_recipe():
    return()

@app.post('/recipes')
def create_recipe():
    return()

@app.get('/recipes/<id>/edit')
def edit_recipe():
    return()

@app.post('/recipes/<id>')
def update_recipe():
    return()

@app.post('/recipes/<id>/delete')
def delete_recipe():
    return()
