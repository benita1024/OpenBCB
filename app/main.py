from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.rpc import get_transactions
from app.graph import build_graph
from app.scorer import score_wallet
from app.cache import get_cached, set_cached

app = FastAPI(title="OpenBCB", description="Solana wallet anomaly detection")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    wallet: str
    limit: int = 100

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        cached = await get_cached(request.wallet)
        if cached:
            return {**cached, "cached": True}

        txns = await get_transactions(request.wallet, limit=request.limit)
        if not txns:
            raise HTTPException(status_code=404, detail="No transactions found for this wallet")

        G = build_graph(txns, request.wallet)
        result = score_wallet(G, request.wallet)
        response = {
            "wallet": request.wallet,
            "transactions_analyzed": len(txns),
            **result
        }

        await set_cached(request.wallet, response)
        return {**response, "cached": False}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))