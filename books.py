from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1990, lt=2024)
    
    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'Coding with J.Q',
                'description': 'A new description of a book',
                'rating': 5,
                'published_date': 1995
            }
        }


BOOKS =[
    Book(1, 'Computer Science Pro', 'codingwithJohn','A very nice book!', 5, 1995),
    Book(2, 'Devops', 'codingwithJohn','Awesome book!', 5, 2012),
    Book(3, 'Be Fast with FASTAPI', 'Learning FAST API','A great book!', 5, 1998),
    Book(4, 'HP1', 'codingwithjohn','A very nice book!', 5, 1999),
    Book(5, 'READ READ', 'codingwithjohn','A very nice book!', 5, 1995),
    Book(6, 'Many Reads', 'FAST API','A very nice book!', 3, 2000),
    Book(7, 'Book6', 'FAST API','A very nice book!', 5, 2023),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


# @app.post("/create_book")
# async def create_book(book_request=Body()):
#     BOOKS.append(book_request)

# endpoint that will allow to find book by id
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def find_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found.')
        
#Endpoint that fetch books by rating, filter by rating
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating:int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

"""
Assignment


Add a new field to Book and BookRequest called published_date: int (for example, published_date: int = 2012). So, this book as published on the year of 2012.

Enhance each Book to now have a published_date

Then create a new GET Request method to filter by published_date"""
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def get_books_by_date(published_date: int = Query(gt=1990, lt=2024)):
    return_books = []
    for book in BOOKS:
        if book.published_date == published_date:
            return_books.append(book)
    return return_books


#Post method to create a book
@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book =Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))

#create api endpoint that updates  books
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_updated = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_updated = True
    if not book_updated:
        raise HTTPException(status_code=404, detail='Item not found so Book is not updated')


#end point that deletes book by id
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail='Item not found and/or Book not deleted')

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1

    return book



