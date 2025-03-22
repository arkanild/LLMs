# OVERVIEW:

A utility to tailor your resumes based on a specific job description. It connects to an open-source LLM, takes your resume and the job description as inputs, and generates a tailored resume in DOC format. This allows users to efficiently apply to multiple job positions with resumes customized for each role.

Happy (Job) Hunting! 🎯


# HOW DOES IT DO IT?

Upload Your Resume – Provide your resume in PDF format.
Enter the Job Description – Input the job description for the position you're applying for.
AI-Powered Customization – The system processes both inputs and sends a structured prompt to an LLM available on Hugging Face.
Inference API – Uses Hugging Face’s Inference API, requiring a token for authentication. Some models are gated and may need additional permissions, but you can switch models if you have the required access.
Customizable Parameters – Through prompt engineering, you can adjust parameters such as temperature, max_new_tokens, etc., giving you flexibility similar to running a local model on PyTorch or TensorFlow.

# ARCHITECTURE DIAGRAM:



## Executable python script, for people not handy with Jupyter notebooks - [Smart_resume.py](https://github.com/arkanild/LLMs/blob/main/smart_resume/smart_resume.py)

# TO DO : 
1. UI for Input Submission – A user-friendly interface for uploading resumes and entering job descriptions.
2. Customizable Output Formats – Allow users to choose the output format (DOC, PDF, etc.).


