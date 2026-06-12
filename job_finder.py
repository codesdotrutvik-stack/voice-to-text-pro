import streamlit as st
import requests
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Job Finder AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .header h1 { color: white; margin: 0; font-size: 1.8rem; }
    .header p { color: rgba(255,255,255,0.85); margin: 0.3rem 0 0; font-size: 0.85rem; }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        width: 100%;
    }
    
    .api-success {
        background: #d1fae5;
        color: #065f46;
        padding: 0.6rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: 500;
    }
    
    .stat-box {
        text-align: center;
        padding: 0.8rem;
        background: white;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
    }
    .stat-number { font-size: 1.3rem; font-weight: 700; color: #667eea; }
    .stat-label { font-size: 0.7rem; color: #64748b; }
    
    .point-item {
        padding: 0.25rem 0;
        margin: 0.15rem 0;
        border-left: 3px solid #667eea;
        padding-left: 0.7rem;
        font-size: 0.85rem;
    }
    
    .saved-badge {
        display: inline-block;
        background: #d1fae5;
        color: #065f46;
        padding: 0.2rem 0.5rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 500;
    }
    
    /* Agentforce Style Chatbot */
    .chatbot-wrapper {
        position: fixed;
        bottom: 0;
        right: 0;
        width: 380px;
        height: 500px;
        background: white;
        border-radius: 16px 16px 0 0;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.15);
        z-index: 1000;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        border-bottom: none;
    }
    
    .chatbot-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: white;
        padding: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .chatbot-header-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .agent-avatar {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #00d4ff, #7b5ea7);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }
    .agent-info h4 {
        margin: 0;
        font-size: 14px;
        font-weight: 600;
    }
    .agent-info p {
        margin: 0;
        font-size: 10px;
        opacity: 0.7;
    }
    .chatbot-close {
        cursor: pointer;
        background: rgba(255,255,255,0.1);
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
    }
    .chatbot-close:hover {
        background: rgba(255,255,255,0.2);
    }
    
    .chatbot-messages {
        flex: 1;
        padding: 16px;
        overflow-y: auto;
        background: #f8fafc;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    
    .bot-message {
        display: flex;
        gap: 10px;
        max-width: 85%;
    }
    .bot-avatar {
        width: 30px;
        height: 30px;
        background: linear-gradient(135deg, #00d4ff, #7b5ea7);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        flex-shrink: 0;
    }
    .bot-bubble {
        background: white;
        padding: 10px 12px;
        border-radius: 12px;
        border-top-left-radius: 4px;
        font-size: 12px;
        color: #1e293b;
        line-height: 1.4;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    .bot-time {
        font-size: 9px;
        color: #94a3b8;
        margin-top: 4px;
    }
    
    .user-message {
        display: flex;
        justify-content: flex-end;
        max-width: 85%;
        align-self: flex-end;
    }
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 12px;
        border-radius: 12px;
        border-top-right-radius: 4px;
        font-size: 12px;
        line-height: 1.4;
    }
    .user-time {
        font-size: 9px;
        color: #94a3b8;
        text-align: right;
        margin-top: 4px;
    }
    
    .chatbot-input-area {
        padding: 12px;
        background: white;
        border-top: 1px solid #e2e8f0;
        display: flex;
        gap: 8px;
    }
    .chatbot-input-area input {
        flex: 1;
        padding: 10px 14px;
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        outline: none;
        font-size: 12px;
    }
    .chatbot-input-area input:focus {
        border-color: #667eea;
    }
    .chatbot-input-area button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 24px;
        padding: 0 18px;
        cursor: pointer;
        font-weight: 500;
        font-size: 12px;
    }
    
    .typing-dots {
        display: flex;
        gap: 4px;
        padding: 10px 12px;
        background: white;
        border-radius: 12px;
        border-top-left-radius: 4px;
        width: 50px;
        border: 1px solid #e2e8f0;
    }
    .typing-dots span {
        width: 6px;
        height: 6px;
        background: #94a3b8;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
    .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
        30% { transform: translateY(-6px); opacity: 1; }
    }
    
    .chatbot-toggle {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 50px;
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        z-index: 999;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s;
    }
    .chatbot-toggle:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1>💼 Job Finder AI</h1>
    <p>Live jobs from Adzuna API • Save jobs permanently • Get company insights</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# API CONFIGURATION
# ============================================================
ADZUNA_APP_ID = "cab85cad"
ADZUNA_API_KEY = "9c920a8f1b37a639553a98541e0ba2e8"
MISTRAL_API_KEY = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"

CITIES = ["All", "Ahmedabad", "Surat", "Rajkot", "Vadodara", "Bangalore", "Mumbai", "Hyderabad"]

POPULAR_ROLES = [
    "Python Developer", "Shopify Developer", "Frontend Developer", 
    "WordPress Developer", "Full Stack Developer", "Data Scientist",
    "React Developer", "Java Developer", "DevOps Engineer"
]

DEFAULT_ROLE = "Python Developer"
DEFAULT_CITY = "Surat"

# ============================================================
# PERMANENT STORAGE
# ============================================================
SAVED_JOBS_FILE = "saved_jobs.json"

def load_saved_jobs():
    try:
        if os.path.exists(SAVED_JOBS_FILE):
            with open(SAVED_JOBS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except:
        return []

def save_saved_jobs(jobs):
    try:
        with open(SAVED_JOBS_FILE, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def fetch_jobs(role, location):
    location_name = location if location != "All" else "India"
    
    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_API_KEY,
        "results_per_page": 12,
        "what": role,
        "where": location_name,
        "sort_by": "date"
    }
    
    try:
        response = requests.get(url, params=params, timeout=25)
        if response.status_code == 200:
            data = response.json()
            jobs = []
            for result in data.get("results", []):
                salary_min = result.get("salary_min", 0)
                salary_max = result.get("salary_max", 0)
                if salary_min and salary_max and salary_min > 0:
                    salary = f"₹{int(salary_min/100000)}-{int(salary_max/100000)} LPA"
                elif salary_min and salary_min > 0:
                    salary = f"₹{int(salary_min/100000)} LPA"
                else:
                    salary = "Not disclosed"
                
                company = result.get("company", {})
                company_name = company.get("display_name", "Private Limited") if isinstance(company, dict) else "Private Limited"
                
                jobs.append({
                    "id": result.get("id"),
                    "title": result.get("title", "N/A"),
                    "company": company_name,
                    "location": result.get("location", {}).get("display_name", location_name) if isinstance(result.get("location"), dict) else location_name,
                    "salary": salary,
                    "description": result.get("description", "")[:400] if result.get("description") else "No description available",
                    "url": result.get("redirect_url", "#"),
                    "created": result.get("created", "Recently")
                })
            return jobs, None
        else:
            return None, f"API Error: {response.status_code}"
    except Exception as e:
        return None, f"Connection Error: {str(e)}"

def get_company_details(company_name, job_title):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Provide brief information about this company and job.

Company: {company_name}
Job Title: {job_title}

Return in this format:
- Industry:
- Required Experience:
- Key Skills:
- Interview Tips:"""

    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 250
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=15)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return f"- Industry: Technology\n- Company: {company_name}\n- Tip: Research the company before interview"

def chat_with_ai(user_message):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""You are JobBot AI, a helpful career assistant. Answer the user's question.

User: {user_message}

Give a friendly, helpful response (2-3 sentences). Be professional but warm."""

    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=15)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "I'm here to help! Ask me about jobs, companies, or career advice."

# ============================================================
# SESSION STATE
# ============================================================
if "saved_jobs" not in st.session_state:
    st.session_state.saved_jobs = load_saved_jobs()
if "jobs" not in st.session_state:
    st.session_state.jobs = []
if "searched" not in st.session_state:
    st.session_state.searched = False
if "company_details" not in st.session_state:
    st.session_state.company_details = {}
if "search_role" not in st.session_state:
    st.session_state.search_role = DEFAULT_ROLE
if "search_city" not in st.session_state:
    st.session_state.search_city = DEFAULT_CITY
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "bot", "content": "Hi! I'm JobBot AI. I can help you with job search, company information, and career advice. Ask me anything!", "time": datetime.now().strftime("%I:%M %p")}
    ]

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 🔍 Search Jobs")
    
    st.session_state.search_role = st.text_input(
        "Job Role", 
        value=st.session_state.search_role,
        placeholder="e.g., Python Developer, Shopify Expert"
    )
    
    st.session_state.search_city = st.selectbox(
        "City", 
        CITIES,
        index=CITIES.index(st.session_state.search_city) if st.session_state.search_city in CITIES else 0
    )
    
    search_clicked = st.button("🔍 Search Jobs", use_container_width=True, type="primary")
    
    st.markdown("---")
    
    st.markdown("### 📌 Quick Filters")
    
    for role in POPULAR_ROLES[:5]:
        if st.button(role, key=f"quick_{role}", use_container_width=True):
            st.session_state.search_role = role
            st.rerun()
    
    st.markdown("---")
    st.success("✅ API Active")
    
    st.markdown("---")
    st.markdown(f"### 📌 Saved Jobs")
    st.markdown(f"**{len(st.session_state.saved_jobs)}** jobs saved")
    
    if st.button("🗑️ Clear All Saved", use_container_width=True):
        st.session_state.saved_jobs = []
        save_saved_jobs([])
        st.rerun()

# ============================================================
# LOAD DEFAULT JOBS
# ============================================================
if not st.session_state.searched and not st.session_state.jobs:
    with st.spinner(f"Loading default jobs..."):
        default_jobs, error = fetch_jobs(DEFAULT_ROLE, DEFAULT_CITY)
        if default_jobs:
            st.session_state.jobs = default_jobs
            st.session_state.searched = True

# ============================================================
# SEARCH LOGIC
# ============================================================
if search_clicked:
    with st.spinner(f"Searching..."):
        jobs, error = fetch_jobs(st.session_state.search_role, st.session_state.search_city)
        if jobs:
            st.session_state.jobs = jobs
            st.session_state.searched = True
            st.session_state.company_details = {}
            st.success(f"✅ Found {len(jobs)} jobs")
        else:
            st.session_state.jobs = []
            st.session_state.searched = True
            st.error(error)

# ============================================================
# RESULTS DISPLAY
# ============================================================
if st.session_state.searched:
    if st.session_state.jobs:
        st.markdown(f"""
        <div class="api-success">
            🎯 {len(st.session_state.jobs)} jobs found for '{st.session_state.search_role}' in {st.session_state.search_city}
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="stat-box"><div class="stat-number">{len(st.session_state.jobs)}</div><div class="stat-label">Jobs Found</div></div>', unsafe_allow_html=True)
        with col2:
            companies = len(set(j.get("company") for j in st.session_state.jobs))
            st.markdown(f'<div class="stat-box"><div class="stat-number">{companies}</div><div class="stat-label">Companies</div></div>', unsafe_allow_html=True)
        with col3:
            locations = len(set(j.get("location") for j in st.session_state.jobs))
            st.markdown(f'<div class="stat-box"><div class="stat-number">{locations}</div><div class="stat-label">Locations</div></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        for idx, job in enumerate(st.session_state.jobs):
            is_saved = any(j.get('id') == job.get('id') for j in st.session_state.saved_jobs)
            
            with st.expander(f"💼 {job['title']} - {job['company']} (📍 {job['location']})", expanded=False):
                st.markdown(f"""
                <div class="point-item"><b>Company:</b> {job['company']}</div>
                <div class="point-item"><b>Location:</b> {job['location']}</div>
                <div class="point-item"><b>Salary:</b> {job['salary']}</div>
                <div class="point-item"><b>Posted:</b> {job['created'][:10] if job['created'] != 'Recently' else 'Recently'}</div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### 📝 Description")
                desc_lines = job['description'][:350].split('.')[:4]
                for line in desc_lines:
                    if line.strip():
                        st.markdown(f'<div class="point-item">• {line.strip()}.</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if not is_saved:
                        if st.button(f"⭐ Save", key=f"save_{idx}"):
                            st.session_state.saved_jobs.append(job)
                            save_saved_jobs(st.session_state.saved_jobs)
                            st.success("Saved!")
                            st.rerun()
                    else:
                        st.markdown('<span class="saved-badge">✓ Saved</span>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"[📋 Apply]({job['url']})", unsafe_allow_html=True)
                
                with col3:
                    if st.button(f"🏢 Company Info", key=f"info_{idx}"):
                        with st.spinner("Fetching..."):
                            details = get_company_details(job['company'], job['title'])
                            st.session_state.company_details[idx] = details
                            st.rerun()
                
                if idx in st.session_state.company_details:
                    st.markdown("---")
                    st.markdown(f"#### 🏢 About {job['company']}")
                    st.info(st.session_state.company_details[idx])
                    
                    if st.button(f"✖️ Close", key=f"close_{idx}"):
                        del st.session_state.company_details[idx]
                        st.rerun()
    
    elif st.session_state.jobs == [] and st.session_state.searched:
        st.warning(f"No jobs found")
        st.info("💡 Try different job role or location")

# ============================================================
# SAVED JOBS DISPLAY
# ============================================================
if st.session_state.saved_jobs:
    st.markdown("---")
    st.markdown("## ⭐ Saved Jobs")
    
    for idx, job in enumerate(st.session_state.saved_jobs):
        with st.expander(f"💼 {job['title']} - {job['company']}", expanded=False):
            st.markdown(f"""
            **Location:** {job['location']}
            **Salary:** {job['salary']}
            """)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"[📋 Apply]({job['url']})", unsafe_allow_html=True)
            with col2:
                if st.button(f"❌ Remove", key=f"remove_{idx}"):
                    st.session_state.saved_jobs.pop(idx)
                    save_saved_jobs(st.session_state.saved_jobs)
                    st.rerun()

# ============================================================
# AGENTFORCE STYLE CHATBOT
# ============================================================
if not st.session_state.chat_open:
    st.markdown("""
    <div class="chatbot-toggle" onclick="window.location.reload()">
        <span>💬</span> Need Help? Chat with JobBot
    </div>
    """, unsafe_allow_html=True)
    if st.button("💬 Need Help? Chat with JobBot", key="chat_toggle_main", use_container_width=True):
        st.session_state.chat_open = True
        st.rerun()

if st.session_state.chat_open:
    st.markdown("---")
    st.markdown("### 💬 JobBot AI Assistant")
    
    # Chat messages
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 12px;">
                <div style="max-width: 70%;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px 14px; border-radius: 18px; border-top-right-radius: 4px; font-size: 13px;">
                        {msg['content']}
                    </div>
                    <div style="font-size: 10px; color: #94a3b8; text-align: right; margin-top: 4px;">
                        {msg.get('time', datetime.now().strftime("%I:%M %p"))}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display: flex; gap: 10px; margin-bottom: 12px;">
                <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #00d4ff, #7b5ea7); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0;">
                    🤖
                </div>
                <div style="max-width: 70%;">
                    <div style="background: white; padding: 10px 14px; border-radius: 18px; border-top-left-radius: 4px; font-size: 13px; border: 1px solid #e2e8f0;">
                        {msg['content']}
                    </div>
                    <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">
                        {msg.get('time', datetime.now().strftime("%I:%M %p"))}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_message = st.text_input("", key="chat_msg", placeholder="Type your message...", label_visibility="collapsed")
    with col2:
        if st.button("Send", key="send_msg"):
            if user_message:
                current_time = datetime.now().strftime("%I:%M %p")
                st.session_state.chat_messages.append({"role": "user", "content": user_message, "time": current_time})
                with st.spinner("🤔"):
                    response = chat_with_ai(user_message)
                    st.session_state.chat_messages.append({"role": "bot", "content": response, "time": datetime.now().strftime("%I:%M %p")})
                st.rerun()
    
    if st.button("✖️ Close Chat", use_container_width=True):
        st.session_state.chat_open = False
        st.rerun()

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("Job Finder AI | Powered by NB")