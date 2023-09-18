import streamlit as st
import os, pathlib, time
from io import BytesIO
from PIL import Image, ImageDraw

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv
import openai

import logging

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

logging.basicConfig(filename='applog.log', level=logging.INFO)

#computer vision configuration
COMPUTER_VISION_ENDPOINT = os.getenv("COMPUTER_VISION_ENDPOINT")
COMPUTER_VISION_KEY = os.getenv("COMPUTER_VISION_KEY")

#init computer vision client
client = ComputerVisionClient(endpoint=COMPUTER_VISION_ENDPOINT, credentials=CognitiveServicesCredentials(COMPUTER_VISION_KEY))

#allowed file extensions for upload(receipts)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp'}

#systen prompt for openai
system_template = '''You are company financial department assistant. Your main task is to summarize the receipts.
The summary must contain all common information required for expense reimbursement.
More specifically is should contain the following information:
1. Date of the receipt
2. Vendor derails: name, address, phone number, all other information that can be useful
3. Transaction details: total amount, currency, payment method, last 4 digits of the card, date of the transaction, transaction ID, service description
If some of the information is missing, please indicate that it is missing.
Output result as python json object with the fields listed above.
'''
st.title("Expenses Submission Copilot")

uploaded_file = st.file_uploader("Upload your receipt", type=ALLOWED_EXTENSIONS)

# Call Azure OCR API
if uploaded_file: 
  result = client.recognize_printed_text_in_stream(uploaded_file)  
  bag_of_words = [word.text for region in result.regions for line in region.lines for word in line.words]
  ocr_text = " ".join(bag_of_words)

      
  messages = [{"role": "system", "content": f"{system_template}"},
            {"role": "user", "content": f"{ocr_text}"}] 
    
  answer = openai.ChatCompletion.create(engine=OPENAI_DEPLOYMENT_NAME,
                                      messages=messages,)
  
  st.header("Receipt summary",divider=True)
  #st.info( answer.choices[0].message.content)
  st.json(answer.choices[0].message.content)
  #st.markdown( "#### " + answer.choices[0].message.content)
  
