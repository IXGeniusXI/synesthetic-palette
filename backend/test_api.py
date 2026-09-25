#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import time

def test_backend_endpoints():
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 Iniciando Testes de Integração Local da API...")
    print("=" * 60)

    # 1. Teste de Health Check
    try:
        req = urllib.request.Request(f"{base_url}/", method="GET")
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            print(f"✅ ROTA 1: GET / (Health Check) -> ONLINE!")
            print(f"   Nome do App: {data['app_name']}")
            print(f"   Modelo Ativo: {data['active_model']}")
    except urllib.error.URLError as e:
        print("❌ Erro ao conectar no servidor local. Certifique-se de que o uvicorn está rodando!")
        print("   Comando para rodar: cd backend && uvicorn app.main:app --reload")
        return

    # 2. Teste da Rota de Tendências
    try:
        req = urllib.request.Request(f"{base_url}/api/trends", method="GET")
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            print(f"\n✅ ROTA 2: GET /api/trends -> SUCESSO!")
            print(f"   Tema da Semana: {data['theme']}")
            print(f"   Conceito: {data['concept']}")
            print(f"   Cores Geradas:")
            for color in data['colors']:
                print(f"     - {color['name']} ({color['hex']}) -> {color['role']}")
    except Exception as e:
        print(f"❌ Rota de Tendências falhou: {e}")

    # 3. Teste da Rota do Co-pilot (Chat)
    try:
        chat_payload = {
            "messages": [
                {"role": "user", "content": "Me sugira uma ideia de combinação conceitual para uma marca de design de interiores de Berlim."}
            ],
            "temperature": 0.5
        }
        req = urllib.request.Request(
            f"{base_url}/api/chat",
            data=json.dumps(chat_payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        print(f"\n🔄 Testando ROTA 3: POST /api/chat (Aguardando resposta do Nebius)...")
        start_time = time.time()
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            end_time = time.time()
            print(f"✅ SUCESSO! Resposta recebida em {end_time - start_time:.2f}s:")
            print("-" * 50)
            print(data['reply'])
            print("-" * 50)
    except Exception as e:
        print(f"❌ Rota do Co-pilot falhou: {e}")

    # 4. Teste da Rota do Gerador de Paleta (JSON Skill)
    try:
        brief_payload = {
            "brand_name": "Studio Berlin",
            "description": "Estúdio de arquitetura brutalista focado em concreto, madeira escura e aço escovado.",
            "aesthetic_goal": "Atemporal, pesado, limpo, industrial e minimalista."
        }
        req = urllib.request.Request(
            f"{base_url}/api/generate-palette",
            data=json.dumps(brief_payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        print(f"\n🔄 Testando ROTA 4: POST /api/generate-palette (Gerador de Paleta Inteligente)...")
        start_time = time.time()
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            end_time = time.time()
            print(f"✅ SUCESSO! Paleta JSON estruturada gerada em {end_time - start_time:.2f}s:")
            print(json.dumps(data, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Rota do Gerador de Paletas falhou: {e}")

    # 5. Teste de Recuperação do Histórico de Conversas (SQLite)
    try:
        req = urllib.request.Request(f"{base_url}/api/chat/history", method="GET")
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            print(f"\n✅ ROTA 5: GET /api/chat/history -> SUCESSO!")
            print(f"   Mensagens registradas no banco local: {len(data['history'])}")
            if data['history']:
                for msg in data['history'][-2:]:  # Mostra as duas últimas mensagens (pergunta e resposta)
                    print(f"     [{msg['role'].upper()}]: {msg['content'][:100].strip()}...")
    except Exception as e:
        print(f"❌ Rota de Histórico de Conversas falhou: {e}")

    # 6. Teste de Recuperação de Paletas Salvas (SQLite)
    palette_id_to_delete = None
    try:
        req = urllib.request.Request(f"{base_url}/api/palettes", method="GET")
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            print(f"\n✅ ROTA 6: GET /api/palettes -> SUCESSO!")
            print(f"   Paletas armazenadas no banco local: {len(data['palettes'])}")
            if data['palettes']:
                first_palette = data['palettes'][0]
                palette_id_to_delete = first_palette["id"]
                print(f"     Última paleta salva no DB: ID {palette_id_to_delete} (Marca: '{first_palette['brand_name']}')")
                print(f"     Cores: {[c['hex'] for c in first_palette['colors']]}")
    except Exception as e:
        print(f"❌ Rota de Recuperação de Paletas falhou: {e}")

    # 7. Teste de Exclusão de Paleta do Banco Local (SQLite)
    if palette_id_to_delete:
        try:
            req = urllib.request.Request(f"{base_url}/api/palettes/{palette_id_to_delete}", method="DELETE")
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read().decode("utf-8"))
                print(f"\n✅ ROTA 7: DELETE /api/palettes/{palette_id_to_delete} -> SUCESSO!")
                print(f"   Mensagem: {data['message']}")
        except Exception as e:
            print(f"❌ Rota de Exclusão de Paleta falhou: {e}")

    print("\n" + "=" * 60)
    print("🏁 Testes finalizados!")

if __name__ == "__main__":
    test_backend_endpoints()
