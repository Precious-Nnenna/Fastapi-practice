from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author:str
    year: int
    PAGES: int
    language: str

class BookCreate(BaseModel):
    title: str
    author:str
    year: int
    PAGES: int
    language: str

class BookUpdatePut(BaseModel):
    title: str
    author:str
    year: int
    pages: int
    language: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    pages: Optional[int] = None
    language: Optional[str] = None

class Books(BaseModel):
    books: list[Book]

class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None
    data: Optional[Book|Books] = None

books: dict[str, Book] = {}


@app.get("/")
def home():
    return{"Message": "This is a books API"}

@app.get("/books")
def get_books():
    return books

@app.get("/books/{id}")
def get_book_by_id(id: UUID):
    book = books.get(str(id))
    if not book:
        return{"error": "Book not found"}
    return book


@app.post("/books")
def add_book(book_in: BookCreate):
    book = Book(
        id = str((UUID(int = len(books) + 1))),
        **book_in.model_dump()
    )
    books[book.id] = book
    return Response(message="Book Added!", data=book)
    


@app.put("/books/{id}")
def update_book(id: UUID, book_in: BookUpdatePut):
    book = books.get(str(id))
    if not book:
        return Response(error_message="Not found")
    
    book_dict = book_in.model_dump()
    for key, value in book_dict.items():
        setattr(book, key, value)

    return Response(message="Book Updated!", data=book)


@app.patch("/books/{id}")
def partial_book_update(id: UUID, book_in: BookUpdate):
    book = books.get(str(id))
    if not book:
        return Response(error_message="Not found")
    
    book_dict = book_in.model_dump(exclude_unset=True)
    for key, value in book_dict.items():
        setattr(book, key, value)

    return Response(message="Book Updated!", data=book)


@app.delete("/books/{id}")
def delete_book(id: UUID):
    book = books.get(str(id))
    if not books:
        return {Response(error_message="Not found")}
    
    del books[book.id]
    return Response(message="Book Deleted!")



