import requests

url = "https://newapi.com/v1/messages"
body = """{
  "model": "claude-4.5-sonnet-think",
  "messages": [
    {
      "role": "user",
      "content": "how can I improve English ability"
    }
  ],
  "max_tokens": 1
}"""
response = requests.request("POST", url, data = body, headers = {
  "Content-Type": "application/json", 
  "anthropic-version": "2023-06-01", 
  "Authorization": "Bearer sk-xxxxx"
})

print(response.text)