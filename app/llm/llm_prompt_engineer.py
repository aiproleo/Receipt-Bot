# llm_prompt_engineer.py
import streamlit as st
import os

from ..db import db_handler

from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_openai import OpenAI, ChatOpenAI, OpenAIEmbeddings

def sql_for_vector(query, relevant_tables, table_info, chat_llm):

    template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    f"You are an assistant that can write SQL Queries."
                    f"Given the text below, write a SQL query that answers the user's question."
                    f"Assume that there is/are SQL table(s) named '{relevant_tables}' "
                    f"Here is a more detailed description of the table(s): "
                    f"{table_info}"
                    "Prepend and append the SQL query with three backticks '```'"
                )
            ),
            HumanMessagePromptTemplate.from_template("{text}"),
        ]
    )
    chat_llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0.4)

    answer = chat_llm(template.format_messages(text=query))

    return answer.content