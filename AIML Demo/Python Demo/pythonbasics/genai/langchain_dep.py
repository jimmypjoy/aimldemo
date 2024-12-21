from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
import os

def setup_environment():
    import sys
    sys.path.append('C:\\gitworkspace\\aimldemo\\jupyterworkapce')
    import stratup_env_setup
    stratup_env_setup.set_env()

setup_environment()

template = """
You are an AI assistant helping a user come up with business ideas based on interest, skills, and geography.

Information provided by the user:

1. Topic of interest: {input_text1}
2. Skills or expertise: {input_text2}
3. Hobbies: {input_text3}
4. Geography: {input_text4}
5. Number of ideas: {n_ideas}

Based on the above information, generate {n_ideas} detailed and innovative business ideas that align with user inputs. Make sure the generated output is relevant to the provided information.
"""

prompt = PromptTemplate(template=template, input_variables=['input_text1', 'input_text2', 'input_text3', 'input_text4', 'n_ideas'])

# Initialize ChatOpenAI correctly
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

output_parser = StrOutputParser()

def run_chain(input_text1, input_text2, input_text3, input_text4, n_ideas):
    chain = prompt | llm | output_parser
    return chain.invoke({
        'input_text1': input_text1,
        'input_text2': input_text2,
        'input_text3': input_text3,
        'input_text4': input_text4,
        'n_ideas': n_ideas
    })
