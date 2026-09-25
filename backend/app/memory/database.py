import os
import sqlite3
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

# Define o caminho do banco de dados dentro do diretório app/memory/data/
DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DB_DIR, "palette_memory.db")

class MemoryDB:
    def __init__(self):
        # Garante que a pasta de dados exista
        os.makedirs(DB_DIR, exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        
        # Tabela para salvar as marcas e paletas geradas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS palettes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand_name TEXT NOT NULL,
                description TEXT,
                aesthetic_goal TEXT,
                colors TEXT NOT NULL, -- JSON String
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela para persistir o histórico de conversas do Co-pilot
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL, -- 'user', 'assistant' ou 'system'
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabela para cachear as tendências semanais
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trends (
                week TEXT PRIMARY KEY, -- Ex: '2026-W39'
                data TEXT NOT NULL,    -- JSON String
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()

    # --- Métodos de Cache de Tendências (Trends) ---
    def save_cached_trend(self, week: str, trend_data: Dict[str, Any]) -> bool:
        cursor = self.conn.cursor()
        data_json = json.dumps(trend_data)
        cursor.execute(
            """
            INSERT OR REPLACE INTO trends (week, data)
            VALUES (?, ?)
            """,
            (week, data_json)
        )
        self.conn.commit()
        return True

    def get_cached_trend(self, week: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT data FROM trends WHERE week = ?", (week,))
        row = cursor.fetchone()
        if row:
            return json.loads(row["data"])
        return None

    # --- Métodos de Paletas ---
    def save_palette(self, brand_name: str, description: str, aesthetic_goal: str, colors: List[Dict[str, Any]]) -> int:
        cursor = self.conn.cursor()
        colors_json = json.dumps(colors)
        cursor.execute(
            """
            INSERT INTO palettes (brand_name, description, aesthetic_goal, colors)
            VALUES (?, ?, ?, ?)
            """,
            (brand_name, description, aesthetic_goal, colors_json)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_palettes(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM palettes ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        palettes = []
        for row in rows:
            palettes.append({
                "id": row["id"],
                "brand_name": row["brand_name"],
                "description": row["description"],
                "aesthetic_goal": row["aesthetic_goal"],
                "colors": json.loads(row["colors"]),
                "created_at": row["created_at"]
            })
        return palettes

    def delete_palette(self, palette_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM palettes WHERE id = ?", (palette_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    # --- Métodos de Histórico de Conversas ---
    def save_chat_message(self, role: str, content: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO chats (role, content) VALUES (?, ?)",
            (role, content)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_chat_history(self, limit: int = 50) -> List[Dict[str, str]]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT role, content FROM chats ORDER BY id ASC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        
        history = []
        for row in rows:
            history.append({
                "role": row["role"],
                "content": row["content"]
            })
        return history

    def clear_chat_history(self) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM chats")
        self.conn.commit()
        return True

# Instância única global do banco de dados local
memory_db = MemoryDB()
