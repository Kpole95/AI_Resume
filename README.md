# AI Resume Job Matcher!

Welcome to the **AI Resume Job Matcher** project! This tool helps job seekers find jobs that best match with their skills and experience by analyzing their resumes and comparing them to real job listings from hh.ru. It works with resumes written in English or Russian and supports both `.pdf` and `.docx` formats. 

---

**Live Demo:**
- The backend (server) of the app is already running on **Yandex Cloud**.
- You simply need to run the frontend (user interface) on your own machine to try it out.

---

## Features

- **Smart Matching with AI:** The app uses a machine learning model to understand the *meaning* of your resume and job descriptions, not just keywords.
- **Custom Match Score:** Jobs are ranked on how closely they match your resume based on:
    - Semantic meaning
    - Skill keyword overlap
    - Your experience level
- **Resume File Support:** Works with `.pdf` and `.docx` resumes automatically.
- **Easy to Use UI:** Built with Streamlit, so it looks nice and is simple to use.
- **Real Job Listings:** The app fetches jobs directly from `hh.ru` (a popular Russian job site).


---

## How the Application works? What it does?
This project has two main parts:
### 1. Frontend (User interface)
- Built with *Streamlit*
- You can run this part on your local computer.
- You upload your resume (pdf or docx) and select or enter your desired job title
  - The system:
      - Reads your resume
      - Extract your skills and experience
      - The app then sends your data to the backend.
      - Fetches real job listings from hh.ru
      - Shows you the best jobs matches with match parcentage score and matched skills

#### Screenshot: Homepage
![Homeoage](assets/images/homepage.png)

#### Screenshot: Resume Upload
![Resume Upload](assets/images/resumeuploaded.png)

#### Screenshot: Results
![Results](assets/images/results.png)

#### Screenshot: Results1
![Results1](assets/images/results1.png)

#### Screenshot: Filter
![Filters](assets/images/filterresults.png)

### 2. Backend (AI + Processing)
- Implemented with *FastAPI* and deployed on *Yandex Cloud*.
- Does the heavy lifting.
- Reads and understands your CV
- Searches for jobs on hh.ru
- Calculates how well each job matches your resume
- Gives a neat and well organized list of results.
 
**NOTE:**
The frontend does *not* access any API keys. All secure work is done in the backed on the cloud.

---


## How matching works?

The system calculates a *match score* for each job using:

1. **Semantic similarity (70%)**
   - The AI reads your resume and every job post and turns them into *vectors* (numbers)
   - It matches them using *cosine similarity* to determine how similar they match in meaning.
   - This part has the most weight: **70% of the final score**

2. **Skill overlap (5% per skill)**
   - It alos checks if your resume has skills that appear in the job posting.
   - For each matching skill, it adds **0.05 bonus** to the score.
   - 
3. **Experience penalty (15%)**
   - if the job requires more years of experienc than you have, it subtracts **0.15** from the score

In the end, you end up with a final score for each job and the jobs are sorted from best to worst match.

---

## How to run this demo on your computer?
- You do not need to set up backend or use any API keys.
- You only need to run the **Streamlit frontend locally**

### Requirements
- **Python 3.10+**
- **Git**


### Step-by-Step Instructions

**1. Clone the Repository**
Open your terminal or command prompt and clone the project from GitHub:

```bash
git clone https://github.com/Kpole95/AI_Resume.git
cd AI_Resume
```

**2. Create and actu=ivate a virtual env**

```
For macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

```
For WIndows:
python -m venv venv
.\venv\Scripts\activate
```

**3. Install required packages**
```
pip install -r requirements.txt
```
**4. Run the frontend application**
```
strramlit run frontend/app.py
```
The app will launch in your browser at:

```You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://172.29.106.186:8501
```
