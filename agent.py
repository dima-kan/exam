from langchain.agents import create_agent
from langchain_core.messages import SystemMessage

from llm import llm
from prompts.prompts import SYSTEM_PROMPT
from tools.document_search import document_search
from tools.sql_tools import sql_tools

all_tools = [document_search, *sql_tools]

agent = create_agent(
    model=llm,
    tools=all_tools,
)

messages = [
    SystemMessage(SYSTEM_PROMPT)
]
