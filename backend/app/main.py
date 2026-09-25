import os
import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Importações do design modular do projeto
from app.core.config import settings
from app.core.nebius import nebius_client
from app.core.trends import generate_weekly_trend
from app.memory.database import memory_db

app = FastAPI(
    title="Synesthetic Palette API",
    description="Backend API powered by Nebius Token Factory & NVIDIA models, with local SQLite memory",
    version="1.1.0"
)

# Configuração de CORS para permitir comunicação com o frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restringir ao endereço do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Schemas de dados Pydantic ---
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    temperature: Optional[float] = 0.5
    max_tokens: Optional[int] = 1000

class BriefRequest(BaseModel):
    brand_name: str
    description: str
    aesthetic_goal: str


# --- Rota Base (Health Check) ---
@app.get("/")
def read_root():
    return {
        "status": "online",
        "app_name": "Synesthetic Palette Backend",
        "llm_provider": "Nebius Token Factory",
        "active_model": settings.ACTIVE_MODEL,
        "database_status": "connected"
    }


# --- Rota para obter o "Trend Drop" de segunda-feira ---
@app.get("/api/trends")
def get_trends():
    try:
        # 1. Calcula o identificador da semana corrente (ex: '2026-W39')
        today = datetime.date.today()
        year, week_num, day_of_week = today.isocalendar()
        week_str = f"{year}-W{week_num:02d}"

        # 2. Tenta recuperar do cache local do SQLite
        cached_trend = memory_db.get_cached_trend(week_str)
        if cached_trend:
            return cached_trend

        # 3. Se não houver cache, gera dinamicamente via Tavily/Nebius
        new_trend = generate_weekly_trend(week_str, week_num)
        
        # 4. Salva no cache local para chamadas subsequentes na mesma semana
        memory_db.save_cached_trend(week_str, new_trend)
        
        return new_trend
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter tendências semanais: {str(e)}")


# --- Rotas do Co-pilot (Chat com Persistência Local) ---
@app.post("/api/chat")
def chat_copilot(payload: ChatRequest):
    # 1. Salva as novas mensagens enviadas pelo usuário no banco local
    for msg in payload.messages:
        if msg.role in ["user", "assistant"]:
            memory_db.save_chat_message(msg.role, msg.content)

    # 2. Recupera o histórico completo do banco de dados local para manter o contexto
    history = memory_db.get_chat_history()
    
    # Caso o banco de dados esteja vazio, usa as mensagens enviadas no payload imediato
    if not history:
        history = [{"role": msg.role, "content": msg.content} for msg in payload.messages]

    try:
        # 3. Envia o histórico completo para a Nebius via nosso cliente modular
        reply = nebius_client.chat_copilot(history, payload.temperature, payload.max_tokens)
        
        # 4. Salva a resposta gerada pelo assistente na memória local
        memory_db.save_chat_message("assistant", reply)
        
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no Co-pilot: {str(e)}")


@app.get("/api/chat/history")
def get_chat_history(limit: Optional[int] = 50):
    try:
        history = memory_db.get_chat_history(limit)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar histórico: {str(e)}")


@app.delete("/api/chat/history")
def clear_chat_history():
    try:
        memory_db.clear_chat_history()
        return {"status": "success", "message": "Histórico de chat limpo localmente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao limpar histórico: {str(e)}")


# --- Rotas de Geração e Persistência de Paletas ---
@app.post("/api/generate-palette")
def generate_palette_skill(payload: BriefRequest):
    try:
        # 1. Gera a paleta inteligente via Nebius Client
        palette_data = nebius_client.generate_palette(
            payload.brand_name,
            payload.description,
            payload.aesthetic_goal
        )
        
        # 2. Extrai as cores geradas para salvar no banco local
        colors_list = []
        if isinstance(palette_data, dict):
            if "palette" in palette_data:
                colors_list = palette_data["palette"]
            elif "colors" in palette_data:
                colors_list = palette_data["colors"]
            else:
                # Caso a estrutura venha aninhada ou diferente, extrai as chaves
                colors_list = palette_data
        
        # Se for uma lista direta de cores
        if isinstance(palette_data, list):
            colors_list = palette_data
            palette_data = {"palette": colors_list}

        # 3. Salva a paleta e o briefing associado no banco SQLite local
        memory_db.save_palette(
            payload.brand_name,
            payload.description,
            payload.aesthetic_goal,
            colors_list
        )
        
        return palette_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar paleta: {str(e)}")


@app.get("/api/palettes")
def get_saved_palettes():
    try:
        palettes = memory_db.get_palettes()
        return {"palettes": palettes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar paletas: {str(e)}")


@app.delete("/api/palettes/{palette_id}")
def delete_saved_palette(palette_id: int):
    try:
        success = memory_db.delete_palette(palette_id)
        if not success:
            raise HTTPException(status_code=404, detail="Paleta não encontrada ou já excluída.")
        return {"status": "success", "message": f"Paleta com ID {palette_id} excluída com sucesso."}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir paleta: {str(e)}")
