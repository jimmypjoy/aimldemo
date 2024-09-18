import streamlit as st
import pandas as pd
from pathlib import Path
import os

# Title of the app
st.title("Hello, Streamlit!")

# Set the folder where the file will be saved
output_folder = r"C:\Users\jimmy\OneDrive\Desktop\temp"

st.write("streamlit version = {}".format(st.__version__))

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

# Create a file uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Display the uploaded file name
    st.write("Uploaded File:", uploaded_file.name)

    # Save the uploaded file to the output folder
    output_path = os.path.join(output_folder, uploaded_file.name)
    with open(output_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write(f"File successfully saved to {output_path}")
else:
    st.write("Please upload a PDF file.")