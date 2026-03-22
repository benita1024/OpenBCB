# OpenBCB

Open-source Solana wallet anomaly scoring API. Brings graph-based AML signal detection to small fintechs, CDFIs, and indie developers priced out of Chainalysis.

## What it does

Takes any Solana wallet address and returns a structured risk score based on four on-chain behavioral signals:

- **Wash trading** — detects round-trip transactions between wallets
- **Fan-out burst** — flags sudden sends to many new wallets in a short window
- **Counterparty clustering** — measures how isolated a wallet's transaction network is
- **Velocity anomaly** — identifies bot-like transaction frequency

## Stack

- **Backend** — FastAPI, NetworkX, Redis, Solana RPC
- **Frontend** — Next.js, Tailwind CSS
- **Infra** — Docker, Digital Ocean

## Quickstart

**Backend**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

**Redis**
```bash
brew services start redis
```

## API
```bash
curl -X POST "http://localhost:8000/analyze" \
-H "Content-Type: application/json" \
-d '{"wallet": "YOUR_WALLET_ADDRESS", "limit": 50}'
```

**Response**
```json
{
  "wallet": "...",
  "transactions_analyzed": 50,
  "overall_score": 24.9,
  "risk_level": "low",
  "signals": {
    "wash_trading": 0.0,
    "fan_out": 0.0,
    "clustering": 0.998,
    "velocity": 0.0
  },
  "cached": false
}
```

## Risk levels

| Score | Level |
|-------|-------|
| 0–39 | Low |
| 40–69 | Medium |
| 70–100 | High |

## Why this exists

Chainalysis costs $50k+/year. Small CDFIs, crypto-native startups, and indie fintech developers have no affordable alternative for on-chain AML signal detection. OpenBCB is free, open source, and deployable in one command.