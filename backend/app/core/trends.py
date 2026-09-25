import os
import datetime
import urllib.request
import json
import re
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.nebius import nebius_client
from app.core.prompts import SYSTEM_TRENDS_PROMPT

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# 10 movimentos de design contemporâneo sofisticados para curadoria dinâmica
THEME_SEEDS = [
    "Biophilic Brutalism (Formas brutas combinadas com verdes botânicos úmidos e concreto texturizado)",
    "Neo-Cybernetic Organicism (Displays de alta frequência com formas fluídas e luminosas)",
    "Y2K Nostalgic Optimism (Gradients translúcidos, metalizados prateados e tons de azul inflável)",
    "Solarpunk Symbiosis (Luz solar dourada profunda, terrosos quentes e biomateriais)",
    "Matte Desolation (Minimalismo desértico silencioso, cinzas minerais e areia desbotada)",
    "Retro-Futuristic Constructivism (Vermelhos industriais pesados, preto carvão e cremes mecânicos)",
    "Digital Lavender & Acid Neon (Cores virtuais de alta energia e contrastes sintéticos desafiadores)",
    "Anarchic Punk-Gothic (Preto asfalto texturizado, cinzas grafite e tons neon ácidos)",
    "Japandi Quietude (Madeiras claras escandinavas, linho cru, tons de chá verde e pedras de rio úmidas)",
    "Chroma Shift (Gradients de interferência eletromagnética, violetas densos e turquesas elétricos)"
]

def fetch_tavily_trends(query: str = "current graphic design visual aesthetic color trends 2026") -> str:
    """Busca tendências recentes de design de forma autônoma se a chave Tavily estiver disponível."""
    if not TAVILY_API_KEY:
        return ""
    
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "include_images": False
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            results = res_json.get("results", [])
            
            # Formata os dados retornados para injeção no LLM
            snippets = []
            for item in results:
                snippets.append(f"Title: {item.get('title')}\nContent: {item.get('content')}")
            return "\n\n".join(snippets)
    except Exception as e:
        print(f"Erro ao consultar Tavily Search: {str(e)}")
        return ""

def generate_weekly_trend(week_str: str, week_num: int) -> Dict[str, Any]:
    """Gera uma tendência de design sofisticada para a semana combinando Tavily ou Fallback dinâmico e LLM."""
    
    # Busca dados em tempo real (caso exista a chave)
    web_context = fetch_tavily_trends()
    
    # Semente estética de fallback baseada no número da semana (rotativo de 0 a 9)
    seed_theme = THEME_SEEDS[week_num % len(THEME_SEEDS)]
    
    user_content = f"Gere o Trend Drop estético para a semana '{week_str}'.\n"
    if web_context:
        user_content += (
            f"Considere os seguintes insights reais e recentes de design coletados na web "
            f"para formular e fundamentar a tendência:\n\n{web_context}"
        )
    else:
        user_content += (
            f"Como fallback para busca ativa, siga e expanda a seguinte semente estética de "
            f"vanguarda de forma madura, profissional e inspiradora: '{seed_theme}'."
        )

    messages = [
        {"role": "system", "content": SYSTEM_TRENDS_PROMPT},
        {"role": "user", "content": user_content}
    ]

    # Usamos temperatura ligeiramente maior (0.3) para permitir refinamento poético mas mantendo a estrutura JSON intacta
    # Definimos max_tokens como 3500 para dar espaço ao processo de raciocínio profundo do modelo
    raw_response = nebius_client._send_request(messages, temperature=0.3, max_tokens=3500)

    # Extração robusta do bloco JSON via Regex
    json_match = re.search(r"(\{.*\}|\[.*\])", raw_response, re.DOTALL)
    if json_match:
        cleaned_text = json_match.group(1).strip()
    else:
        cleaned_text = raw_response

    return json.loads(cleaned_text)
