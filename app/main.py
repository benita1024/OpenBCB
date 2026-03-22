from fastapi import FastAPI
from app.rpc import get_signatures
from app.rpc import get_transactions
from app.graph import build_graph


app = FastAPI(title="Flare", description="Solana wallet anomaly detection")

@app.get("/test-graph")
async def test_graph():
    wallet = "vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg"
    txns = await get_transactions(wallet, limit=5)
    G = build_graph(txns, wallet)
    return {
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "sample_nodes": list(G.nodes)[:5]
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