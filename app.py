import streamlit as st
import time
import json
import os
from detector import load_logs, build_graph, detect_distributed, generate_explanation, persist_graph

CONFIG_FILE = "config.json"

def load_vercel_url():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get("vercel_url", "")
        except json.JSONDecodeError:
            return ""  # fallback if file is empty or invalid
    return ""

def save_vercel_url(url):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"vercel_url": url}, f, indent=4)

# Streamlit UI
st.set_page_config(page_title="GENDEF Web Monitor", layout="wide")
st.title("🕵️ GENDEF: Website Brute Force Detection")

# Load last saved URL
default_url = load_vercel_url()
vercel_url = st.text_input(
    "Enter your Vercel login endpoint URL (e.g., https://your-site.vercel.app/api/login)",
    value=default_url
)

threshold = st.slider("Attack Detection Threshold (IPs per User)", 2, 20, 5)
start = st.button("🚀 Start Web Monitoring")

if start:
    if not vercel_url.strip():
        st.error("⚠️ Please enter the Vercel URL before starting monitoring.")
    else:
        save_vercel_url(vercel_url)  # Persist entered URL
        st.success(f"Monitoring started for: {vercel_url}")
        output = st.empty()

        while True:
            try:
                logs = load_logs()
                G = build_graph(logs)
                alerts = detect_distributed(G, threshold)
                persist_graph(G)

                if alerts:
                    for user, ips in alerts:
                        explanation = generate_explanation(user, ips)
                        output.markdown(f"## 🚨 Attack on `{user}`")
                        output.markdown(f"**IPs:** `{', '.join(ips)}`")
                        output.markdown(f"### 🔍 Mistral Analysis\n```\n{explanation}\n```")
                time.sleep(10)
            except Exception as e:
                st.error(f"Monitoring error: {e}")
                break
