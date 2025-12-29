---
name: annual-report
description: "Generate a personalized Claude Code annual usage report with programmer-style aesthetics (GitHub Dark theme, JetBrains Mono font, terminal/code block visualizations). Use when user asks for: (1) Annual report generation, (2) Usage statistics summary, (3) Claude Code year in review. Trigger keywords: annual report, year review, usage report, 年度报告, 年终总结."
---

# Annual Report Generator

Generate a beautiful, personalized HTML annual report for Claude Code usage. The report should be **dynamically generated** based on user's unique data patterns, not just template filling.

## Data Collection

Read all available data from `~/.claude/`:

### stats-cache.json (Required)
```json
{
  "dailyActivity": [{"date": "2025-01-01", "messageCount": 100, "sessionCount": 3, "toolCallCount": 50}],
  "dailyModelTokens": [{"date": "2025-01-01", "tokensByModel": {"claude-sonnet": 50000}}],
  "modelUsage": {"claude-sonnet": {"inputTokens": 1000, "outputTokens": 500, "cacheReadInputTokens": 10000}},
  "totalSessions": 100,
  "totalMessages": 5000,
  "longestSession": {"messageCount": 300, "timestamp": "2025-12-01"},
  "firstSessionDate": "2025-01-15",
  "hourCounts": {"9": 10, "14": 50, "20": 80}
}
```

### history.jsonl (Required)
Each line: `{"project": "/path/to/project", "timestamp": 1234567890, "display": "user message"}`

Extract: project frequency, time range, conversation patterns.

### todos/*.json (Optional)
Task tracking: `[{"content": "task", "status": "completed|pending|in_progress"}]`

### file-history/ (Optional)
Count directories (sessions with edits) and files (total edits).

### plans/*.md (Optional)
Count plan files for architectural thinking score.

### Code Proxy Database (Optional)
macOS: `~/Library/Application Support/com.example.codeProxy/code_proxy.db`
Query `request_logs` for API metrics.

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
