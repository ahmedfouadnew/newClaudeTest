# FRC / FTC Assistant

An AI chatbot specializing in FIRST Robotics Competition (FRC) and FIRST Tech Challenge (FTC) — robot design, programming, game strategy, and season-specific knowledge.

## Setup

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in your API keys in .env
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## API Keys needed
- `ANTHROPIC_API_KEY` — from https://console.anthropic.com
- `TBA_API_KEY` — from https://www.thebluealliance.com/account (coming in Step 4)
