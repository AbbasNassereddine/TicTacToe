# Tic Tac Toe Bot with Streamlit

By: Abbas NAssereddine
For: Tech Tank Team


This project implements a Tic Tac Toe bot using Streamlit, OpenAI, and AWS Bedrock services. The bot can play Tic Tac Toe in two modes: `Human` (interaction with a user) and `Auto` (interaction between two AI models).

## Features

- **Human Mode**: Interact directly with the bot to play Tic Tac Toe.
- **Auto Mode**: Alternate gameplay between Bedrock and GPT models.
- **Dynamic Icons**: Replace symbols (e.g., `X` and `O`) with SVG-based shapes rendered as images.
- **Game Validation**: Automatically checks for game victory conditions, to deterministically confirm victory and prevent overreliance on bot to determine game outcome.

## Setup Instructions

### Prerequisites

1. **Python 3.8+**
2. **Streamlit**: For building the web application.
3. **AWS Credentials**: Required for Bedrock integration.
4. **OpenAI API Key**: For ChatGPT integration.
5. **TT.env File**: Contains environment variables for AWS and OpenAI credentials.

### Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file named `TT.env` in the project root with the following variables:
   ```env
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_REGION=your_aws_region
   OPENAI_API_KEY=your_openai_api_key
   ```

### Running the Application

Start the Streamlit app by running:

```bash
streamlit run app.py
```

## Code Structure

### Key Functions

#### Credential Management

- **`getCredentialsBedrock()`**: Retrieves AWS Bedrock credentials using `boto3` and sets up the Anthropic Bedrock client.
- **`getCredentialsGPT()`**: Initializes the OpenAI client with the API key.

#### Chat Handling

- **`get_chatgpt_response()`**: Retrieves a response from ChatGPT using OpenAI.
- **`get_bedrock_response()`**: Retrieves a response from Bedrock using the Anthropic client.

#### Icon Generation

- **`icon_style(input)`**: Generates icons using OpenAI's DALL-E model.
- **`icon_bedrock(input, client)`**: Generates icons using Bedrock's Stability AI.

### Session State Initialization

The application initializes session state variables for:

- `client1` and `client2`: GPT and Bedrock clients.
- `icon1` and `icon2`: User-selected icons for `X` and `O`.
- `chat_history`: Stores conversation history.
- `mode`: Tracks the selected mode (`Human` or `Auto`).

### Game Modes

#### Human Mode

- Displays chat history.
- Replaces `X` and `O` with SVG icons.
- Accepts user input and interacts with the bot.
- Validates game outcomes.

#### Auto Mode

- Alternates gameplay between Bedrock and GPT models.
- Tracks responses from both models.
- Validates game outcomes.

### Passing Instructions to Anthropic in the form of a first user prompt without explicitly displaying the prompt

As the Anthropic Chat Completion APi lacks an explicit "system"role, these instructions can be given in the form of a user payload that cna be potentially run only in the back end without displaying to front-end as follows:

 ```
st.session_state.chat_history = []
    st.session_state.chat_history.append({
            "role": "user",
            "content": 'Introduce yourself as a bot that plays Tic Tac Toe.  Display the board in a 3x3 grid.' 
        })
st.markdown("### Chat:")
    for chat in st.session_state.chat_history[1:]

 ```


#### Game Validation and Outcome Testing

- **`check_victory(chat)`**: Validates the Tic Tac Toe board to determine if a player has won.
Game Validation: Regex Extraction in Detail
The game validation function uses regex to extract and process the game state from the bot's response. Here's a breakdown of how this works:

   ##### Regex to Extract Symbols and Numbers:
   
   The regex pattern r'X|O|[0-9]' is used to match:
   X: Represents one player's moves.
   O: Represents the other player's moves.
   [0-9]: Represents available positions on the board.
   This ensures only valid characters relevant to the Tic Tac Toe game are extracted from the bot's response.
   
   Example Input and Output:
   
   Input Bot Response:
   "X | O | 3
    4 | X | 6
    O | 8 | 9"
   Regex Output:
   ['X', 'O', '3', '4', 'X', '6', 'O', '8', '9']
   Filter and Limit Data:
   
   Remove Unnecessary Characters: After extraction, the list excludes spaces and grid symbols like | or newlines.
   Limit to First 9 Items: Ensures only the first 9 valid positions (corresponding to the 3x3 board) are retained.
   Final List Example:
   ['X', 'O', '3', '4', 'X', '6', 'O', '8', '9']
   Determine Player Moves:
   
   Indices of X: Find the positions where X is present, converted to a set of indices.
   Example: {1, 5}
   Indices of O: Find the positions where O is present, converted to a set of indices.
   Example: {2, 7}
   These indices represent the board positions occupied by each player.
   Validate Against Winning Combinations:
   
   The function checks if any predefined winning combination (rows, columns, or diagonals) is a subset of the X or O indices.
   Example Winning Combination: {1, 5, 9} (Diagonal)
   If a match is found, the game is declared won by the corresponding player.



## Example SVG Icons

- **Triangle Icon**:

  
![image](https://github.com/user-attachments/assets/ef14d224-63f4-498d-99f1-710ee028fea0)


- **Red Circle Icon**:
  ```
  data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTAiIGhlaWdodD0iNTAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHNpcmNsZSBjeD0iMjUiIGN5PSIyNSIgcj0iMjAiIGZpbGw9InJlZCIgLz48L3N2Zz4=
  ```

## **Dependencies**

- `streamlit`: For UI rendering.
- `boto3`: For AWS integration.
- `anthropic`: For Bedrock API integration.
- `openai`: For OpenAI API integration.
- `Pillow`: For image processing.
- `requests`: For handling HTTP requests.
- `dotenv`: For managing environment variables.
- `re`: For regex operations.
- `base64`: For encoding SVG icons.


## How It Works

1. **Human Mode**: Users interact with the bot, inputting moves. The bot processes responses and displays the updated board.
2. **Auto Mode**: Bedrock and GPT bots take turns until a winner is determined or the board is full.
3. **Icons**: Customizable SVG-based shapes are used to replace `X` and `O` on the board.
4. **Game Validation and Testing**: Ensures that the game is correctly won based on Tic Tac Toe rules.

## What Can be Improved

1. Incorporate icons instesad of X and Os, however, markdown does not support generating inside preformatted blocks.Also, image generation in-text lead to slow run time
2. Improve UI
3. Offer more choice to user

## Future Enhancements

- Use DALLE library to generate custom icons to replace standard X and O
- Deployment of the function_app.py to Cloud Functions (eg: Azure Functions)
- Incorporate CI/CD

