import gradio as gr
import openai
import os
import chatbot
import subprocess

def send_to_pepper(msg):
    ssh_command = f"ssh nao@172.20.10.103 -i id_pepper \"/home/nao/DumpIT/run.sh '{msg}'\""
    subprocess.run(ssh_command, shell=True, check=True)

def main():

    CHAT_GPT = True
    SEND_TO_PEPPER = False

    if CHAT_GPT:
        print(os.environ["OPENAI_API_KEY"])
        exit()
        client = openai.Client(api_key=os.environ["OPENAI_API_KEY"])
        chbot = chatbot.Chatbot(client, "gpt-4")
        
    def our_response(message, history):
        print("XXX Input XXX")
        message += ". (Odpověz maximálně ve 3 větách.)"
        print(message)

        if CHAT_GPT:
            bot_msg = chbot.chat(message)
        else:
            bot_msg = f"Your message was {message}"

        print("XXX Output XXX")
        print(bot_msg)

        if SEND_TO_PEPPER:
            send_to_pepper(bot_msg)

        return bot_msg
    
    

    demo = gr.ChatInterface(
        fn=our_response,
        chatbot=gr.Chatbot(value=[[None, "Ahoj, jsem virtuální asistent a jsem tu abych ti pomohl s výběrem oboru na FITu (Fakulta Informačních Technologií)."]]),
        multimodal=False,
        undo_btn=None,
        retry_btn=None,
        clear_btn=None,
        title="Robot Pepper",
    )
    # launch online
    demo.launch(share=False)
    #demo.launch()

if __name__ == "__main__":
    main()
