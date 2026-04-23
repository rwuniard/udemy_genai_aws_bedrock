import streamlit as st

def main():
    print("Hello from sme-assistant-ui!")
    prompt = st.chat_input("Enter your prompt here")
    if prompt:
        st.write(f"You entered: {prompt}")

if __name__ == "__main__":
    main()
