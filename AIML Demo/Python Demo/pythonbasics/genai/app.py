import streamlit as st
from langchain_dep import run_chain

st.title('Your own Business-idea-Generator')

input_text1 = st.text_input('Write your topic of interest')
input_text2 = st.text_input('And your skills')
input_text3 = st.text_input('do you mind sharing your hobbies :)')
input_text4 = st.text_input('which part of this world you want to try your hand on')
n_ideas = st.slider('No of ideas', 1, 10)

if st.button('Generate ideas'):
    if input_text1 and input_text2 and input_text3 and input_text4:
        ideas = run_chain(input_text1,input_text2,input_text3,input_text4,n_ideas)
        st.write("Here are your business ideas:")
        st.write(ideas)

    else:
        st.warning("Please check if you missed any required information")
