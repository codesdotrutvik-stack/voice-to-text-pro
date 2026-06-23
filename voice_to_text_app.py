import streamlit as st
import assemblyai as aai
from datetime import datetime
import os
import requests
import json
import hashlib

st.set_page_config(page_title="Voice to Text Pro", page_icon="✨", layout="wide")

# ============================================================
# API KEYS
# ============================================================
ASSEMBLYAI_KEY = "5e874d691c74442f8b602827e6d26752"
MISTRAL_KEY = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"

aai.settings.api_key = ASSEMBLYAI_KEY

# ============================================================
# HISTORY FILE
# ============================================================
HISTORY_FILE = "history.json"

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        return []
    except:
        return []

def save_history(history):
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except:
        pass

# ============================================================
# PREMIUM CSS — Next-Level Design
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500&display=swap');

*, *::before, *::after {
    margin: 0; padding: 0; box-sizing: border-box;
    font-family: 'Geist', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── App Background ── */
.stApp {
    background: #09090b;
    min-height: 100vh;
}

.block-container {
    padding: 2.5rem 2rem !important;
    max-width: 860px !important;
    margin: 0 auto;
}

/* ── Animations ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
@keyframes pulse-ring {
    0%   { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.4); }
    70%  { box-shadow: 0 0 0 10px rgba(139, 92, 246, 0); }
    100% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0); }
}
@keyframes glow-line {
    0%, 100% { opacity: 0.4; }
    50%       { opacity: 1; }
}

/* ── Header ── */
.vtp-header {
    text-align: center;
    padding: 3rem 0 2rem;
    animation: fadeUp 0.6s ease;
}
.vtp-logo-ring {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 1.2rem;
    box-shadow: 0 0 32px rgba(124, 58, 237, 0.35);
    font-size: 1.5rem;
}
.vtp-title {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #fafafa;
    line-height: 1;
    margin-bottom: 0.5rem;
}
.vtp-title .accent {
    background: linear-gradient(120deg, #a78bfa, #818cf8, #6366f1);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s linear infinite;
}
.vtp-subtitle {
    color: #52525b;
    font-size: 0.85rem;
    font-weight: 400;
    letter-spacing: 0.02em;
}
.vtp-subtitle span {
    color: #71717a;
    margin: 0 6px;
}

/* ── Card ── */
.card {
    background: #111113;
    border: 1px solid #1f1f23;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    animation: fadeUp 0.5s ease;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
    border-color: #2d2d33;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
}
.card-icon {
    width: 32px; height: 32px;
    background: rgba(124, 58, 237, 0.12);
    border: 1px solid rgba(124, 58, 237, 0.2);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}
.card-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #a1a1aa;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.card-caption {
    font-size: 0.72rem;
    color: #3f3f46;
    margin-top: 2px;
    letter-spacing: 0.01em;
}

/* ── Upload Zone ── */
[data-testid="stFileUploader"] {
    width: 100% !important;
}
[data-testid="stFileUploader"] > div {
    background: rgba(124, 58, 237, 0.03) !important;
    border: 1.5px dashed #27272a !important;
    border-radius: 12px !important;
    padding: 1.8rem 1.5rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: rgba(124, 58, 237, 0.4) !important;
    background: rgba(124, 58, 237, 0.05) !important;
}
[data-testid="stFileUploader"] label { color: #52525b !important; font-size: 0.82rem !important; }

/* ── Audio / Video ── */
[data-testid="stAudio"], [data-testid="stVideo"] {
    width: 100% !important;
    border-radius: 10px;
    overflow: hidden;
}
[data-testid="stAudio"] audio {
    filter: invert(1) hue-rotate(180deg) !important;
}

/* ── Transcription Box ── */
.text-box {
    background: #0d0d10;
    border: 1px solid #1f1f23;
    border-radius: 12px;
    padding: 20px;
    min-height: 140px;
    color: #d4d4d8;
    font-size: 0.9rem;
    line-height: 1.9;
    white-space: pre-wrap;
    max-height: 520px;
    overflow-y: auto;
    animation: fadeUp 0.4s ease;
    font-family: 'Geist', sans-serif;
}
.text-box::-webkit-scrollbar { width: 4px; }
.text-box::-webkit-scrollbar-track { background: transparent; }
.text-box::-webkit-scrollbar-thumb { background: #3f3f46; border-radius: 10px; }

/* ── History Item ── */
.history-item {
    background: #111113;
    border: 1px solid #1f1f23;
    border-radius: 12px;
    padding: 14px 16px;
    margin: 6px 0;
    transition: all 0.18s ease;
    animation: fadeUp 0.4s ease;
    position: relative;
}
.history-item:hover {
    border-color: rgba(124, 58, 237, 0.3);
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.06);
}
.history-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
}
.history-meta { flex: 1; min-width: 0; }
.history-mode {
    color: #a78bfa;
    font-weight: 600;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
}
.history-time {
    color: #3f3f46;
    font-size: 0.68rem;
    margin-bottom: 6px;
    font-family: 'Geist Mono', monospace;
}
.history-text {
    color: #71717a;
    font-size: 0.82rem;
    line-height: 1.6;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* ── Buttons — global Streamlit override ── */
.stButton > button {
    background: #18181b !important;
    color: #a1a1aa !important;
    border: 1px solid #27272a !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.8rem !important;
    padding: 7px 16px !important;
    transition: all 0.18s ease !important;
    box-shadow: none !important;
    letter-spacing: 0.01em;
}
.stButton > button:hover {
    background: #1f1f23 !important;
    border-color: #3f3f46 !important;
    color: #e4e4e7 !important;
    transform: translateY(-1px);
}

/* Primary button */
.stButton > button[kind="primary"],
div[data-testid="column"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #6d28d9, #5b21b6) !important;
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4) !important;
    transform: translateY(-1px);
}

/* ── Section Labels ── */
.section-label {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #3f3f46;
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 1.6rem 0 0.8rem;
}
.section-label::before, .section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1f1f23;
}

