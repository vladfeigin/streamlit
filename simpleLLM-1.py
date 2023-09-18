import streamlit as st
from langchain.llms import AzureOpenAI
import openai
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_DEPLOYMENT_ENDPOINT = os.getenv("OPENAI_DEPLOYMENT_ENDPOINT")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
OPENAI_DEPLOYMENT_VERSION = os.getenv("OPENAI_DEPLOYMENT_VERSION")

# Configure OpenAI API
openai.api_type = "azure"
openai.api_version = '2023-05-15'
openai.api_base = OPENAI_DEPLOYMENT_ENDPOINT
openai.api_key = OPENAI_API_KEY

st.title("quick start with langchain and streamlit")


def generate_response(input_text):
    
    messages = [{"role": "system", "content": "you are a user's assistant. Answering trivia questions is one of your primary functions."},
            {"role": "user", "content": f"{input_text}"}] 
    
    answer = openai.ChatCompletion.create(engine=OPENAI_DEPLOYMENT_NAME,
                                      messages=messages,)
    st.info(answer.choices[0].message.content)
  

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?',)
  st.form_submit_button('Submit')
  generate_response(text)
