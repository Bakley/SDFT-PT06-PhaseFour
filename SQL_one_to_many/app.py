# Basic Setup
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///books.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
api = Api(app)

# Define the model with an ORM
class Book(db.Model):
    __tablename__ = 'books'  #meta-data

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

    # foreign key
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))

    ## Relationship create a bidirectional relationship 
    author = db.relationship('Author', back_populates='books')


    def to_dict(self):
        """Convert model instnce to a json output"""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author_id,
            "deleted": self.deleted
        }
    

class Author(db.Model):
    __tablename__ = 'authors'  #meta-data

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) #Equi VARCAR(100)
    deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

    ## Relationship create a bidirectional relationship 
    books = db.relationship('Book', back_populates='author')

    def to_dict(self):
        """Convert model instnce to a json output"""
        return {
            "id": self.id,
            "name": self.name,
            "deleted": self.deleted
        }
# Initialize the database
with app.app_context():
    db.create_all()
    from faker import Faker

    # Initialize Faker
    fake = Faker()

    # Drop all tables and create them again
    db.drop_all()
    db.create_all()

    # Seed authors
    authors = []
    for _ in range(5):  # Create 5 random authors
        author = Author(name=fake.name())
        db.session.add(author)
        authors.append(author)

    db.session.commit()

    # Seed books
    for _ in range(10):  # Create 10 random books
        random_author = fake.random_element(authors)  # Select a random author from the list

        # import pdb; pdb.set_trace()
        book = Book(title=fake.sentence(nb_words=4), author=random_author)
        db.session.add(book)

    db.session.commit()

    print("Database seeded successfully with Faker!")


# Business Logic this is what controls the information input in the database and how to manipulate
class BookService:

    def retrive_all_books(self, include_deleted=False):
        """Retrieve all books, optionally including soft-deleted ones."""
        if include_deleted:
            return Book.query.all()
        return Book.query.filter_by(deleted=False).all()

    def retrive_book_by_id(self, book_id, include_deleted=False):
        """Retrieve a single book by ID, optionally including soft-deleted ones."""
        if include_deleted:
            return Book.query.get(book_id)
        return Book.query.filter_by(id=book_id, deleted=False).first()

    def add_book(self, title, author_id):
        author = Author.query.get(author_id)
        new_item = Book(title=title, author=author)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    def update_book(self, book_id, title=None, author=None):
        item = self.retrive_book_by_id(book_id)
        if item:
            if title:
                item.title = title
            if author:
                item.author = author
            db.session.commit()
            return item
        return None

    def soft_delete_book(self, book_id):
        item = self.retrive_book_by_id(book_id)
        if item:
            item.deleted = True
            db.session.commit()
            return item
        return False
    
    def restore_book(self, book_id):
        item = self.retrive_book_by_id(book_id, include_deleted=True)
        if item:
            item.deleted = False
            db.session.commit()
            return item
        return False

bookservice = BookService()

# Resources
class BookResource(Resource):
     
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, help="Title is required to be a string")
        self.reqparse.add_argument('author', type=str, help="Author is required to be a string")

    def get(self, book_id):
        item = bookservice.retrive_book_by_id(book_id)
        if item:
            return item.to_dict(), 200
        return {
            'error': "Book not found"
        }, 404
    
    def put(self, book_id):
        args = self.reqparse.parse_args()
        book = bookservice.update_book(book_id, title=args["title"], author=args["author"])

        if book:
            return book.to_dict(), 200
        return {
            'error': "Book not found"
        }, 404
    
    def delete(self, book_id):
        """Soft delete a book by ID."""
        if bookservice.soft_delete_book(book_id):
            return {"message": "Book deleted successfully"}, 204
        return {"error": "Book not found"}, 404

class BookListResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='Title is required and must be a string.')
        self.reqparse.add_argument('author', type=str, required=True, help='Author is required and must be a string.')

    def get(self):
        """Retrieve all books, excluding deleted ones."""
        return [book.to_dict() for book in bookservice.retrive_all_books()], 200

    def post(self):
        """Add a new book."""
        args = self.reqparse.parse_args()
        new_book = bookservice.add_book(args['title'], args['author'])
        return new_book.to_dict(), 201

class RestoreBookResource(Resource):
    """Endpoint to restore a soft-deleted book."""

    def post(self, book_id):
        restored_book = bookservice.restore_book(book_id)
        if restored_book:
            return restored_book.to_dict(), 200
        return {"error": "Book not found or not deleted"}, 404

api.add_resource(BookListResource, '/books')
api.add_resource(BookResource, '/books/<int:book_id>')
api.add_resource(RestoreBookResource, '/books/<int:book_id>/restore')

if __name__ == "__main__":
    app.run()
