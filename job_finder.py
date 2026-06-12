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
    
    /* Chatbot CSS */
    .chat-float {
        position: fixed;
        bottom: 25px;
        right: 25px;
        width: 55px;
        height: 55px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        z-index: 999;
        font-size: 26px;
        transition: 0.3s;
    }
    .chat-float:hover {
        transform: scale(1.05);
    }
    .chat-popup-box {
        position: fixed;
        bottom: 90px;
        right: 25px;
        width: 340px;
        height: 450px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        z-index: 1000;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }
    .chat-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 10px 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .chat-close-btn {
        cursor: pointer;
        font-size: 18px;
    }
    .chat-messages-area {
        flex: 1;
        padding: 10px;
        overflow-y: auto;
        background: #f8fafc;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .msg-bot {
        display: flex;
        gap: 8px;
    }
    .msg-bot-icon {
        width: 28px;
        height: 28px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
    }
    .msg-bot-text {
        background: white;
        padding: 8px 12px;
        border-radius: 12px;
        font-size: 12px;
        color: #1e293b;
        border: 1px solid #e2e8f0;
        max-width: 80%;
    }
    .msg-user {
        display: flex;
        justify-content: flex-end;
    }
    .msg-user-text {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 8px 12px;
        border-radius: 12px;
        font-size: 12px;
        max-width: 80%;
    }
    .msg-time {
        font-size: 9px;
        color: #94a3b8;
        margin-top: 2px;
    }
    .chat-input-container {
        padding: 10px;
        background: white;
        border-top: 1px solid #e2e8f0;
        display: flex;
        gap: 8px;
    }
    .chat-input-container input {
        flex: 1;
        padding: 8px 12px;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        outline: none;
        font-size: 12px;
    }
    .chat-input-container button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0 16px;
        cursor: pointer;
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
POPULAR_ROLES = ["Python Developer", "Shopify Developer", "Frontend Developer", "WordPress Developer", "Full Stack Developer"]
DEFAULT_ROLE = "Python Developer"
DEFAULT_CITY = "Surat"

SAVED_JOBS_FILE = "saved_jobs.json"

def load_saved_jobs():
    try:
        if os.path.exists(SAVED_JOBS_FILE):
            with open(SAVED_JOBS_FILE, "r") as f:
                return json.load(f)
        return []
    except:
        return []

def save_saved_jobs(jobs):
    try:
        with open(SAVED_JOBS_FILE, "w") as f:
            json.dump(jobs, f, indent=2)
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
                    "description": result.get("description", "")[:400] if result.get("description") else "No description",
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
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    prompt = f"""Provide brief info about {company_name} for {job_title}.
Return format:
- Industry:
- Required Experience:
- Key Skills:
- Interview Tips:"""
    data = {"model": "mistral-small-latest", "messages": [{"role": "user", "content": prompt}], "max_tokens": 200}
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=15)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return f"- Industry: Technology\n- Company: {company_name}"

def chat_response(msg):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    prompt = f"You are JobBot. Answer briefly: {msg}"
    data = {"model": "mistral-small-latest", "messages": [{"role": "user", "content": prompt}], "max_tokens": 150}
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=15)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "Thanks for your message! How can I help?"

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
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False
if "chat_list" not in st.session_state:
    st.session_state.chat_list = []

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### 🔍 Search Jobs")
    st.session_state.search_role = st.text_input("Job Role", value=st.session_state.search_role)
    st.session_state.search_city = st.selectbox("City", CITIES, index=CITIES.index(st.session_state.search_city) if st.session_state.search_city in CITIES else 0)
    search_clicked = st.button("🔍 Search Jobs", use_container_width=True, type="primary")
    
    st.markdown("---")
    st.markdown("### 📌 Quick Filters")
    for role in POPULAR_ROLES:
        if st.button(role, key=f"quick_{role}", use_container_width=True):
            st.session_state.search_role = role
            st.rerun()
    
    st.markdown("---")
    st.success("✅ API Active")
    st.markdown("---")
    st.markdown(f"### 📌 Saved Jobs: {len(st.session_state.saved_jobs)}")
    if st.button("🗑️ Clear All Saved", use_container_width=True):
        st.session_state.saved_jobs = []
        save_saved_jobs([])
        st.rerun()

# ============================================================
# LOAD DEFAULT JOBS
# ============================================================
if not st.session_state.searched and not st.session_state.jobs:
    with st.spinner("Loading jobs..."):
        jobs, _ = fetch_jobs(DEFAULT_ROLE, DEFAULT_CITY)
        if jobs:
            st.session_state.jobs = jobs
            st.session_state.searched = True

# ============================================================
# SEARCH LOGIC
# ============================================================
if search_clicked:
    with st.spinner("Searching..."):
        jobs, _ = fetch_jobs(st.session_state.search_role, st.session_state.search_city)
        if jobs:
            st.session_state.jobs = jobs
            st.session_state.searched = True
            st.session_state.company_details = {}
            st.success(f"✅ Found {len(jobs)} jobs")
        else:
            st.session_state.jobs = []
            st.session_state.searched = True
            st.error("No jobs found")

