# SVG Icons Library

Use these minimal, stroke-based SVG icons for the annual report. All icons follow the GitHub Dark aesthetic.

**Icon Style Requirements**:
- `viewBox="0 0 24 24"`
- `fill="none"`
- `stroke="currentColor"` (inherits text color)
- `stroke-width="1.5"`

## Available Icons

### Moon (Night Owl)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
</svg>
```

### Sun (Early Bird)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>
</svg>
```

### Clock (Time)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
</svg>
```

### Code (Programming)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/>
</svg>
```

### Check (Success/Complete)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/>
</svg>
```

### Folder (Project)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
</svg>
```

### Zap (Fast/Performance)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>
</svg>
```

### Terminal (Command Line)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="m4 17 6-6-6-6M12 19h8"/>
</svg>
```

### Chart (Statistics)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>
</svg>
```

### Git Branch (Version Control)
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M6 21V9a9 9 0 0 0 9 9"/>
</svg>
```

## Creating Custom Icons

When you need an icon not listed above, create a simple stroke-based SVG that matches this style:

```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
  <path d="..."/>
</svg>
```

**Guidelines**:
- Keep paths simple and minimal
- Use stroke only, no fill
- Maintain consistent stroke-width of 1.5
- Center the icon within the 24x24 viewBox
