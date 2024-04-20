# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 18:45:51 2024

@author: User
"""

import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets[your_api])

input_prompt = """
You are a team of scientists participating in a hackathon to develop groundbreaking solutions for real-world problems. Your task is to generate innovative ideas that can have a significant positive impact on society. Consider the following problem statement:

Problem Statement: {}

Category: {}
Subfield: {}

consider providing multiple solution highlightind ideas with attractive captcha and quote related to solution mentioned by legends center aligned at top of every idea

consider having below elements detailed in every idea

article related:
    
Proposed solution:
    
Unique Selling Point:
    
feature:
    
target audiance:
    


"""

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Streamlit app

st.set_page_config(page_title="Innovative Solutions Generator",
                   page_icon=":bulb:",
                   layout="wide")
st.title(":bulb: Innovative Solutions Generator")
st.text("Enter a problem statement and receive generated ideas for groundbreaking solutions.")
problem_statement = st.text_area("Problem Statement")
# Selectbox for hardware or software
category = st.selectbox("Select Category", ["Software and Hardware","Hardware", "Software"])

# Text input for subfield
subfield = st.text_input("Enter Subfield (e.g., Cybersecurity, Machine Learning)")

submit = st.button("Submit")

if submit:
    if problem_statement:
        response = get_gemini_response(input_prompt.format(problem_statement,category,subfield))
        st.markdown("## Generated Ideas:")
        st.write(response)
    else:
        st.warning("Please enter a problem statement.")
