from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.schema.output_parser import StrOutputParser
import os
from my_key import openai_key

prompt  = """

Explain briefly about {topic} in {language}

"""

prompt_temp = PromptTemplate.from_template(prompt)

inputs = [("Trekking","English"),("Metaphysics","Hindi")]

prompts = [prompt_temp.format(topic=t,language=l) for t, l in inputs]
print(prompts)

os.environ['OPENAI_API_KEY'] = openai_key

llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.7)

responses = llm.map().invoke(prompts)

print(responses)

for rs in responses:
    print(rs.content)
    print("*"*100)

from langchain_core.prompts import ChatPromptTemplate
prompt  = """
Explain briefly about {topic}.
"""
chat_prompt = ChatPromptTemplate.from_template(prompt)
print(chat_prompt)

topics = ['Astrology','Metaphysics', 'Quantum Computing']
prompts = [chat_prompt.format(topic = t) for t in topics]
print(prompts)

responses2  = llm.map().invoke(prompts)

for res in responses2:
    print(res.content)
    print('%&'*100)

messages = [
    ("system", "Act as an expert in real estate and provide brief answers"),
    ("human", "what is your name?"),
    ("ai", "my name is AIBot"),
    ("human", "{user_prompt}")
]

chat_template = ChatPromptTemplate.from_messages(messages)

text_prompts = ["What is your name?","explain commercial real estate to me"]

chat_prompts = [chat_template.format(user_prompt=p) for p in text_prompts]

print(chat_prompts)

responses = llm.map().invoke(chat_prompts)

for r in responses:
    print(r.content)
    print('!$'*100)




