from flask import Flask, jsonify, request

app = Flask(__name__)

# Resources
books = []

# getting item from the data
@app.route('/', methods=['GET'])
def get_all_books():
    return jsonify(books), 200

@app.route('/<int:book_id>', methods=['GET'])
def get_a_single_resource(book_id):
    book = next((item for item in books if item['id'] == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({
        'error': "Resource not found"
    }), 404

# Append item to the resource

@app.route('/', methods=["POST"])
def create_resource():
    new_item = request.get_json()
    import pdb; pdb.set_trace()
    new_item['id'] = books[-1]['id'] + 1 if books else 1
    books.append(new_item)
    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run()