# ============================================================
# RESULTS DISPLAY
# ============================================================
if st.session_state.searched:
    if st.session_state.jobs:
        st.markdown(f'<div class="api-success">🎯 {len(st.session_state.jobs)} jobs found</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Jobs Found", len(st.session_state.jobs))
        col2.metric("Companies", len(set(j.get("company") for j in st.session_state.jobs)))
        col3.metric("Locations", len(set(j.get("location") for j in st.session_state.jobs)))
        
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
                for line in job['description'][:300].split('.')[:3]:
                    if line.strip():
                        st.markdown(f'<div class="point-item">• {line.strip()}.</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if not is_saved:
                        if st.button("⭐ Save", key=f"save_{idx}"):
                            st.session_state.saved_jobs.append(job)
                            save_saved_jobs(st.session_state.saved_jobs)
                            st.rerun()
                    else:
                        st.markdown('<span class="saved-badge">✓ Saved</span>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f"[📋 Apply]({job['url']})", unsafe_allow_html=True)
                with col3:
                    if st.button("🏢 Company Info", key=f"info_{idx}"):
                        details = get_company_details(job['company'], job['title'])
                        st.session_state.company_details[idx] = details
                        st.rerun()
                
                if idx in st.session_state.company_details:
                    st.info(st.session_state.company_details[idx])
                    if st.button("✖️ Close", key=f"close_{idx}"):
                        del st.session_state.company_details[idx]
                        st.rerun()
    else:
        st.warning("No jobs found. Try different search.")

# ============================================================
# SAVED JOBS
# ============================================================
if st.session_state.saved_jobs:
    st.markdown("---")
    st.markdown("## ⭐ Saved Jobs")
    for idx, job in enumerate(st.session_state.saved_jobs):
        with st.expander(f"💼 {job['title']} - {job['company']}", expanded=False):
            st.markdown(f"📍 {job['location']} | 💰 {job['salary']}")
            if st.button("❌ Remove", key=f"rem_{idx}"):
                st.session_state.saved_jobs.pop(idx)
                save_saved_jobs(st.session_state.saved_jobs)
                st.rerun()

# ============================================================
# CHATBOT - SIMPLE WORKING
# ============================================================
st.markdown("""
<div class="chat-float" id="chatFloatBtn">
    💬
</div>

<script>
    let chatVisible = false;
    let chatPopup = null;
    
    function createChatPopup() {
        let div = document.createElement('div');
        div.className = 'chat-popup-box';
        div.id = 'chatPopupBox';
        div.innerHTML = `
            <div class="chat-header">
                <span>🤖 JobBot</span>
                <span class="chat-close-btn" id="closeChatPopup">✕</span>
            </div>
            <div class="chat-messages-area" id="chatMessagesArea">
                <div class="msg-bot">
                    <div class="msg-bot-icon">🤖</div>
                    <div class="msg-bot-text">👋 Hi! Ask me about jobs, companies, or career advice!</div>
                </div>
            </div>
            <div class="chat-input-container">
                <input type="text" id="chatInputMsg" placeholder="Type a message..." />
                <button id="sendChatMsgButton">Send</button>
            </div>
        `;
        document.body.appendChild(div);
        
        document.getElementById('closeChatPopup').onclick = function() {
            closeChatPopup();
        };
        
        document.getElementById('sendChatMsgButton').onclick = function() {
            sendChatMsg();
        };
        
        document.getElementById('chatInputMsg').onkeypress = function(e) {
            if (e.key === 'Enter') sendChatMsg();
        };
        
        return div;
    }
    
    function closeChatPopup() {
        if (chatPopup) {
            chatPopup.remove();
            chatPopup = null;
            chatVisible = false;
        }
    }
    
    function sendChatMsg() {
        let input = document.getElementById('chatInputMsg');
        let msg = input.value.trim();
        if (msg === '') return;
        
        let now = new Date();
        let timeStr = now.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
        
        let messagesDiv = document.getElementById('chatMessagesArea');
        messagesDiv.innerHTML += `
            <div class="msg-user">
                <div class="msg-user-text">${escapeHtml(msg)}</div>
            </div>
            <div class="msg-time" style="text-align: right;">${timeStr}</div>
        `;
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
        input.value = '';
        
        let hiddenInput = document.querySelector('input[data-testid="stTextInput"][aria-label="chat_hidden"]');
        let hiddenBtn = document.querySelector('button[key="send_chat"]');
        if (hiddenInput && hiddenBtn) {
            hiddenInput.value = msg;
            hiddenBtn.click();
        }
    }
    
    function escapeHtml(text) {
        let div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    document.getElementById('chatFloatBtn').onclick = function() {
        if (chatVisible && chatPopup) {
            closeChatPopup();
            chatVisible = false;
        } else {
            chatPopup = createChatPopup();
            chatVisible = true;
        }
    };
</script>
""", unsafe_allow_html=True)

# Hidden Streamlit elements
chat_hidden = st.text_input("", key="chat_hidden", label_visibility="collapsed")

if st.button("", key="send_chat"):
    if chat_hidden:
        st.session_state.chat_list.append({"role": "user", "content": chat_hidden})
        bot_reply = chat_response(chat_hidden)
        st.session_state.chat_list.append({"role": "bot", "content": bot_reply})
        st.rerun()

for msg in st.session_state.chat_list:
    if msg["role"] == "bot":
        st.markdown(f'<div id="botReply" style="display:none;">{msg["content"]}</div>', unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("💼 Job Finder AI | Powered by Adzuna API + Mistral AI")