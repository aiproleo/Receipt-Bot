import streamlit as st

import os
import re

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from ..db import db_handler


def is_valid_postgresql_uri(uri):
    """
    Validate the PostgreSQL URI format using regular expression.

    Parameters:
    uri (str): The PostgreSQL URI to validate.

    Returns:
    bool: True if the URI is valid, False otherwise.
    """
    regex = (
        r"^(postgresql|postgres):\/\/"              # Scheme
        r"(?:(?P<user>[^:@\s]+)(?::(?P<password>[^@\s]*))?@)?"  # Optional user and password
        r"(?P<host>[^:\/\s]+)"                      # Host
        r"(?::(?P<port>\d+))?"                      # Optional port
        r"(?:\/(?P<dbname>[^\?\s]*))?"              # Database name
        r"(?:\?(?P<params>[^\s]+))?$"               # Optional query parameters
    )

    match = re.match(regex, uri)
    if not match:
        return False
    return True


def session_init():
    """
    Initialize the Streamlit session state.

    This function sets up the initial session state for Streamlit, including
    messages, data home directory, and database schema. It also initializes
    the vector database with the table information from the database schema.
    """

    # Initialize messages in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize DATA_HOME in session state
    if "DATA_HOME" not in st.session_state:
        st.session_state.DATA_HOME = []
        st.session_state.DATA_HOME = 'data/'

    # Initialize DB_SCHEMA in session state
    if "DB_SCHEMA" not in st.session_state:
        st.session_state.DB_SCHEMA = []
        table_info: str = db_handler.DatabaseHandler().get_db_schema()
        st.session_state.DB_SCHEMA = table_info

def get_vector_db(query="any"):

    csv_path='./data/db/TABLES_COLUMNS.CSV'
    chroma_persist = './data/chroma'
                  
    loader = CSVLoader(file_path=csv_path, encoding="utf8")
    documents = loader.load()
    if len(documents) > 0:
        st.write("Sample Documents:")
        for i in range(min(3, len(documents))):  # Display up to 3 documents
            st.write(f"Document {i + 1}:")
            st.write(documents[i])

    st.info("Database Schema loaded successfully!")

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    if not os.path.isdir(chroma_persist):
        vectordb = Chroma.from_documents(documents, embedding=embeddings, persist_directory=chroma_persist)
        st.success("Chroma DB created successfully!")
    else:
        vectordb = Chroma(persist_directory=chroma_persist, embedding_function=embeddings)
        if vectordb:
            st.info(vectordb.__sizeof__())
            # Retrieve relevant documents
            retriever = vectordb.as_retriever()
            documents = retriever.get_relevant_documents("a")
            st.info(f"documents: {len(documents)}")

            # Display sample documents using Streamlit
            if len(documents) > 0:
                st.write("Sample Documents:")
                for i in range(min(3, len(documents))):  # Display up to 3 documents
                    st.write(f"Document {i + 1}:")
                    st.write(documents[i])
            else:
                st.write("No relevant documents found.")
        else:
            st.write("Failed to load Chroma DB. Check logs for more details.")


    return vectordb


