---
name: annual-report
description: "Generate a personalized Claude Code annual usage report with programmer-style aesthetics (GitHub Dark theme, JetBrains Mono font, terminal/code block visualizations). Use when user asks for: (1) Annual report generation, (2) Usage statistics summary, (3) Claude Code year in review. Trigger keywords: annual report, year review, usage report, 年度报告, 年终总结."
---

# Annual Report Generator

Generate a beautiful, personalized HTML annual report for Claude Code usage. The report should be **dynamically generated** based on user's unique data patterns, not just template filling.

## Data Collection

**IMPORTANT**: Use the data collection script to gather all statistics accurately.

### Step 1: Run Collection Script

```bash
python3 /path/to/annual-report/scripts/collect_all.py --year 2025
```

The script outputs a comprehensive JSON to stdout containing all data sources.

### Step 2: Parse JSON Output

The JSON structure:
```json
{
  "meta": {
    "generated_at": "...",
    "year": 2025,
    "data_sources": {
      "code_proxy": {"status": "ok", "records": 5078},
      "stats_cache": {"status": "ok"},
      "history": {"status": "ok", "entries": 12345},
      "todos": {"status": "ok", "files": 515},
      "file_history": {"status": "ok", "sessions": 74},
      "plans": {"status": "ok", "files": 18}
    }
  },
  "code_proxy": { ... },
  "stats_cache": { ... },
  "history": { ... },
  "todos": { ... },
  "file_history": { ... },
  "plans": { ... },
  "derived": {
    "milestones": [...]
  }
}
```

### Data Sources (Priority Order)

#### 1. Code Proxy Database (PRIMARY - if available)
Location: `~/.code_proxy/code_proxy.db`

**This is the richest data source.** When available, it provides:
- Total API requests and token usage
- Per-model statistics (requests, tokens, response time)
- Hourly and daily distribution
- Endpoint usage breakdown
- Response time percentiles (p50, p90, p99)

#### 2. stats-cache.json (Core Statistics)
Location: `~/.claude/stats-cache.json`

Contains: session counts, message counts, model usage, hour distribution, longest session.

#### 3. history.jsonl (Project Distribution)
Location: `~/.claude/history.jsonl`

Contains: project paths, timestamps, conversation history.

#### 4. todos/*.json (Task Tracking)
Location: `~/.claude/todos/`

Contains: task status (completed/pending/in_progress), completion rates.

#### 5. file-history/ (Edit Activity)
Location: `~/.claude/file-history/`

Contains: sessions with file edits, most edited files.

#### 6. plans/*.md (Architectural Thinking)
Location: `~/.claude/plans/`

Contains: plan file count for architectural thinking score.

## Report Generation Philosophy

**DO NOT simply fill a template with placeholders.**

Instead:
1. Analyze the collected data to find **unique patterns and stories**
2. Identify what makes this user's usage **distinctive**
3. Generate content that **tells their personal story**
4. Choose which sections to include based on **data richness**

### Personalization Examples

**If user is extreme night owl (80%+ activity after 20:00)**:
- Lead with "Midnight Coder" persona
- Include a "Your Night Shift" section with late-night stats
- Add insight about peak creativity hours

**If user has one dominant project (>60%)**:
- Feature that project prominently
- Tell the story of that project's development
- Show project-specific milestones

**If user switched models frequently**:
- Deep dive into model strategy section
- Compare performance across models
- Highlight smart routing patterns

**If user has high task completion (>70%)**:
- Emphasize productivity achievements
- Show task completion streaks
- Feature "Getting Things Done" badge

**If user codes on holidays**:
- Call out holiday coding sessions
- Add "Dedicated Developer" insight
- Show specific holiday stats

## Visual Style Guide

Reference `assets/template.html` for styling. Key elements:

### CRITICAL: No Emoji Policy

**NEVER use emoji in the generated report.** Emoji breaks the professional, programmer-aesthetic style.

❌ **DO NOT**:
```html
<span>🚀 Launches</span>
<span>⭐ Stars</span>
<h2>📊 Statistics</h2>
```

✅ **DO**: Use inline SVG icons instead:
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="..."/>
</svg>
```

### SVG Icon Examples

Use these minimal, stroke-based SVG icons (matching the GitHub Dark aesthetic):

**Moon (Night Owl)**:
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
</svg>
```

**Sun (Early Bird)**:
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>
</svg>
```

**Clock (Time)**:
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
</svg>
```

**Code (Programming)**:
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/>
</svg>
```

**Check (Success/Complete)**:
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/>
</svg>
```

**Folder (Project)**:
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
</svg>
```

**Zap (Fast/Performance)**:
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>
</svg>
```

