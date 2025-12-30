# HTML Components

Reusable HTML component template for the annual report. Mix and match based on data availability.

## Terminal Window

For command-line style displays:

```html
<div class="terminal">
  <div class="terminal-header">
    <div class="terminal-dot red"></div>
    <div class="terminal-dot yellow"></div>
    <div class="terminal-dot green"></div>
  </div>
  <div class="terminal-body">
    <pre>$ claude --version
Claude Code v1.0.0
</pre>
  </div>
</div>
```

```css
.terminal {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}

.terminal-header {
  display: flex;
  gap: 8px;
  padding: 12px;
  background: var(--bg-tertiary);
}

.terminal-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.terminal-dot.red { background: #f85149; }
.terminal-dot.yellow { background: #d29922; }
.terminal-dot.green { background: #3fb950; }

.terminal-body {
  padding: 16px;
}
```

## Code Block

For structured data with syntax highlighting:

```html
<div class="code-block">
  <div class="code-header">
    <span class="code-filename">stats.json</span>
    <span class="code-lang">JSON</span>
  </div>
  <div class="code-content">
    <span class="keyword">"sessions"</span>: <span class="number">1234</span>,
    <span class="keyword">"messages"</span>: <span class="number">5678</span>
  </div>
</div>
```

```css
.code-block {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
}

.code-header {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  border-bottom: 1px solid var(--border);
}

.code-filename { color: var(--text); }
.code-lang { color: var(--text-dim); }
.code-content { padding: 16px; }

.keyword { color: var(--blue); }
.string { color: var(--green); }
.number { color: var(--amber); }
.comment { color: var(--text-dim); }
```

## Git Log

For timeline/milestones display:

```html
<div class="git-log">
  <div class="git-commit">
    <div class="git-hash">a1b2c3d</div>
    <div class="git-message">feat: First session started</div>
    <div class="git-meta">2025-01-15 · Beginning of the journey</div>
  </div>
  <div class="git-commit">
    <div class="git-hash">e4f5g6h</div>
    <div class="git-message">milestone: 1000 messages reached</div>
    <div class="git-meta">2025-06-20 · Major milestone</div>
  </div>
</div>
```

```css
.git-log {
  border-left: 2px solid var(--border);
  padding-left: 24px;
}

.git-commit {
  position: relative;
  margin-bottom: 24px;
}

.git-commit::before {
  content: '';
  position: absolute;
  left: -29px;
  top: 4px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--green);
}

.git-hash {
  font-size: 12px;
  color: var(--amber);
}

.git-message {
  color: var(--text);
  margin: 4px 0;
}

.git-meta {
  font-size: 12px;
  color: var(--text-dim);
}
```

## Progress Bars

For rankings/comparisons:

```html
<div class="progress-item">
  <div class="progress-header">
    <span class="progress-label">Claude Sonnet</span>
    <span class="progress-value">65%</span>
  </div>
  <div class="progress-bar">
    <div class="progress-fill" style="width: 65%;"></div>
  </div>
</div>
```

```css
.progress-item {
  margin-bottom: 16px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.progress-label { color: var(--text); }
.progress-value { color: var(--text-dim); }

.progress-bar {
  height: 8px;
  background: var(--bg-tertiary);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--green);
  border-radius: 4px;
}

.progress-fill.amber { background: var(--amber); }
```

## Heatmap

For time distribution:

```html
<div class="heatmap-grid">
  <div class="heatmap-cell heat-1"><span class="hour">00</span><span class="count">12</span></div>
  <div class="heatmap-cell heat-3"><span class="hour">01</span><span class="count">45</span></div>
  <div class="heatmap-cell heat-5"><span class="hour">20</span><span class="count">500</span></div>
</div>
```

Heat levels: `heat-1` (lightest) to `heat-5` (darkest)

```css
.heatmap-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
}

.heatmap-cell {
  padding: 12px;
  border-radius: 4px;
  text-align: center;
}

.heat-1 { background: rgba(63, 185, 80, 0.1); }
.heat-2 { background: rgba(63, 185, 80, 0.25); }
.heat-3 { background: rgba(63, 185, 80, 0.4); }
.heat-4 { background: rgba(63, 185, 80, 0.6); }
.heat-5 { background: rgba(63, 185, 80, 0.8); }

.hour { display: block; font-size: 18px; color: var(--text); }
.count { display: block; font-size: 12px; color: var(--text-dim); }
```

## Metric Cards

For key stats:

```html
<div class="metric-grid">
  <div class="metric-card">
    <div class="metric-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="m4 17 6-6-6-6M12 19h8"/>
      </svg>
    </div>
    <div class="metric-value">1,234</div>
    <div class="metric-label">Sessions</div>
    <div class="metric-change">+15% vs last year</div>
  </div>
</div>
```

```css
.metric-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.metric-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 24px;
  text-align: center;
}

.metric-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
  color: var(--green);
}

.metric-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--text);
}

.metric-label {
  color: var(--text-dim);
  margin-top: 8px;
}

.metric-change {
  font-size: 12px;
  color: var(--green);
  margin-top: 8px;
}
```

## Stats Table

For detailed breakdowns:

```html
<table class="stats-table">
  <thead>
    <tr>
      <th>Model</th>
      <th>Requests</th>
      <th>Tokens</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>claude-sonnet</td>
      <td>1,234</td>
      <td>5.2M</td>
    </tr>
  </tbody>
</table>
```

```css
.stats-table {
  width: 100%;
  border-collapse: collapse;
}

.stats-table th,
.stats-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}

.stats-table th {
  color: var(--text-dim);
  font-weight: 500;
}

.stats-table tr:hover {
  background: var(--bg-tertiary);
}
```

## Persona Card

For user profile:

```html
<div class="persona-card">
  <div class="persona-avatar">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
    </svg>
  </div>
  <h2 class="persona-title">Night Owl Developer</h2>
  <div class="persona-tags">
    <span class="persona-tag">Late Night Coder</span>
    <span class="persona-tag">High Productivity</span>
  </div>
</div>
```

```css
.persona-card {
  text-align: center;
  padding: 48px;
}

.persona-avatar {
  width: 120px;
  height: 120px;
  margin: 0 auto 24px;
  padding: 24px;
  border-radius: 50%;
  background: var(--bg-secondary);
  border: 2px solid var(--green);
  color: var(--green);
}

.persona-title {
  font-size: 28px;
  color: var(--text);
  margin-bottom: 16px;
}

.persona-tags {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.persona-tag {
  padding: 6px 12px;
  background: var(--bg-tertiary);
  border-radius: 16px;
  font-size: 12px;
  color: var(--text-dim);
}
```

## Quote Block

For insights:

```html
<div class="quote-block">
  <p class="quote-text">Your peak productivity hours are between 20:00 and 02:00</p>
  <p class="quote-author">-- Data Analysis</p>
</div>
```

```css
.quote-block {
  padding: 24px;
  border-left: 4px solid var(--green);
  background: var(--bg-secondary);
}

.quote-text {
  font-size: 18px;
  color: var(--text);
  font-style: italic;
}

.quote-author {
  color: var(--text-dim);
  margin-top: 12px;
}
```
