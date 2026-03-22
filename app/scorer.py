import networkx as nx
from app.signals import wash_trading_signal, fan_out_signal, clustering_signal, velocity_signal

WEIGHTS = {
    "wash_trading": 0.35,
    "fan_out": 0.25,
    "clustering": 0.25,
    "velocity": 0.15
}

def score_wallet(G: nx.DiGraph, target: str) -> dict:
    signals = {
        "wash_trading": round(wash_trading_signal(G, target), 4),
        "fan_out": round(fan_out_signal(G, target), 4),
        "clustering": round(clustering_signal(G, target), 4),
        "velocity": round(velocity_signal(G, target), 4)
    }

    weighted_score = sum(signals[k] * WEIGHTS[k] for k in signals)
    overall = round(weighted_score * 100, 1)

    risk_level = (
        "high" if overall >= 70
        else "medium" if overall >= 40
        else "low"
    )

    return {
        "overall_score": overall,
        "risk_level": risk_level,
        "signals": signals,
        "weights": WEIGHTS
    }