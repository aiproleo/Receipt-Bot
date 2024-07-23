# llm_handler.py
import streamlit as st
import vector_chroma

import os
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

from ..db import db_handler

class LLMHandler:
    def __init__(self):
        self.chat_llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0.4)
        self.POSTGRESQL_AI_URI = os.getenv("POSTGRESQL_AI_URI")
        self.db_schema: str = db_handler.DatabaseHandler().get_db_schema()

    def sql_based_on_tables(self, query):
        template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                        f"You are an assistant that can write complicated SQL Queries."
                        f"Given the text below, write a SQL query that answers the user's question."
                        f"DB connection string is {self.POSTGRESQL_AI_URI}"
                        f"Here is a detailed description of the table(s): "
                        f"{self.db_schema}"
                        "Prepend and append the SQL query with three backticks '```'"
                    )
                ),
                HumanMessagePromptTemplate.from_template("{text}"),
            ]
        )
        answer = self.chat_llm(template.format_messages(text=query))
        return answer.content


    def get_response_from_llm(self, query):
        content = self.sql_based_on_tables(query)
        return content


    def get_sql_from_vector(self, query):
        st.error('here')
        vector_chroma.get_response_from_llm_vector()
        st.error('here2')

        # vectordb = st.session_state.VECTOR_EMBEDDINGS
        # retriever = vectordb.as_retriever()
        # docs = retriever.get_relevant_documents(query)

        # relevant_tables = []
        # relevant_tables_and_columns = []

        # for doc in docs:
        #     table_name, column_name, data_type = doc.page_content.split("\n")
        #     table_name = table_name.split(":")[1].strip()
        #     relevant_tables.append(table_name)
        #     column_name = column_name.split(":")[1].strip()
        #     data_type = data_type.split(":")[1].strip()
        #     relevant_tables_and_columns.append((table_name, column_name, data_type))

        # tables = ",".join(relevant_tables)
        # table_info = st.session_state.DB_SCHEMA

        # return llm_prompt_engineer.sql_for_vector(query, relevant_tables, table_info, self.chat_llm)
