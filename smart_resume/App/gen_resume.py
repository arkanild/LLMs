
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

# Get Hugging Face API token from environment variable
HF_TOKEN = "<your hugging face token>"  # Replace with your actual token

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

def save_resume_to_word(resume_text, output_path="optimized_resume.docx"):
    """Saves the optimized resume text into a Word document."""
    doc = Document()
    
    for line in resume_text.split("\n"):
        if line.strip():  # Avoid empty lines
            doc.add_paragraph(line)
    
    doc.save(output_path)
    print(f"Resume saved as {output_path}")

save_resume_to_word(new_resume)

