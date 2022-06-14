# coding:utf-8

from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from request_id_middleware import RequestIDMiddleware


app = FastAPI()

app.add_middleware(RequestIDMiddleware)


@app.get("/items")
async def get_items():
    return {"name": "hello item", "price": 7.1}


@app.get("/users")
async def get_users():
    return [{"username": "alex"}, {"username": "bob", "age": 21}, {"username": "alice"}]


@app.get("/raise")
async def raise_error():
    raise HTTPException(status_code=418, detail="something bad happened...")
