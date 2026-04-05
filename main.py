import uvicorn
from fastapi import FastAPI

from api.routes.chat import router as chat_router

app = FastAPI(title="study-rag-ash", version="0.1.0")
app.include_router(chat_router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "RAG API is running."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
