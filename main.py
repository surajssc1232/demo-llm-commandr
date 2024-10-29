import cohere
import os
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv('api_key')

co = cohere.ClientV2(api_key)

def chat_with_cohere():
    print("Animebot is ready! Ask me anything about any anime but just not MHA its bad. Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break

        response = co.chat(
            model="command-r",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        
        assistant_message = response.message.content[0].text
        print(f"Chatbot: {assistant_message}")

if __name__ == "__main__":
    chat_with_cohere()