import networkx as nx

def extract_transfers(transaction: dict) -> list[dict]:
    transfers = []
    try:
        accounts = transaction["transaction"]["message"]["accountKeys"]
        pre = transaction["meta"]["preBalances"]
        post = transaction["meta"]["postBalances"]
        block_time = transaction.get("blockTime", 0)

        for i, account in enumerate(accounts):
            address = account["pubkey"] if isinstance(account, dict) else account
            delta = post[i] - pre[i]
            if delta > 0 and i != 0:
                sender = accounts[0]["pubkey"] if isinstance(accounts[0], dict) else accounts[0]
                transfers.append({
                    "from": sender,
                    "to": address,
                    "amount": delta / 1e9,
                    "timestamp": block_time
                })
    except (KeyError, IndexError, TypeError):
        pass
    return transfers

def build_graph(transactions: list[dict], target_wallet: str) -> nx.DiGraph:
    G = nx.DiGraph()
    G.add_node(target_wallet, is_target=True)

    for tx in transactions:
        for transfer in extract_transfers(tx):
            sender = transfer["from"]
            receiver = transfer["to"]
            amount = transfer["amount"]
            timestamp = transfer["timestamp"]

            if not G.has_edge(sender, receiver):
                G.add_edge(sender, receiver,
                    amount=amount,
                    timestamps=[timestamp],
                    count=1
                )
            else:
                G[sender][receiver]["timestamps"].append(timestamp)
                G[sender][receiver]["count"] += 1
                G[sender][receiver]["amount"] += amount

    return G