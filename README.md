# AI Resume Job Matcher!

Welcome to the *AI Resume Job Matcher* project! This tool helps job seekers find jons that best match with their skills and experience by analyzing their resumes and comparing them to real job listings from hh.ru. It works with resumes written in English or Russian. 

---

## What it does?

- Upload your resume (PDF or Docx)
- ENter or Select your desired job title
- The system:
    - Reads your resume
    - Extracts your skills and experience
    - Fetches real job listing from hh.ru\
    - Scores jobs bases on how well they match your resume
  - Shows you the best job matches with match parcentage score and matched skills

---


## How matching works?

The system calculates a *match score* for each job using:

1. **Semantic similarity (70%)**
   Compares the meaning of your resume with the job description using a multilingual model
2. **Skill overlap (5% per skill)**
   Adds points for every skill from your resume found in the job description.
3. **Experience penalty (15%)**
   SUbtracrs points if yoyr experienc is less than the job requires.

---

## Requirements 

- Docker installed
- 