/* ── Status / Alerts ── */
.stAlert {
    background: rgba(16, 185, 129, 0.06) !important;
    border: 1px solid rgba(16, 185, 129, 0.2) !important;
    border-radius: 10px !important;
    color: #6ee7b7 !important;
}
[data-testid="stNotification"] { border-radius: 10px !important; }

/* ── Checkbox ── */
[data-testid="stCheckbox"] label {
    color: #71717a !important;
    font-size: 0.8rem !important;
}
[data-testid="stCheckbox"] span[aria-checked="true"] {
    background: #7c3aed !important;
    border-color: #7c3aed !important;
}

/* ── Select Box ── */
[data-testid="stSelectbox"] > div > div {
    background: #111113 !important;
    border-color: #27272a !important;
    color: #d4d4d8 !important;
    border-radius: 8px !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #7c3aed !important; }

/* ── File caption ── */
.file-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 8px;
    color: #3f3f46;
    font-size: 0.72rem;
    font-family: 'Geist Mono', monospace;
}
.file-dot {
    width: 4px; height: 4px;
    background: #3f3f46;
    border-radius: 50%;
}

/* ── Badge ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(124, 58, 237, 0.1);
    border: 1px solid rgba(124, 58, 237, 0.2);
    color: #a78bfa;
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 2px 8px;
    border-radius: 20px;
}

/* ── Divider ── */
.vdivider {
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, #1f1f23 30%, #1f1f23 70%, transparent 100%);
    margin: 1.5rem 0;
}

/* ── Download icon button in history ── */
.dl-icon-btn {
    background: rgba(124, 58, 237, 0.08);
    border: 1px solid rgba(124, 58, 237, 0.15);
    border-radius: 8px;
    width: 34px; height: 34px;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer;
    transition: all 0.18s ease;
    flex-shrink: 0;
    color: #7c3aed;
    font-size: 0.85rem;
}
.dl-icon-btn:hover {
    background: rgba(124, 58, 237, 0.16);
    border-color: rgba(124, 58, 237, 0.35);
}

