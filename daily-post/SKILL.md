---
name: daily-post
description: 从 Hacker News、Reddit (r/LocalLLaMA, r/ClaudeAI) 和 GitHub Trending 实时抓取 AI/LLM 相关新闻和热门仓库，整理为 Markdown 写入 ~/DailyPost/。当用户要获取最新 AI 资讯、AI 新闻汇总、每日 AI 速报、AI 工具动态时使用。触发词：AI 新闻, AI 资讯, 每日 AI, daily AI, AI 速报, scrape AI news, Hacker News, GitHub trending, daily post, /daily-post
---

# daily-post

从三个数据源抓取 AI/LLM 相关内容，输出到 `~/DailyPost/YYYY-MM-DD.md`。

## 使用方式

运行抓取脚本：

```bash
python3 scripts/fetch_news.py
```

输出文件：`~/DailyPost/YYYY-MM-DD.md`，按日期命名，同一天多次运行会覆盖。

## 数据源与抓取策略

| 来源 | 方式 | 筛选策略 |
|------|------|----------|
| Hacker News | 官方 Firebase API | 从 Top 80 按标题关键词过滤，最多 20 条 |
| Reddit r/LocalLLaMA + r/ClaudeAI | `.json` 后缀直接请求 | 取 hot 前 20，最多各 15 条 |
| GitHub Trending | HTML 页面正则解析 | 按语言 + 关键词过滤，最多 15 个仓库 |

## 关键词列表

脚本内 `AI_KEYWORDS` 包含约 60 个 AI/LLM 领域关键词：模型名（gpt, claude, llama, deepseek...）、技术术语（rag, embeddings, quantization...）、工具链（ollama, vllm, langchain...）等。短关键词（ai, llm, mcp 等）使用词边界匹配避免误匹配。

## 修改筛选规则

编辑 `scripts/fetch_news.py` 中的：
- `AI_KEYWORDS` — 增删关键词
- `AI_LANGS`（`scrape_github` 函数内）— 调整 GitHub 语言过滤
- `match_ai()` — 修改匹配逻辑
