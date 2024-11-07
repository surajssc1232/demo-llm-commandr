import cohere
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key and validate
api_key = os.getenv('api_key')
if not api_key:
    print("Error: API key not found. Please make sure you have a .env file with api_key=YOUR_API_KEY")
    sys.exit(1)

try:
    co = cohere.ClientV2(api_key)
except Exception as e:
    print(f"Error initializing Cohere client: {str(e)}")
    sys.exit(1)

ANIME_SYSTEM_PROMPT = """You are an anime expert chatbot. Your role is to:
1. Answer questions about anime series, characters, plots, and creators
2. Provide recommendations based on users' interests
3. Discuss anime-related topics, including manga adaptations
4. Share interesting facts about the anime industry
Only respond to anime-related queries. If a question is not about anime, politely remind the user that you can only discuss anime-related topics."""

def is_anime_related(text):
    try:
        check_response = co.chat(
            model="command-r",
            messages=[
                {
                    "role": "system",
                    "content": "You are a classifier. Respond with 'yes' if the following message is related to anime, manga, or Japanese animation. Otherwise, respond with 'no'."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        return check_response.message.content[0].text.lower().strip().startswith('yes')
    except Exception as e:
        print(f"Error in anime classification: {str(e)}")
        return True  # Default to true to allow the message to go through

def process_message(message, validate=True):
    try:
        if validate and not is_anime_related(message):
            return "I'm specialized in anime-related topics only. Please ask me something about anime, manga, or Japanese animation!"
        
        response = co.chat(
            model="command-r",
            messages=[
                {
                    "role": "system",
                    "content": ANIME_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response.message.content[0].text
    except Exception as e:
        return f"Sorry, there was an error processing your message: {str(e)}"

def chat_with_cohere():
    print("Animebot is ready! Ask me anything about any anime but just not MHA its bad. Type 'exit' to end the conversation.")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Chatbot: Goodbye! Thanks for discussing anime with me!")
                break

            assistant_message = process_message(user_input)
            print(f"Chatbot: {assistant_message}")
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Please try again or type 'exit' to quit.")

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            message = ' '.join(sys.argv[1:])
            response = process_message(message, validate=True)
            print(f"Chatbot: {response}")
        else:
            chat_with_cohere()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Fatal error: {str(e)}")