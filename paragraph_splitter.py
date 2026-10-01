from uuid import uuid4
import json
import os
import dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from pinecone import ServerlessSpec
from pinecone import Pinecone


dotenv.load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")


# Embedding model
embedding = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    api_key=api_key,
)


# Pinecone
index_name = "information-hospital"

pc = Pinecone(api_key=pinecone_api_key)


if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
    )

index = pc.Index(index_name)


vector_store = PineconeVectorStore(
    index=index,
    embedding=embedding
)


file_paths = [
    r"D:\exam\general.txt",
    r"D:\exam\for_workers.txt"
]


documents = []
ids = []


for file_path in file_paths:

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    blocks = text.split("\n\n")

    for block in blocks:

        if block.strip():

            document = Document(
                page_content=block.strip(),
                metadata={
                    "source": file_path
                }
            )

            documents.append(document)
            ids.append(str(uuid4()))


vector_store.add_documents(
    documents=documents,
    ids=ids
)


with open("D:\exam\ids", "w", encoding="utf-8") as file:
    json.dump(ids, file, ensure_ascii=False, indent=2)



print(len(ids))
print(len(documents))