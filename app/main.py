from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.rpc import get_transactions
from app.graph import build_graph
from app.scorer import score_wallet

app = FastAPI(title="OpenBCB", description="Solana wallet anomaly detection")

class AnalyzeRequest(BaseModel):
    wallet: str
    limit: int = 100

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        txns = await get_transactions(request.wallet, limit=request.limit)
        if not txns:
            raise HTTPException(status_code=404, detail="No transactions found for this wallet")
        G = build_graph(txns, request.wallet)
        result = score_wallet(G, request.wallet)
        return {
            "wallet": request.wallet,
            "transactions_analyzed": len(txns),
            **result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))