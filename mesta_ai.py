import streamlit as st

st.set_page_config(page_title="Voice Test", page_icon="🔊")

st.title("🔊 Voice Test")

st.markdown("""
<script>
function testSpeak() {
    if ('speechSynthesis' in window) {
        var msg = new SpeechSynthesisUtterance("Hello! This is a test. Voice is working!");
        msg.lang = 'en-US';
        msg.rate = 0.9;
        window.speechSynthesis.speak(msg);
        document.getElementById('status').innerHTML = '✅ Speaking... Check your speakers';
        document.getElementById('status').style.color = 'green';
    } else {
        document.getElementById('status').innerHTML = '❌ Speech not supported in this browser';
        document.getElementById('status').style.color = 'red';
    }
}
</script>

<button onclick="testSpeak()" style="padding: 12px 24px; font-size: 16px; background: #8b5cf6; color: white; border: none; border-radius: 8px; cursor: pointer;">
    🔊 Test Voice
</button>

<p id="status" style="margin-top: 20px; font-size: 14px;">Click the button to test voice</p>
""", unsafe_allow_html=True)

st.info("If you hear voice when clicking the button, voice works. If not, check:")
st.markdown("""
1. **Speakers/Headphones** are connected and volume is up
2. **Browser** is Chrome, Edge, or Safari
3. **Sound settings** in your computer
""")