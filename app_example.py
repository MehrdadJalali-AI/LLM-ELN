import os
import time

import gradio as gr
import openai



openai.api_key = os.environ["OPENAI_API_KEY"]
openai.organization = os.environ["Organization_KEY"]


system_message = {"role": "system", "content": "You are a helpful assistant."}


def user(user_message, history):
    return "", history + [[user_message, None]]


import logging
def logewirte(history):
    for history_one in history:
        print (history_one)

def bot_3(history, messages_history):
    model = "gpt-3.5-turbo"
    user_message = history[-1][0]
    bot_message, messages_history = ask_gpt(user_message, messages_history, model)
    messages_history += [{"role": "assistant", "content": bot_message}]
    history[-1][1] = bot_message
    time.sleep(1)
    return history, messages_history


def ask_gpt(message, messages_history, model):
    messages_history += [{"role": "user", "content": message}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages_history
    )
    return response['choices'][0]['message']['content'], messages_history


def init_history(messages_history):
    messages_history = []
    messages_history += [system_message]
    return messages_history


with gr.Blocks() as demo:
    gr.Markdown("ChatGPT")
    with gr.Tab("GPT-3.5"):
        chatbot = gr.Chatbot(label ='record')
        msg = gr.Textbox(label ='input')
        recording = gr.Button('recorder')
        sub = gr.Button("send")
        clear = gr.Button("clear")
        state = gr.State([])


        # 首先，输入[msg, chatbot]俩变量，然后赋值[msg, chatbot]来变量
        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot_3, [chatbot, state], [chatbot, state])


        sub.click(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot_3, [chatbot, state], [chatbot, state])
        clear.click(lambda: None, None, chatbot, queue=False).success(init_history, [state], [state])

        recording.click(logewirte,None,None)

demo.launch()

