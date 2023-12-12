import json
from flask import Flask, request, jsonify
import sqlite3
import os

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to mi API conected to my books database"

# 0.Ruta para obtener todos los libros
@app.route('/v1/all_books', methods=['GET'])
def all_books():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    select_books = "SELECT * FROM books"
    result = cursor.execute(select_books).fetchall()
    connection.close()
    return jsonify(result)


# 1.Ruta para obtener el conteo de libros por autor ordenados de forma descendente
@app.route('/v1/books_author', methods=['GET'])
def books_author():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()

    query = '''
    SELECT author, COUNT(*) 
    FROM books 
    GROUP BY 1 
    ORDER BY 2 DESC'''

    result = cursor.execute(query).fetchall()
    connection.close()
    return jsonify(result)

# 2.Ruta para obtener los libros de un autor como argumento en la llamada
@app.route('/v1/author', methods=['GET'])
def author():
    author = request.args['author']
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    query = '''
    SELECT * 
    FROM books 
    WHERE author LIKE ?'''
    result = cursor.execute(query, (author,)).fetchall() # Tengo que revisar esto
    connection.close()
    return jsonify(result)



# 3.Ruta para obtener los libros filtrados por título, publicación y autor
@app.route('/v1/books_filtered', methods=['GET'])
def books_filtered():    
    query = "SELECT * FROM books WHERE"
    filters = []
    if 'title' in request.args:
        title = request.args['title']
        query += " title LIKE ? AND"
        filters.append(title)
    if 'published' in request.args:
        published = request.args['published']
        query += " published = ? AND"
        filters.append(published)
    if 'author' in request.args:
        author = request.args['author']
        query += " author LIKE ? AND"
        filters.append(author)
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    result = cursor.execute(query[:-4], filters).fetchall()
    return jsonify(result)

app.run()