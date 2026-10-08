from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

from config.config import cfg
from llm import llm

db = SQLDatabase.from_uri(cfg.database_url)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
