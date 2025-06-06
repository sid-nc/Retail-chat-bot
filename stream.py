import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pymysql
import os
import re

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyCZZpqO2AYGJXMAzN9b8aHvUuLb1Cog2PE") 

password = quote_plus("Sqled@2611")

try:
    engine = create_engine(f"mysql+pymysql://root:{password}@localhost:3306/atliq_tshirts")
    db = SQLDatabase(engine)
    st.success("Database connection successful.")
except Exception as e:
    st.error(f"Database connection failed: {e}")
    exit()

try:
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",
        google_api_key=GOOGLE_API_KEY
    )
    st.success("Google Gemini AI initialized successfully")
except Exception as e:
    st.error(f"Google Gemini AI initialization failed: {e}")
    exit()

sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

st.title("Gen AI Project")

user_query = st.text_input("Enter your query about stock:")

if user_query:
    try:
        sql_response = sql_chain.invoke({"query": user_query})
        
        

        if "result" in sql_response:
            result_string = sql_response["result"]
            
            match = re.search(r'\d+', result_string)
            if match:
                stock_count = match.group() 
                st.success(f"{stock_count} ")
            else:
                st.warning("No stock quantity found in the result.")
        else:
            st.warning("No result found.")
    except Exception as e:
        st.error(f"Error executing query: {e}")
else:
    st.warning("Please enter a valid query to get the result.")
