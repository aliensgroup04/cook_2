# -*- coding: utf-8 -*-
"""cooking.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EZKm1yMTM1n8IhHb5SaE6iJwGisqZORi
"""
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, ValidationError
from typing import List
import os

st.title("🍽️ AI Chef Assistant")

dish_name = st.text_input("Enter a dish name", placeholder="E.g., Pasta, Biryani")

# Define Recipe schema
class Recipe(BaseModel):
    ingredients: List[str] = Field(description="List of ingredients for the dish")
    process: List[str] = Field(description="Steps to prepare the dish")
    varieties: List[str] = Field(description="Similar dish varieties")

output_parser = PydanticOutputParser(pydantic_object=Recipe)

# Load API key securely
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro", google_api_key=os.getenv("GOOGLE_API_KEY", "AIzaSyCBhbuJbxjlghoZ3X1HQhS_qwuMpSE1wC0")
)

prompt_template = ChatPromptTemplate(
    messages=[
        ("system", """You are an AI Chef Assistant.
                      Given a dish name, provide ingredients and step-by-step instructions.
                      Format: {output_format_instructions}"""),
        ("human", "Give me the recipe for {dish_name}.")
    ],
    partial_variables={"output_format_instructions": output_parser.get_format_instructions()},
)

chain = prompt_template | model | output_parser

if st.button("Get Recipe") and dish_name:
    with st.spinner("Fetching recipe...⏳"):
        response = chain.stream({"dish_name": dish_name})
        if response:
            st.subheader("🛒 Ingredients")
            st.write("\n".join(f"- {item}" for item in response.ingredients))

            st.subheader("👨‍🍳 Preparation Steps")
            st.write("\n".join(f"{i+1}. {step}" for i, step in enumerate(response.process)))

            st.subheader("🍽️ Similar Dishes")
            st.write(", ".join(response.varieties))

st.markdown("---")
st.markdown("Chef Assistant Made by Suman", unsafe_allow_html=True)
