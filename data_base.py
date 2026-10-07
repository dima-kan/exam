import dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from pinecone import ServerlessSpec
from pinecone import Pinecone
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    BaseMessage,
    trim_messages,
)

dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
supabase_uri = os.getenv("DATABASE_URL")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    api_key=api_key
)
embedding = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    api_key=api_key,
)

pc = Pinecone(api_key=pinecone_api_key)

index_name = "data-try"

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

@tool
def document_search(query: str):
    """
    Пошук у внутрішньому документі Медичного Центру "Омега-Мед"
    (правила внутрішнього трудового розпорядку для працівників).
    База містить інформацію про: прийом на роботу та випробувальний термін,
    робочий час і графіки, оплату праці (аванс, зарплата, доплати, премії),
    відпустки (щорічні, соціальні, без збереження зарплати), відрядження,
    навчання, дисципліну, охорону праці, конфіденційність, звільнення.
    Використовуй для питань працівників про їхні права, обов'язки та правила центру.
    :param query: str -- запит користувача
    :return: знайдені фрагменти документа
    """
    result = vector_store.similarity_search(query, k=3)
    return result

db = SQLDatabase.from_uri(supabase_uri)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_tools = toolkit.get_tools()

agent = create_agent(
    model=llm,
    tools=[document_search, *sql_tools]
)


messages = [
    SystemMessage("""
    Ти — корисний асистент із двома джерелами знань:
    1. Векторна база (document_search) — для пошуку інформації про (правила внутрішнього трудового розпорядку для працівників).
    2. SQL-база Supabase — для відповідей на питання про структуровані дані.

    ###ІНСТРУКЦІЯ###
    1. Якщо користувач питає про правила   — використовуй document_search.
    2. Якщо питання стосується структурованих даних — використовуй SQL-інструменти.
    3. Якщо не маєш інформації — не вигадуй.

    Правила роботи з SQL:
    - Спочатку подивись список таблиць.
    - Потім переглянь схему потрібної таблиці.
    - Генеруй ТІЛЬКИ SELECT-запити. Ніколи не змінюй дані.
    """)
]
