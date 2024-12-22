import gradio as gr
from langchain_core.messages import AIMessage, HumanMessage
from llm_response_chat import response_from_llm

# Function to handle user input and generate a response
def chatbot_interface(user_input, chat_history):
    # Ensure chat_history is initialized
    if chat_history is None:
        chat_history = []

    # Append user's message to chat history
    chat_history.append(HumanMessage(content=user_input))

    # Format the chat history for display
    formatted_history = "\n".join([
        f"User: {msg.content}" if isinstance(msg, HumanMessage) else f"Assistant: {msg.content}"
        for msg in chat_history
    ])

    # Generate assistant's response
    response = ""
    for chunk in response_from_llm(user_input, chat_history):
        response += chunk

    # Append assistant's response to chat history
    chat_history.append(AIMessage(content=response))

    # Update the chat display
    formatted_history += f"\nAssistant: {response}"

    return formatted_history, chat_history


# Create Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>Demo Chatbot</h1>")
    
    # Chatbot interface
    chatbot_display = gr.Textbox(
        label="Chat History",
        lines=20,
        interactive=False
    )
    user_input = gr.Textbox(
        label="Your Message",
        placeholder="How can I help you?",
        lines=1
    )
    submit_button = gr.Button("Send")

    # Define behavior when user submits a message
    submit_button.click(
        chatbot_interface,
        inputs=[user_input, gr.State()],  # Use gr.State to maintain chat history
        outputs=[chatbot_display, gr.State()]
    )

# Launch the Gradio app
demo.launch()
