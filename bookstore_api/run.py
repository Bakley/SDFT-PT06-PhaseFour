from flask import Flask, jsonify, request
from book_model import Book


app = Flask(__name__)

# In-memory storage
books = []

# Global id for init
next_id = 1

@app.route("/books", methods=['GET'])
def get_books():
    return jsonify([book.to_dict() for book in books]), 200

@app.route("/books/<int:book_id>", methods=['GET'])
def get_single_book(book_id):
    book = next((book for book in books if book.id == book_id), None)
    if book is None:
        return jsonify({
            "error": 'Book not found'
        }), 404
    return jsonify(book.to_dict()), 200

@app.route('/books', methods=["POST"])
def add_book():
    global next_id
    data = request.get_json()
    book = Book(
        id=next_id,
        title=data["title"],
        author=data["author"],
        year=data["year"]
    )
    books.append(book)
    next_id += 1
    return jsonify(book.to_dict()), 201

if __name__ == "__main__":
    app.run()
