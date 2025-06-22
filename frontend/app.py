import streamlit as st
import requests
import re
import math
import os
<<<<<<< HEAD
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info("Starting Streamlit app")

# Page Configuration
try:
    st.set_page_config(
        page_title="AI Resume Job Matcher",
        page_icon="🎯",
        layout="wide"
    )
    logger.info("Page config set")
except Exception as e:
    logger.error(f"Page config failed: {str(e)}")
    raise

# Styling
try:
    st.markdown("""
    <style>
        /* Using a system font for reliability */
        html, body, [class*="st-"] { font-family: sans-serif; }
        .main { background-color: #0E1117; }
        .st-emotion-cache-16txtl3 { background-color: #0E1117; }
        body, .st-emotion-cache-10trblm, h1, h2, h3, p, label, .st-emotion-cache-1y4p8pa { color: #E6EDF3; }
        .st-emotion-cache-16txtl3 { border: 1px solid #30363D; border-radius: 12px; }
        div.st-emotion-cache-1v0mbdj {
            border: 1px solid #30363D; border-radius: 10px;
            padding: 1.5rem; margin-bottom: 1rem; background-color: #161B22;
        }
        h1 { color: #58A6FF; }
        h2 { color: #58A6FF; padding-top: 1rem; border-top: 1px solid #30363d; }
        [data-testid="stProgressBar"] > div > div > div {
            background-image: linear-gradient(90deg, #1F6FEB, #58A6FF);
        }
    </style>
    """, unsafe_allow_html=True)
    logger.info("CSS applied")
except Exception as e:
    logger.error(f"CSS application failed: {str(e)}")
    raise
=======
# page confirmation
st.set_page_config(
    page_title="AI Resume Job Matcher",
    page_icon="🎯",
    layout="wide"
)

