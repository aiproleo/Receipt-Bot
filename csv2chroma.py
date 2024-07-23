import os, streamlit as st
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader

def main():
    persist_directory = './data/chroma'

    loader = CSVLoader(file_path='./data/db/TABLES_COLUMNS.CSV', encoding="utf8")
    documents = loader.load()
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectordb = Chroma.from_documents(documents, embedding=embeddings, persist_directory=persist_directory)

if __name__ == "__main__":
    main()
