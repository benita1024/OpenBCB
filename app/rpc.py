import httpx
import asyncio
from typing import Optional

SOLANA_RPC_URL = "https://api.devnet.solana.com"
SEMAPHORE = asyncio.Semaphore(10)

async def get_signatures(wallet: str, limit: int = 100) -> list[dict]:
    async with httpx.AsyncClient() as client:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [wallet, {"limit": limit}]
        }
        response = await client.post(SOLANA_RPC_URL, json=payload, timeout=30)
        data = response.json()
        return data.get("result", [])

async def get_transaction(client: httpx.AsyncClient, signature: str) -> Optional[dict]:
    async with SEMAPHORE:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [signature, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]
        }
        try:
            response = await client.post(SOLANA_RPC_URL, json=payload, timeout=30)
            return response.json().get("result")
        except Exception:
            return None

async def get_transactions(wallet: str, limit: int = 100) -> list[dict]:
    signatures = await get_signatures(wallet, limit)
    if not signatures:
        return []

    async with httpx.AsyncClient(timeout=60) as client:
        tasks = [get_transaction(client, s["signature"]) for s in signatures]
        results = await asyncio.gather(*tasks)

    return [r for r in results if r is not None]