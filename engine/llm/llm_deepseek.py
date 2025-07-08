# engine/llm/llm_deepseek.py
import requests
import json
from config import LLM_CONFIG

class DeepSeekChat:
    def __init__(self):
        self.url = LLM_CONFIG["url"]
        self.api_key = LLM_CONFIG["key"]
        self.model = LLM_CONFIG["model"]

    def user_message(self, message: str):
        return {"role": "user", "content": message}

    def system_message(self, message: str):
        return {"role": "system", "content": message}

    def assistant_message(self, message: str):
        return {"role": "assistant", "content": message}

    def submit_prompt(self, messages, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0
        }
        print("🟡 [DEBUG] 提交请求内容：", json.dumps(payload, indent=2, ensure_ascii=False))
        response = requests.post(self.url + "/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]