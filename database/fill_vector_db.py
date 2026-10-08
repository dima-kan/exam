import json
from pathlib import Path
from uuid import uuid4

from langchain_core.documents import Document

from config.config import cfg
from database.vector_db import vector_store

documents = []
ids = []

for file in Path(cfg.data_dir).glob("*.txt"):
    text = file.read_text(encoding="utf-8")

    for block in text.split("\n\n"):

        if block.strip():

            document = Document(
                page_content=block.strip(),
                metadata={"source": file.name},
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