**Terminal (Command Line)**:
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="m4 17 6-6-6-6M12 19h8"/>
</svg>
```

**Chart (Statistics)**:
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>
</svg>
```

**Git Branch (Version Control)**:
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M6 21V9a9 9 0 0 0 9 9"/>
</svg>
```

When you need an icon not listed above, create a simple stroke-based SVG that matches this style:
- `viewBox="0 0 24 24"`
- `fill="none"`
- `stroke="currentColor"` (inherits text color)
- `stroke-width="1.5"`

### Color Palette (GitHub Dark)
```css
--bg: #0d1117;
--bg-secondary: #161b22;
--bg-tertiary: #21262d;
--border: #30363d;
--text: #c9d1d9;
--text-dim: #8b949e;
--green: #3fb950;
--amber: #d29922;
--blue: #58a6ff;
--purple: #a371f7;
```

### Typography
- Font: JetBrains Mono (Google Fonts)
- Base size: 14px
- Monospace throughout

### Layout
- Full-screen scroll-snap sections
- `scroll-snap-type: y mandatory` on html
- Each section is `min-height: 100vh`

### Visual Components (mix and match based on data)

**Terminal Window**: For command-line style displays
```html
<div class="terminal">
  <div class="terminal-header">
    <div class="terminal-dot red"></div>
    <div class="terminal-dot yellow"></div>
    <div class="terminal-dot green"></div>
  </div>
  <div class="terminal-body">...</div>
</div>
```

**Code Block**: For structured data with syntax highlighting
```html
<div class="code-block">
  <div class="code-header">
    <span class="code-filename">file.rs</span>
    <span class="code-lang">Rust</span>
  </div>
  <div class="code-content">...</div>
</div>
```

**Git Log**: For timeline/milestones
```html
<div class="git-log">
  <div class="git-commit">
    <div class="git-hash">a1b2c3d</div>
    <div class="git-message">feat: Something happened</div>
    <div class="git-meta">2025-01-01 · Description</div>
  </div>
</div>
```

**Progress Bars**: For rankings/comparisons
```html
<div class="progress-item">
  <div class="progress-header">
    <span class="progress-label">Project Name</span>
    <span class="progress-value">42%</span>
  </div>
  <div class="progress-bar">
    <div class="progress-fill" style="width: 42%;"></div>
  </div>
</div>
```

**Heatmap**: For time distribution
```html
<div class="heatmap-grid">
  <div class="heatmap-cell heat-5"><span class="hour">20</span><span class="count">500</span></div>
</div>
```
Heat levels: `heat-1` (lightest) to `heat-5` (darkest)

**Metric Cards**: For key stats
```html
<div class="metric-card">
  <div class="metric-icon"><svg>...</svg></div>
  <div class="metric-value">1,234</div>
  <div class="metric-label">Label</div>
  <div class="metric-change">Comparison text</div>
</div>
```

**Stats Table**: For detailed breakdowns
```html
<table class="stats-table">
  <thead><tr><th>Column</th></tr></thead>
  <tbody><tr><td>Value</td></tr></tbody>
</table>
```

**Persona Card**: For user profile
```html
<div class="persona-card">
  <div class="persona-avatar"><svg>...</svg></div>
  <h2 class="persona-title">Night Owl Developer</h2>
  <div class="persona-tags">
    <span class="persona-tag">trait_name</span>
  </div>
</div>
```

**Quote Block**: For insights
```html
<div class="quote-block">
  <p class="quote-text">Insightful observation</p>
  <p class="quote-author">— source</p>
</div>
```

## Section Ideas (choose based on data)

Not all sections apply to every user. Select 6-10 that best tell their story:

1. **Hero** (always) - ASCII art, key stats summary
2. **Persona** - Programming personality based on patterns
3. **Time Pattern** - When they code, heatmap visualization
4. **Project Focus** - Where they spent time
5. **Model Strategy** - How they use different models
6. **Token Economics** - Input/output patterns
7. **Productivity** - Tasks, files, plans
8. **Milestones** - Key moments in git-log style
9. **Deep Insights** - Behavioral analysis
10. **Holiday Coding** - If they code on holidays
11. **Streak Analysis** - Consecutive day patterns
12. **Growth Story** - If usage increased over time
13. **Summary** - Wrap-up with key numbers
14. **Footer** - Generated by Claude Code

## Output

Generate complete HTML file and save to `~/Desktop/claude-annual-report-{YEAR}.html`.

The HTML should be:
- Self-contained (inline CSS, no external dependencies except Google Fonts)
- Responsive (works on mobile)
- Animated (fade-in on scroll, progress bar animations)
- Unique to the user's data story

After saving, inform user of the file location.
