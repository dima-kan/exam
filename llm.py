from langchain_google_genai import ChatGoogleGenerativeAI

from config.config import cfg

llm = ChatGoogleGenerativeAI(
    model=cfg.llm_model,
    api_key=cfg.gemini_api_key,
)
