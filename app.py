from flask import Flask, render_template, redirect

app = (__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/recipes')
def recipes():
    return()

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
