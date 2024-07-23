import streamlit as st


class ChatUI:
    def __init__(self, db_handler, llm_handler, vector_or_others):
        self.db_handler = db_handler
        self.llm_handler = llm_handler
        self.vector_or_others = vector_or_others

    def send_message(self, message):
        respond_contents = self.llm_handler.get_sql_from_vector(message)

        result = self.db_handler.execute_sql(respond_contents)


        result = result.replace("),", "),  \n")

        return {"message": respond_contents + "\n\n ###### Result: ###### \n\n" + result}

    def run(self):
        """
        Runs the chat UI, displaying messages and handling user input.
        """
        if "messages" not in st.session_state:
            st.session_state.messages = []


        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("⌨️ ask me "):
            st.chat_message("user").markdown(prompt)            # 1.Display user message in chat message container

            st.session_state.messages.append(
                {"role": "user", "content": prompt})            # 2. Add user message to chat history

            response = self.send_message(prompt)["message"]     # 3. Get message from ChatGPT
            with st.chat_message("assistant"):
                st.info(response)                           # 4. Display message from ChatGPT

            st.session_state.messages.append(
                {"role": "assistant", "content": response})     # 5. keep history
