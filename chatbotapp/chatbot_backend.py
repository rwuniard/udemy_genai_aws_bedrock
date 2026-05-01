from langchain_aws import ChatBedrockConverse


def get_chatbot():
    return ChatBedrockConverse(
        credentials_profile_name="default",
        model="us.deepseek.r1-v1:0",
        temperature=0.7,
        max_tokens=1000
    )


def main():
    print("Hello from chatbot_backend!")
    messages = [
        {"role": "user", "content": "What is the capital of France?"}
    ]
    chatbot = get_chatbot()
    response = chatbot.invoke(messages)
    print(response)

if __name__ == "__main__":
    main()