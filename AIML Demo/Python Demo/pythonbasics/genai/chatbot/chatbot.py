import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from llm_response_chat import response_from_llm

st.title('Demo Chatbot')

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display the conversation history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# User input
user_input = st.chat_input("How can you help?")

if user_input is not None and user_input != '':
    # Append the user's message to the chat history
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    # Placeholder for assistant's response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        # Stream the assistant's response
        for chunk in response_from_llm(user_input, st.session_state.chat_history):
            full_response += chunk
            placeholder.markdown(full_response)

        # Append the assistant's message to the chat history
        st.session_state.chat_history.append(AIMessage(content=full_response))
