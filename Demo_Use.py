# streamlit_app.py

import streamlit as st
import requests

# MCP server URL
MCP_URL = "https://free-web-search.onrender.com/"  # Replace with your actual Render URL

st.set_page_config(page_title="Web Search Summarizer", layout="centered")
st.title("🔍 Web Search Summarizer")

query = st.text_input("Enter your search query:")

if st.button("Search and Summarize") and query.strip():
    with st.spinner("Searching the web and summarizing..."):
        payload = {
            "jsonrpc": "2.0",
            "method": "web_search_summarizer",
            "params": {"query": query},
            "id": "1"
        }

        try:
            res = requests.post(MCP_URL, json=payload, timeout=300)
            res.raise_for_status()
            result = res.json()

            if "error" in result and result["error"]:
                msg = result["error"].get("message", "Unknown error")
                st.error(f"Tool Error: {msg}")
            elif "result" in result:
                st.subheader("🧠 Summary")
                st.markdown(result["result"]["answer"])

                st.subheader("🔗 Sources")
                for url in result["result"].get("sources", []):
                    st.markdown(f"- [{url}]({url})")
            else:
                st.error("Unexpected response format.")

        except Exception as e:
            st.error(f"Request failed: {e}")
