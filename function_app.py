from dotenv import load_dotenv
import os
import boto3
import streamlit as st
import pandas as pd
from anthropic import AnthropicBedrock
from openai import OpenAI
from PIL import Image
import re
import base64
import requests

# Convert an image URL to base64
def convert_image_to_base64(image_url):
    response = requests.get(image_url)
    image_data = response.content
    return base64.b64encode(image_data).decode('utf-8')


# Load OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

# Get credentials for Bedrock
def getCredentialsBedrock():
    load_dotenv(dotenv_path=r'TT.env')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION')
    
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

# Get credentials for GPT
def getCredentialsGPT():
    load_dotenv(dotenv_path=r'TT.env')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=openai_api_key)
    return client

# Get user input text
def get_text():
    st_text = st.text_input("You: ")
    return st_text

# Get ChatGPT response
def get_chatgpt_response(chat_history, model_id):
    response = st.session_state.client1.chat.completions.create(
        model=model_id,
        messages=chat_history
    )
    assistant_message = response.choices[0].message.content
    return assistant_message

# Get Bedrock response
def get_bedrock_response(chat_history):
    response = st.session_state.client2.messages.create(
        model=st.session_state.MODEL_ID,
        max_tokens=256,
        messages=chat_history
    )
    assistant_message = response.content[0].text
    return assistant_message

# Generate an icon using OpenAI's DALL-E
def icon_style(input):
    client = OpenAI(api_key=openai_api_key)
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"A small and simple {input} icon",
        quality="standard",
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    return image_url

# Generate an icon using Bedrock
def icon_bedrock(input, client):
    response = client.invoke_model(
        model="stability-ai.stable-diffusion",
        prompt=input
    )
    return response["body"].read()


def check_victory(chat):
    # Extract X, O, and numbers using regex
    outcome_list = re.findall(r'X|O|[0-9]', chat)
    
    # Remove spaces and unwanted characters
    outcome_list = [i for i in outcome_list if i not in [' ', '|']]
    
    # Limit to the first 9 positions (Tic Tac Toe board size)
    outcome_list = outcome_list[:9]
    
    # Get indices of X and O
    indices_of_X = {str(index + 1) for index, value in enumerate(outcome_list) if value == 'X'}
    indices_of_O = {str(index + 1) for index, value in enumerate(outcome_list) if value == 'O'}
    
    # Define winning combinations
    winning_combinations = [
        {"1", "2", "3"},  # Top row 1,23
        {"4", "5", "6"},  # Middle row
        {"7", "8", "9"},  # Bottom row
        {"1", "4", "7"},  # Left column
        {"2", "5", "8"},  # Middle column
        {"3", "6", "9"},  # Right column
        {"1", "5", "9"},  # Diagonal from top-left
        {"3", "5", "7"},  # Diagonal from top-right
    ]
    
    # Check if X or O combinations are inclcued in the winning combinations defined above
    for combo in winning_combinations:
        if combo.issubset(indices_of_X):
            result= "Correct. Game is won by X."
            break
        if combo.issubset(indices_of_O):
            result= "Correct. Game is won by O."
            break
        else:
            result="Are you sure the game has been won?"
    return result    




# Initialize session state variables and ensure variable are initialized only when the code first runs and not on subsequent runs of the bot
if 'client1' not in st.session_state or 'client2' not in st.session_state:
    st.session_state.icon1 = ''
    st.session_state.icon2 = ''
    st.session_state.client1 = getCredentialsGPT() # GPT credentials
    st.session_state.client2 = getCredentialsBedrock() # Bedrock credentials
    st.session_state.MODEL_ID = os.getenv('MODEL_ID')
    st.session_state.chat_history = []
    st.session_state.chat_history.append({
            "role": "user",
            "content": 'Introduce yourself as a bot that plays Tic Tac Toe.  Display the board in a 3x3 grid.' 
        })

if 'mode' not in st.session_state:
    st.session_state.mode = ''

# Mode Choice in Markdown
st.markdown("### Choose Your Mode")
mode_prompt = st.selectbox("Choose the mode you would like to:", ["Select Mode", "Auto", "Human"])

# Update session state for mode selection
if mode_prompt != "Select Mode":
    st.session_state.mode = mode_prompt

