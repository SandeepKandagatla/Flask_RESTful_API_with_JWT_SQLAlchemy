from flask import Flask,jsonify,request,Response
import json
from settings import *
from BookModel import *


@app.route('/books')
def get_books():
    return jsonify({'books':Book.get_all_books()})

def validBookObject(bookObject):
    if ('name' in bookObject and 'price' in bookObject and 'isbn' in bookObject):
        return True
    else:
        return False

@app.route('/books',methods=['POST'])
def add_book():
    request_data=request.get_json()
    if(validBookObject(request_data)):
        Book.add_book(request_data['name'],request_data['price'],request_data['isbn'])
        response=Response("",201,mimetype='application/json')
        response.headers['Location']="/books/"+str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg={
            "error":"Invalid Book Object Passed in the Request",
            "helpString":"Data Passed in similar to this {'name':'bookname,'price':7.99,'isbn':9587648576}"
        }
        response=Response(json.dumps(invalidBookObjectErrorMsg),status=400,mimetype='application/json')
        return response


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value={}
    for book in books:
        if book["isbn"]==isbn:
            return_value={
                'name':book["name"],
                'price':book["price"]
            }
    return jsonify(return_value)

# PUT  /books/912345678123
# {
#     'name':'A',
#     'price':7.99,
# }
def valid_put_request_data(request_data):
    if ('name' in request_data and 'price' in request_data):
        return True
    else:
        return False

@app.route('/books/<int:isbn>',methods=['PUT'])
def replace_book(isbn):
    request_data=request.get_json()
    if(not valid_put_request_data(request_data)):
        invalidBookObjectErrorMsg={
            "error":"Invalid Book Object Passed in the Request",
            "helpString":"Data Passed in similar to this {'name':'bookname,'price':7.99,'isbn':9587648576}"
        }
        response=Response(json.dumps(invalidBookObjectErrorMsg),status=400,mimetype='application/json')
        return response

    Book.replace_book(isbn,request_data['name'],request_data['price'])
    response=Response("",status=204)
    return response


def valid_patch_request_data(request_data):
    if ('name' in request_data or 'price' in request_data):
        return True
    else:
        return False
# PATCH  /books/912345678123
# {
#     'name':'A',
# }
@app.route('/books/<int:isbn>',methods=['PATCH'])
def update_book(isbn):
    request_data=request.get_json()
    if(not valid_patch_request_data(request_data)):
        invalidBookObjectErrorMsg={
            "error":"Invalid Book Object Passed in the Request",
            "helpString":"Data Passed in similar to this {'name':'bookname,'price':7.99,'isbn':9587648576}"
        }
        response=Response(json.dumps(invalidBookObjectErrorMsg),status=400,mimetype='application/json')
        return response

    if("name" in request_data):
        Book.update_book_name(isbn,request_data['name'])
    if("price" in request_data):
        Book.update_book_price(isbn,request_data['price'])
    response=Response("",status=204)
    response.headers['Location']="/books"+str(isbn)
    return response

# DELETE  /books/912345678123
@app.route('/books/<int:isbn>',methods=['DELETE'])
def delete_book(isbn):
    if(Book.delete_book(isbn)):
        response=Response("",status=204)
        return response

    invalidBookObjectErrorMsg={
        "error":"Book with the ISBN that was provided was not found,so unable to delete",
    }
    response=Response(json.dumps(invalidBookObjectErrorMsg),status=404,mimetype='application/json')
    return response




app.run(port=5000)