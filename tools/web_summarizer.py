import os
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from schemas import ToolMetadata
from groq import Groq  # or whatever SDK you're using

# Setup your Groq or other LLM client
llm = Groq(api_key=os.environ["GROQ_API_KEY"])

tool_metadata = ToolMetadata(
    name="web_search_summarizer",
    description="Searches the web and summarizes results with sources.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query to summarize from web"
            }
        },
        "required": ["query"]
    }
)

def run(params):
    query = params["query"]
    urls = [url for url in search(query, num_results=3)]
    summaries = []

    for url in urls:
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.content, "html.parser")
            paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
            full_text = "\n".join(paragraphs)[:3000]

            summary_prompt = f"Summarize the following article content:\n\n{full_text}"
            summary = llm.chat.completions.create(
                messages=[{"role": "user", "content": summary_prompt}],
                model="llama3-8b-8192"
            ).choices[0].message.content.strip()

            summaries.append({"url": url, "summary": summary})
        except Exception as e:
            summaries.append({"url": url, "summary": f"Error summarizing {url}: {e}"})

    combined = "\n\n".join([f"Source: {s['url']}\n{s['summary']}" for s in summaries])
    final_prompt = f"""
    You are an intelligent assistant helping summarize search results.

    Your job is to:
    - Extract relevant points from the article summaries that directly answer the user's question.
    - Format the answer as clear and concise bullet points.
    - If the summaries do not contain enough relevant information, say:
    "Insufficient Info. Please refer to the provided sources for more information."

    --- Article Summaries ---
    {combined}

    --- User Question ---
    {query}

    --- Your Response (in bullet points or fallback message) ---
    """

    final_answer = llm.chat.completions.create(
        messages=[{"role": "user", "content": final_prompt}],
        model="llama3-8b-8192"
    ).choices[0].message.content.strip()

    return {
        "answer": final_answer,
        "sources": [s["url"] for s in summaries]
    }