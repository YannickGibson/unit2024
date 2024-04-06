"""Interface to communicate with chatbot, results can be streamed to robot Pepper for text to speech http://doc.aldebaran.com/2-5/home_pepper.html."""

import os
import subprocess
from typing import Any
import gradio as gr
import openai

import chatbot.chatbot as chatbot


def send_to_pepper(message: str) -> None:
    """Send text to robot Pepper for it to voice it out. Runs a subprocess, waits for it to finish.
    
    Args:
        message: Text to send to robot Pepper.
    """
    ssh_command = f"ssh nao@172.20.10.103 -i tts_private_key \"/home/nao/DumpIT/run.sh '{message}'\""
    subprocess.run(ssh_command, shell=True, check=True)


def main() -> None:
    """Main function to run the chatbot interface. Optionally uses text to speach via Pepper.
    For ChatGPT set 'OPEN_API_KEY' environmental variable.
    """

    CHAT_GPT = False
    SEND_TO_PEPPER = False
    BOTS_INITIAL_MESSAGE = "Ahoj, jsem virtuální asistent a jsem tu abych ti pomohl s výběrem oboru na FITu (Fakulta Informačních Technologií)."

    if CHAT_GPT:
        client = openai.Client(api_key=os.environ["OPENAI_API_KEY"])
        chbot = chatbot.Chatbot(client, "gpt-4")
        
    def our_response(message: str, history: Any) -> str:
        """Function to be called when user inputs a message. It will return a response from the chatbot.
        
        Args:
            message: User input.
            history: Chat history.
        
        Returns:
            Response from the chatbot.
        """

        # For each message specify that the response needs to be brief.
        message += ". (Odpověz maximálně ve 3 větách.)"

        print("XXX Input XXX")
        print(message)

        if CHAT_GPT:
            bot_msg = chbot.chat(message)
        else:
            bot_msg = f"Your message was '{message}'"

        print("XXX Output XXX")
        print(bot_msg)

        if SEND_TO_PEPPER:
            send_to_pepper(bot_msg)

        return bot_msg
    
    web_interface = gr.ChatInterface(
        fn=our_response,
        chatbot=gr.Chatbot(value=[[None, BOTS_INITIAL_MESSAGE]]),
        title="Robot Pepper",
        multimodal=False,
        undo_btn=None,
        retry_btn=None,
        clear_btn=None,
    )
    web_interface.launch()


if __name__ == "__main__":
    main()
