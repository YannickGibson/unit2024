
import openai
import os
import chatbot

def main():
    client = openai.Client(api_key=os.environ["OPENAI_API_KEY"])
    chbot = chatbot.Chatbot(client, "gpt-4")
    while True:
        msg = chbot.chat(input(" > "))
        print(msg)

if __name__ == "__main__":
    main()
