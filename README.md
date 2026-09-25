# Synesthetic Palette — Personal AI Design Co-pilot

> **Weekly color and design-trend forecasting powered by Nebius AI Token Factory and NVIDIA open models.**  
> Built for the *Nebius x NVIDIA Global AI Hackathon 2026*.

---

## 🎨 Overview

**Synesthetic Palette** is a personal AI design co-pilot that democratizes trend forecasting for graphic designers, motion artists, and small creative studios.

While enterprise trend intelligence platforms are priced out of reach for individual creators, **Synesthetic Palette** delivers weekly actionable design drops—combining highly curated color palettes (HEX, RGB, OKLCH), typography pairings, and visual direction references—grounded in real-time web insights and accelerated by advanced open models.

---

## 🚀 Key Features

*   **Weekly Trend Drops:** Every Monday, get a curated visual and sensory theme backed by real-world trend forecasting.
*   **AI Co-Pilot (Personal AI Track):** An interactive assistant always ready to dissect your client briefs, recommend complementary color strategies, and suggest typographic choices based on your active project mood.
*   **Local & Persistent Memory:** The assistant securely remembers your brand guidelines, project history, and style preferences on your local machine.
*   **Pro-grade Export Formats:** Export color mappings instantly into Figma-friendly files, CSS variables, and Adobe Swatch Exchange (ASE) formats.

---

## 🧠 Technical Architecture

The application is split into a robust Python backend and a highly polished, visual React frontend:

```
synesthetic-palette/
├── backend/            # Python FastAPI backend & AI Orchestration
│   ├── app/
│   │   ├── core/       # Nebius Token Factory integration & Prompt Templates
│   │   ├── memory/     # Local SQLite/JSON persistent state
│   │   └── main.py     # API Endpoints
│   ├── .env.example
│   └── requirements.txt
├── frontend/           # React + TypeScript Web Interface
│   ├── src/
│   │   ├── components/ # Interactive canvas, chat panel, palette previewers
│   │   ├── styles/     # Vanilla CSS design system (Clean, Minimal, High-Fidelity)
│   │   └── App.tsx
│   └── package.json
├── LICENSE             # MIT License (Mandatory for Hackathon)
└── README.md
```

### Powered By:
1.  **Nebius Token Factory:** Accelerating the text and reasoning layer via OpenAI-compatible endpoints using the ultra-fast, high-efficiency **`nvidia/Nemotron-3_5-Lightning`** model.
2.  **NVIDIA Open Models:** Utilizing advanced models for semantic mapping of visual descriptions to sensory aesthetics.
3.  **Tavily Search API:** Used for real-time web grounding and automated visual/pop-culture trend harvesting.

---

## 🛠️ Quick Start

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment variables template and configure your `NEBIUS_API_KEY`:
   ```bash
   cp .env.example .env
   ```
5. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---
© 2026 Eugenio Santiago. Built as an open-source visual co-pilot.
