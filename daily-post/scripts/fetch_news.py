#!/usr/bin/env python3
"""从 Hacker News、Reddit、GitHub Trending 抓取 AI/LLM 相关新闻，输出 Markdown 到 ~/DailyPost/"""

import json
import os
import re
import urllib.request
import urllib.error
from datetime import datetime

# ── 配置 ──────────────────────────────────────────────
OUTPUT_DIR = os.path.expanduser("~/DailyPost")
HN_TOP = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"
REDDIT_BASE = "https://www.reddit.com"
SUBREDDITS = ["LocalLLaMA", "ClaudeAI"]
GITHUB_TRENDING = "https://github.com/trending?since=daily"

AI_KEYWORDS = [
    "ai", "llm", "gpt", "claude", "openai", "anthropic", "gemini",
    "model", "machine learning", "deep learning", "neural", "transformer",
    "diffusion", "rag", "agent", "prompt", "fine-tun", "fine tun",
    "rlhf", "token", "embedding", "vector", "chatbot", "copilot",
    "llama", "mistral", "mixtral", "weights",
    "quantization", "inference", "langchain", "langgraph",
    "mcp", "tool use", "function call", "multimodal", "vision",
    "stable diffusion", "sora", "dall-e", "midjourney",
    "retrieval", "chain of thought", "reasoning",
    "qwen", "deepseek", "yi ", "phi-", "falcon", "guanaco",
    "roleplay", "uncensored", "lora", "gguf", "ggml", "mlx",
    "ollama", "vllm", "text-generation", "webui",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


# ── 工具函数 ──────────────────────────────────────────

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def fetch_html(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode()


SHORT_KWS = {
    "ai", "llm", "gpt", "mcp", "rag", "lora", "mlx", "gguf", "ggml",
}
SHORT_KWS_PATTERN = re.compile(
    r'\b(?:' + '|'.join(re.escape(kw) for kw in SHORT_KWS) + r')\b', re.IGNORECASE
)


def match_ai(title):
    t = title.lower()
    if SHORT_KWS_PATTERN.search(t):
        return True
    return any(kw in t for kw in AI_KEYWORDS if kw not in SHORT_KWS)


# ── Hacker News ───────────────────────────────────────

def scrape_hn():
    print("  Fetching Hacker News top stories...")
    ids = fetch_json(HN_TOP)[:80]
    results = []
    for sid in ids:
        try:
            story = fetch_json(HN_ITEM.format(sid))
        except Exception:
            continue
        title = story.get("title", "")
        if not title or not match_ai(title):
            continue
        results.append({
            "title": title,
            "url": story.get("url") or f"https://news.ycombinator.com/item?id={sid}",
            "score": story.get("score", 0),
            "comments": story.get("descendants", 0),
        })
        if len(results) >= 20:
            break
    return sorted(results, key=lambda r: r["score"], reverse=True)


# ── Reddit ────────────────────────────────────────────

def scrape_reddit(sub):
    print(f"  Fetching r/{sub}...")
    data = fetch_json(f"{REDDIT_BASE}/r/{sub}/.json")
    posts = data.get("data", {}).get("children", [])
    results = []
    for p in posts[:20]:
        d = p["data"]
        results.append({
            "title": d.get("title", ""),
            "url": f"https://www.reddit.com{d.get('permalink', '')}",
            "score": d.get("score", 0),
            "comments": d.get("num_comments", 0),
            "author": d.get("author", ""),
        })
    return sorted(results, key=lambda r: r["score"], reverse=True)[:15]


# ── GitHub Trending ───────────────────────────────────

def scrape_github():
    print("  Scraping GitHub Trending...")
    html = fetch_html(GITHUB_TRENDING)
    articles = re.findall(
        r'<article[^>]*class="[^"]*Box-row[^"]*"[^>]*>(.*?)</article>',
        html, re.DOTALL,
    )
    ai_langs = {"Python", "Jupyter Notebook", "TypeScript", "Rust", "Go", "C++"}
    repos = []

    for a in articles:
        h2 = re.search(
            r'<h2[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', a, re.DOTALL
        )
        if not h2:
            continue
        href = h2.group(1)
        name = re.sub(r'\s+', ' ', h2.group(2)).strip()

        desc_m = re.search(
            r'<p[^>]*class="[^"]*col-9[^"]*"[^>]*>(.*?)</p>', a, re.DOTALL
        )
        desc = re.sub(r'\s+', ' ', desc_m.group(1)).strip() if desc_m else ""

        lang_m = re.search(r'itemprop="programmingLanguage"[^>]*>([^<]+)<', a)
        lang = lang_m.group(1).strip() if lang_m else ""

        stars_m = re.search(r'(\d[\d,]*)\s*stars?\s*today', a)
        stars = f"{stars_m.group(1)} stars today" if stars_m else ""

        if lang in ai_langs or match_ai(name) or match_ai(desc):
            repos.append({
                "title": name,
                "url": f"https://github.com{href}",
                "desc": desc,
                "lang": lang,
                "stars": stars,
            })

    return repos[:15]


# ── Markdown 生成 ─────────────────────────────────────

def build_md(hn, reddit, github):
    today = datetime.now().strftime("%Y-%m-%d")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md = [
        f"# AI/LLM Daily Report -- {today}",
        "",
        "> Sources: Hacker News, Reddit, GitHub Trending",
        "",
        "---",
        "",
        "## Hacker News",
        "",
    ]

    if hn:
        for i, item in enumerate(hn, 1):
            md.append(f"{i}. [{item['title']}]({item['url']})")
            md.append(f"   Score: {item['score']} | Comments: {item['comments']}")
            md.append("")
    else:
        md.append("*No matching AI content today*")
        md.append("")

    md += ["---", "", "## Reddit", ""]

    for sub in SUBREDDITS:
        posts = reddit.get(sub, [])
        md.append(f"### r/{sub}")
        md.append("")
        if posts:
            for i, p in enumerate(posts, 1):
                md.append(f"{i}. [{p['title']}]({p['url']})")
                md.append(
                    f"   Score: {p['score']} | Comments: {p['comments']} "
                    f"| u/{p['author']}"
                )
                md.append("")
        else:
            md.append("*No content*")
            md.append("")

    md += ["---", "", "## GitHub Trending", ""]

    if github:
        for i, r in enumerate(github, 1):
            badge = f" [{r['lang']}]" if r["lang"] else ""
            md.append(f"{i}. [{r['title']}]({r['url']}){badge}")
            if r["desc"]:
                md.append(f"   {r['desc']}")
            if r["stars"]:
                md.append(f"   {r['stars']}")
            md.append("")
    else:
        md.append("*No AI-related repos today*")
        md.append("")

    md += ["---", "", f"*Report generated at {ts}*"]
    return "\n".join(md)


# ── 入口 ──────────────────────────────────────────────

def main():
    print("AI News Scraper starting...\n")

    print("[1/3] Hacker News")
    try:
        hn = scrape_hn()
        print(f"  Found {len(hn)} AI-related items")
    except Exception as e:
        print(f"  Failed: {e}")
        hn = []

    print("\n[2/3] Reddit")
    reddit = {}
    for sub in SUBREDDITS:
        try:
            reddit[sub] = scrape_reddit(sub)
            print(f"  r/{sub}: {len(reddit[sub])} items")
        except Exception as e:
            print(f"  r/{sub} failed: {e}")
            reddit[sub] = []

    print("\n[3/3] GitHub Trending")
    try:
        gh = scrape_github()
        print(f"  Found {len(gh)} AI repos")
    except Exception as e:
        print(f"  Failed: {e}")
        gh = []

    print("\nGenerating Markdown...")
    md = build_md(hn, reddit, gh)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"{datetime.now().strftime('%Y-%m-%d')}.md"
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Written to: {path}")
    print(f"Size: {len(md)} chars, {len(md.splitlines())} lines")


if __name__ == "__main__":
    main()
