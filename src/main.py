from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from chromadb.utils import embedding_functions

import chromadb
from chromadb.api.models.Collection import Collection

from chromadb.api.types import GetResult, Documents

from services import stream_chat, get_pdf_text, get_text_chunks

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
collection: Collection = client.get_or_create_collection(
    name="default", embedding_function=default_ef
)

# TODO: Add auth and rate limiting on all APIs


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
    text = get_pdf_text(content)
    text_chunks: Documents = get_text_chunks(text)
    collection.add(documents=text_chunks, ids=[str(i) for i in range(len(text_chunks))])
