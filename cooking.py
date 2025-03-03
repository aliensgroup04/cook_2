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

class Recipe(BaseModel):
    ingredients: List[str] = Field(description="List of ingredients for preparing the dish")
    process: List[str] = Field(description="Steps to follow for preparing the dish")
    varieties: List[str] = Field(description="List of names of similar varieties to that dish")
# Output parser
output_parser = PydanticOutputParser(pydantic_object=Recipe)

model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyCBhbuJbxjlghoZ3X1HQhS_qwuMpSE1wC0")

# Prompt Template
prompt_template = ChatPromptTemplate(
    messages=[
        (
            "system",
            """You are a helpful AI Chef Assistant.
            Given a dish name by the user, you provide the process of preparation step by step along with ingredients.
            Output Format Instructions:
            {output_format_instructions}""",
        ),
        ("human", "Give me the recipe and step-by-step instructions for cooking {dish_name}."),
    ],
    partial_variables={
        "output_format_instructions": output_parser.get_format_instructions()
    },
)

# Chain definition
chain = prompt_template | model | output_parser

# Streamlit UI
st.title("🍽️ AI Chef Assistant")

dish_name = st.text_input("Enter a dish name", placeholder="E.g., Pasta, Biryani")

if st.button("Get Recipe") and dish_name:
    st.subheader(f"🍽️ Recipe for {dish_name}")
    
    with st.spinner("Fetching recipe...⏳"):
        recipe_container = st.empty()  # Placeholder to update the response
        
        # Stream response
        recipe = None
        for chunk in chain.stream({"dish_name": dish_name}):
            if isinstance(chunk, Recipe):
                recipe = chunk
                break  # Stop when full recipe is received

        # Display the recipe
        if recipe:
            recipe_container.subheader("🥕 Ingredients:")
            recipe_container.markdown("\n".join(f"- {i}" for i in recipe.ingredients))

            recipe_container.subheader("👨‍🍳 Preparation Steps:")
            recipe_container.markdown("\n".join(f"{idx + 1}. {step}" for idx, step in enumerate(recipe.process)))

            if recipe.varieties:
                recipe_container.subheader("🍽️ Similar Varieties:")
                recipe_container.markdown("\n".join(f"- {v}" for v in recipe.varieties))

st.markdown("---")
st.markdown("Chef Assistant Made by Suman", unsafe_allow_html=True)
