from fastapi import FastAPI

app = FastAPI()

BOOKS =[
    {
        "title": "John", "author": "Ikram", "category": "History"
    }
]


@app.get("/books")
async def read_all_books():
    return BOOKS

