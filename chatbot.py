import requests

api_key = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"

url = "https://api.mistral.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def ask_mistral(question):
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": "You are a helpful teacher. Explain in simple language."},
            {"role": "user", "content": question}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

print("AI Study Buddy Started! Type 'quit' to exit")
print("-" * 40)

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    answer = ask_mistral(user_input)
    print("AI Teacher:", answer)
    print("-" * 40)