import os
import requests

# Setup environment for API key or other configurations
def setup_environment():
    import sys
    sys.path.append('C:\\gitworkspace\\aimldemo\\jupyterworkapce')
    import stratup_env_setup
    stratup_env_setup.set_env()

setup_environment()

def response_from_llm(user_question, chat_history):
    # Convert chat_history to a list of plain strings (content only)
    serialized_chat_history = [
        message.content if hasattr(message, 'content') else str(message)
        for message in chat_history
    ]

    # Prepare the input data for the REST endpoint
    payload = {
        "chathistory": serialized_chat_history,
        "context": "You are a helpful assistant, answer the following questions considering the history of the conversation as well.",
        "question": user_question,
        "answer": ""  # Empty while querying
    }

    # Log the input to the REST endpoint
    print("Input to Flask REST API:\n", payload)

    # Make a POST request to the LLM REST endpoint
    try:
        response = requests.post("http://127.0.0.1:5000/", json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print("Error calling Flask REST API:", e)
        return "An error occurred while communicating with the Flask service."

    # Parse the response
    response_data = response.json()
    print("Response from Flask REST API:\n", response_data)

    # Return the answer field from the response
    return response_data.get("answer", "No answer provided.")
