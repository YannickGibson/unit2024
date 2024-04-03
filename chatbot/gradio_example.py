import gradio as gr
import openai
import os
import chatbot

def main():

    CHAT_GPT = False
    if CHAT_GPT:
        client = openai.Client(api_key=os.environ["OPENAI_API_KEY"])
        chbot = chatbot.Chatbot(client, "gpt-4")
        def our_response(message, history):
            msg = chbot.chat(message)
            return msg
    else:
        def our_response(message, history):
            return f"Your message was: {message}"
    

    demo = gr.ChatInterface(
        our_response,
        multimodal=True,
        undo_btn=None,
        retry_btn=None,
        clear_btn=None,
        title="Robot Pepper",
    )
    demo.launch()

if __name__ == "__main__":
    main()
