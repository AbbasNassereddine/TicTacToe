from dotenv import load_dotenv
import os
import boto3
import streamlit as st
import pandas as pd
from anthropic import AnthropicBedrock 

def getCredentials():
    load_dotenv(dotenv_path=r'TT.env')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION=os.getenv('AWS_REGION')
    sts_client = boto3.client(
        'sts',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION  
    )
    response = sts_client.get_session_token()
    client = AnthropicBedrock(
        aws_access_key=response['Credentials']['AccessKeyId'],
        aws_secret_key=response['Credentials']['SecretAccessKey'],
        aws_region=AWS_REGION,
        aws_session_token=response['Credentials']['SessionToken']

)
    return client



def get_text():
    st_text = st.text_input("You: ")
    return st_text


def get_response(input_message,chat_history):
    chat_history.append({"role": "user", "content": input_message})
    message = st.session_state.client.messages.create(
            model=st.session_state.MODEL_ID,
            max_tokens=256,
            messages=chat_history
        )
    chat_history.append({"role": "assistant", "content": message.content[0].text})
    for chat in chat_history:
        st.write(f"{chat['role'].capitalize()}: {chat['content']}")


if 'client' not in st.session_state:
    # Initialize the client once and store it in session stat
    st.session_state.client = getCredentials()  
    st.session_state.MODEL_ID = os.getenv('MODEL_ID')
    st.session_state.chat_history = []

user_input = get_text()



if user_input:
    get_response(user_input, st.session_state.chat_history)








