import json
import urllib.request
import re
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.prompts import SYSTEM_COPILOT_PROMPT, SYSTEM_PALETTE_PROMPT

class NebiusClient:
    def __init__(self):
        self.api_key = settings.NEBIUS_API_KEY
        self.url = settings.NEBIUS_URL
        self.model = settings.ACTIVE_MODEL

    def _send_request(self, messages: List[Dict[str, str]], temperature: float, max_tokens: int) -> str:
        if not self.api_key:
            raise ValueError("Chave NEBIUS_API_KEY não configurada no backend.")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        req = urllib.request.Request(
            self.url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST"
        )

        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            return res_json["choices"][0]["message"]["content"].strip()

    def chat_copilot(self, chat_history: List[Dict[str, str]], temperature: float = 0.5, max_tokens: int = 1000) -> str:
        messages = [{"role": "system", "content": SYSTEM_COPILOT_PROMPT}]
        # Certifica-se de que cada mensagem possui apenas "role" e "content"
        formatted_history = []
        for msg in chat_history:
            formatted_history.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        messages.extend(formatted_history)
        return self._send_request(messages, temperature, max_tokens)

    def generate_palette(self, brand_name: str, description: str, aesthetic_goal: str) -> Dict[str, Any]:
        user_content = (
            f"Marca: {brand_name}\n"
            f"Descrição: {description}\n"
            f"Estilo visual desejado: {aesthetic_goal}"
        )
        
        messages = [
            {"role": "system", "content": SYSTEM_PALETTE_PROMPT},
            {"role": "user", "content": user_content}
        ]

        raw_response = self._send_request(messages, temperature=0.1, max_tokens=2000)

        # Extração robusta de JSON via Regex
        json_match = re.search(r"(\{.*\}|\[.*\])", raw_response, re.DOTALL)
        if json_match:
            cleaned_text = json_match.group(1).strip()
        else:
            cleaned_text = raw_response

        return json.loads(cleaned_text)

nebius_client = NebiusClient()
