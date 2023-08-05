from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from chromadb.utils import embedding_functions

import chromadb
from chromadb.api.models.Collection import Collection

from chromadb.api.types import GetResult

from services import stream_chat

app = FastAPI()

default_ef = embedding_functions.DefaultEmbeddingFunction()

# Lots of different embedding functions are available.
# https://docs.trychroma.com/embeddings
# Embedding functions can be run on the CPU or GPU.
# ef = embedding_functions.InstructorEmbeddingFunction()
# ef = embedding_functions.InstructorEmbeddingFunction(
# model_name="hkunlp/instructor-xl", device="cuda")

client = chromadb.PersistentClient(path="./chroma")
# TODO: create a collection per user
collection: Collection = client.get_or_create_collection(name="default")


@app.get("/chroma/heartbeat")
async def chroma_heartbeat() -> int:
    return client.heartbeat()


@app.get("/chroma/peak")
async def chroma_heartbeat() -> GetResult:
    return collection.get()


@app.post("/stream_chat/{chat_input}", response_class=StreamingResponse)
async def stream_chat(chat_input: str):
    return StreamingResponse(stream_chat(chat_input), media_type="text/event-stream")


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content: bytes = await file.read()
    vector = convert_to_vector(content)  # You'll need to implement this function

    # Add vector to Faiss index
    try:
        index.add(np.array([vector]))
        return {"detail": "File uploaded and vector added to datastore"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
