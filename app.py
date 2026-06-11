import streamlit as st
import requests
from datetime import datetime
import base64

api_key = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"
url = "https://api.mistral.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
    }
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    .main-header p {
        color: #bfdbfe;
        margin: 0;
    }
    .stButton button {
        background-color: #1e3a8a;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #3b82f6;
    }
    .user-msg {
        background-color: #dbeafe;
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 4px solid #1e3a8a;
    }
    .ai-msg {
        background-color: white;
        padding: 12px;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 4px solid #10b981;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .quiz-card {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>📚 AI Study Buddy Pro</h1>
    <p>Your Personal AI Teacher – Learn Anything, Anytime!</p>
</div>
""", unsafe_allow_html=True)

if "chat" not in st.session_state:
    st.session_state.chat = []
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = ""

def ask_ai(question, mode):
    if mode == "Simple (Like I'm 5)":
        prompt = "Explain like the student is 5 years old. Very simple words. Short sentences."
    elif mode == "Detailed":
        prompt = "Explain in detail with examples."
    else:
        prompt = "Explain clearly and simply."
    
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

def download_chat():
    chat_text = f"AI Study Buddy Chat - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    for msg in st.session_state.chat:
        chat_text += f"🧑‍🎓 You: {msg['q']}\n\n"
        chat_text += f"🤖 AI: {msg['a']}\n\n"
        chat_text += "="*50 + "\n\n"
    return chat_text

tabs = st.tabs(["💬 Chat", "📝 Quiz", "💾 History"])

with tabs[0]:
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown("### ⚙️ Settings")
        mode = st.selectbox("Select Mode", ["Simple (Like I'm 5)", "Normal", "Detailed"])
    
    with col1:
        st.markdown("### 💬 Ask your question")
        user_input = st.text_area("", height=100, placeholder="Example: What is Python? Explain loops...")
        
        if st.button("🚀 Ask AI", use_container_width=True) and user_input:
            with st.spinner("🧠 AI is thinking..."):
                answer = ask_ai(user_input, mode)
                st.session_state.chat.append({"q": user_input, "a": answer, "time": datetime.now().strftime("%H:%M")})
                st.rerun()
    
    st.markdown("---")
    st.markdown("### 💬 Conversation")
    
    if len(st.session_state.chat) == 0:
        st.info("No messages yet. Ask me something!")
    
    for item in reversed(st.session_state.chat[-20:]):
        st.markdown(f'<div class="user-msg"><strong>🧑‍🎓 You</strong> <span style="color:gray;font-size:10px;">{item.get("time", "")}</span><br>{item["q"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ai-msg"><strong>🤖 AI Teacher</strong><br>{item["a"]}</div>', unsafe_allow_html=True)
        st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat = []
            st.rerun()
    with col2:
        if st.button("📥 Download Chat", use_container_width=True):
            chat_content = download_chat()
            b64 = base64.b64encode(chat_content.encode()).decode()
            href = f'<a href="data:text/plain;base64,{b64}" download="chat_history.txt">📁 Click to Download</a>'
            st.markdown(href, unsafe_allow_html=True)

with tabs[1]:
    st.markdown("### 📝 Quiz Generator")
    
    quiz_topic = st.text_input("Quiz Topic:", placeholder="Python, AI, History, Science...")
    num_q = st.slider("Number of Questions:", 3, 8, 5)
    
    if st.button("🎯 Generate Quiz", use_container_width=True) and quiz_topic:
        with st.spinner("Creating quiz..."):
            prompt = f"Generate {num_q} multiple choice questions about {quiz_topic}. Format each question like this:\n\n1. What is Python?\nA) A snake\nB) A programming language\nC) A game\nD) A car\nAnswer: B\n\nCreate simple questions."
            
            data = {
                "model": "mistral-small-latest",
                "messages": [{"role": "user", "content": prompt}]
            }
            response = requests.post(url, json=data, headers=headers)
            quiz_raw = response.json()["choices"][0]["message"]["content"]
            
            st.session_state.quiz_questions = []
            st.session_state.quiz_answers = {}
            st.session_state.quiz_topic = quiz_topic
            
            lines = quiz_raw.split('\n')
            current_q = {}
            for line in lines:
                line = line.strip()
                if line and line[0].isdigit() and '.' in line:
                    if current_q:
                        st.session_state.quiz_questions.append(current_q)
                    current_q = {'question': line, 'options': []}
                elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                    if current_q:
                        current_q['options'].append(line)
                elif line.startswith('Answer:'):
                    if current_q:
                        current_q['answer'] = line.split(':')[1].strip()
            
            if current_q:
                st.session_state.quiz_questions.append(current_q)
            
            st.rerun()
    
    if st.session_state.quiz_questions:
        st.markdown("---")
        st.markdown(f"### 📋 Quiz: {st.session_state.quiz_topic}")
        
        for i, q in enumerate(st.session_state.quiz_questions):
            with st.container():
                st.markdown(f'<div class="quiz-card"><b>{q["question"]}</b></div>', unsafe_allow_html=True)
                
                if q.get('options'):
                    answer = st.radio("Select answer:", q['options'], key=f"quiz_{i}", index=None, label_visibility="collapsed")
                    if answer:
                        st.session_state.quiz_answers[f"q{i}"] = answer
        
        if st.button("✅ Submit Quiz", use_container_width=True):
            st.balloons()
            st.success(f"🎉 Quiz Submitted! Check your answers above.")
            
            with st.expander("📊 Quiz Results"):
                for i, q in enumerate(st.session_state.quiz_questions):
                    user_ans = st.session_state.quiz_answers.get(f"q{i}", "Not answered")
                    correct_ans = q.get('answer', 'N/A')
                    st.write(f"**Q{i+1}:** {q['question'][:50]}...")
                    st.write(f"Your answer: {user_ans}")
                    st.write(f"Correct answer: {correct_ans}")
                    st.write("---")
        
        if st.button("🗑️ Clear Quiz", use_container_width=True):
            st.session_state.quiz_questions = []
            st.session_state.quiz_answers = {}
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 🔥 Popular Quiz Topics")
    popular_topics = ["Python", "Machine Learning", "World History", "Science", "English Grammar", "JavaScript"]
    cols = st.columns(3)
    for i, topic in enumerate(popular_topics):
        with cols[i % 3]:
            if st.button(topic, use_container_width=True):
                with st.spinner("Creating quiz..."):
                    prompt = f"Generate 5 multiple choice questions about {topic}. Format: 1. Question\nA) Option\nB) Option\nC) Option\nD) Option\nAnswer: Letter"
                    
                    data = {
                        "model": "mistral-small-latest",
                        "messages": [{"role": "user", "content": prompt}]
                    }
                    response = requests.post(url, json=data, headers=headers)
                    quiz_raw = response.json()["choices"][0]["message"]["content"]
                    
                    st.session_state.quiz_questions = []
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_topic = topic
                    
                    lines = quiz_raw.split('\n')
                    current_q = {}
                    for line in lines:
                        line = line.strip()
                        if line and line[0].isdigit() and '.' in line:
                            if current_q:
                                st.session_state.quiz_questions.append(current_q)
                            current_q = {'question': line, 'options': []}
                        elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                            if current_q:
                                current_q['options'].append(line)
                        elif line.startswith('Answer:'):
                            if current_q:
                                current_q['answer'] = line.split(':')[1].strip()
                    
                    if current_q:
                        st.session_state.quiz_questions.append(current_q)
                    
                    st.rerun()

with tabs[2]:
    st.markdown("### 💾 Chat History")
    
    if len(st.session_state.chat) > 0:
        st.markdown(f"**Total Messages:** {len(st.session_state.chat)}")
        
        st.markdown("---")
        st.markdown("### 📜 Recent Conversations")
        
        for i, msg in enumerate(reversed(st.session_state.chat[-15:])):
            with st.expander(f"Q: {msg['q'][:50]}..."):
                st.markdown(f"**🧑‍🎓 Question:** {msg['q']}")
                st.markdown(f"**🤖 Answer:** {msg['a'][:500]}...")
                st.caption(f"Time: {msg.get('time', 'N/A')}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export All Chats", use_container_width=True):
                chat_content = download_chat()
                b64 = base64.b64encode(chat_content.encode()).decode()
                href = f'<a href="data:text/plain;base64,{b64}" download="full_chat_history.txt">📁 Download</a>'
                st.markdown(href, unsafe_allow_html=True)
        with col2:
            if st.button("🗑️ Delete All History", use_container_width=True):
                st.session_state.chat = []
                st.session_state.quiz_questions = []
                st.session_state.quiz_answers = {}
                st.rerun()
    else:
        st.info("No chat history yet. Start a conversation!")

st.markdown("""
<div style="text-align: center; color: #6b7280; margin-top: 2rem; padding: 1rem;">
    Made with ❤️ using Mistral AI | AI Study Buddy Pro
</div>
""", unsafe_allow_html=True)