# Style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0E1117; }
    .st-emotion-cache-16txtl3 { background-color: #0E1117; }
    body, .st-emotion-cache-10trblm, h1, h2, h3, p, label, .st-emotion-cache-1y4p8pa { color: #E6EDF3; }
    .st-emotion-cache-16txtl3 { border: 1px solid #30363D; border-radius: 12px; }
    div.st-emotion-cache-1v0mbdj {
        border: 1px solid #30363D; border-radius: 10px;
        padding: 1.5rem; margin-bottom: 1rem; background-color: #161B22;
    }
    h1 { color: #58A6FF; }
    h2 { color: #58A6FF; padding-top: 1rem; border-top: 1px solid #30363d; }
    [data-testid="stProgressBar"] > div > div > div {
        background-image: linear-gradient(90deg, #1F6FEB, #58A6FF);
    }
</style>
""", unsafe_allow_html=True)
>>>>>>> f3e9499a61ba98af25341bb3fad9afc203e9b957

logger.info("App initialized, serving UI")

# [CHANGE] The default URL now points to your live Yandex Cloud backend.
# This makes it easy for anyone to run the frontend locally for a demo.
API_URL = os.getenv("API_URL", "https://bbackis1oi638qdm6tiu.containers.yandexcloud.net/resumes/search-and-score")

# Experience options
EXPERIENCE_LEVELS = [
    "Doesn't matter", "Нет опыта", "От 1 года до 3 лет",
    "От 3 до 6 лет", "Более 6 лет"
]

# Industry tagged list jobs 
INDUSTRY_JOB_TITLES = {
    "Information Technology (IT) & Software": [
        "Machine Learning Engineer", "Data Scientist", "Data Analyst", "Python Developer",
        "Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer",
        "DevOps Engineer", "QA Engineer", "Cloud Engineer", "Cybersecurity Analyst",
        "AI Researcher", "Mobile Developer", "Site Reliability Engineer", "IT Support Specialist"
    ],
    "Product & Project Management": [
        "Product Manager", "Project Manager", "Business Analyst", "Scrum Master",
        "Agile Coach", "Program Manager", "Operations Manager", "Technical Program Manager"
    ],
    "Finance & Accounting": [
        "Financial Analyst", "Accountant", "Tax Consultant", "Auditor", "Investment Banker",
        "Portfolio Manager", "Risk Analyst", "Treasury Analyst", "Compliance Officer", "Controller",
        "Finance Manager", "Billing Specialist"
    ],
    "Healthcare & Life Sciences": [
        "Registered Nurse", "Medical Assistant", "Healthcare Administrator", "Pharmacist",
        "Physician Assistant", "Clinical Research Associate", "Public Health Analyst",
        "Medical Coder", "Radiologic Technologist", "Lab Technician",
        "Health Information Technician", "Dental Hygienist"
    ],
    "Engineering & Manufacturing": [
        "Mechanical Engineer", "Civil Engineer", "Electrical Engineer", "Systems Engineer",
        "Manufacturing Engineer", "Industrial Engineer", "Design Engineer", "Process Engineer",
        "Quality Assurance Engineer", "CAD Technician", "HVAC Engineer", "Structural Engineer"
    ],
    "Logistics & Supply Chain": [
        "Logistics Coordinator", "Supply Chain Analyst", "Procurement Specialist",
        "Warehouse Manager", "Transportation Planner", "Inventory Analyst",
        "Shipping Supervisor", "Import/Export Coordinator"
    ],
    "Marketing, Media & Communications": [
        "Digital Marketing Manager", "SEO Specialist", "Content Strategist", "Copywriter",
        "Social Media Manager", "Marketing Analyst", "Email Marketing Specialist",
        "Brand Manager", "Communications Specialist", "Public Relations Manager"
    ],
    "Retail & Customer Service": [
        "Store Manager", "Retail Sales Associate", "Cashier", "Customer Service Representative",
        "Merchandise Planner", "Inventory Specialist", "Call Center Agent", "E-commerce Manager"
    ],
    "Human Resources (HR)": [
        "HR Manager", "Recruiter", "Talent Acquisition Specialist", "HR Generalist",
        "HR Coordinator", "Compensation Analyst", "Learning and Development Specialist"
    ],
    "Legal & Compliance": [
        "Legal Assistant", "Paralegal", "Corporate Lawyer", "Compliance Analyst",
        "Contract Manager", "Litigation Support Specialist", "Legal Counsel"
    ],
    "Education & Training": [
        "Teacher", "Instructional Designer", "Education Coordinator", "Curriculum Developer",
        "School Counselor", "Professor", "Academic Advisor", "Online Course Developer"
    ],
    "Consulting & Strategy": [
        "Management Consultant", "Strategy Consultant", "Business Consultant",
        "IT Consultant", "Operations Consultant", "Data Strategy Analyst"
    ]
}

JOB_TITLE_SUGGESTIONS = ["Select a suggested job title..."]
TITLE_TO_INDUSTRY = {}
for industry, titles in INDUSTRY_JOB_TITLES.items():
    for title in titles:
        JOB_TITLE_SUGGESTIONS.append(title)
        TITLE_TO_INDUSTRY[title] = industry

# Session state
if 'jobs' not in st.session_state: st.session_state.jobs = []
if 'search_ran' not in st.session_state: st.session_state.search_ran = False
if 'page' not in st.session_state: st.session_state.page = 1

# Backend function
def find_jobs(uploaded_file, custom_keyword, suggested_keyword):
    keyword = custom_keyword or suggested_keyword
    if not uploaded_file:
        st.error("Please upload your resume first.")
        logger.error("No resume uploaded")
        return
    if not keyword or keyword == JOB_TITLE_SUGGESTIONS[0]:
        st.error("Please enter a custom title or choose one from the list.")
        logger.error("No job title selected")
        return

    st.session_state.search_ran = True
    st.session_state.jobs = []
    st.session_state.search_keyword_display = keyword
    st.session_state.page = 1

    with st.spinner(f"Analyzing resume and searching for '{keyword}' roles..."):
        try:
            logger.info(f"Sending request to {API_URL} with keyword: {keyword}")
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            data = {"keyword": keyword}
            response = requests.post(API_URL, files=files, data=data, timeout=90)
            logger.info(f"Received response: status {response.status_code}")
            if response.status_code == 200:
                st.session_state.jobs = response.json().get("matches", [])
                logger.info(f"Found {len(st.session_state.jobs)} job matches")
            else:
                st.error(f"Server Error: {response.status_code} - {response.text}")
                logger.error(f"Server error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error("API Error: Could not connect to the backend.")
            logger.error(f"API error: {str(e)}")

# UI header
st.title("AI Resume Job Matcher")

# Input form
with st.container(border=True):
    st.markdown("### Start Your Search")
    uploaded_file = st.file_uploader("1. Upload Your Resume")

    col1, col2 = st.columns(2)
    suggested_keyword = col1.selectbox("2. Choose a Suggested Job Title", options=JOB_TITLE_SUGGESTIONS)
    if suggested_keyword in TITLE_TO_INDUSTRY:
        st.caption(f"Industry: **{TITLE_TO_INDUSTRY[suggested_keyword]}**")

    custom_keyword = col2.text_input("...OR Enter a Custom Title", placeholder="e.g., Senior Java Developer")

    st.button("Find Job Matches", type="primary", use_container_width=True,
              on_click=find_jobs, args=(uploaded_file, custom_keyword, suggested_keyword))

    st.caption("Job data sourced from hh.ru")

<<<<<<< HEAD
# Optional grouped titles reviewed
=======
# optional grouped titles reviewd
>>>>>>> f3e9499a61ba98af25341bb3fad9afc203e9b957
with st.expander("💼 View All Suggested Job Titles by Industry"):
    for industry, titles in INDUSTRY_JOB_TITLES.items():
        st.markdown(f"**{industry}**")
        st.markdown(", ".join(titles))
        st.markdown("---")

# Display results
if st.session_state.search_ran:
    st.markdown("---")
    if st.session_state.jobs:
        st.success(f"**Search Complete:** Found **{len(st.session_state.jobs)}** jobs for '{st.session_state.get('search_keyword_display', '')}'.")

        st.markdown("### Refine Your Results")
        f1, f2 = st.columns([2, 1])
        keyword_filter = f1.text_input("Filter results by keyword")
        exp_filter = f2.selectbox("Filter by experience", options=EXPERIENCE_LEVELS)

        jobs = st.session_state.jobs
        if keyword_filter:
            jobs = [j for j in jobs if re.search(keyword_filter, j.get("job_title", ""), re.I)]
        if exp_filter != "Doesn't matter":
            jobs = [j for j in jobs if j.get("experience") == exp_filter]

        st.markdown("---")
        if not jobs:
            st.warning("No jobs match your current filters.")
        else:
            st.write(f"Displaying **{len(jobs)}** matching jobs:")

            items_per_page = 5
            total_pages = math.ceil(len(jobs) / items_per_page)
            nav_cols = st.columns([1, 1, 1, 3])

            if nav_cols[0].button("◀️ Previous") and st.session_state.page > 1:
                st.session_state.page -= 1
            if nav_cols[1].button("Next ▶️") and st.session_state.page < total_pages:
                st.session_state.page += 1
            nav_cols[2].write(f"Page {st.session_state.page} of {total_pages}")

            start = (st.session_state.page - 1) * items_per_page
            end = start + items_per_page
            for job in jobs[start:end]:
                with st.container(border=True):
                    st.subheader(job.get("job_title", "No Title"))
                    st.caption(f"🏢 {job.get('company', 'N/A')} | 📍 {job.get('location', 'N/A')} | 💼 {job.get('experience', 'N/A')} | 💰 {job.get('salary', 'N/A')}")
                    score = int(job.get("score", 0) * 100)
                    st.progress(score, text=f"{score}% Match")
                    with st.expander("View Details & Matched Skills"):
                        st.link_button("Apply on hh.ru", job.get("url", "#"))
                        st.markdown("---")
                        st.markdown(job.get("description", "No description available."))
                        st.markdown(f"--- \n**Matched Skills:** {', '.join(job.get('matched_skills', [])) or 'None'}")
    else:
        st.warning(f"No jobs were found for '{st.session_state.get('search_keyword_display', '')}'. Try another keyword.")
