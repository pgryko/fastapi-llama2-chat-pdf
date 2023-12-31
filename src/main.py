from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from chromadb.utils import embedding_functions

import chromadb
from chromadb.api.models.Collection import Collection

from chromadb.api.types import Documents
from starlette.responses import RedirectResponse

from .services import (
    stream_chat as service_stream_chat,
    get_pdf_text,
    get_text_chunks,
    compute_md5,
)
from .schemas import GetResultMetaNone

app = FastAPI(
    title="FastAPI llama2 chat",
    description="An API that lets you use llama2 to chat with documents.",
    version="1.0.0",
    swagger_ui_url="/docs",
)

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
    """From chromadb get the current time in nanoseconds since epoch.
    Used to check if the chroma service is alive."""
    return client.heartbeat()


@app.get("/chroma/get")
async def chroma_get() -> GetResultMetaNone:
    """Return what's stored in the collection."""
    return collection.get()


@app.delete("/chroma/delete")
async def chroma_delete() -> None:
    """Deletes the contents of the collection"""
    return collection.delete()


@app.post("/stream_chat/{chat_input}", response_class=StreamingResponse)
async def stream_chat(chat_input: str):
    return StreamingResponse(
        service_stream_chat(chat_input), media_type="text/event-stream"
    )


@app.get("/stream_chat/{chat_input}", response_class=StreamingResponse)
async def stream_chat(chat_input: str):
    return StreamingResponse(
        service_stream_chat(chat_input),
        media_type="text/event-stream",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-cache",
            "Transfer-Encoding": "chunked",
        },
    )


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content: bytes = await file.read()
    md5 = compute_md5(content)
    text = get_pdf_text(content)
    text_chunks: Documents = get_text_chunks(text)
    # Append the md5 to the id to add pseudo uniqueness to uploaded documents.
    # Its annoying that collection does not return info about the documents added (e.g. duplicated added)
    collection.add(
        documents=text_chunks, ids=[md5 + str(i) for i in range(len(text_chunks))]
    )


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")


#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