/* ── Footer ── */
.vtp-footer {
    text-align: center;
    color: #27272a;
    font-size: 0.65rem;
    padding: 2rem 0 1rem;
    letter-spacing: 0.04em;
}
.vtp-footer strong { color: #3f3f46; }

/* ── Audio recorder widget ── */
[data-testid="stAudioInput"] {
    background: transparent !important;
}
[data-testid="stAudioInput"] > div {
    background: #0d0d10 !important;
    border: 1px solid #1f1f23 !important;
    border-radius: 12px !important;
}

/* hide top spacer Streamlit adds above file uploader label */
[data-testid="stFileUploader"] section { display: none !important; }
[data-testid="stFileUploader"] label { display: none !important; }

/* Collapse empty markdown containers that create blank boxes */
.stMarkdown:empty { display: none !important; }
div[data-testid="stVerticalBlock"] > div:empty { display: none !important; }

/* ── Global dark override for any leftover white backgrounds ── */
.element-container { background: transparent !important; }
.stTextInput > div, .stSelectbox > div { background: transparent !important; }

/* Remove Streamlit's default top/bottom padding on containers */
section[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if "history" not in st.session_state:
    st.session_state.history = load_history()
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""
if "original_text" not in st.session_state:
    st.session_state.original_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""
if "copy_msg" not in st.session_state:
    st.session_state.copy_msg = ""
if "last_processed_audio" not in st.session_state:
    st.session_state.last_processed_audio = None
if "last_processed_file" not in st.session_state:
    st.session_state.last_processed_file = None
if "show_translate" not in st.session_state:
    st.session_state.show_translate = False

# ============================================================
# FUNCTIONS
# ============================================================
def translate_text(text, target_lang):
    lang_map = {
        "Hindi": "Hindi", "Gujarati": "Gujarati", "Spanish": "Spanish",
        "French": "French", "German": "German", "Chinese": "Chinese", "Japanese": "Japanese"
    }
    language = lang_map.get(target_lang, "Hindi")
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_KEY}", "Content-Type": "application/json"}
    prompt = f"Translate the following text to {language}. Only output the translation, no additional text.\n\nText:\n{text}"
    data = {"model": "mistral-small-latest", "messages": [{"role": "user", "content": prompt}], "max_tokens": 2000}
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "Translation failed."

def format_transcript(transcript, conversation_mode):
    if conversation_mode and transcript.utterances:
        formatted = ""
        for utterance in transcript.utterances:
            speaker = f"Speaker {utterance.speaker}"
            formatted += f"**{speaker}:** {utterance.text}\n\n"
        return formatted
    return transcript.text

def add_to_history(text, full_text, mode):
    entry = {
        "text": text[:500] + ("..." if len(text) > 500 else ""),
        "full_text": full_text,
        "time": datetime.now().strftime("%I:%M %p · %d %b"),
        "mode": mode
    }
    st.session_state.history.insert(0, entry)
    save_history(st.session_state.history)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="vtp-header">
    <div class="vtp-logo-ring">🎙️</div>
    <div class="vtp-title">Voice to Text <span class="accent">Pro</span></div>
    <div class="vtp-subtitle">
        Upload audio or video
        <span>·</span>
        Record your voice
        <span>·</span>
        AI transcribes &amp; translates
    </div>
</div>
""", unsafe_allow_html=True)

# Status banner
if st.session_state.copy_msg:
    st.success(st.session_state.copy_msg)
    st.session_state.copy_msg = ""

# ============================================================
# RECORD SECTION  — no wrapper divs that create extra boxes
# ============================================================
st.markdown("""
<div class="card">
    <div class="card-header">
        <div class="card-icon">🎤</div>
        <div>
            <div class="card-label">Record Voice</div>
            <div class="card-caption">Tap the mic and start speaking</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

audio_value = st.audio_input("", key="audio_recorder", label_visibility="collapsed")

audio_hash = None
if audio_value is not None:
    audio_hash = hashlib.md5(audio_value.getvalue()).hexdigest()

if audio_value is not None and audio_hash != st.session_state.last_processed_audio:
    st.session_state.last_processed_audio = audio_hash
    with st.spinner("Transcribing your recording…"):
        try:
            temp_file = "temp_audio.wav"
            with open(temp_file, "wb") as f:
                f.write(audio_value.getvalue())
            config = aai.TranscriptionConfig(speaker_labels=True, speakers_expected=2)
            transcriber = aai.Transcriber(config=config)
            transcript = transcriber.transcribe(temp_file)
            if transcript.text:
                formatted = format_transcript(transcript, True)
                st.session_state.transcribed_text = formatted
                st.session_state.original_text = transcript.text
                add_to_history(formatted, formatted, "Conversation")
                st.success("Transcription complete")
            else:
                st.error("No speech detected — please try again.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass

# ============================================================
# UPLOAD SECTION
# ============================================================
st.markdown("""
<div class="card" style="margin-top:1rem;">
    <div class="card-header">
        <div class="card-icon">📂</div>
        <div>
            <div class="card-label">Upload File</div>
            <div class="card-caption">MP3 · WAV · M4A · FLAC · WebM · MP4 · MOV · AVI · MKV</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload audio or video",
    type=["mp3", "wav", "m4a", "flac", "webm", "mp4", "mov", "avi", "mkv"],
    label_visibility="collapsed"
)

if uploaded_file is not None:
    file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()
    file_type = uploaded_file.type
    if "video" in file_type or uploaded_file.name.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        st.video(uploaded_file)
    else:
        st.audio(uploaded_file, format="audio/wav")

    file_size = len(uploaded_file.getvalue()) / (1024 * 1024)
    st.markdown(f"""
    <div class="file-meta">
        <span>📄 {uploaded_file.name}</span>
        <span class="file-dot"></span>
        <span>{file_size:.1f} MB</span>
    </div>
    """, unsafe_allow_html=True)

    col_mode, col_btn = st.columns([2, 1])
    with col_mode:
        conversation_mode = st.checkbox("Speaker Labels (Conversation Mode)", value=True)
    with col_btn:
        transcribe_clicked = st.button("✦ Transcribe", type="primary", use_container_width=True)

    if transcribe_clicked:
        if file_hash != st.session_state.last_processed_file:
            st.session_state.last_processed_file = file_hash
            with st.spinner("Uploading & transcribing…"):
                try:
                    file_ext = uploaded_file.name.split('.')[-1]
                    temp_file = f"temp_upload.{file_ext}"
                    with open(temp_file, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    config = aai.TranscriptionConfig(speaker_labels=True, speakers_expected=2)
                    transcriber = aai.Transcriber(config=config)
                    transcript = transcriber.transcribe(temp_file)
                    if transcript.text:
                        formatted = format_transcript(transcript, conversation_mode)
                        st.session_state.transcribed_text = formatted
                        st.session_state.original_text = transcript.text
                        st.session_state.translated_text = ""
                        mode = "Conversation" if conversation_mode else "Standard"
                        add_to_history(formatted, formatted, mode)
                        st.success("Transcription complete")
                    else:
                        st.error("No speech detected — please try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    try:
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
                    except:
                        pass
        else:
            st.warning("This file has already been transcribed.")

# ============================================================
# TRANSCRIPTION OUTPUT
# ============================================================
if st.session_state.transcribed_text:
    st.markdown('<div class="section-label">Transcription</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="text-box">{st.session_state.transcribed_text}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            label="↓ Download",
            data=st.session_state.transcribed_text,
            file_name=f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_main"
        )
    with col2:
        if st.button("✕ Clear", key="clear_transcription", use_container_width=True):
            st.session_state.transcribed_text = ""
            st.session_state.original_text = ""
            st.session_state.translated_text = ""
            st.session_state.show_translate = False
            st.rerun()
    with col3:
        if st.button("⇄ Translate", key="translate_btn", use_container_width=True):
            st.session_state.show_translate = not st.session_state.show_translate
            st.rerun()

# ============================================================
# TRANSLATION
# ============================================================
if st.session_state.show_translate and st.session_state.transcribed_text:
    st.markdown('<div class="section-label">Translation</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        target_lang = st.selectbox(
            "Language",
            ["Hindi", "Gujarati", "Spanish", "French", "German", "Chinese", "Japanese"],
            label_visibility="collapsed"
        )
    with col2:
        do_translate = st.button("Go", type="primary", use_container_width=True)

    if do_translate:
        with st.spinner(f"Translating to {target_lang}…"):
            translated = translate_text(st.session_state.transcribed_text, target_lang)
            if translated:
                st.session_state.translated_text = translated

    if st.session_state.translated_text:
        st.markdown(f'<div class="text-box" style="border-color:#2d2317;">{st.session_state.translated_text}</div>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button(
                label="↓ Download Translation",
                data=st.session_state.translated_text,
                file_name=f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="dl_translation"
            )

# ============================================================
# HISTORY — with inline download icon on right side
# ============================================================
if st.session_state.history:
    st.markdown('<div class="section-label">History</div>', unsafe_allow_html=True)

    for idx, item in enumerate(st.session_state.history):
        # History card with meta on left, download on right (via Streamlit columns)
        col_text, col_dl = st.columns([9, 1])
        with col_text:
            st.markdown(f"""
            <div class="history-item">
                <div class="history-mode">{item['mode']}</div>
                <div class="history-time">{item['time']}</div>
                <div class="history-text">{item['text']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_dl:
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            st.download_button(
                label="↓",
                data=item.get('full_text', item['text']),
                file_name=f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{idx}.txt",
                mime="text/plain",
                use_container_width=True,
                key=f"dl_hist_{idx}"
            )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    if st.button("✕ Clear All History", use_container_width=True):
        st.session_state.history = []
        save_history(st.session_state.history)
        st.rerun()

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="vtp-footer">
    Voice to Text Pro &nbsp;·&nbsp; <strong>AssemblyAI</strong> + <strong>Mistral</strong> &nbsp;·&nbsp; by Nirbhay
</div>
""", unsafe_allow_html=True)