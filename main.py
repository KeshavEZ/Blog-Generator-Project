
#importing all the libraries
import streamlit as st
from langchain_groq import ChatGroq
import logging
import re
from collections import Counter
from langchain_community.document_loaders import UnstructuredHTMLLoader, PyPDFLoader
import pandas as pd
from dotenv import load_dotenv
import os

#loading dotenv
load_dotenv()



logging.basicConfig(level=logging.INFO)


client = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name='mixtral-8x7b-32768'
)


styles = ["Formal", "Casual", "Technical", "Persuasive"]


st.title("AI-Powered Blog Generator")


#st.sidebar.header("Blog Configuration")




topic = st.text_input("Enter the topic for the blog", "")
style = st.selectbox("Select writing style", styles)
blog_type = st.selectbox("Select blog type", ["How-to", "Listicle", "Opinion", "News"])
#Keywords = st.selectbox("Select Keywords", list(DD_data['keyword']))
user_data = st.text_input("Enter dot-dash data")


Title_length = st.text_input("Enter the number of words of the title of your blog")
total_words = st.text_input("Enter the total number of words you want in your blog")





default_EZ_content = "EZ is a global Business Support Service provider that has disrupted the traditional industry through innovation and integration of AI to modernize existing workflows and processes"

# User input for EZ_content
EZ_content = st.text_input("Enter the content related to EZ that you want me to learn.", "")


if not EZ_content:
    EZ_content = default_EZ_content

#function to generate content of the blog

def generate_content(topic, style, blog_type, user_data, EZ_content):
    prompt = f"""
    Task: Write a detailed {style} {blog_type} blog post about {topic} using {user_data} and relevant information from {EZ_content}.
    Instructions:
    The blog should be beautifully and properly formatted using markdown and should consist of {total_words} words.
    The blog title should be SEO Optimized and should consist of only {Title_length} words strictly.
    The blog title, should be crafted with the {topic} in mind and should be catchy and engaging. But not overly expressive.
    Generate a title that is concise and direct.
    """
    try:
        
        response = client.invoke(prompt)

        logging.info(f"Response: {response}")

        if hasattr(response, 'content'):
            content = response.content  
        else:
            content = f"Unexpected response structure: {response}"

        return content
    except Exception as e:
        logging.error(f"Error in content generation: {str(e)}")
        return f"An error occurred: {str(e)}"



#SEO optimization
def optimize_seo(content):
    words = re.findall(r'\w+', content.lower())
    word_count = Counter(words)
    top_keywords = [word for word, count in word_count.most_common(10) if len(word) > 5]

    if len(top_keywords) >= 3:
        meta_description = f"Discover insights on {', '.join(top_keywords[:3])} in this comprehensive {top_keywords[0]} guide."
        title = f"{top_keywords[0].capitalize()}: A Deep Dive into {' and '.join(top_keywords[1:3]).capitalize()}"
    else:
        meta_description = "SEO optimization could not be completed due to lack of keywords."
        title = "SEO title could not be generated."

    return content, {'description': meta_description, 'title': title}


def apply_terminology(content):
    
    return content



 
if st.button("Generate Blog"):
    if topic:
        
        blog_content = generate_content(topic, style, blog_type, user_data, EZ_content)

        
        if "An error occurred" in blog_content:
            st.error(blog_content)
        else:
            
            blog_content = apply_terminology(blog_content)

            
            blog_content, meta = optimize_seo(blog_content)

            
            st.subheader("Generated Blog Content")
            st.write(blog_content)

            st.subheader("SEO Optimized Metadata")
            st.write(f"Meta Title: {meta['title']}")
            st.write(f"Meta Description: {meta['description']}")
    else:
        st.error("Please enter a topic to generate the blog.")
