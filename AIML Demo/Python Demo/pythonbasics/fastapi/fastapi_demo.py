from fastapi import FastAPI
from threading import Thread
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello JMJ": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    server_thread = Thread(target=run_server)
    server_thread.start()
