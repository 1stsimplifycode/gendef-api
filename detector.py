import networkx as nx
import json
import requests
from datetime import datetime
import os

MISTRAL_API_KEY = "SqUX4Q0EbojcQRdA3iHo5rhn2lQIsjRl"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
LOG_FILE = "sample_log.json"
GRAPH_STORE = "stored_graphs.json"


def load_logs():
    try:
        with open("sample_log.json", 'r') as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except json.JSONDecodeError:
        return []


def build_graph(data):
    G = nx.Graph()
    for entry in data:
        ip = entry['ip']
        user = entry['username']
        G.add_node(ip, type='ip')
        G.add_node(user, type='user')
        G.add_edge(ip, user)
    return G

def detect_distributed(G, threshold=5):
    alerts = []
    for user in [n for n, d in G.nodes(data=True) if d['type'] == 'user']:
        ips = [n for n in G.neighbors(user) if G.nodes[n]['type'] == 'ip']
        if len(ips) >= threshold:
            alerts.append((user, ips))
    return alerts

def generate_explanation(user, ips):
    prompt = f"""
    Multiple IP addresses: {', '.join(ips)} have attempted to access the account '{user}'.
    This may indicate a distributed brute force web login attack.
    Generate a brief explanation and firewall rules to block these IPs.
    """
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "mistral-small",
        "messages": [
            {"role": "system", "content": "You are a cybersecurity assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    res = requests.post(MISTRAL_API_URL, headers=headers, json=body)
    return res.json()['choices'][0]['message']['content']

def persist_graph(G):
    from networkx.readwrite import json_graph
    data = json_graph.node_link_data(G)
    timestamp = datetime.now().isoformat()
    entry = {"timestamp": timestamp, "graph": data}

    if os.path.exists(GRAPH_STORE):
        with open(GRAPH_STORE, 'r') as f:
            existing = json.load(f)
    else:
        existing = []

    existing.append(entry)
    with open(GRAPH_STORE, 'w') as f:
        json.dump(existing, f, indent=4)

    return True
