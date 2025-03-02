from sqlalchemy import Table, Column, create_engine, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime, timedelta
engine = create_engine('sqlite:///library.db')
Base = declarative_base()
# STEP 1 Table structure add
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique = True, nullable = False)
    author = Column(String, nullable = False)
    available = Column(Boolean, default=True, nullable = False)
    year_published = Column(Integer, nullable = False)
    borrowed_books = relationship('BorrowedBook', back_populates='book')

class Reader(Base):
    __tablename__ = 'readers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable = False)
    email = Column(String, unique=True, nullable = False)
    borrowed_books = relationship('BorrowedBook', back_populates='reader')

class BorrowedBook(Base):
    __tablename__ = 'borrowed_books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable = False)
    reader_id = Column(Integer, ForeignKey('readers.id'), nullable = False)
    borrowed_at = Column(DateTime, default=datetime.now, nullable = False)
    return_due_date = Column(DateTime,default=lambda: datetime.now() + timedelta(days=14), nullable = False)
    book = relationship('Book', back_populates='borrowed_books')
    reader = relationship('Reader', back_populates='borrowed_books')

Base.metadata.create_all(engine)
# STEP 2 Functions add
Session = sessionmaker(bind=engine)

# 1
def add_book(title, author, year_published):
    session = Session()
    book = Book(title=title, author=author, year_published=year_published, available=True)
    session.add(book)
    session.commit()
    session.close()
    print(f'Book {title} added')
# 2
def add_reader(name, email):
    session = Session()
    reader = Reader(name=name, email=email)
    session.add(reader)
    session.commit()
    session.close()
    print(f'User {name} added')
# 3
def borrow_book(book_title, reader_id):
    session = Session()
    book = session.query(Book).filter_by(title=book_title, available=True).first()
    reader = session.query(Reader).filter_by(id=reader_id).first()
    if book and reader:
        book.available = False
        borrowed_book = BorrowedBook(book_id=book.id, reader_id=reader.id)
        session.add(borrowed_book)
        session.commit()
        print(f'Book "{book.title}" borrowed by {reader.name}')
    else:
        print('Book not available or reader not found')
    session.close()

# 4
def update_book_info(book_title, new_title, new_author):
    session = Session()
    book = session.query(Book).filter_by(title=book_title).first()
    if book:
        if new_title:
            book.title = new_title
        if new_author:
            book.author = new_author
        session.commit()
        print('Book info updated')
    else:
        print('Book not found')
    session.close()
# 5
def delete_book(book_title):
    session = Session()
    book = session.query(Book).filter_by(title=book_title).first()
    if book:
        session.delete(book)
        session.commit()
        print('Book deleted')
    else:
        print('Book not found')
    session.close()
# 6
def delete_reader(reader_id):
    session = Session()
    reader = session.query(Reader).filter_by(id=reader_id).first()
    if reader:
        session.query(BorrowedBook).filter_by(reader_id=reader.id).delete()

        session.delete(reader)
        session.commit()
        print('User deleted')
    else:
        print('Reader not found')
    session.close()
# 7
def show_books():
    session = Session()
    books = session.query(Book).all()
    for book in books:
        if book.available:
            bukle = 'In stock'
        else:
            bukle = 'Not in stock'
        print(f'Title: {book.title} Author: {book.author} Stock: {bukle}')
    session.close()
# 8
def show_borrowed_books():
    session = Session()
    borrowed_books = (
        session.query(BorrowedBook, Book.title, Reader.name)
        .join(Book, BorrowedBook.book_id == Book.id)
        .join(Reader, BorrowedBook.reader_id == Reader.id)
        .all()
    )
    print('Borrowed Books:')
    if borrowed_books:
        for borrowed_book, title, reader_name in borrowed_books:
            print(f'Book {title} borrowed by {reader_name}')
    else:
        print('No borrowed books found')

    session.close()
# Menu
while True:
    print('1. Add Book')
    print('2. Add Reader')
    print('3. Borrow Book')
    print('4. Update Book Info')
    print('5. Delete Book')
    print('6. Delete Reader')
    print('7. Show Books')
    print('8. Show Borrowed Books')
    print('9. Exit')

    choice = input('Select an option: ')

    if choice == '1':
        title = input('Enter book title: ')
        author = input('Enter author: ')
        year = int(input('Enter publication year: '))
        add_book(title, author, year)
    elif choice == '2':
        name = input('Enter reader name: ')
        email = input('Enter reader email: ')
        add_reader(name, email)
    elif choice == '3':
        title = input('Enter book title: ')
        reader_id = int(input('Enter reader id: '))
        borrow_book(title, reader_id)
    elif choice == '4':
        title = input('Enter book title: ')
        new_title = input('New title: ')
        new_author = input('New author: ')
        update_book_info(title, new_title, new_author)
    elif choice == '5':
        title = input('Enter book title: ')
        delete_book(title)
    elif choice == '6':
        reader_id = int(input('Enter reader ID: '))
        delete_reader(reader_id)
    elif choice == '7':
        show_books()
    elif choice == '8':
        show_borrowed_books()
    elif choice == '9':
        break
    else:
        print('Please enter number from menu')