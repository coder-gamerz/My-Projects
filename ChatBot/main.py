import customtkinter as tk
import openai
from dotenv import dotenv_values

config = dotenv_values(r'/home/codergamerz/Documents/main.env')

abc = config['CHATGPT_API_KEY']
openai.api_key = abc

messages = [{"role": "system", "content": 'You are a therapist and a coding assistant. Respond to all input in 25 words or less.'}]

def transcribe():
    global messages
    a = entry.get()  

    messages.append({"role": "user", "content": a})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    
    label['text'] = system_message['content']

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    
    text_box.delete("1.0", tk)
    text_box.insert(tk, chat_transcript)

def handle_button_click():
    transcribe()


window = tk.CTk()
window.title("Chat Transcription")


label = tk.CTkLabel(window, text="Prompt: ")
label.pack()


entry = tk.CTkEntry(window)
entry.pack()


button = tk.CTkButton(window, text="Submit", command=handle_button_click)
button.pack()


text_box = tk.CTkTextbox(window, height=10, width=40)
text_box.pack()

window.mainloop()
