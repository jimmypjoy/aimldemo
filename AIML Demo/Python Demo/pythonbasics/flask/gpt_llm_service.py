from flask import Flask, request, jsonify
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
