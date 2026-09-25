import React, { useState, useEffect, useRef } from 'react';
import { 
  Sparkles, 
  Send, 
  Copy, 
  Check, 
  RefreshCw, 
  Download
} from 'lucide-react';

// Interfaces de dados
interface Color {
  hex: string;
  rgb: string;
  oklch: string;
  name: string;
  role: string;
}

interface Typography {
  primary: string;
  secondary: string;
  justification: string;
}

interface TrendDrop {
  week: string;
  theme: string;
  concept: string;
  colors: Color[];
  typography: Typography;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface Toast {
  id: string;
  message: string;
}

// Fallback estático do Trend Drop caso a API esteja offline (Resiliência)
const FALLBACK_TREND: TrendDrop = {
  week: "2026-W39",
  theme: "Neo-Cybernetic Organicism",
  concept: "A fusão entre formas biológicas fluídas e paletas cromáticas inspiradas em displays de alta frequência. Ideal para interfaces modernas que buscam passar uma sensação híbrida, viva e tecnológica.",
  colors: [
    { hex: "#050B14", rgb: "5, 11, 20", oklch: "0.08, 0.03, 240", name: "Deep Abyss", role: "Fundo / Base" },
    { hex: "#0D1527", rgb: "13, 21, 39", oklch: "0.13, 0.04, 244", name: "Midnight Surface", role: "Superfície / Card" },
    { hex: "#00FF66", rgb: "0, 255, 102", oklch: "0.86, 0.28, 142", name: "Vivid Bio-Green", role: "Destaque / Neon" },
    { hex: "#00F0FF", rgb: "0, 240, 255", oklch: "0.78, 0.22, 196", name: "Neon Cyan", role: "Destaque Secundário" }
  ],
  typography: {
    primary: "Geist Mono (Vercel)",
    secondary: "Instrument Serif",
    justification: "A tipografia combina a precisão técnica da Geist Mono para dados de swatches com a elegância orgânica e fashion-editorial da Instrument Serif para os títulos."
  }
};

const BACKEND_URL = "http://127.0.0.1:8000";

export default function App() {
  // Estados principais
  const [trend, setTrend] = useState<TrendDrop>(FALLBACK_TREND);
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'assistant', content: 'Olá Eugenio! Sou seu **Synesthetic Co-pilot**. Com base no nosso design system de Berlim, posso te ajudar a direcionar conceitos visuais, ajustar harmonias de cores ou analisar briefs para seus novos projetos. O que estamos criando hoje?' }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [toasts, setToasts] = useState<Toast[]>([]);
  
  // Estados do Gerador de Paletas
  const [brandName, setBrandName] = useState('');
  const [brandDesc, setBrandDesc] = useState('');
  const [aesthetic, setAesthetic] = useState('');
  const [generatedPalette, setGeneratedPalette] = useState<Color[] | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [apiOnline, setApiOnline] = useState(false);

  // Refs para controle de rolagem
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Verifica saúde da API do Backend ao carregar
  useEffect(() => {
    fetch(`${BACKEND_URL}/`)
      .then(res => res.json())
      .then(data => {
        if (data.status === "online") {
          setApiOnline(true);
          // Se estiver online, carrega os dados reais de tendência
          fetchTrends();
        }
      })
      .catch(() => {
        setApiOnline(false);
        showToast("Backend offline. Rodando em modo standalone local.");
      });
  }, []);

  // Auto-scroll para mensagens de chat (Princípio de Usabilidade Emil Kowalski)
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  // Busca dados de tendência reais do Backend
  const fetchTrends = async () => {
    try {
      const res = await fetch(`${BACKEND_URL}/api/trends`);
      const data = await res.json();
      setTrend(data);
    } catch (e) {
      console.error("Erro ao buscar tendências:", e);
    }
  };

  // Gerencia notificações Toast (Estilo Sonner)
  const showToast = (message: string) => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts(prev => [...prev, { id, message }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 4000); // 4 segundos de duração
  };

  // Copia o valor cromático ao clipboard e alerta o usuário com animação
  const handleCopy = (value: string, label: string) => {
    navigator.clipboard.writeText(value);
    showToast(`Copiado: ${label} (${value})`);
  };

  // Envio de mensagem para o Co-pilot via API do Nebius
  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMsg: ChatMessage = { role: 'user', content: inputMessage };
    setMessages(prev => [...prev, userMsg]);
    setInputMessage('');
    setIsTyping(true);

