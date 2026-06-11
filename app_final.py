import streamlit as st
import requests
import pyttsx3
import threading

api_key = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"
url = "https://api.mistral.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="AI Study Buddy", page_icon="📚")

st.title("📚 AI Study Buddy")
st.markdown("---")

if "chat" not in st.session_state:
    st.session_state.chat = []

def ask_ai(question, mode):
    if mode == "Simple":
        prompt = "Explain like the student is 5 years old. Very simple words."
    elif mode == "Detailed":
        prompt = "Explain clearly and thoroughly with examples."
    else:
        prompt = "Explain in simple language."
    
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

def speak_text(text):
    def _speak():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    thread = threading.Thread(target=_speak)
    thread.start()

col1, col2 = st.columns([3, 1])

with col2:
    mode = st.selectbox("Mode", ["Simple", "Normal", "Detailed"])
    voice = st.checkbox("🔊 Voice Output")

with col1:
    user_input = st.text_area("💬 Your question:", height=100, placeholder="Type anything you want to learn...")
    
    if st.button("🚀 Ask AI", use_container_width=True):
        if user_input:
            with st.spinner("Thinking..."):
                answer = ask_ai(user_input, mode)
                st.session_state.chat.append({"q": user_input, "a": answer})
                if voice:
                    speak_text(answer)
                st.rerun()

st.markdown("---")
st.subheader("💬 Conversation")

for i, item in enumerate(reversed(st.session_state.chat)):
    st.markdown(f"**🧑‍🎓 You:** {item['q']}")
    st.markdown(f"**🤖 AI:** {item['a']}")
    st.markdown("---")

if st.button("🗑️ Clear Chat"):
    st.session_state.chat = []
    st.rerun()

st.markdown("---")
st.markdown("### 📚 Quick Topics")

topics = ["Python", "AI", "Maths", "Science", "History", "Cricket", "Bollywood", "Gujarati"]
cols = st.columns(4)
for i, topic in enumerate(topics):
    with cols[i % 4]:
        if st.button(topic):
            answer = ask_ai(f"Explain {topic} in simple words", mode)
            st.session_state.chat.append({"q": f"Tell me about {topic}", "a": answer})
            st.rerun()

st.markdown("---")
st.caption("Made with NIRBHAY | AI Study Buddy")