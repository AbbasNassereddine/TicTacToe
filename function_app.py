from dotenv import load_dotenv
import os
import boto3
import streamlit as st
import pandas as pd
from anthropic import AnthropicBedrock 
from openai import OpenAI


openai_api_key = os.getenv('OPENAI_API_KEY')

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



def getCredentialsGPT():
    load_dotenv(dotenv_path=r'TT.env')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(

        api_key=openai_api_key
    )
    return client

def get_text():
    st_text = st.text_input("You: ")
    return st_text


def get_chatgpt_response(input_message, chat_history,icon1,icon2):
    # Append the user's message to the chat history
    chat_history.append({"role": "user", "content": input_message})
    
    # Make the API call to get the assistant's response
    response = st.session_state.client.chat.completions.create(
        model="gpt-4",  # Specify the model (e.g., "gpt-4" or another available model)
        messages=chat_history  # Directly pass the entire chat history
    )
    
    # Extract the assistant's message from the API response
    #assistant_message = # Assuming 'response' is the result of the API call
    assistant_message = response.choices[0].message.content

    
    # Append the assistant's message to the chat history
    chat_history.append({"role": "assistant", "content": assistant_message})
    
    # Display the entire chat history
    for chat in chat_history:
        st.write(f"{chat['role'].capitalize()}: {chat['content']}")



def get_bedrock_response(input_message,chat_history):
    chat_history.append({"role": "user", "content": input_message})
    message = st.session_state.client.messages.create(
            model=st.session_state.MODEL_ID,
            max_tokens=256,
            messages=chat_history
        )
    chat_history.append({"role": "assistant", "content": message.content[0].text})
    for chat in chat_history:
        st.write(f"{chat['role'].capitalize()}: {chat['content']}")

def icon_style (input):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content":'generate the svg code only of a '+input+' icon to be used in a tic tac tow game' }
        ]
    )
    return response.choices[0].message.content        


if 'client' not in st.session_state:
    st.session_state.icon2=''
    st.session_state.icon1=''
    # Initialize the client once and store it in session state
    st.session_state.client = getCredentialsGPT()  
    st.session_state.MODEL_ID = os.getenv('MODEL_ID')
    st.session_state.chat_history = []
    st_text = st.text_input("Choose  the first icon: ")
    st.session_state.icon1=icon_style (input)
    st_text = st.text_input("Choose  the second icon: ")
    st.session_state.icon2=icon_style (input)








user_input = get_text()
if user_input:
    get_chatgpt_response(user_input, st.session_state.chat_history,st.session_state.icon1,st.session_state.icon2)