# Display selected mode
if st.session_state.mode:
    st.write(f"You selected: {st.session_state.mode}")
else:
    st.warning("Please select a mode to continue.")

# Human mode handling
if st.session_state.mode == 'Human':
    # Display chat history
    st.markdown("### Chat:")
    for chat in st.session_state.chat_history[1:]:
        if chat["role"] == "user":
            st.markdown(f"**You**: {chat['content']}")
        elif chat["role"] == "assistant":
            triangle_svg_base64 = (
                "PHN2ZyB3aWR0aD0iNTAiIGhlaWdodD0iNTAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPHBvbHlnb24gcG9pbnRzPSIyNSwwIDUwLDUwIDAsNTAiIHN0eWxlPSJmaWxsOmJsdWU7c3Ryb2tlOmJsYWNrO3N0cm9rZS13aWR0aDoxIiAvPgo8L3N2Zz4="
            )
            circle_svg_base64 = (
                "PHN2ZyB3aWR0aD0iNTAiIGhlaWdodD0iNTAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPHBvbHlnb24gcG9pbnRzPSIyNSwwIDUwLDUwIDAsNTAiIHN0eWxlPSJmaWxsOmJsdWU7c3Ryb2tlOmJsYWNrO3N0cm9rZS13aWR0aDoxIiAvPgo8L3N2Zz4="
            )
            # Replace 'X' with the triangle icon
            content_with_icon = chat["content"].replace(
                "X",
                f'<img src="data:image/svg+xml;base64,{triangle_svg_base64}" alt="Triangle Symbol" width="20"/>',
            )
            st.markdown(f"**Bot**: {content_with_icon}", unsafe_allow_html=True)

    # Take user input
    user_input = st.text_input("Enter your message:")
    if user_input:
        # Append user input to chat history with instructions for the bot
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input 
        })

        # Get bot response
        bot_response = get_bedrock_response(st.session_state.chat_history)

        # Append bot response to chat history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": bot_response
        })

        # Display bot response
        st.markdown("### Bot says:")
        st.write(bot_response)

        # Use def check victory to validate that the game has actually been won or not
        if 'game is won' in bot_response.lower():
            st.markdown("### Game Over!")
            game_status = check_victory(bot_response)
            st.markdown(game_status)

# Auto mode
if st.session_state.mode == "Auto":
    user_input = "Play tic tac toe"
    if user_input:
        bot1_chat_history = [{"role": "user", "content": "Play tic tac toe. Display the board clearly. Ask the user to just answer with the number of the position of your choice in it without other text. Display the board in a 3x3 grid only once when you answer. So not tell me what I chose. You will play as X. Provide available numbers to use. Once a player wins also mention: 'Game is won !'"}]
        bot2_chat_history = [{"role": "user", "content": "We are playing tic tac toe. Always just answer with the number of the position of your choice in it without other text. You will play as O."}]

        bot1_response = get_bedrock_response(bot1_chat_history)
        if bot1_response:
            st.markdown("### Bot 1 (Bedrock) says:")
            st.markdown(bot1_response)
        else:
            st.warning("Bot 1 did not respond.")
            st.stop()

        for _ in range(5):

            bot2_response = get_chatgpt_response(bot2_chat_history, "gpt-3.5-turbo")
            if bot2_response:
                bot1_chat_history.append({"role": "assistant", "content": bot1_response})
                bot1_chat_history.append({"role": "user", "content": bot2_response})
                st.markdown("### Bot 2 (ChatGPT) says:")
                st.write(bot2_response)
            else:
                st.warning("Bot 2 did not respond.")
                break

            bot1_response = get_bedrock_response(bot1_chat_history)
            if bot1_response:
                bot2_chat_history.append({"role": "assistant", "content": bot2_response})
                bot2_chat_history.append({"role": "user", "content": bot1_response})
                st.markdown("### Bot 1 (Bedrock) says:")
                st.write(bot1_response)
            else:
                st.warning("Bot 1 did not respond.")
                break
            if 'game is won' in bot1_response.lower():
                bot1_chat_history.append({"role": "user", "content": check_victory(bot1_response)})
                st.markdown("### Bot 2 says:")
                st.markdown(check_victory(bot1_response.lower()))
                bot1_response = get_bedrock_response(bot1_chat_history)
                st.markdown(bot1_response)
   