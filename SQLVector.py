import os, streamlit as st
import vector_chroma

import dotenv
dotenv.load_dotenv()

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader

from app import (
    ui,
    db_handler,
    llm,
    utils
)

utils.streamlit_components.streamlit_ui('🐬🦣 Chat with Vector🍃🦭')

if __name__ == "__main__":
    
    st.error('here')
    vector_chroma.get_response_from_llm_vector()
    st.error('here2')

    db_handler = db_handler.DatabaseHandler()   # init: session_state add uri, with save() get unique_id.
    llm_handler = llm.llm_handler.LLMHandler()      # Initialize the language model handler with the OpenAI API key
    
    app = ui.chat_ui.ChatUI(db_handler, llm_handler, 'chroma')   # Create an instance of the Streamlit UI and pass the handlers to it
    app.run()   # Run the Streamlit application
