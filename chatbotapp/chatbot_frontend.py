import streamlit as st
from chatbot_backend import ChatbotBackend

def main():
    st.title("Chatbot")

    # Initialize chatbot if not already present
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = ChatbotBackend()
    # Get chatbot from session state
    chatbot = st.session_state.chatbot

    # Initialize messages if not already present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Get user input
    prompt = st.chat_input("Enter your prompt here")
    # Send message to backend and display response
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        # Send message to backend and display response
        response = chatbot.send_message(prompt)
        # Add response to messages and display it
        st.session_state.messages.append({"role": "assistant", "content": response})
        # Display response
        with st.chat_message("assistant"):
            st.write(response)


if __name__ == "__main__":
    main()