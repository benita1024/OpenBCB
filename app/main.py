from fastapi import FastAPI
from app.rpc import get_signatures
from app.rpc import get_transactions
from app.graph import build_graph
from app.signals import wash_trading_signal, fan_out_signal, clustering_signal, velocity_signal


app = FastAPI(title="Flare", description="Solana wallet anomaly detection")


@app.get("/test-signals")
async def test_signals():
    wallet = "vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg"
    txns = await get_transactions(wallet, limit=20)
    G = build_graph(txns, wallet)
    return {
        "wash_trading": wash_trading_signal(G, wallet),
        "fan_out": fan_out_signal(G, wallet),
        "clustering": clustering_signal(G, wallet),
        "velocity": velocity_signal(G, wallet)
    }

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