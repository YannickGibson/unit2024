import gradio as gr
import openai
import os
import chatbot
import subprocess

def send_message(msg):
    ssh_command = f"ssh nao@172.20.10.103 -i id_pepper \"/home/nao/DumpIT/run.sh '{msg}'\""
    subprocess.run(ssh_command, shell=True, check=True)

def main():

    CHAT_GPT = False
    if CHAT_GPT:
        client = openai.Client(api_key=os.environ["OPENAI_API_KEY"])
        chbot = chatbot.Chatbot(client, "gpt-4")
        def our_response(message, history):
            bot_msg = chbot.chat(message)
            return bot_msg
    else:
        
        def our_response(message, history):
            bot_msg = f"Your message was {message}"
            send_message(bot_msg)
            return bot_msg
    

    demo = gr.ChatInterface(
        our_response,
        multimodal=False,
        undo_btn=None,
        retry_btn=None,
        clear_btn=None,
        title="Robot Pepper",
        theme="dark"
    )
    demo.launch()

if __name__ == "__main__":
    main()
