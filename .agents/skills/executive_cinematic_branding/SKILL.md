---
name: Executive Cinematic Branding
description: Guidelines and assets for implementing the Navy and Gold professional branding.
---

# Executive Cinematic Branding Skill

This skill provides the design tokens, CSS patterns, and aesthetic rules for the "Executive Cinematic" branding used in the EdwaredCloud systems.

## Core Design Tokens

- **Background:** Deep Navy (`#020c1b`)
- **Primary Surface:** Navy (`#0a192f`) with Glassmorphism (`backdrop-filter: blur(15px)`)
- **Accent:** Gold (`#FFD700`)
- **Secondary Text:** Slate (`#8892b0`)
- **Fonts:** Montserrat (Headings, 600+) and Open Sans (Body)

## Implementation Patterns

### 1. Hero Section

Use giant typography (`4rem`+) with tight letter-spacing and high contrast.

```css
.hero-title {
  font-size: 4.5rem;
  color: #e6f1ff;
  font-weight: 700;
}
```

### 2. Glassmorphism Cards

Cards should have a subtle border, background blur, and a left-aligned layout.

```css
.card {
  background: rgba(17, 34, 64, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(102, 255, 237, 0.1);
  color: #e6f1ff;
}
```

### 3. Hover Effects

Hover states should emphasize the Gold accent and use smooth transitions.

```css
.card:hover {
  border-color: #ffd700;
  transform: translateY(-8px);
}
```

## 5S Methodology Compliance

- **Seiri (Sort):** Keep styles in external `.css` files.
- **Seiton (Set in order):** Use CSS variables for all design tokens.
- **Seiso (Shine):** Ensure high contrast and clear readability.
- **Seiketsu (Standardize):** Follow these rules for all future modules.
- **Shitsuke (Sustain):** Review every new UI component against this branding.
