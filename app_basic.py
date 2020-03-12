from flask import Flask,jsonify,request,Response
import json
from settings import *

#app=Flask(__name__)
#print(__name__)

books=[
    {
        'name':'A',
        'price':7.99,
        'isbn':912345678123
    },
    {
        'name':'B',
        'price':6.99,
        'isbn':923754238493
    }
]

@app.route('/books',)
def get_books():
    return jsonify({'books':books})

#POST /books
# {
#     'name':'bookname',
#     'price':5.99,
#     'isbn':697798900909
# }
def validBookObject(bookObject):
    if ('name' in bookObject and 'price' in bookObject and 'isbn' in bookObject):
        return True
    else:
        return False

@app.route('/books',methods=['POST'])
def add_book():
    request_data=request.get_json()
    if(validBookObject(request_data)):
        new_book={
            "name":request_data["name"],
            "price":request_data["price"],
            "isbn":request_data["isbn"]
        }
        books.insert(0,new_book)
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
@app.route('/books/<int:isbn>',methods=['PUT'])
def replace_book(isbn):
    request_data=request.get_json()
    new_book={
        "name":request_data["name"],
        "price":request_data["price"],
        "isbn":isbn
    }
    i=0
    for book in books:
        currentIsbn=book["isbn"]
        if currentIsbn==isbn:
            books[i]=new_book
        i+=1
    response=Response("",status=204)
    return response

# PATCH  /books/912345678123
# {
#     'name':'A',
# }
@app.route('/books/<int:isbn>',methods=['PATCH'])
def update_book(isbn):
    request_data=request.get_json()
    updated_book={}
    if("name" in request_data):
        updated_book["name"]=request_data["name"]
    if("price" in request_data):
        updated_book["price"]=request_data["price"]
    for book in books:
        if book['isbn']==isbn:
            book.update(updated_book)
    response=Response("",status=204)
    response.headers['Location']="/books"+str(isbn)
    return response

# DELETE  /books/912345678123
@app.route('/books/<int:isbn>',methods=['DELETE'])
def delete_book(isbn):
    i=0
    for book in books:
        if book['isbn']==isbn:
            books.pop(i)
            response=Response("",status=204)
            return response
        i+=1
    invalidBookObjectErrorMsg={
        "error":"Book with the ISBN that was provided was not found,so unable to delete",
    }
    response=Response(json.dumps(invalidBookObjectErrorMsg),status=404,mimetype='application/json')
    return response




app.run(port=5000)