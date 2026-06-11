import streamlit as st
import requests

api_key = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"

url = "https://api.mistral.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

st.title("📚 AI Study Buddy")
st.write("Ask me anything - I will explain like a teacher!")

mode = st.radio("Choose mode:", ["Normal", "Explain like I'm 5"])

user_question = st.text_input("Your question:")

if st.button("Ask"):
    if user_question:
        if mode == "Explain like I'm 5":
            system_prompt = "You are a teacher. Explain like the student is 5 years old. Use very simple words. Short sentences."
        else:
            system_prompt = "You are a helpful teacher. Explain clearly and simply."
        
        data = {
            "model": "mistral-small-latest",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ]
        }
        
        response = requests.post(url, json=data, headers=headers)
        answer = response.json()["choices"][0]["message"]["content"]
        
        st.write("### Answer:")
        st.write(answer)