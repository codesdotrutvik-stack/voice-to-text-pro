import requests

api_key = "tXPmUYPeEqwD48MrvREFmn3GmvB7KqRk"

url = "https://api.mistral.ai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "mistral-small-latest",
    "messages": [
        {"role": "user", "content": "Say Hello"}
    ]
}

response = requests.post(url, json=data, headers=headers)
print(response.json()["choices"][0]["message"]["content"])