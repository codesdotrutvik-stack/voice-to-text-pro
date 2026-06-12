import streamlit as st
import requests
from datetime import datetime
import json
import base64

api_key = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"
url = "https://api.mistral.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="AI Study Buddy", page_icon="✨", layout="wide")

# Agent tools
def agent_add(a, b):
    return a + b

def agent_multiply(a, b):
    return a * b

def agent_time():
    return datetime.now().strftime("%I:%M %p, %B %d")

def agent_capitalize(text):
    return text.upper()

if "chat" not in st.session_state:
    st.session_state.chat = []
if "agent_history" not in st.session_state:
    st.session_state.agent_history = []

def ask_ai(question, mode):
    if mode == "Simple":
        prompt = "Explain like the student is 5 years old. Very simple words."
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

# Custom CSS
st.markdown("""
<style>
    .main-header h1 {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .user-msg {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 18px;
        margin: 5px 0;
        max-width: 80%;
        margin-left: auto;
    }
    .ai-msg {
        background: #f1f5f9;
        padding: 10px 15px;
        border-radius: 18px;
        margin: 5px 0;
        max-width: 80%;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>✨ AI Study Buddy Pro</h1></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    mode = st.selectbox("Mode", ["Normal", "Simple", "Detailed"])
    
    st.markdown("---")
    st.markdown("### 📚 Quick Topics")
    topics = ["Python", "AI", "Math", "Science", "History"]
    for topic in topics:
        if st.button(topic, key=f"side_{topic}"):
            answer = ask_ai(f"Explain {topic} simply", mode)
            st.session_state.chat.append({"q": f"Explain {topic}", "a": answer})
            st.rerun()
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat = []
        st.rerun()

tabs = st.tabs(["💬 Chat", "🤖 AI Agent", "💾 History"])

with tabs[0]:
    user_input = st.text_area("Ask anything...", height=80, key="chat_input")
    
    if st.button("✨ Ask") and user_input:
        with st.spinner("Thinking..."):
            answer = ask_ai(user_input, mode)
            st.session_state.chat.append({"q": user_input, "a": answer})
            st.rerun()
    
    for item in reversed(st.session_state.chat[-15:]):
        st.markdown(f'<div class="user-msg"><strong>You</strong><br>{item["q"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ai-msg"><strong>AI</strong><br>{item["a"]}</div>', unsafe_allow_html=True)

with tabs[1]:
    st.markdown("### 🤖 AI Agent with Tools")
    
    st.info("""
    **Available Tools:**
    - 🔢 `add` numbers (e.g., "add 5 and 3")
    - ✖️ `multiply` numbers (e.g., "multiply 4 by 5")
    - ⏰ `time` (e.g., "what time is it?")
    - 🔤 `uppercase` (e.g., "make this uppercase: hello")
    """)
    
    agent_input = st.text_input("Ask the agent:", key="agent_input", placeholder="Example: add 10 and 20")
    
    if st.button("🚀 Run Agent"):
        if agent_input:
            response = None
            
            if "add" in agent_input.lower() or "+" in agent_input:
                numbers = [int(s) for s in agent_input.split() if s.isdigit()]
                if len(numbers) >= 2:
                    response = f"🧮 {numbers[0]} + {numbers[1]} = {agent_add(numbers[0], numbers[1])}"
                else:
                    response = "⚠️ Please give me two numbers to add"
            
            elif "multiply" in agent_input.lower() or "*" in agent_input or "×" in agent_input:
                numbers = [int(s) for s in agent_input.split() if s.isdigit()]
                if len(numbers) >= 2:
                    response = f"✖️ {numbers[0]} × {numbers[1]} = {agent_multiply(numbers[0], numbers[1])}"
                else:
                    response = "⚠️ Please give me two numbers to multiply"
            
            elif "time" in agent_input.lower():
                response = f"⏰ {agent_time()}"
            
            elif "uppercase" in agent_input.lower() or "capitalize" in agent_input.lower():
                text = agent_input.replace("uppercase", "").replace("capitalize", "").strip()
                if text:
                    response = f"🔤 Uppercase: {agent_capitalize(text)}"
                else:
                    response = "⚠️ Please provide text to convert"
            
            else:
                with st.spinner("Thinking..."):
                    data = {
                        "model": "mistral-small-latest",
                        "messages": [{"role": "user", "content": agent_input}]
                    }
                    resp = requests.post(url, json=data, headers=headers)
                    response = resp.json()["choices"][0]["message"]["content"]
            
            if response:
                st.success(response)
                st.session_state.agent_history.append({"q": agent_input, "a": response})
    
    if st.session_state.agent_history:
        st.markdown("---")
        st.markdown("### 📜 Agent History")
        for item in reversed(st.session_state.agent_history[-10:]):
            st.markdown(f"**You:** {item['q']}")
            st.markdown(f"**Agent:** {item['a']}")
            st.markdown("---")

with tabs[2]:
    if st.session_state.chat:
        chat_text = "\n\n".join([f"You: {c['q']}\nAI: {c['a']}" for c in st.session_state.chat])
        b64 = base64.b64encode(chat_text.encode()).decode()
        st.markdown(f'<a href="data:text/plain;base64,{b64}" download="chat_history.txt">📥 Download Chat</a>', unsafe_allow_html=True)
        
        if st.button("🗑️ Clear All History"):
            st.session_state.chat = []
            st.session_state.agent_history = []
            st.rerun()
    else:
        st.info("No chat history yet")

st.markdown("---")
st.caption("✨ Made with Mistral AI | AI Study Buddy Pro")