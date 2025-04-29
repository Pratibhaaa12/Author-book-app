from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
     
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Sector51@localhost/book_authordb'


db = SQLAlchemy(app)

class Author(db.Model):
    __tablename__='author'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500))
    phone_number = db.Column(db.String(15), nullable=False)


    book = db.relationship('Book' , backref = 'author', uselist=False)

class Book(db.Model):
    __tablename__='book'
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200), nullable=False)
    type_book= db.Column(db.String(500))

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), unique=True, nullable=False)

# Create DB Tables
with app.app_context():
    db.create_all()

@app.route('/authors', methods=['POST'])
def create_author():
    author = request.get_json()
    new_author= Author(
        name=author.get('name'),
        email=author.get('email',''),
        phone_number=author.get('phone_number','')
    )
    db.session.add(new_author)
    db.session.commit()
    return jsonify({"message": "Author created", "id": new_author.id}), 201

# Get All Authors
@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    result = [{"id": a.id, "name": a.name, "email": a.email, "phone_number": a.phone_number, "book": a.book.id if a.book else None} for a in authors]
    return jsonify(result)

# Get Author by ID
@app.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    author = Author.query.get_or_404(author_id)
    return jsonify({
        "id": author.id,
        "name": author.name,
        "email": author.email,
        "phone_number": author.phone_number,
        "book": author.book.id if author.book else None
    })


# Update Author
@app.route('/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    author = Author.query.get_or_404(author_id)
    data = request.get_json()
    author.name = data.get('name', author.name)
    author.email = data.get('email', author.email)
    author.phone_number = data.get('phone_number', author.phone_number)
    db.session.commit()
    return jsonify({"message": "Author updated"})

# Delete Author
@app.route('/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    return jsonify({"message": "Author deleted"})

@app.route('/authors',methods=['DELETE'])
def  delete_authors():
    Author.query.delete()
    db.session.commit()
    return jsonify({"message":"ALL authors deleted"})







# Create book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    author_id = data.get('author_id')

    if author_id is None:
        return jsonify({'error': 'author_id is required'}), 400

    author = Author.query.get_or_404(author_id)

    new_book = Book(
        name=data['name'],
        type_book=data.get('type_book', ''),
        author_id=author.id
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book created", "id": new_book.id}), 201


# Get All Books
@app.route('/books', methods=['GET'])
def get_books():
    books= Book.query.all()
    result = [{"id": b.id, "name": b.name, "type": b.name, "author_id":b.author_id} for b in books]
    return jsonify(result)

# Get Book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({
        "id": book.id,
        "name": book.name,
        "type_book": book.type_book,
        "author_id": book.author_id
    })

# Update Book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    book.name = data.get('name', book.name)
    book.type_book = data.get('type_book', book.type_book)
    db.session.commit()
    return jsonify({"message": "Book updated"})

# Delete Book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})

@app.route('/books',methods=['DELETE'])
def  delete_books():
    Book.query.delete()
    db.session.commit()
    return jsonify({"message":"ALL books deleted"})




if __name__ == '__main__':
    app.run(debug=True)
