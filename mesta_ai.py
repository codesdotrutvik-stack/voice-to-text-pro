import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Mesta AI", page_icon="✨", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
    background: #0d0d0f !important;
    color: #e2e8f0 !important;
}

#MainMenu, footer, header { visibility: hidden !important; display: none !important; }

.block-container {
    padding: 2rem 3rem 5rem !important;
    max-width: 900px !important;
}

/* ── HEADER ── */
.mesta-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2.5rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}

.header-left { display: flex; align-items: center; gap: 14px; }

.header-logo {
    width: 46px; height: 46px;
    background: linear-gradient(135deg, #a78bfa, #7c3aed);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    box-shadow: 0 0 24px rgba(139,92,246,0.35);
}

.header-title {
    font-size: 1.3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #c4b5fd, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.header-sub { font-size: 0.68rem; color: #64748b; margin-top: 2px; }

.header-right { display: flex; align-items: center; gap: 10px; }

.badge {
    font-size: 0.68rem;
    background: rgba(139,92,246,0.15);
    border: 1px solid rgba(139,92,246,0.3);
    padding: 4px 12px;
    border-radius: 20px;
    color: #a78bfa;
    font-weight: 600;
}

.status-dot {
    width: 8px; height: 8px;
    background: #22c55e;
    border-radius: 50%;
    box-shadow: 0 0 6px #22c55e;
    display: inline-block;
    margin-right: 6px;
}

/* ── MODE TOGGLE ── */
.mode-toggle-wrap {
    display: flex;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 50px;
    padding: 4px;
    gap: 4px;
    margin-bottom: 1.8rem;
    width: fit-content;
}

.mode-btn {
    padding: 8px 24px;
    border-radius: 50px;
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    border: none;
    transition: all 0.2s;
    color: #64748b;
    background: transparent;
}

.mode-btn.active {
    background: linear-gradient(135deg, #7c3aed, #6d28d9);
    color: white;
    box-shadow: 0 0 16px rgba(124,58,237,0.4);
}

/* ── INPUT AREA ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 50px !important;
    padding: 14px 22px !important;
    color: #e2e8f0 !important;
    font-size: 0.92rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: border 0.2s !important;
}

.stTextInput > div > div > input::placeholder { color: #475569 !important; }

.stTextInput > div > div > input:focus {
    border-color: rgba(139,92,246,0.5) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important;
    outline: none !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #94a3b8 !important;
    border-radius: 50px !important;
    padding: 9px 22px !important;
    font-size: 0.82rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.18) !important;
    color: #e2e8f0 !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 0 18px rgba(124,58,237,0.35) !important;
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 26px rgba(124,58,237,0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── CHAT BUBBLES ── */
.user-bubble {
    background: linear-gradient(135deg, #7c3aed, #6d28d9);
    color: white;
    padding: 13px 18px;
    border-radius: 20px;
    border-bottom-right-radius: 4px;
    margin: 10px 0;
    margin-left: auto;
    max-width: 72%;
    font-size: 0.9rem;
    line-height: 1.5;
    text-align: right;
    box-shadow: 0 4px 20px rgba(124,58,237,0.25);
}

.ai-bubble {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #e2e8f0;
    padding: 13px 18px;
    border-radius: 20px;
    border-bottom-left-radius: 4px;
    margin: 10px 0;
    max-width: 72%;
    font-size: 0.9rem;
    line-height: 1.5;
}

.ai-name {
    font-size: 0.7rem;
    font-weight: 600;
    color: #a78bfa;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 5px;
}

.timestamp {
    font-size: 0.6rem;
    color: #475569;
    margin-top: 6px;
}

/* ── SECTION LABELS ── */
.section-label {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #475569;
    margin: 1.8rem 0 0.9rem 0;
}

/* ── QUICK QUESTIONS ── */
.stButton > button[data-testid] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    color: #94a3b8 !important;
    border-radius: 12px !important;
    font-size: 0.8rem !important;
    padding: 10px 14px !important;
}

/* ── DIVIDER ── */
.divider {
    height: 1px;
    background: rgba(255,255,255,0.06);
    margin: 1.5rem 0;
}

/* ── FOOTER ── */
.footer {
    text-align: center;
    font-size: 0.62rem;
    color: #334155;
    padding: 2rem;
    margin-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    letter-spacing: 0.5px;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: #7c3aed !important; }

/* ── INFO / SUCCESS boxes ── */
.stAlert {
    background: rgba(124,58,237,0.08) !important;
    border: 1px solid rgba(124,58,237,0.2) !important;
    border-radius: 12px !important;
    color: #a78bfa !important;
}
</style>
""", unsafe_allow_html=True)

# ── CONFIG ──
MISTRAL_API_KEY = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pending_audio" not in st.session_state:
    st.session_state.pending_audio = None
if "output_mode" not in st.session_state:
    st.session_state.output_mode = "text"

# ── HEADER ──
st.markdown("""
<div class="mesta-header">
    <div class="header-left">
        <div class="header-logo">✨</div>
        <div>
            <div class="header-title">Mesta AI</div>
            <div class="header-sub">Your personal intelligent assistant</div>
        </div>
    </div>
    <div class="header-right">
        <span><span class="status-dot"></span><span style="font-size:0.7rem;color:#475569;">Online</span></span>
        <span class="badge">v2.0</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── OUTPUT MODE TOGGLE ──
st.markdown('<div class="section-label">⚙️ Response Mode</div>', unsafe_allow_html=True)
col_t, col_v, col_blank = st.columns([1, 1, 4])
with col_t:
    if st.button(
        "📝  Text" if st.session_state.output_mode != "text" else "✅  Text",
        use_container_width=True,
        type="primary" if st.session_state.output_mode == "text" else "secondary"
    ):
        st.session_state.output_mode = "text"
        st.rerun()
with col_v:
    if st.button(
        "🔊  Voice" if st.session_state.output_mode != "voice" else "✅  Voice",
        use_container_width=True,
        type="primary" if st.session_state.output_mode == "voice" else "secondary"
    ):
        st.session_state.output_mode = "voice"
        st.rerun()

mode_label = "📝 Text replies only" if st.session_state.output_mode == "text" else "🔊 Voice + Text replies"
st.markdown(f'<div style="font-size:0.75rem;color:#475569;margin-bottom:1.2rem;padding-left:4px;">{mode_label}</div>', unsafe_allow_html=True)

# ── TTS FUNCTION ──
def speak_text(text):
    safe_text = text.replace("'", "\\'").replace("\n", " ").replace('"', '\\"')
    return f"""
    <script>
    (function() {{
        try {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance('{safe_text}');
            msg.lang = 'en-US';
            msg.rate = 1.0;
            msg.pitch = 1.05;
            msg.volume = 1.0;
            var voices = window.speechSynthesis.getVoices();
            var preferred = voices.find(v => v.name.includes('Google') || v.name.includes('Samantha') || v.name.includes('Daniel'));
            if (preferred) msg.voice = preferred;
            window.speechSynthesis.speak(msg);
        }} catch(e) {{ console.log('TTS error:', e); }}
    }})();
    </script>
    """

# ── API FUNCTION ──
def ask_mistral(question):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": "You are Mesta AI, a sleek and intelligent personal assistant. Answer clearly and concisely in 2-3 sentences."},
            {"role": "user", "content": question}
        ],
        "max_tokens": 200
    }
    try:
        response = requests.post(MISTRAL_URL, json=data, headers=headers, timeout=15)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Connection issue: {str(e)}"

# ── PLAY PENDING AUDIO ──
if st.session_state.pending_audio:
    st.components.v1.html(st.session_state.pending_audio, height=0)
    st.session_state.pending_audio = None

# ── INPUT ──
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">💬 Ask Mesta</div>', unsafe_allow_html=True)

user_question = st.text_input(
    "", placeholder="Ask me anything...",
    key="text_input", label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1.2, 1.5, 3])
with col1:
    ask_clicked = st.button("✨ Ask Mesta", use_container_width=True, type="primary")
with col2:
    clear_clicked = st.button("🗑️ Clear Chat", use_container_width=True)

# ── PROCESS ──
def process_question(q):
    answer = ask_mistral(q)
    st.session_state.chat_history.append({
        "q": q, "a": answer,
        "t": datetime.now().strftime("%I:%M %p"),
        "mode": st.session_state.output_mode
    })
    if st.session_state.output_mode == "voice":
        st.session_state.pending_audio = speak_text(answer)
    st.rerun()

if ask_clicked and user_question:
    with st.spinner("✨ Thinking..."):
        process_question(user_question)

if clear_clicked:
    st.session_state.chat_history = []
    st.session_state.pending_audio = None
    st.rerun()

# ── QUICK QUESTIONS ──
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">⚡ Quick Questions</div>', unsafe_allow_html=True)

quick_qs = [
    "Who are you?", "What can you do?",
    "Tell me something inspiring", "Future of AI",
    "What is machine learning?", "Tell me a joke"
]

cols = st.columns(3)
for i, q in enumerate(quick_qs):
    with cols[i % 3]:
        if st.button(q, use_container_width=True, key=f"qq_{i}"):
            with st.spinner("✨ Thinking..."):
                process_question(q)

# ── CONVERSATION ──
if st.session_state.chat_history:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">💬 Conversation</div>', unsafe_allow_html=True)

    for chat in reversed(st.session_state.chat_history[-15:]):
        voice_tag = ' 🔊' if chat.get("mode") == "voice" else ''
        st.markdown(
            f'<div class="user-bubble"><strong>You</strong><br>{chat["q"]}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'''<div class="ai-bubble">
                <div class="ai-name">✨ Mesta{voice_tag}</div>
                {chat["a"]}
                <div class="timestamp">{chat["t"]}</div>
            </div>''',
            unsafe_allow_html=True
        )

# ── FOOTER ──
st.markdown(
    '<div class="footer">✨ MESTA AI &nbsp;·&nbsp; Created by Nirbhay &nbsp;·&nbsp; Powered by Mistral AI</div>',
    unsafe_allow_html=True
)