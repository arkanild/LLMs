OVERVIEW: 
An utility to tailor your resumes based on a particular job description. It connects to an open source LLM, takes your resume and the job description as an input 
and produces a tailored resume in doc format. Using this one can apply to multiple job positions and tailor their resumes based on 
specific job description. 
Happy(job) Hunting!!

HOW IT WORKS: 
The system asks for a resume in pdf format and input the Job description of the chosen job that you want to apply. 
It then takes up both these inputs and sends a structured prompt specific to an LLM in the huggingface open library. 
It uses the Inference API of the huggingface library. You would need to generate a token and authenticate yourself into huggingface repo. 
Some models are gatekeeped and require additional permissions, you can easily switch the model if you have these permissions. 

The prompt through prompt engineering is structured in such a way that you are able to toggle the parameters(temparature, max_new_tokens, etc).
This gives the user the flexibility to create prompts like they would incase of a local model run on pyTorch or Tensorflow. 

Architecture diagram:



executable python script, for people not handy on Jupyter notebooks - https://github.com/arkanild/LLMs/blob/main/smart_resume/smart_resume.py

TO DO : 
1. UI for submitting the inputs and JD.
2. Output can be derived in any format given by the user. 


