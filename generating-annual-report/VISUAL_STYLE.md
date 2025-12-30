# Visual Style Guide

Complete styling specifications for the annual report. Reference this file for colors, fonts, and effects.

## Color Palette (GitHub Dark)

```css
:root {
  --bg: #0d1117;
  --bg-secondary: #161b22;
  --bg-tertiary: #21262d;
  --border: #30363d;
  --text: #c9d1d9;
  --text-dim: #8b949e;
  --green: #3fb950;
  --amber: #d29922;
  --red: #f85149;
  --blue: #58a6ff;
  --purple: #a371f7;
}
```

## Typography

- **Font**: JetBrains Mono (Google Fonts)
- **Base size**: 14px
- **Monospace throughout**

```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
```

```css
body {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  color: var(--text);
  background: var(--bg);
}
```

## Layout

- Full-screen scroll-snap sections
- `scroll-snap-type: y mandatory` on html
- Each section is `min-height: 100vh`

```css
html {
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
}

.screen {
  min-height: 100vh;
  scroll-snap-align: start;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

## Code Particle Background Effect

**ALWAYS include** a programmer-style particle background effect.

### HTML

Add a fixed canvas element at the start of `<body>`:
```html
<canvas id="particles"></canvas>
```

### CSS

```css
#particles {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    pointer-events: none;
}
```

### JavaScript Implementation

**Particle Characters**:
- Code symbols: `01<>{}[];:=/\*+-&|!?.#$%^~\`@`
- Code keywords: `fn`, `let`, `if`, `for`, `use`, `()`, `=>`, `{}`, `[]`, `//`, `/*`, `*/`, `0x`, `&&`, `||`

**Animation Behavior**:
- Slow falling motion (speed: 0.3-1.0)
- Slight horizontal drift
- Occasional character changes
- Low opacity (3%-15%) to not distract from content

**Color Distribution**:
- 70% green (`rgba(63, 185, 80, opacity)`)
- 10% purple (`rgba(163, 113, 247, opacity)`)
- 10% blue (`rgba(88, 166, 255, opacity)`)
- 10% amber (`rgba(210, 153, 34, opacity)`)

**Connection Lines**:
- Draw faint lines between nearby particles (distance < 120px)
- Line opacity based on distance: `(1 - dist/maxDist) * 0.04`
- Color: green with very low opacity

**Performance**:
- Particle count based on screen size: `Math.min(width * height / 25000, 80)`
- Use `requestAnimationFrame` for smooth animation
- Handle window resize events

**Example JavaScript Structure**:
```javascript
(function() {
    const canvas = document.getElementById('particles');
    const ctx = canvas.getContext('2d');
    const codeChars = '01<>{}[];:=/\\*+-&|!?.#$%^~`@';
    const keywords = ['fn', 'let', 'if', 'for', '()', '=>', '{}', '[]', '//', '&&'];

    class Particle {
        constructor() { this.reset(); }

        reset() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.speed = 0.3 + Math.random() * 0.7;
            this.opacity = 0.03 + Math.random() * 0.12;
            this.char = this.pickChar();
            this.color = this.pickColor();
        }

        pickChar() {
            return Math.random() < 0.7
                ? codeChars[Math.floor(Math.random() * codeChars.length)]
                : keywords[Math.floor(Math.random() * keywords.length)];
        }

        pickColor() {
            const r = Math.random();
            if (r < 0.7) return `rgba(63, 185, 80, ${this.opacity})`;
            if (r < 0.8) return `rgba(163, 113, 247, ${this.opacity})`;
            if (r < 0.9) return `rgba(88, 166, 255, ${this.opacity})`;
            return `rgba(210, 153, 34, ${this.opacity})`;
        }

        update() {
            this.y += this.speed;
            this.x += Math.sin(this.y * 0.01) * 0.3;
            if (this.y > canvas.height) this.reset();
            if (Math.random() < 0.005) this.char = this.pickChar();
        }

        draw() {
            ctx.fillStyle = this.color;
            ctx.font = '12px JetBrains Mono';
            ctx.fillText(this.char, this.x, this.y);
        }
    }

    let particles = [];

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const count = Math.min(canvas.width * canvas.height / 25000, 80);
        particles = Array.from({length: count}, () => new Particle());
    }

    function drawConnections() {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 120) {
                    ctx.strokeStyle = `rgba(63, 185, 80, ${(1 - dist/120) * 0.04})`;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => { p.update(); p.draw(); });
        drawConnections();
        requestAnimationFrame(animate);
    }

    window.addEventListener('resize', resize);
    resize();
    animate();
})();
```

## Animations

### Fade In on Scroll

```javascript
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
```

```css
.fade-in {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}

.fade-in.visible {
    opacity: 1;
    transform: translateY(0);
}
```

### Progress Bar Animation

```css
.progress-fill {
    width: 0;
    transition: width 1s ease-out;
}

.progress-fill.animate {
    width: var(--target-width);
}
```
