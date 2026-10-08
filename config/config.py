from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")
    gemini_api_key: str
    pinecone_api_key: str
    database_url: str

    llm_model: str = "gemini-3.5-flash-lite"
    embedding_model: str = "gemini-embedding-001"
    embedding_dimension: int = 3072
    index_name: str = "information-hospital"
    metric: str = "cosine"
    cloud: str = "aws"
    region: str = "us-east-1"
    data_dir: str = "data"
    ids_file: str = "id.json"


cfg = Settings()
