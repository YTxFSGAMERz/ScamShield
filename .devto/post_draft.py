import json
import os
import sys
import requests
from pathlib import Path

api_key = os.getenv("DEVTO_API_KEY")
if not api_key and not sys.stdin.isatty():
    api_key = sys.stdin.read().strip()

if not api_key:
    print("ERROR: DEVTO_API_KEY missing.")
    sys.exit(1)

meta_file = Path(__file__).parent / "meta.json"
post_file = Path(__file__).parent / "post.md"

with open(meta_file, "r", encoding="utf-8") as f:
    meta = json.load(f)

with open(post_file, "r", encoding="utf-8") as f:
    body_markdown = f.read()

payload = {
    "article": {
        "title": meta.get("title"),
        "body_markdown": body_markdown,
        "published": False,
        "tags": meta.get("tags", []),
        "description": meta.get("description"),
        "main_image": meta.get("main_image"),
    }
}

headers = {
    "api-key": api_key,
    "accept": "application/vnd.forem.api-v1+json",
    "content-type": "application/json",
}

response = requests.post("https://dev.to/api/articles", headers=headers, json=payload, timeout=30)

if response.status_code in (200, 201):
    data = response.json()
    draft_id = data.get("id")
    draft_url = data.get("url")
    print(f"Draft ID: {draft_id}")
    print(f"Draft URL: {draft_url}")
else:
    print(f"Failed to create draft. HTTP {response.status_code}: {response.text}")
    sys.exit(1)
