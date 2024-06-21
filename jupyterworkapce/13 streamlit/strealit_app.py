import streamlit as st
import pandas as pd

# Title of the app
st.title("Hello, Streamlit!")

st.write("Test message")

st.markdown("""
    # Test message
    """)

# Input widgets
name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=1, max_value=100)

# Display the input
if st.button("Submit"):
    st.write(f"Hello {name}, you are {age} years old!")

df = pd.DataFrame({
    'first_column':[1,2,3,4],
    'second_column': [10,20,30,40]
})

st.write(df)