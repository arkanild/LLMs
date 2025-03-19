#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install -qqq markdownify --progress-bar off


# In[ ]:


pip install -qqq pypdf --progress-bar off


# In[ ]:


pip install -qqq transformers --progress-bar off


# In[ ]:


pip install -qqq huggingface_hub --progress-bar off


# In[ ]:


pip install -qqq reportlab --progress-bar off


# In[ ]:


pip install -qqq --upgrade transformers


# In[ ]:


pip install -qqq pandas


# In[ ]:


pip install -qqq markdown --progress-bar-off


# In[ ]:


pip install -qqq torch


# In[ ]:


pip install -qqq requests


# In[ ]:


import os
import pypdf
import requests
import pandas as pd
from markdownify import markdownify
import markdown
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from huggingface_hub import InferenceClient
import warnings
warnings.filterwarnings("ignore")


# In[ ]:


# Get Hugging Face API token from environment variable
HF_TOKEN = "<your hugging face token>"  # Replace with your actual token


# In[ ]:


def pdf_to_markdown(pdf_path):
    """Converts a PDF resume to Markdown format and stores it in a Pandas DataFrame."""
    text = ""
    
    with open(pdf_path, "rb") as pdf_file:
        reader = pypdf.PdfReader(pdf_file)
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n\n"
    
    markdown_text = markdownify(text)
    df = pd.DataFrame({"Markdown_Resume": [markdown_text]})
    return df


# In[ ]:


#checking the model before prompting it
# client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=HF_TOKEN)
# client = InferenceClient(model="Qwen/QwQ-32B", token = HF_TOKEN)

# test_response = client.text_generation("You are a resume optimiser", max_new_tokens=50)
# print(test_response)


# In[ ]:


def rewrite_resume(markdown_resume, job_description, hf_token):
    """Uses Hugging Face Inference API to optimize the resume while keeping its format intact."""
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    SYSTEM_PROMPT = """
    You are an AI assistant specialized in providing helpful, detailed, and polite answers. 
    Your task is to **rewrite resumes** to align with job descriptions while strictly maintaining the original format.
    - Identify important keywords and skills from the job description and integrate them naturally into the resume.
    - Modify experience and skills sections to highlight achievements relevant to the job description.
    - Remove or downplay less relevant details while keeping the resume structure intact.
    - Ensure strong action-oriented language and quantified achievements where possible.
    - Preserve proper Markdown formatting in the updated resume.
    """.strip()

    prompt = f"""[INST] <<SYS>>
    {SYSTEM_PROMPT}
    <</SYS>>

    Here is a resume:
    {markdown_resume}

    And here is the job description:
    {job_description}

    Please optimize the resume to match the job description while keeping its original format.
    [/INST]"""

    
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 2048, "temperature": 0.7, "do_sample": True}}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        output = response.json()
        print("\n=== AI Response ===\n", output[0]["generated_text"])  # Debugging step
        return output[0]["generated_text"].strip()
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")


# In[ ]:


# Example usage
pdf_path = "actual_resume.pdf"  # Replace with your PDF file path
df = pdf_to_markdown(pdf_path)
job_desc = """About the Role
As a Lead Data Engineer, you will serve as the technical anchor for the engineering team, responsible for designing and developing scalable, high-performance data solutions. You will own and drive data architecture that supports both functional and non-functional business needs, ensuring reliability, efficiency, and scalability.
Your expertise in big data technologies, distributed systems, and cloud platforms will help shape the engineering roadmap and best practices for data processing, analytics, and real-time data serving. You will play a key role in architecting and optimizing data pipelines using Hadoop, Spark, Scala/Java, and cloud technologies to support enterprise-wide data initiatives.
Additionally, experience with API development for serving low-latency data and Customer Data Platforms (CDP) will be a strong plus.
"""
new_resume = rewrite_resume(df["Markdown_Resume"].iloc[0], job_desc, HF_TOKEN)


# In[ ]:


def save_resume_to_word(resume_text, output_path="optimized_resume.docx"):
    """Saves the optimized resume text into a Word document."""
    doc = Document()
    
    for line in resume_text.split("\n"):
        if line.strip():  # Avoid empty lines
            doc.add_paragraph(line)
    
    doc.save(output_path)
    print(f"Resume saved as {output_path}")

# Example usage
pdf_path = "resume.pdf"  # Replace with your actual PDF file path
df = pdf_to_markdown(pdf_path)
job_desc = "Software Engineer with Python and AI experience."
new_resume = rewrite_resume(df["Markdown_Resume"].iloc[0], job_desc, HF_TOKEN)

# Save the AI-optimized resume to a Word document
save_resume_to_word(new_resume)

