from flask import Flask, render_template, request, jsonify
import sqlite3
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/enternew')
def enternew():
    return render_template('food.html')

@app.route('/addfood', methods = ['POST'])
def addfood():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    try:
        name = request.form['name']
        calories = request.form['calories']
        cuisine = request.form['cuisine']
        is_vegetarian = request.form['is_vegetarian']
        is_gluten_free = request.form['is_gluten_free']
        cursor.execute('INSERT INTO foods (name,calories,cuisine,is_vegetarian,is_gluten_free) VALUES (?,?,?,?,?)', (name,calories,cuisine,is_vegetarian,is_gluten_free))
        connection.commit()
        message = 'Record succesfully added'
    except:
        connection.rollback()
        message = 'Error in insert operation'
    finally:
        return render_template('result.html', message = message)
        connection.close()

@app.route('/favorite')
def favorite():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT * FROM foods WHERE name = "lasagna"')
        favorite = jsonify(cursor.fetchone())
    except:
        connection.rollback()
        favorite = 'Sorry, nothing was found'
    finally:
        return favorite
        connection.close()


@app.route('/search', methods = ['GET'])
def search():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    try:
        name = request.args['name']
        cursor.execute('SELECT * FROM foods WHERE name IS ?', (name,))
        query = jsonify(cursor.fetchone())
    except:
        connection.rollback()
        query = 'Sorry, nothing was found'
    finally:
        return query
        connection.close()

@app.route('/drop')
def drop():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    try:
        cursor.execute('DROP TABLE foods')
        message = 'Table has been dropped'
    except:
        connection.rolback()
        message = 'Table could not be dropped'
    finally:
        return render_template('result.html', message=message)
