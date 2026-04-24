import streamlit as st
import requests
import json

def main():
    print("Hello from sme-assistant-ui!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Enter your prompt here")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        response = requests.post(
            #"https://v749g1yxl6.execute-api.us-east-1.amazonaws.com/test/sme_assistant",
            "https://1drdjbbcj7.execute-api.us-east-1.amazonaws.com/stage_sme_assistant/sme_assistant",
            json={"prompt": prompt}
        )
        if response.status_code == 200:
            response_data = response.json()
            if isinstance(response_data, dict) and "body" in response_data:
                result = json.loads(response_data["body"])
                print(response_data)
                st.session_state.messages.append({"role": "assistant", "content": result})
                with st.chat_message("assistant"):
                    st.write(result)

   

if __name__ == "__main__":
    main()
