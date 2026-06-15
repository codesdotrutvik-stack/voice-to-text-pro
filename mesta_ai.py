import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Mesta AI", page_icon="✦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #07080f !important;
    color: #e2e8f0 !important;
}

#MainMenu, footer, header { visibility: hidden !important; display: none !important; }

.block-container {
    padding: 0 2.5rem 5rem !important;
    max-width: 880px !important;
}

/* HEADER */
.mesta-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.4rem 0 1.2rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 0;
}
.header-left { display: flex; align-items: center; gap: 12px; }
.header-logo {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #a78bfa, #7c3aed);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    box-shadow: 0 0 18px rgba(124,58,237,0.4);
}
.header-title { font-size: 1.1rem; font-weight: 700; color: #f1f5f9; }
.header-sub { font-size: 0.67rem; color: #475569; margin-top: 1px; }
.online-dot {
    width: 7px; height: 7px;
    background: #22c55e;
    border-radius: 50%;
    box-shadow: 0 0 6px #22c55e;
    display: inline-block;
}
.model-badge {
    font-size: 0.67rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    padding: 4px 12px;
    border-radius: 20px;
    color: #64748b;
}

/* HERO */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
}
.hero-greeting {
    font-size: 2.1rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #818cf8, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.4rem;
}
.hero-sub { font-size: 0.9rem; color: #475569; margin-bottom: 1.5rem; }

/* WAVE ANIMATION */
.wave-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    height: 60px;
    margin: 0.5rem auto 1.5rem auto;
    width: 200px;
}
.wave-bar {
    width: 4px;
    border-radius: 4px;
    background: linear-gradient(to top, #7c3aed, #a78bfa);
    animation: wave-idle 1.4s ease-in-out infinite;
    height: 8px;
}
.wave-bar:nth-child(1)  { animation-delay: 0.0s; }
.wave-bar:nth-child(2)  { animation-delay: 0.1s; }
.wave-bar:nth-child(3)  { animation-delay: 0.2s; }
.wave-bar:nth-child(4)  { animation-delay: 0.3s; }
.wave-bar:nth-child(5)  { animation-delay: 0.4s; }
.wave-bar:nth-child(6)  { animation-delay: 0.3s; }
.wave-bar:nth-child(7)  { animation-delay: 0.2s; }
.wave-bar:nth-child(8)  { animation-delay: 0.1s; }
.wave-bar:nth-child(9)  { animation-delay: 0.0s; }
.wave-bar:nth-child(10) { animation-delay: 0.15s; }
.wave-bar:nth-child(11) { animation-delay: 0.25s; }
.wave-bar:nth-child(12) { animation-delay: 0.35s; }

@keyframes wave-idle {
    0%, 100% { height: 8px;  opacity: 0.3; }
    50%       { height: 14px; opacity: 0.6; }
}

.wave-container.speaking .wave-bar {
    animation: wave-speak 0.6s ease-in-out infinite;
}
.wave-container.speaking .wave-bar:nth-child(odd)  { animation-duration: 0.5s; }
.wave-container.speaking .wave-bar:nth-child(even) { animation-duration: 0.7s; }
.wave-container.speaking .wave-bar:nth-child(1)  { animation-delay: 0.0s; }
.wave-container.speaking .wave-bar:nth-child(2)  { animation-delay: 0.05s; }
.wave-container.speaking .wave-bar:nth-child(3)  { animation-delay: 0.1s; }
.wave-container.speaking .wave-bar:nth-child(4)  { animation-delay: 0.15s; }
.wave-container.speaking .wave-bar:nth-child(5)  { animation-delay: 0.2s; }
.wave-container.speaking .wave-bar:nth-child(6)  { animation-delay: 0.15s; }
.wave-container.speaking .wave-bar:nth-child(7)  { animation-delay: 0.1s; }
.wave-container.speaking .wave-bar:nth-child(8)  { animation-delay: 0.05s; }
.wave-container.speaking .wave-bar:nth-child(9)  { animation-delay: 0.0s; }
.wave-container.speaking .wave-bar:nth-child(10) { animation-delay: 0.08s; }
.wave-container.speaking .wave-bar:nth-child(11) { animation-delay: 0.12s; }
.wave-container.speaking .wave-bar:nth-child(12) { animation-delay: 0.18s; }

@keyframes wave-speak {
    0%, 100% { height: 10px; }
    50%       { height: 48px; }
}

.wave-status {
    font-size: 0.72rem;
    color: #475569;
    text-align: center;
    margin-top: -0.8rem;
    margin-bottom: 1rem;
    letter-spacing: 0.5px;
}
.wave-status.active { color: #a78bfa; }

/* INPUT — FULLY DARK */
.stTextInput > div > div > input {
    background: #13141f !important;
    border: 1px solid rgba(139,92,246,0.25) !important;
    border-radius: 50px !important;
    padding: 15px 24px !important;
    color: #f1f5f9 !important;
    font-size: 0.93rem !important;
    font-family: 'Inter', sans-serif !important;
    caret-color: #a78bfa !important;
    -webkit-text-fill-color: #f1f5f9 !important;
}
.stTextInput > div > div > input::placeholder {
    color: #2d3748 !important;
    -webkit-text-fill-color: #2d3748 !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(139,92,246,0.55) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.1) !important;
    background: #16172a !important;
    outline: none !important;
}

/* BUTTONS */
.stButton > button {
    background: #13141f !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #64748b !important;
    border-radius: 50px !important;
    padding: 9px 22px !important;
    font-size: 0.82rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #1e1f2e !important;
    color: #e2e8f0 !important;
    border-color: rgba(255,255,255,0.15) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 0 22px rgba(124,58,237,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 32px rgba(124,58,237,0.55) !important;
}

/* VOICE TYPE PILLS */
.voice-pills {
    display: flex;
    gap: 8px;
    justify-content: center;
    margin-bottom: 1.6rem;
    flex-wrap: wrap;
}
.voice-pill {
    padding: 7px 18px;
    border-radius: 30px;
    font-size: 0.78rem;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid rgba(255,255,255,0.09);
    background: #13141f;
    color: #64748b;
    transition: all 0.2s;
}
.voice-pill.active {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    border-color: transparent;
    color: white;
    box-shadow: 0 0 16px rgba(124,58,237,0.35);
}

/* QUICK QUESTIONS */
.section-label {
    font-size: 0.63rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #2d3748;
    margin: 1.6rem 0 0.9rem 0;
}
.divider {
    height: 1px;
    background: rgba(255,255,255,0.04);
    margin: 1.2rem 0;
}

/* CHAT BUBBLES */
.user-bubble {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white;
    padding: 13px 18px;
    border-radius: 20px 20px 4px 20px;
    margin: 10px 0;
    margin-left: auto;
    max-width: 70%;
    font-size: 0.88rem;
    line-height: 1.55;
    text-align: right;
    box-shadow: 0 4px 20px rgba(124,58,237,0.2);
}
.ai-bubble {
    background: #13141f;
    border: 1px solid rgba(255,255,255,0.07);
    color: #e2e8f0;
    padding: 13px 18px;
    border-radius: 20px 20px 20px 4px;
    margin: 10px 0;
    max-width: 70%;
    font-size: 0.88rem;
    line-height: 1.55;
}
.ai-name {
    font-size: 0.68rem;
    font-weight: 600;
    color: #a78bfa;
    margin-bottom: 6px;
    display: flex; align-items: center; gap: 5px;
}
.msg-time { font-size: 0.6rem; color: #2d3748; margin-top: 6px; }

/* MODE INDICATOR */
.mode-indicator {
    font-size: 0.72rem;
    color: #334155;
    margin-bottom: 1rem;
}

/* FOOTER */
.footer {
    text-align: center;
    font-size: 0.6rem;
    color: #1e293b;
    padding: 2rem;
    margin-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.03);
    letter-spacing: 1px;
    text-transform: uppercase;
}

.stSpinner > div { border-top-color: #7c3aed !important; }
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
if "voice_type" not in st.session_state:
    st.session_state.voice_type = "man"

# ── HEADER ──
st.markdown("""
<div class="mesta-header">
    <div class="header-left">
        <div class="header-logo">✦</div>
        <div>
            <div class="header-title">Mesta AI <span style="font-size:0.65rem;color:#7c3aed;">✔</span></div>
            <div class="header-sub">Intelligent Assistant</div>
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
        <span style="display:flex;align-items:center;gap:6px;">
            <span class="online-dot"></span>
            <span style="font-size:0.67rem;color:#334155;">Online</span>
        </span>
        <span class="model-badge">Mistral Small</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HERO + WAVE ──
st.markdown("""
<div class="hero">
    <div class="hero-greeting">Hello, Nirbhay! 👋</div>
    <div class="hero-sub">How can I help you today?</div>
</div>
""", unsafe_allow_html=True)

# Wave animation — JS controls speaking class
st.components.v1.html("""
<div style="text-align:center;">
    <div class="wave-container" id="waveEl">
        <div class="wave-bar"></div><div class="wave-bar"></div>
        <div class="wave-bar"></div><div class="wave-bar"></div>
        <div class="wave-bar"></div><div class="wave-bar"></div>
        <div class="wave-bar"></div><div class="wave-bar"></div>
        <div class="wave-bar"></div><div class="wave-bar"></div>
        <div class="wave-bar"></div><div class="wave-bar"></div>
    </div>
    <div class="wave-status" id="waveStatus">Ready</div>
</div>

<style>
.wave-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    height: 60px;
    margin: 0 auto;
    width: 200px;
}
.wave-bar {
    width: 4px;
    border-radius: 4px;
    background: linear-gradient(to top, #7c3aed, #a78bfa);
    animation: wave-idle 1.4s ease-in-out infinite;
    height: 8px;
}
.wave-bar:nth-child(1)  { animation-delay: 0.0s; }
.wave-bar:nth-child(2)  { animation-delay: 0.1s; }
.wave-bar:nth-child(3)  { animation-delay: 0.2s; }
.wave-bar:nth-child(4)  { animation-delay: 0.3s; }
.wave-bar:nth-child(5)  { animation-delay: 0.4s; }
.wave-bar:nth-child(6)  { animation-delay: 0.3s; }
.wave-bar:nth-child(7)  { animation-delay: 0.2s; }
.wave-bar:nth-child(8)  { animation-delay: 0.1s; }
.wave-bar:nth-child(9)  { animation-delay: 0.0s; }
.wave-bar:nth-child(10) { animation-delay: 0.15s; }
.wave-bar:nth-child(11) { animation-delay: 0.25s; }
.wave-bar:nth-child(12) { animation-delay: 0.35s; }
@keyframes wave-idle {
    0%, 100% { height: 8px;  opacity: 0.3; }
    50%       { height: 14px; opacity: 0.6; }
}
.wave-container.speaking .wave-bar {
    animation: wave-speak 0.55s ease-in-out infinite;
}
.wave-container.speaking .wave-bar:nth-child(1)  { animation-delay: 0.00s; animation-duration: 0.45s; }
.wave-container.speaking .wave-bar:nth-child(2)  { animation-delay: 0.05s; animation-duration: 0.55s; }
.wave-container.speaking .wave-bar:nth-child(3)  { animation-delay: 0.10s; animation-duration: 0.40s; }
.wave-container.speaking .wave-bar:nth-child(4)  { animation-delay: 0.15s; animation-duration: 0.65s; }
.wave-container.speaking .wave-bar:nth-child(5)  { animation-delay: 0.20s; animation-duration: 0.50s; }
.wave-container.speaking .wave-bar:nth-child(6)  { animation-delay: 0.15s; animation-duration: 0.60s; }
.wave-container.speaking .wave-bar:nth-child(7)  { animation-delay: 0.10s; animation-duration: 0.45s; }
.wave-container.speaking .wave-bar:nth-child(8)  { animation-delay: 0.05s; animation-duration: 0.55s; }
.wave-container.speaking .wave-bar:nth-child(9)  { animation-delay: 0.00s; animation-duration: 0.40s; }
.wave-container.speaking .wave-bar:nth-child(10) { animation-delay: 0.08s; animation-duration: 0.50s; }
.wave-container.speaking .wave-bar:nth-child(11) { animation-delay: 0.12s; animation-duration: 0.65s; }
.wave-container.speaking .wave-bar:nth-child(12) { animation-delay: 0.18s; animation-duration: 0.45s; }
@keyframes wave-speak {
    0%, 100% { height: 6px; }
    50%       { height: 50px; }
}
.wave-status {
    font-size: 0.72rem;
    color: #475569;
    margin-top: 6px;
    letter-spacing: 0.5px;
}
.wave-status.active { color: #a78bfa; }
</style>

<script>
window._mestaStartWave = function(text) {
    var el = document.getElementById('waveEl');
    var st = document.getElementById('waveStatus');
    if (!el) return;
    el.classList.add('speaking');
    st.textContent = 'Speaking...';
    st.classList.add('active');
    var duration = Math.max(2000, text.length * 55);
    setTimeout(function() {
        el.classList.remove('speaking');
        st.textContent = 'Ready';
        st.classList.remove('active');
    }, duration);
};
window.addEventListener('message', function(e) {
    if (e.data && e.data.type === 'mesta_speak') {
        window._mestaStartWave(e.data.text || '');
    }
});
</script>
""", height=100)

# ── TTS + WAVE ──
def speak_text(text, voice_type="man"):
    safe = text.replace("'", "\\'").replace("\n", " ").replace('"', '\\"')
    voice_logic = ""
    if voice_type == "man":
        voice_logic = """
        var v = voices.find(function(v) {
            return v.lang.startsWith('en') && v.name.match(/male|man|david|mark|daniel|google uk english male/i);
        }) || voices.find(function(v) { return v.lang.startsWith('en') && !v.name.match(/female|woman/i); });
        msg.pitch = 0.85; msg.rate = 0.95;
        """
    elif voice_type == "woman":
        voice_logic = """
        var v = voices.find(function(v) {
            return v.lang.startsWith('en') && v.name.match(/female|woman|samantha|zira|google us english|karen|victoria/i);
        }) || voices.find(function(v) { return v.lang.startsWith('en'); });
        msg.pitch = 1.2; msg.rate = 1.0;
        """
    else:  # realistic
        voice_logic = """
        var v = voices.find(function(v) {
            return v.name.match(/google|neural|natural|premium|enhanced/i) && v.lang.startsWith('en');
        }) || voices.find(function(v) { return v.lang === 'en-US'; });
        msg.pitch = 1.0; msg.rate = 0.97;
        """

    return f"""
    <script>
    (function() {{
        try {{
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance('{safe}');
            msg.lang = 'en-US';
            msg.volume = 1.0;
            var voices = window.speechSynthesis.getVoices();
            {voice_logic}
            if (v) msg.voice = v;

            // trigger wave in parent iframe
            try {{
                window.parent.postMessage({{type:'mesta_speak', text:'{safe}'}}, '*');
            }} catch(e) {{}}

            // also try direct DOM in same page
            setTimeout(function() {{
                var frames = window.parent.document.querySelectorAll('iframe');
                for (var i=0; i<frames.length; i++) {{
                    try {{
                        var waveEl = frames[i].contentDocument.getElementById('waveEl');
                        if (waveEl) {{
                            waveEl.classList.add('speaking');
                            var st = frames[i].contentDocument.getElementById('waveStatus');
                            if(st) {{ st.textContent='Speaking...'; st.classList.add('active'); }}
                            var dur = Math.max(2000, '{safe}'.length * 55);
                            setTimeout(function(){{
                                waveEl.classList.remove('speaking');
                                if(st) {{ st.textContent='Ready'; st.classList.remove('active'); }}
                            }}, dur);
                        }}
                    }} catch(e) {{}}
                }}
            }}, 100);

            window.speechSynthesis.speak(msg);
        }} catch(e) {{ console.log('TTS:', e); }}
    }})();
    </script>
    """

# ── API ──
def ask_mistral(question):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": "You are Mesta AI, a sleek intelligent assistant created by Nirbhay. Answer clearly and concisely in 2-3 sentences."},
            {"role": "user", "content": question}
        ],
        "max_tokens": 200
    }
    try:
        r = requests.post(MISTRAL_URL, json=data, headers=headers, timeout=15)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Connection issue: {str(e)}"

# ── PLAY PENDING AUDIO ──
if st.session_state.pending_audio:
    st.components.v1.html(st.session_state.pending_audio, height=0)
    st.session_state.pending_audio = None

# ── RESPONSE MODE ──
st.markdown('<div class="section-label">⚙ Response Mode</div>', unsafe_allow_html=True)
col_t, col_v, col_sp = st.columns([1, 1, 4])
with col_t:
    if st.button(
        "✅  Text" if st.session_state.output_mode == "text" else "📝  Text",
        use_container_width=True,
        type="primary" if st.session_state.output_mode == "text" else "secondary"
    ):
        st.session_state.output_mode = "text"
        st.rerun()
with col_v:
    if st.button(
        "✅  Voice" if st.session_state.output_mode == "voice" else "🔊  Voice",
        use_container_width=True,
        type="primary" if st.session_state.output_mode == "voice" else "secondary"
    ):
        st.session_state.output_mode = "voice"
        st.rerun()

# ── VOICE TYPE SELECTOR ──
if st.session_state.output_mode == "voice":
    st.markdown('<div class="section-label">🎙 Voice Type</div>', unsafe_allow_html=True)
    vc1, vc2, vc3, vc_sp = st.columns([1, 1, 1, 3])
    with vc1:
        if st.button(
            "✅ 👨 Man" if st.session_state.voice_type == "man" else "👨 Man",
            use_container_width=True,
            type="primary" if st.session_state.voice_type == "man" else "secondary"
        ):
            st.session_state.voice_type = "man"
            st.rerun()
    with vc2:
        if st.button(
            "✅ 👩 Woman" if st.session_state.voice_type == "woman" else "👩 Woman",
            use_container_width=True,
            type="primary" if st.session_state.voice_type == "woman" else "secondary"
        ):
            st.session_state.voice_type = "woman"
            st.rerun()
    with vc3:
        if st.button(
            "✅ 🎭 Realistic" if st.session_state.voice_type == "realistic" else "🎭 Realistic",
            use_container_width=True,
            type="primary" if st.session_state.voice_type == "realistic" else "secondary"
        ):
            st.session_state.voice_type = "realistic"
            st.rerun()
    voice_labels = {"man": "👨 Deep male voice", "woman": "👩 Female voice", "realistic": "🎭 Most natural voice available"}
    st.markdown(f'<div class="mode-indicator">{voice_labels[st.session_state.voice_type]}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="mode-indicator">📝 &nbsp;Text replies only</div>', unsafe_allow_html=True)

# ── QUICK QUESTIONS ──
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">⚡ Quick Questions</div>', unsafe_allow_html=True)

quick_qs = [
    ("🖥", "Explain Quantum Computing", "In simple terms"),
    ("💡", "Ideas for a startup", "Need creative ideas"),
    ("📝", "Improve my resume", "Make it more professional"),
    ("🐍", "Write Python code", "For data analysis"),
    ("🤖", "Latest AI trends", "What's new in AI?"),
    ("😄", "Tell me a joke", "Make me smile"),
]

cols = st.columns(3)
for i, (icon, title, sub) in enumerate(quick_qs):
    with cols[i % 3]:
        if st.button(f"{icon} {title}", use_container_width=True, key=f"qq_{i}"):
            with st.spinner("✦ Thinking..."):
                answer = ask_mistral(title)
                st.session_state.chat_history.append({
                    "q": title, "a": answer,
                    "t": datetime.now().strftime("%I:%M %p"),
                    "mode": st.session_state.output_mode,
                    "voice": st.session_state.voice_type
                })
                if st.session_state.output_mode == "voice":
                    st.session_state.pending_audio = speak_text(answer, st.session_state.voice_type)
                st.rerun()

# ── INPUT ──
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-label">💬 Ask Mesta</div>', unsafe_allow_html=True)

user_question = st.text_input(
    "", placeholder="Ask Mesta anything...",
    key="text_input", label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1.3, 1.3, 3])
with col1:
    ask_clicked = st.button("✦ Ask Mesta", use_container_width=True, type="primary")
with col2:
    clear_clicked = st.button("🗑 Clear Chat", use_container_width=True)

if ask_clicked and user_question:
    with st.spinner("✦ Thinking..."):
        answer = ask_mistral(user_question)
        st.session_state.chat_history.append({
            "q": user_question, "a": answer,
            "t": datetime.now().strftime("%I:%M %p"),
            "mode": st.session_state.output_mode,
            "voice": st.session_state.voice_type
        })
        if st.session_state.output_mode == "voice":
            st.session_state.pending_audio = speak_text(answer, st.session_state.voice_type)
        st.rerun()

if clear_clicked:
    st.session_state.chat_history = []
    st.session_state.pending_audio = None
    st.rerun()

# ── CONVERSATION ──
if st.session_state.chat_history:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">💬 Conversation</div>', unsafe_allow_html=True)
    for chat in reversed(st.session_state.chat_history[-15:]):
        voice_icon = ""
        if chat.get("mode") == "voice":
            icons = {"man": "👨🔊", "woman": "👩🔊", "realistic": "🎭🔊"}
            voice_icon = " " + icons.get(chat.get("voice", "man"), "🔊")
        st.markdown(
            f'<div class="user-bubble"><strong>You</strong><br>{chat["q"]}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'''<div class="ai-bubble">
                <div class="ai-name">✦ Mesta{voice_icon}</div>
                {chat["a"]}
                <div class="msg-time">{chat["t"]}</div>
            </div>''',
            unsafe_allow_html=True
        )

# ── FOOTER ──
st.markdown(
    '<div class="footer">✦ Mesta AI &nbsp;·&nbsp; Created by Nirbhay &nbsp;·&nbsp; Powered by Mistral AI</div>',
    unsafe_allow_html=True
)