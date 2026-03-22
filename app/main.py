from fastapi import FastAPI
from app.rpc import get_signatures


app = FastAPI(title="Flare", description="Solana wallet anomaly detection")

@app.get("/test-rpc")
async def test_rpc():
    sigs = await get_signatures("vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg")
    return {"signature_count": len(sigs), "first": sigs[0] if sigs else None}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(wallet: str):
    return {"wallet": wallet, "score": None, "message": "not implemented yet"}