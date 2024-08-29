from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
import logging

app = Flask(__name__)
api = Api(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Book:
    _id_counter = 1

    def __init__(self, title, author):
        self.id = Book._id_counter
        self.title = title
        self.author = author
        self.deleted = False  # Soft delete flag
        Book._id_counter += 1

    def to_dict(self):
        """Convert book object to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "deleted": self.deleted
        }

class BookService:
    def __init__(self):
        self.books = []

    def get_all_books(self, include_deleted=False):
        """Retrieve all books, with an option to include deleted ones."""
        if include_deleted:
            return self.books
        return [book for book in self.books if not book.deleted]

    def get_book_by_id(self, book_id, include_deleted=False):
        """Retrieve a book by its ID, with an option to include deleted ones."""
        return next((book for book in self.books if book.id == book_id and (include_deleted or not book.deleted)), None)

    def add_book(self, title, author):
        """Add a new book."""
        new_book = Book(title, author)
        self.books.append(new_book)
        return new_book

    def update_book(self, book_id, title, author):
        """Update an existing book."""
        book = self.get_book_by_id(book_id)
        if book:
            book.title = title
            book.author = author
            return book
        return None

    def soft_delete_book(self, book_id):
        """Soft delete a book by setting its deleted flag to True."""
        book = self.get_book_by_id(book_id)
        if book:
            book.deleted = True
            return True
        return False

    def restore_book(self, book_id):
        """Restore a soft-deleted book by setting its deleted flag to False."""
        book = self.get_book_by_id(book_id, include_deleted=True)
        if book and book.deleted:
            book.deleted = False
            return book
        return None

book_service = BookService()

class BookResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='Title is required and must be a string.')
        self.reqparse.add_argument('author', type=str, required=True, help='Author is required and must be a string.')

    def get(self, book_id):
        """Retrieve a single book by ID."""
        book = book_service.get_book_by_id(book_id)
        if book:
            return book.to_dict(), 200
        return {"error": "Book not found"}, 404

    def put(self, book_id):
        """Update an existing book."""
        args = self.reqparse.parse_args()
        updated_book = book_service.update_book(book_id, args['title'], args['author'])
        if updated_book:
            return updated_book.to_dict(), 200
        return {"error": "Book not found"}, 404

    def delete(self, book_id):
        """Soft delete a book by ID."""
        if book_service.soft_delete_book(book_id):
            return {"message": "Book deleted successfully"}, 200
        return {"error": "Book not found"}, 404

class BookListResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='Title is required and must be a string.')
        self.reqparse.add_argument('author', type=str, required=True, help='Author is required and must be a string.')

    def get(self):
        """Retrieve all books, excluding deleted ones."""
        return [book.to_dict() for book in book_service.get_all_books()], 200

    def post(self):
        """Add a new book."""
        args = self.reqparse.parse_args()
        new_book = book_service.add_book(args['title'], args['author'])
        return new_book.to_dict(), 201

class RestoreBookResource(Resource):
    """Endpoint to restore a soft-deleted book."""

    def post(self, book_id):
        restored_book = book_service.restore_book(book_id)
        if restored_book:
            return restored_book.to_dict(), 200
        return {"error": "Book not found or not deleted"}, 404

api.add_resource(BookListResource, '/books')
api.add_resource(BookResource, '/books/<int:book_id>')
api.add_resource(RestoreBookResource, '/books/<int:book_id>/restore')

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors."""
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
