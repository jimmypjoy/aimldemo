from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
from langchain_core.output_parsers import StrOutputParser

#os.environ['OPENAI_API_KEY'] = 'xxxx'
def setup_environment():
    import sys
    sys.path.append('C:\\gitworkspace\\aimldemo\\jupyterworkapce')
    import stratup_env_setup
    stratup_env_setup.set_env()

setup_environment()

llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.7)
output_parser = StrOutputParser()

def response_from_llm(user_question, chat_history):
    template_chat = '''
    You are a helpful assistant, answer the following questions considering the history of the conversation as well:

    Chat history: {chat_history}
    User question: {user_question}
    '''

    prompt = ChatPromptTemplate.from_template(template_chat)
    chain = prompt | llm | output_parser

    return chain.stream({'chat_history': chat_history, 'user_question': user_question})
