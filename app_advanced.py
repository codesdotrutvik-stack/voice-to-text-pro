import streamlit as st
import requests
import json
from datetime import datetime
import base64

api_key = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"
url = "https://api.mistral.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="wide")

custom_css = """
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.main-header {
    text-align: center;
    padding: 2rem;
    background: rgba(255,255,255,0.1);
    border-radius: 20px;
    margin-bottom: 2rem;
}
.chat-message {
    padding: 1rem;
    border-radius: 15px;
    margin-bottom: 1rem;
    animation: fadeIn 0.5s;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.user-message {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
}
.assistant-message {
    background: rgba(255,255,255,0.95);
    color: #333;
    border-left: 5px solid #667eea;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>📚 AI Study Buddy Pro</h1>
    <p>Your Personal AI Teacher – Learn Anything, Anytime!</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### ⚙️ Settings")
    mode = st.selectbox("Learning Mode", ["Normal", "Explain like I'm 5", "Expert Mode", "Exam Preparation"])
    theme = st.toggle("🌙 Dark Mode", value=False)
    voice_output = st.toggle("🔊 Voice Output", value=False)

with col1:
    tabs = st.tabs(["💬 Chat", "📝 Quiz", "📚 Topics", "💾 History"])

def ask_ai(question, mode):
    if mode == "Explain like I'm 5":
        system_prompt = "You are a teacher. Explain like the student is 5 years old. Use very simple words. Short sentences. Be fun and engaging!"
    elif mode == "Expert Mode":
        system_prompt = "You are an expert. Give detailed, technical, and comprehensive explanations."
    elif mode == "Exam Preparation":
        system_prompt = "You are an exam trainer. Give concise answers suitable for exams. Include key points."
    else:
        system_prompt = "You are a helpful teacher. Explain clearly and simply. Be encouraging."
    
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

with tabs[0]:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">🧑‍🎓 <strong>You:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message">🤖 <strong>AI Teacher:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
    
    user_input = st.text_area("✏️ Type your question here...", height=100)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1,1,4])
    with col_btn1:
        if st.button("🚀 Ask", use_container_width=True):
            if user_input:
                with st.spinner("🧠 AI is thinking..."):
                    answer = ask_ai(user_input, mode)
                    st.session_state.chat_history.append({"role": "user", "content": user_input})
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    if voice_output:
                        st.audio(generate_speech(answer), format="audio/mp3")
                    st.rerun()
    with col_btn2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

with tabs[1]:
    st.markdown("### 📝 Quiz Generator")
    topic = st.text_input("Quiz Topic:", placeholder="e.g., Python Loops, Solar System, World War II")
    num_questions = st.slider("Number of Questions:", 3, 15, 5)
    difficulty = st.selectbox("Difficulty:", ["Easy", "Medium", "Hard"])
    
    if st.button("🎯 Generate Quiz", use_container_width=True):
        if topic:
            with st.spinner("Creating quiz..."):
                quiz_prompt = f"Generate {num_questions} multiple choice questions about {topic}. Difficulty: {difficulty}. Format: Q1: question\nA) option1\nB) option2\nC) option3\nD) option4\nAnswer: X"
                quiz_data = ask_ai(quiz_prompt, "Normal")
                st.session_state.quiz = quiz_data
                st.session_state.quiz_topic = topic
                st.success("✅ Quiz ready!")
    
    if "quiz" in st.session_state:
        st.markdown("---")
        st.markdown("### 📋 Your Quiz")
        st.write(st.session_state.quiz)
        
        user_answer = st.text_input("Your answer (A/B/C/D):")
        if st.button("✅ Check Answer"):
            check_prompt = f"Question: {st.session_state.quiz}\nUser answer: {user_answer}\nIs this correct? Tell yes/no and give explanation."
            check_result = ask_ai(check_prompt, "Normal")
            st.info(check_result)

with tabs[2]:
    st.markdown("### 📚 Quick Topics to Learn")
    
    quick_topics = {
        "🐍 Python": "Python is a programming language. It's easy to learn and very powerful.",
        "🤖 AI": "AI means machines that can think and learn like humans.",
        "🧮 Maths": "Mathematics is the study of numbers, shapes, and patterns.",
        "🔬 Science": "Science helps us understand how the world works.",
        "🌍 History": "History is the story of what happened in the past.",
        "💻 Web Dev": "Web development is building websites and web applications."
    }
    
    cols = st.columns(3)
    for i, (topic_name, description) in enumerate(quick_topics.items()):
        with cols[i % 3]:
            if st.button(topic_name, use_container_width=True):
                answer = ask_ai(f"Explain {topic_name} simply", mode)
                st.session_state.chat_history.append({"role": "user", "content": f"Tell me about {topic_name}"})
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.success(f"Added to chat! Go to Chat tab to see answer.")
    
    st.markdown("---")
    st.markdown("### 🔥 Trending Topics")
    trending = ["Machine Learning", "Data Science", "Web3", "Cybersecurity", "Cloud Computing", "Blockchain"]
    for topic in trending:
        if st.button(topic):
            answer = ask_ai(f"Explain {topic} in simple words", mode)
            st.session_state.chat_history.append({"role": "user", "content": f"What is {topic}?"})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.success(f"Added to chat!")

with tabs[3]:
    st.markdown("### 💾 Chat History")
    
    if st.button("📥 Download Chat History"):
        chat_text = "\n\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.chat_history])
        b64 = base64.b64encode(chat_text.encode()).decode()
        href = f'<a href="data:text/plain;base64,{b64}" download="chat_history.txt">📁 Click to Download</a>'
        st.markdown(href, unsafe_allow_html=True)
    
    if st.button("🗑️ Delete All History"):
        st.session_state.chat_history = []
        st.success("Chat history deleted!")
    
    if st.session_state.chat_history:
        st.markdown("### Recent Conversations")
        for i, msg in enumerate(reversed(st.session_state.chat_history[-10:])):
            st.text(f"{msg['role'].upper()}: {msg['content'][:100]}...")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.7);">
    Made with ❤️ using Mistral AI | AI Study Buddy Pro
</div>
""", unsafe_allow_html=True)