    try {
      if (apiOnline) {
        const response = await fetch(`${BACKEND_URL}/api/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            messages: [...messages, userMsg].map(m => ({ role: m.role, content: m.content }))
          })
        });
        const data = await response.json();
        setMessages(prev => [...prev, { role: 'assistant', content: data.reply }]);
      } else {
        // Simulação offline inteligente se o backend não estiver rodando
        setTimeout(() => {
          setMessages(prev => [...prev, { 
            role: 'assistant', 
            content: `[MODO OFFLINE] Recebi sua ideia sobre o projeto! Com base na nossa direção atual do **${trend.theme}**, eu sugiro trabalharmos com contrastes acentuados de luminosidade. Tente usar o **${trend.colors[2].hex}** como o seu ponto focal primário contra o fundo denso em **${trend.colors[0].hex}** para causar máxima vibração visual.` 
          }]);
        }, 1200);
      }
    } catch (err) {
      showToast("Falha ao enviar mensagem ao co-pilot.");
    } finally {
      setIsTyping(false);
    }
  };

  // Envia brief para o gerador de paletas inteligente (Nebius Skill)
  const handleGeneratePalette = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!brandName || !brandDesc) {
      showToast("Por favor, insira o nome e a descrição da marca.");
      return;
    }

    setIsGenerating(true);
    setGeneratedPalette(null);

    try {
      if (apiOnline) {
        const response = await fetch(`${BACKEND_URL}/api/generate-palette`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            brand_name: brandName,
            description: brandDesc,
            aesthetic_goal: aesthetic || "Minimalista, moderno, elegante"
          })
        });
        const data = await response.json();
        
        // Converte o retorno do GPT em um formato de cores compatível
        if (data.palette && data.palette.colors) {
          setGeneratedPalette(data.palette.colors);
          showToast("Paleta de cores gerada sob medida pela Nebius!");
        } else {
          // Fallback estruturado de cores caso o JSON seja ligeiramente diferente
          setGeneratedPalette([
            { hex: "#1A2E40", rgb: "26, 46, 64", oklch: "0.24, 0.05, 230", name: "Steel Shadow", role: "Fundo" },
            { hex: "#E9D985", rgb: "233, 217, 133", oklch: "0.86, 0.12, 95", name: "Warm Amber", role: "Acento" },
            { hex: "#B2C9AB", rgb: "178, 201, 171", oklch: "0.78, 0.06, 130", name: "Sage Gray", role: "Suporte" },
            { hex: "#05070A", rgb: "5, 7, 10", oklch: "0.04, 0.02, 240", name: "Absolute Ink", role: "Base" }
          ]);
          showToast("Paleta estruturada com fallback conceitual.");
        }
      } else {
        // Simulação offline estilizada
        setTimeout(() => {
          setGeneratedPalette([
            { hex: "#112233", rgb: "17, 34, 51", oklch: "0.15, 0.04, 240", name: "Brutalist Concrete", role: "Fundo / Base" },
            { hex: "#FF5533", rgb: "255, 85, 51", oklch: "0.62, 0.23, 30", name: "Active Terracotta", role: "Destaque" },
            { hex: "#A0AAB5", rgb: "160, 170, 181", oklch: "0.68, 0.02, 240", name: "Slate Trim", role: "Bordas" },
            { hex: "#FFFFFF", rgb: "255, 255, 255", oklch: "1.00, 0.00, 0", name: "Pure Light", role: "Tipografia" }
          ]);
          showToast("[MODO OFFLINE] Paleta brutalista de amostra criada!");
        }, 1800);
      }
    } catch (err) {
      showToast("Erro de comunicação com o gerador da Nebius.");
    } finally {
      setIsGenerating(false);
    }
  };

  // Gera download de swatches CSS
  const handleDownloadSwatches = (swatches: Color[]) => {
    let cssText = `:root {\n`;
    swatches.forEach(color => {
      const cleanName = color.name.toLowerCase().replace(/\s+/g, '-');
      cssText += `  --color-${cleanName}: ${color.hex}; /* ${color.role} */\n`;
    });
    cssText += `}`;

    const element = document.createElement("a");
    const file = new Blob([cssText], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = "palette-variables.css";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    showToast("Download das variáveis CSS iniciado!");
  };

  return (
    <div className="app-container">
      {/* HEADER DA APLICAÇÃO */}
      <header className="app-header">
        <div className="logo-container">
          <div className="logo-icon" />
          <span className="logo-text">Synesthetic Palette</span>
        </div>
        <div className="header-status">
          <div className="status-dot" style={{ backgroundColor: apiOnline ? '#00FF66' : '#FF5533', boxShadow: apiOnline ? '0 0 8px #00FF66' : '0 0 8px #FF5533' }} />
          <span>{apiOnline ? 'NEBIUS ACTIVE' : 'LOCAL STANDALONE'}</span>
        </div>
      </header>

      {/* GRADE PRINCIPAL DA UI */}
      <main className="app-main">
        {/* PAINEL ESQUERDO: DASHBOARD DE TENDÊNCIAS E GERADOR DE PALETAS */}
        <section className="dashboard-panel">
          <span className="editorial-tag">Drop Semanal • {trend.week}</span>
          <h1 className="editorial-title">{trend.theme}</h1>
          <p className="editorial-desc">{trend.concept}</p>

          {/* PALETA DO DROP SEMANAL */}
          <div className="drop-card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 style={{ fontStyle: 'italic', fontFamily: 'var(--font-display)', fontSize: '22px' }}>Amostras Cromáticas</h3>
              <button 
                onClick={() => handleDownloadSwatches(trend.colors)}
                style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px' }}
                title="Baixar variáveis de CSS"
              >
                <Download size={14} /> Exportar CSS
              </button>
            </div>
            <div className="swatch-grid">
              {trend.colors.map((color, i) => (
                <div key={i} className="swatch" onClick={() => handleCopy(color.hex, color.name)}>
                  <div className="swatch-color-preview" style={{ backgroundColor: color.hex }}>
                    <div className="swatch-copy-overlay">
                      <Copy size={16} /> Copiar HEX
                    </div>
                  </div>
                  <div className="swatch-info">
                    <div className="swatch-name">{color.name}</div>
                    <div className="swatch-role">{color.role}</div>
                    <div className="swatch-code">{color.hex}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* PAR TIPOGRÁFICO DO DROP */}
          <div className="typography-pairing">
            <h3 style={{ fontStyle: 'italic', fontFamily: 'var(--font-display)', fontSize: '22px', marginBottom: '10px' }}>Equilíbrio Tipográfico</h3>
            <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>{trend.typography.justification}</p>
            <div className="pairing-fonts">
              <span className="pairing-preview-serif" style={{ fontFamily: 'var(--font-display)' }}>{trend.typography.secondary} (Italic Display)</span>
              <span className="pairing-preview-mono" style={{ fontFamily: 'var(--font-mono)' }}>{trend.typography.primary} (Precision Text)</span>
            </div>
          </div>

          <hr style={{ borderColor: 'var(--border-color)', margin: '40px 0' }} />

          {/* BRIEF DISSECTOR (GERADOR INTELIGENTE DE PALETAS) */}
          <div className="brief-dissector-section">
            <h2 className="form-title">Dissecador de Briefing</h2>
            <p style={{ fontSize: '14px', color: 'var(--text-muted)', marginBottom: '24px' }}>
              Insira os detalhes do projeto abaixo. A inteligência da **Nebius** dissecará os atributos sensoriais do texto e gerará uma paleta conceitual sob medida.
            </p>
            <form onSubmit={handleGeneratePalette} className="generator-form">
              <div className="input-group">
                <label className="input-label">Nome da Marca / Projeto</label>
                <input 
                  type="text" 
                  className="input-field" 
                  placeholder="Ex.: Studio Aura" 
                  value={brandName}
                  onChange={(e) => setBrandName(e.target.value)}
                />
              </div>
              <div className="input-group">
                <label className="input-label">Descrição Conceitual / Briefing</label>
                <textarea 
                  className="textarea-field" 
                  placeholder="Ex.: Um estúdio de yoga moderno e minimalista em Berlim Oriental focado em iluminação quente, plantas e concreto escovado..."
                  value={brandDesc}
                  onChange={(e) => setBrandDesc(e.target.value)}
                />
              </div>
              <div className="input-group">
                <label className="input-label">Meta Estética (Opcional)</label>
                <input 
                  type="text" 
                  className="input-field" 
                  placeholder="Ex.: Brutalista, Etéreo, Acolhedor..." 
                  value={aesthetic}
                  onChange={(e) => setAesthetic(e.target.value)}
                />
              </div>
              <button type="submit" className="submit-btn" disabled={isGenerating}>
                {isGenerating ? (
                  <>
                    <RefreshCw className="spinning" size={16} /> Dissecando Briefing...
                  </>
                ) : (
                  <>
                    <Sparkles size={16} /> Gerar Paleta Conceitual
                  </>
                )}
              </button>
            </form>

            {/* PALETA GERADA DINAMICAMENTE */}
            {generatedPalette && (
              <div className="drop-card" style={{ marginTop: '24px', border: '1px solid var(--accent-cyan)', animation: 'bubble-appear 0.4s var(--ease-spring)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <h3 style={{ fontStyle: 'italic', fontFamily: 'var(--font-display)', fontSize: '22px', color: 'var(--accent-cyan)' }}>Paleta sob Medida</h3>
                  <button 
                    onClick={() => handleDownloadSwatches(generatedPalette)}
                    style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px' }}
                  >
                    <Download size={14} /> Swatch CSS
                  </button>
                </div>
                <div className="swatch-grid">
                  {generatedPalette.map((color, i) => (
                    <div key={i} className="swatch" onClick={() => handleCopy(color.hex, color.name)} style={{ border: '1px solid rgba(0, 240, 255, 0.15)' }}>
                      <div className="swatch-color-preview" style={{ backgroundColor: color.hex }}>
                        <div className="swatch-copy-overlay">
                          <Copy size={16} /> Copiar HEX
                        </div>
                      </div>
                      <div className="swatch-info">
                        <div className="swatch-name">{color.name}</div>
                        <div className="swatch-role">{color.role}</div>
                        <div className="swatch-code">{color.hex}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </section>

        {/* PAINEL DIREITO: INTERACTIVE AI CO-PILOT (STYLE CONCIERGE) */}
        <section className="copilot-panel">
          <div className="chat-container">
            <div className="chat-header">
              <span className="editorial-tag">Style Concierge</span>
              <h2 style={{ fontStyle: 'italic', fontFamily: 'var(--font-display)', fontSize: '28px', fontWeight: 500 }}>AI Co-pilot</h2>
              <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Sugestões estéticas em tempo real alimentadas pelo Nemotron da NVIDIA.</p>
            </div>

            {/* HISTÓRICO DE MENSAGENS */}
            <div className="chat-messages">
              {messages.map((msg, i) => (
                <div key={i} className={`message-bubble ${msg.role}`}>
                  {/* Formatação básica de markdown para negritos simples e listas */}
                  {msg.content.split('\n').map((line, idx) => {
                    
                    // Substitui negritos em markdown (**texto**) por elementos HTML
                    const boldRegex = /\*\*(.*?)\*\*/g;
                    const parts = [];
                    let lastIndex = 0;
                    let match;
                    
                    while ((match = boldRegex.exec(line)) !== null) {
                      if (match.index > lastIndex) {
                        parts.push(line.substring(lastIndex, match.index));
                      }
                      parts.push(<strong key={match.index} style={{ color: 'var(--accent-green)' }}>{match[1]}</strong>);
                      lastIndex = boldRegex.lastIndex;
                    }
                    if (lastIndex < line.length) {
                      parts.push(line.substring(lastIndex));
                    }

                    return (
                      <p key={idx} style={{ marginBottom: idx < msg.content.split('\n').length - 1 ? '8px' : '0' }}>
                        {parts.length > 0 ? parts : line}
                      </p>
                    );
                  })}
                </div>
              ))}

              {/* INDICADOR DE DIGITAÇÃO / PENSAMENTO DO COPILOT */}
              {isTyping && (
                <div className="thinking-container">
                  <div className="thinking-dots">
                    <div className="thinking-dot" />
                    <div className="thinking-dot" />
                    <div className="thinking-dot" />
                  </div>
                  <span>Synesthetic Palette está formulando conselhos...</span>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>

            {/* INPUT DE ENVIO DE MENSAGENS */}
            <form onSubmit={handleSendMessage} className="chat-input-container">
              <input 
                type="text" 
                className="chat-input" 
                placeholder="Pergunte ao Co-pilot sobre cores, conceitos visuais ou direções..." 
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                disabled={isTyping}
              />
              <button type="submit" className="send-btn" disabled={isTyping || !inputMessage.trim()}>
                <Send size={16} />
              </button>
            </form>
          </div>
        </section>
      </main>

      {/* MINI-TOAST DE MICRO-INTERAÇÕES (ESTILO SONNER) */}
      <div className="toast-container">
        {toasts.map(toast => (
          <div key={toast.id} className="toast">
            <Check className="toast-icon" size={16} />
            <span>{toast.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
