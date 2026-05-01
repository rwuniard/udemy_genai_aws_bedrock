from langchain_aws import ChatBedrockConverse
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from rich.pretty import pprint


class ChatbotBackend:
    def __init__(self):
        self.agent = self.get_agent()

    def send_message(self, message):
        messages = [
            {"role": "user", "content": message}
        ]
        return self.agent.invoke(messages)

    def get_llm(self):
        return ChatBedrockConverse(
            credentials_profile_name="default",
            model="us.deepseek.r1-v1:0",
            temperature=0.7,
            max_tokens=1000
        )

    def get_agent(self):
        model = self.get_llm()
        return create_agent(
            model=model,
            tools=[], 
            checkpointer=InMemorySaver()
        )

    def send_message(self, message):
        messages = [
            {"role": "user", "content": message}
        ]
        result = self.agent.invoke(
            {
                "messages": messages,
                "user_id": "user_123",
                "preferences": {"theme": "dark"}
            },
            {"configurable": {"thread_id": "1"}}
        )
        return result["messages"][-1].content[0]["text"]

def main():
    print("Hello from chatbot_backend!")
    chatbot = ChatbotBackend()
    user_input = ""
    while user_input != "exit":
        user_input = input("Enter your message: ")
        response = chatbot.send_message(user_input)
        print("Response:", response)


if __name__ == "__main__":
    main()