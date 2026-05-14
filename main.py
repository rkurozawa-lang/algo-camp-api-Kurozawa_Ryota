from fastapi import Body, FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

#単体のポストパラメータ
@app.post("/users/create")
def create_user(name: str = Body(), age: int = Body(), birthday:  str = Body()):
    content = {
        "name": name,
        "age": age,
        "birthday": birthday
    }
    print(content)
    return "OK"
