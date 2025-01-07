import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
#print(api_key)
#input("Enter your name: ")
#lansmith Tracking
os.environ["LANGCHAIN_API_KEY"] =os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot with OPENAI"

# prompt template

prompt=ChatPromptTemplate.from_messages(
    [
     ("system", "You are a helpful assistsnt. Please respond to the user queries"),
     ("user", "Question:{question}")
    ]
)

def get_response(question, api_key, llm,temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm)
    output_parser = StrOutputParser()
    chain=prompt | llm | output_parser
    answer=chain.invoke({"question":question})
    return answer

## Title of the app
st.title('Simple Q&A Chatbot with OPENAI')

## sidebar for settings
st.sidebar.title('Settings')
#api_key = st.sidebar.text_input('Enter your Open AI API Key', type='password')

# dropdown for selecting the model
llm = st.selectbox('Select the model', ['gpt-3.5-turbo', 'gpt-4o', 'gpt-4'])

temperature = st.sidebar.slider('Temperature', 0.0, 1.0, 0.5)
max_tokens = st.sidebar.slider('Max Tokens', 1, 200, 50)


st.write("You can ask your questions here")
user_input = st.text_input("You:")
if user_input:
    response = get_response(user_input, api_key, llm,temperature, max_tokens)
    st.write(response)
else:
    st.write("Please enter your question")
