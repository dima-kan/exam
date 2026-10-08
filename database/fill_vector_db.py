import json
import os
from uuid import uuid4

from langchain_core.documents import Document

from config.config import cfg
from database.vector_db import vector_store

documents = []
ids = []

for file_name in os.listdir(cfg.data_dir):

    if not file_name.endswith(".txt"):
        continue

    with open(os.path.join(cfg.data_dir, file_name), "r", encoding="utf-8") as f:
        text = f.read()

    blocks = text.split("\n\n")

    for block in blocks:

        if block.strip():

            document = Document(
                page_content=block.strip(),
                metadata={"source": file_name},
            )

            documents.append(document)
            ids.append(str(uuid4()))

vector_store.add_documents(
    documents=documents,
    ids=ids,
)

with open(cfg.ids_file, "w", encoding="utf-8") as file:
    json.dump(ids, file, ensure_ascii=False, indent=2)

print(len(ids))
print(len(documents))
