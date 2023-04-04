import streamlit as st
import tiktoken
import openai
from dotenv import load_dotenv
import os
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Load environment variables
load_dotenv()

# Configure Azure OpenAI Service API
openai.api_type = "azure"
openai.api_version = "2022-12-01"
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_key = os.getenv("OPENAI_API_KEY")

COMPLETION_MODEL = 'text-davinci-003'

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(10))
def run_prompt(prompt, max_tokens=1000):
    response = openai.Completion.create(
        engine=COMPLETION_MODEL,
        prompt=prompt,
        temperature=0.7,
        max_tokens=max_tokens
    )
    return response['choices'][0]['text']

# configure UI elements with Streamlit

st.title('Email summarization demo app')
email = st.text_area('Email', height=400)
summarize_button = st.button('Summarize email')
answer_button = st.button('Generate answer')

if summarize_button:
    prompt = f"""
    Email:
    {email}
    Please summarize the email.
    Summary:"""
    summary = run_prompt(prompt)
    
    st.write('Summary:')
    st.write(summary)
    
if answer_button:
    prompt = f"""
    Email:
    {email}
    Please generate an answer to the email above.
    Answer:"""
    answer = run_prompt(prompt)

    st.write('Answer:')
    st.write(answer)