import os, streamlit as st
import logging
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to load CSV data into Document objects
def load_csv_to_documents(file_path):
    loader = CSVLoader(file_path=file_path, encoding="utf8")
    return loader.load()

def load_chroma(persist_directory):
    try:
        # Initialize embeddings first
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        return vectordb

    except Exception as e:
        st.error(f"An error occurred while loading Chroma: {e}")
        return None

def get_response_from_llm_vector(query="tables"):

    vectordb = load_chroma(persist_directory='./data/chroma')
    if vectordb:
        st.write(vectordb.__sizeof__())
        # Retrieve relevant documents
        retriever = vectordb.as_retriever()
        documents = retriever.get_relevant_documents(query)

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


# Function to create embeddings and save to Chroma
def save_to_chroma(documents, persist_directory):
    try:
        # Log the start of the embedding process
        logging.info("Creating embeddings...")
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

        # Log the start of the Chroma saving process
        logging.info("Saving documents to Chroma...")
        vectordb = Chroma.from_documents(documents, embedding=embeddings, persist_directory=persist_directory)

        # Log successful saving
        logging.info("Documents successfully saved to Chroma.")
        return vectordb
    except Exception as e:
        # Log any exceptions that occur
        logging.error(f"An error occurred while saving to Chroma: {e}")
        st.error(f"An error occurred while saving to Chroma: {e}")
        return None

# Streamlit app
def main():
    st.title('CSV to Chroma DB')

    # Load CSV data
    documents = load_csv_to_documents('./data/db/TABLES_COLUMNS.CSV')
    st.write("CSV file loaded successfully!")

    # Save documents to Chroma
    persist_directory = './data/chroma4'
    vectordb = save_to_chroma(documents, persist_directory)

    if vectordb:
        st.write("Data saved to Chroma DB successfully!")

        # Display the content of the first document
        if len(documents) > 0:
            st.write("Sample Document:")
    else:
        st.write("Failed to save data to Chroma DB. Check logs for more details.")

if __name__ == "__main__":
    st.error('here')
    # main()
    get_response_from_llm_vector()
    st.error('here2')
