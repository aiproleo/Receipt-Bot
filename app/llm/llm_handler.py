# llm_handler.py
import streamlit as st
import os

from langchain_chroma import Chroma
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

from ..db  import db_handler
from . import llm_prompt_engineer

class LLMHandler:
    def __init__(self):
        self.chat_llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0.4)
        self.POSTGRESQL_AI_URI = os.getenv("POSTGRESQL_AI_URI")

    def get_sql_from_vector(self, query, table_info):

        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        vectordb = Chroma(persist_directory='./data/chroma', embedding_function=embeddings)
        
        if vectordb:
            retriever = vectordb.as_retriever()
            docs = retriever.get_relevant_documents(query)

            # Display sample documents using Streamlit
            if len(docs) > 0:
                st.subheader("Filtered Documents:")
                for i in range(min(5, len(docs))):  # Display up to 3 docs
                    st.write(f"Document {i + 1}:")
                    st.write(docs[i])
            else:
                st.write("No relevant docs found.")
        else:
            st.write("Failed to load Chroma DB. Check logs for more details.")

        relevant_tables = []
        relevant_tables_and_columns = []

        for doc in docs:
            table_name, column_name, data_type = doc.page_content.split("\n")
            table_name = table_name.split(":")[1].strip()
            relevant_tables.append(table_name)
            column_name = column_name.split(":")[1].strip()
            data_type = data_type.split(":")[1].strip()
            relevant_tables_and_columns.append((table_name, column_name, data_type))

        tables = ",".join(relevant_tables)

        return llm_prompt_engineer.sql_for_vector(query, tables,table_info, self.chat_llm)
