from flask import Flask, request, jsonify
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
import json

app = Flask(__name__)

# Setup environment for API key or other configurations
def setup_environment():
    import sys
    sys.path.append('C:\\gitworkspace\\aimldemo\\jupyterworkapce')
    import stratup_env_setup
    stratup_env_setup.set_env()

setup_environment()

# Initialize the OpenAI model
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

@app.route("/", methods=["POST"])
def process_request():
    try:
        # Parse the JSON input
        data = request.get_json()
        chat_history = data.get("chathistory", [])
        context = data.get("context", "")
        question = data.get("question", "")

        # Ensure all fields are provided
        if not context or not question:
            return jsonify({"error": "Missing required fields: 'context' or 'question'"}), 400

        # Create the prompt
        template = """
        {context}
        
        Chat history:
        {chat_history}
        
        User question: {question}
        """
        formatted_prompt = PromptTemplate.from_template(template).format(
            context=context, chat_history="\n".join(chat_history), question=question
        )

        # Get response from LLM
        response = llm.predict(formatted_prompt)

        # Return the response
        return jsonify({
            "chathistory": chat_history,
            "context": context,
            "question": question,
            "answer": response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/split_query", methods=["POST"])
def split_metadata_and_query():
    """
    Splits the user's question into metadata (only file_name and page_number) and the actual query using GPT-3.5.
    """
    try:
        # Parse the JSON input
        data = request.get_json()
        user_question = data.get("question", "")
        print("user_question:", user_question)

        if not user_question:
            return jsonify({"error": "Missing required field: 'question'"}), 400

        # Create the prompt for metadata extraction
        split_prompt = """
        You are an assistant that helps split a user's question into metadata and a text query.
        Metadata should only include the fields "file_name" and "page_number".
        Return the metadata as a valid JSON object and the remaining text query separately.

        User question: "{user_question}"

        Extracted Metadata (JSON format with only file_name and page_number fields):
        Remaining Query:
        """
        formatted_split_prompt = PromptTemplate.from_template(split_prompt).format(
            user_question=user_question
        )

        print("%" * 50)
        print("formatted_split_prompt:", formatted_split_prompt)

        # Get response from LLM
        response = llm.predict(formatted_split_prompt)

        print("response:", response)

        # Debugging: Check if response contains "\n\n"
        print("Checking response split by '\\n\\n'...")
        response_parts = response.split("\n\n")
        print("response_parts:", response_parts)

        if len(response_parts) < 2:
            raise ValueError("Response format is incorrect. Expected two parts separated by double newline.")

        metadata_str = response_parts[0].strip()
        print("metadata_str (before JSON parsing):", metadata_str)

        remaining_query = response_parts[1].split(":", 1)[1].strip().strip('"')
        print("remaining_query:", remaining_query)

        # Convert metadata to a dictionary
        metadata = json.loads(metadata_str)
        print("metadata:", metadata)

        # Return the response
        response_json = {"question": user_question, "metadata": metadata, "query": remaining_query}
        print("Response JSON:", response_json)
        return jsonify(response_json)

    except Exception as e:
        print("Exception caught:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
