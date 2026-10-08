from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from config.config import cfg

embedding = GoogleGenerativeAIEmbeddings(
    model=cfg.embedding_model,
    api_key=cfg.gemini_api_key,
)

pc = Pinecone(api_key=cfg.pinecone_api_key)

if not pc.has_index(cfg.index_name):
    pc.create_index(
        name=cfg.index_name,
        dimension=cfg.embedding_dimension,
        metric=cfg.metric,
        spec=ServerlessSpec(
            cloud=cfg.cloud,
            region=cfg.region,
        ),
    )

index = pc.Index(cfg.index_name)

vector_store = PineconeVectorStore(
    index=index,
    embedding=embedding,
)
