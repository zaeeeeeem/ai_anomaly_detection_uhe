# Frontend Design Document - Production Grade UI

## Medical AI Anomaly Detection Platform

**Version**: 2.0 Production
**Last Updated**: 2026-01-27
**Design Philosophy**: Clinical Elegance meets Modern SaaS

---

## 1. DESIGN VISION & PHILOSOPHY

### 1.1 Core Concept: "Clinical Intelligence"

A design system that communicates **trust**, **precision**, and **modern intelligence**. The interface should feel like a high-end medical analytics platform - clean enough for healthcare professionals, yet sophisticated enough to convey AI-powered intelligence.

### 1.2 Design Principles

| Principle | Description |
|-----------|-------------|
| **Clarity** | Information hierarchy must be instantly scannable |
| **Confidence** | Visual cues that inspire trust in the AI system |
| **Precision** | Every pixel, spacing, and color serves a purpose |
| **Calm** | Avoid visual noise; healthcare requires focus |
| **Intelligence** | Subtle sophistication that suggests advanced technology |

### 1.3 Aesthetic Direction

**NOT THIS:**
- Generic SaaS dashboards
- Flat, lifeless interfaces
- Overwhelming data density
- Startup-y playful designs

**THIS:**
- Bloomberg Terminal meets Apple Health
- Stripe Dashboard precision
- Linear.app sophistication
- Medical device interfaces (clean, trustworthy)

---

## 2. COLOR SYSTEM

### 2.1 Primary Palette

```css
:root {
  /* ═══════════════════════════════════════════════
     BRAND COLORS - Medical Intelligence Theme
     ═══════════════════════════════════════════════ */

  /* Primary: Deep Teal - Trust, Medical, Professional */
  --color-primary-50: #f0fdfa;
  --color-primary-100: #ccfbf1;
  --color-primary-200: #99f6e4;
  --color-primary-300: #5eead4;
  --color-primary-400: #2dd4bf;
  --color-primary-500: #14b8a6;  /* Main Brand Color */
  --color-primary-600: #0d9488;
  --color-primary-700: #0f766e;
  --color-primary-800: #115e59;
  --color-primary-900: #134e4a;
  --color-primary-950: #042f2e;

  /* Secondary: Slate - Neutral Intelligence */
  --color-slate-50: #f8fafc;
  --color-slate-100: #f1f5f9;
  --color-slate-200: #e2e8f0;
  --color-slate-300: #cbd5e1;
  --color-slate-400: #94a3b8;
  --color-slate-500: #64748b;
  --color-slate-600: #475569;
  --color-slate-700: #334155;
  --color-slate-800: #1e293b;
  --color-slate-900: #0f172a;
  --color-slate-950: #020617;
}
```

### 2.2 Semantic Colors

```css
:root {
  /* ═══════════════════════════════════════════════
     SEMANTIC COLORS - Status & Feedback
     ═══════════════════════════════════════════════ */

  /* Success - Medical Safe */
  --color-success-light: #dcfce7;
  --color-success-main: #22c55e;
  --color-success-dark: #16a34a;
  --color-success-text: #15803d;

  /* Warning - Attention Required */
  --color-warning-light: #fef3c7;
  --color-warning-main: #f59e0b;
  --color-warning-dark: #d97706;
  --color-warning-text: #b45309;

  /* Error/Danger - Critical Alert */
  --color-danger-light: #fee2e2;
  --color-danger-main: #ef4444;
  --color-danger-dark: #dc2626;
  --color-danger-text: #b91c1c;

  /* Info - Neutral Information */
  --color-info-light: #dbeafe;
  --color-info-main: #3b82f6;
  --color-info-dark: #2563eb;
  --color-info-text: #1d4ed8;

  /* Flagged - AI Detection Alert (Custom) */
  --color-flagged-light: #fef2f2;
  --color-flagged-main: #f87171;
  --color-flagged-dark: #dc2626;
  --color-flagged-glow: rgba(239, 68, 68, 0.2);

  /* Safe - AI Verified Safe (Custom) */
  --color-safe-light: #f0fdf4;
  --color-safe-main: #4ade80;
  --color-safe-dark: #22c55e;
  --color-safe-glow: rgba(34, 197, 94, 0.2);

  /* Borderline - Needs Review (Custom) */
  --color-borderline-light: #fff7ed;
  --color-borderline-main: #fb923c;
  --color-borderline-dark: #ea580c;
  --color-borderline-glow: rgba(251, 146, 60, 0.2);
}
```

### 2.3 Background System

```css
:root {
  /* ═══════════════════════════════════════════════
     BACKGROUNDS - Layered Depth System
     ═══════════════════════════════════════════════ */

  /* Base Backgrounds */
  --bg-base: #fafbfc;           /* App background */
  --bg-surface: #ffffff;         /* Cards, panels */
  --bg-elevated: #ffffff;        /* Modals, dropdowns */
  --bg-sunken: #f1f5f9;         /* Inset areas */
  --bg-overlay: rgba(15, 23, 42, 0.6); /* Modal overlays */

  /* Interactive Backgrounds */
  --bg-hover: rgba(20, 184, 166, 0.04);
  --bg-active: rgba(20, 184, 166, 0.08);
  --bg-selected: rgba(20, 184, 166, 0.12);

  /* Gradient Backgrounds */
  --bg-gradient-hero: linear-gradient(135deg, #f0fdfa 0%, #ffffff 50%, #f8fafc 100%);
  --bg-gradient-card: linear-gradient(180deg, #ffffff 0%, #fafbfc 100%);
  --bg-gradient-sidebar: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);

  /* Subtle Patterns (for visual interest) */
  --bg-pattern-dots: radial-gradient(circle, #e2e8f0 1px, transparent 1px);
  --bg-pattern-grid: linear-gradient(#e2e8f0 1px, transparent 1px),
                     linear-gradient(90deg, #e2e8f0 1px, transparent 1px);
}
```

### 2.4 Dark Mode Palette (Admin Dashboard)

```css
[data-theme="dark"] {
  --bg-base: #0a0f1a;
  --bg-surface: #111827;
  --bg-elevated: #1f2937;
  --bg-sunken: #030712;

  --color-text-primary: #f1f5f9;
  --color-text-secondary: #94a3b8;
  --color-text-muted: #64748b;

  --color-border: #1e293b;
  --color-border-light: #334155;
}
```

---

## 3. TYPOGRAPHY SYSTEM

### 3.1 Font Stack

```css
:root {
  /* ═══════════════════════════════════════════════
     TYPOGRAPHY - Professional Medical Theme
     ═══════════════════════════════════════════════ */

  /* Display Font - Headlines, Hero Text */
  --font-display: 'Cabinet Grotesk', 'SF Pro Display', -apple-system, sans-serif;

  /* Body Font - All readable content */
  --font-body: 'Satoshi', 'Inter', 'SF Pro Text', -apple-system, sans-serif;

  /* Mono Font - Code, Data, IDs */
  --font-mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;

  /* Data Font - Numbers, Scores, Metrics */
  --font-data: 'Tabular Nums', 'JetBrains Mono', monospace;
}
```

### 3.2 Type Scale

```css
:root {
  /* Font Sizes - Modular Scale (1.25 ratio) */
  --text-2xs: 0.625rem;   /* 10px - Micro labels */
  --text-xs: 0.75rem;     /* 12px - Captions */
  --text-sm: 0.875rem;    /* 14px - Small body */
  --text-base: 1rem;      /* 16px - Body */
  --text-lg: 1.125rem;    /* 18px - Large body */
  --text-xl: 1.25rem;     /* 20px - Subheadings */
  --text-2xl: 1.5rem;     /* 24px - Section titles */
  --text-3xl: 1.875rem;   /* 30px - Page titles */
  --text-4xl: 2.25rem;    /* 36px - Hero text */
  --text-5xl: 3rem;       /* 48px - Display */
  --text-6xl: 3.75rem;    /* 60px - Large display */

  /* Line Heights */
  --leading-none: 1;
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;

  /* Letter Spacing */
  --tracking-tighter: -0.05em;
  --tracking-tight: -0.025em;
  --tracking-normal: 0;
  --tracking-wide: 0.025em;
  --tracking-wider: 0.05em;
  --tracking-widest: 0.1em;

  /* Font Weights */
  --font-light: 300;
  --font-regular: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  --font-extrabold: 800;
}
```

### 3.3 Typography Components

```css
/* ═══════════════════════════════════════════════
   TYPOGRAPHY CLASSES
   ═══════════════════════════════════════════════ */

/* Display Headings */
.heading-display {
  font-family: var(--font-display);
  font-size: var(--text-5xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
  color: var(--color-slate-900);
}

/* Page Title */
.heading-page {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
  color: var(--color-slate-900);
}

/* Section Title */
.heading-section {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-snug);
  color: var(--color-slate-800);
}

/* Card Title */
.heading-card {
  font-family: var(--font-body);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  line-height: var(--leading-snug);
  color: var(--color-slate-800);
}

/* Body Text */
.text-body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  font-weight: var(--font-regular);
  line-height: var(--leading-relaxed);
  color: var(--color-slate-600);
}

/* Small Text */
.text-small {
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--font-regular);
  line-height: var(--leading-normal);
  color: var(--color-slate-500);
}

/* Caption */
.text-caption {
  font-family: var(--font-body);
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  line-height: var(--leading-normal);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
  color: var(--color-slate-400);
}

/* Data/Metrics */
.text-data {
  font-family: var(--font-mono);
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-none);
  font-feature-settings: 'tnum';
  color: var(--color-slate-900);
}

/* Score Display */
.text-score {
  font-family: var(--font-mono);
  font-size: var(--text-4xl);
  font-weight: var(--font-extrabold);
  line-height: var(--leading-none);
  font-feature-settings: 'tnum';
}
```

---

## 4. SPACING & LAYOUT SYSTEM

### 4.1 Spacing Scale

```css
:root {
  /* ═══════════════════════════════════════════════
     SPACING - 4px Base Unit System
     ═══════════════════════════════════════════════ */

  --space-0: 0;
  --space-px: 1px;
  --space-0-5: 0.125rem;  /* 2px */
  --space-1: 0.25rem;     /* 4px */
  --space-1-5: 0.375rem;  /* 6px */
  --space-2: 0.5rem;      /* 8px */
  --space-2-5: 0.625rem;  /* 10px */
  --space-3: 0.75rem;     /* 12px */
  --space-3-5: 0.875rem;  /* 14px */
  --space-4: 1rem;        /* 16px */
  --space-5: 1.25rem;     /* 20px */
  --space-6: 1.5rem;      /* 24px */
  --space-7: 1.75rem;     /* 28px */
  --space-8: 2rem;        /* 32px */
  --space-9: 2.25rem;     /* 36px */
  --space-10: 2.5rem;     /* 40px */
  --space-11: 2.75rem;    /* 44px */
  --space-12: 3rem;       /* 48px */
  --space-14: 3.5rem;     /* 56px */
  --space-16: 4rem;       /* 64px */
  --space-20: 5rem;       /* 80px */
  --space-24: 6rem;       /* 96px */
  --space-28: 7rem;       /* 112px */
  --space-32: 8rem;       /* 128px */
}
```

### 4.2 Layout Grid

```css
:root {
  /* Container Widths */
  --container-xs: 20rem;    /* 320px */
  --container-sm: 24rem;    /* 384px */
  --container-md: 28rem;    /* 448px */
  --container-lg: 32rem;    /* 512px */
  --container-xl: 36rem;    /* 576px */
  --container-2xl: 42rem;   /* 672px */
  --container-3xl: 48rem;   /* 768px */
  --container-4xl: 56rem;   /* 896px */
  --container-5xl: 64rem;   /* 1024px */
  --container-6xl: 72rem;   /* 1152px */
  --container-7xl: 80rem;   /* 1280px */
  --container-full: 100%;

  /* Sidebar Widths */
  --sidebar-collapsed: 72px;
  --sidebar-expanded: 280px;
  --sidebar-admin: 260px;

  /* Navbar Heights */
  --navbar-height: 64px;
  --navbar-height-mobile: 56px;
}
```

### 4.3 Main Layout Structure

```css
/* ═══════════════════════════════════════════════
   MAIN LAYOUT - 100vh Fixed, No Scroll
   ═══════════════════════════════════════════════ */

html, body {
  height: 100%;
  overflow: hidden;
  background: var(--bg-base);
}

#root {
  height: 100%;
  overflow: hidden;
}

.app-layout {
  display: grid;
  grid-template-columns: var(--sidebar-expanded) 1fr;
  grid-template-rows: var(--navbar-height) 1fr;
  grid-template-areas:
    "sidebar navbar"
    "sidebar content";
  height: 100vh;
  overflow: hidden;
}

.app-sidebar {
  grid-area: sidebar;
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.app-navbar {
  grid-area: navbar;
  height: var(--navbar-height);
  border-bottom: 1px solid var(--color-border);
}

.app-content {
  grid-area: content;
  height: calc(100vh - var(--navbar-height));
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Scrollable Areas ONLY */
.scroll-area {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: var(--color-slate-300) transparent;
}

.scroll-area::-webkit-scrollbar {
  width: 6px;
}

.scroll-area::-webkit-scrollbar-track {
  background: transparent;
}

.scroll-area::-webkit-scrollbar-thumb {
  background: var(--color-slate-300);
  border-radius: 3px;
}

.scroll-area::-webkit-scrollbar-thumb:hover {
  background: var(--color-slate-400);
}
```

---

## 5. COMPONENT DESIGN SPECIFICATIONS

### 5.1 Buttons

```css
/* ═══════════════════════════════════════════════
   BUTTON SYSTEM
   ═══════════════════════════════════════════════ */

.btn {
  /* Base */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);

  /* Typography */
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  line-height: 1;
  white-space: nowrap;

  /* Sizing */
  padding: var(--space-2-5) var(--space-4);
  min-height: 40px;

  /* Shape */
  border-radius: var(--radius-lg);
  border: none;

  /* Interaction */
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);

  /* Focus */
  outline: none;
}

.btn:focus-visible {
  box-shadow: 0 0 0 2px var(--bg-base), 0 0 0 4px var(--color-primary-500);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* Primary Button */
.btn-primary {
  background: linear-gradient(135deg, var(--color-primary-500) 0%, var(--color-primary-600) 100%);
  color: white;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05),
              0 4px 12px rgba(20, 184, 166, 0.25);
}

.btn-primary:hover {
  background: linear-gradient(135deg, var(--color-primary-600) 0%, var(--color-primary-700) 100%);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1),
              0 8px 24px rgba(20, 184, 166, 0.35);
  transform: translateY(-1px);
}

.btn-primary:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1),
              0 2px 8px rgba(20, 184, 166, 0.2);
}

/* Secondary Button */
.btn-secondary {
  background: var(--bg-surface);
  color: var(--color-slate-700);
  border: 1px solid var(--color-slate-200);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.btn-secondary:hover {
  background: var(--color-slate-50);
  border-color: var(--color-slate-300);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}

/* Ghost Button */
.btn-ghost {
  background: transparent;
  color: var(--color-slate-600);
}

.btn-ghost:hover {
  background: var(--bg-hover);
  color: var(--color-slate-900);
}

/* Danger Button */
.btn-danger {
  background: linear-gradient(135deg, var(--color-danger-main) 0%, var(--color-danger-dark) 100%);
  color: white;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05),
              0 4px 12px rgba(239, 68, 68, 0.25);
}

.btn-danger:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1),
              0 8px 24px rgba(239, 68, 68, 0.35);
  transform: translateY(-1px);
}

/* Button Sizes */
.btn-sm {
  padding: var(--space-1-5) var(--space-3);
  min-height: 32px;
  font-size: var(--text-xs);
}

.btn-lg {
  padding: var(--space-3) var(--space-6);
  min-height: 48px;
  font-size: var(--text-base);
}

.btn-xl {
  padding: var(--space-4) var(--space-8);
  min-height: 56px;
  font-size: var(--text-lg);
}

/* Icon Button */
.btn-icon {
  padding: var(--space-2);
  min-height: 40px;
  min-width: 40px;
}

.btn-icon.btn-sm {
  padding: var(--space-1-5);
  min-height: 32px;
  min-width: 32px;
}
```

### 5.2 Input Fields

```css
/* ═══════════════════════════════════════════════
   INPUT SYSTEM
   ═══════════════════════════════════════════════ */

.input-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.input-label {
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-slate-700);
}

.input-label.required::after {
  content: '*';
  color: var(--color-danger-main);
  margin-left: var(--space-1);
}

.input {
  /* Base */
  width: 100%;
  padding: var(--space-3) var(--space-4);

  /* Typography */
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-slate-900);

  /* Shape */
  background: var(--bg-surface);
  border: 1px solid var(--color-slate-200);
  border-radius: var(--radius-lg);

  /* Transition */
  transition: all 0.2s ease;
}

.input::placeholder {
  color: var(--color-slate-400);
}

.input:hover {
  border-color: var(--color-slate-300);
}

.input:focus {
  outline: none;
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.1);
}

.input:disabled {
  background: var(--color-slate-50);
  color: var(--color-slate-400);
  cursor: not-allowed;
}

/* Input States */
.input.error {
  border-color: var(--color-danger-main);
}

.input.error:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.input.success {
  border-color: var(--color-success-main);
}

.input-error-message {
  font-size: var(--text-sm);
  color: var(--color-danger-text);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

/* Input with Icon */
.input-with-icon {
  position: relative;
}

.input-with-icon .input {
  padding-left: var(--space-10);
}

.input-with-icon .input-icon {
  position: absolute;
  left: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-slate-400);
  pointer-events: none;
}

.input-with-icon .input:focus + .input-icon {
  color: var(--color-primary-500);
}

/* Textarea */
.textarea {
  min-height: 120px;
  resize: vertical;
  line-height: var(--leading-relaxed);
}
```

### 5.3 Cards

```css
/* ═══════════════════════════════════════════════
   CARD SYSTEM
   ═══════════════════════════════════════════════ */

.card {
  background: var(--bg-surface);
  border: 1px solid var(--color-slate-200);
  border-radius: var(--radius-xl);
  overflow: hidden;
  transition: all 0.2s ease;
}

.card-elevated {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04),
              0 4px 12px rgba(0, 0, 0, 0.04);
}

.card-interactive {
  cursor: pointer;
}

.card-interactive:hover {
  border-color: var(--color-primary-200);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06),
              0 12px 32px rgba(20, 184, 166, 0.08);
  transform: translateY(-2px);
}

.card-header {
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--color-slate-100);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
}

.card-body {
  padding: var(--space-6);
}

.card-footer {
  padding: var(--space-4) var(--space-6);
  background: var(--color-slate-50);
  border-top: 1px solid var(--color-slate-100);
}

/* Card Variants */
.card-flagged {
  border-color: var(--color-flagged-main);
  background: linear-gradient(135deg, var(--bg-surface) 0%, var(--color-flagged-light) 100%);
}

.card-flagged::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: var(--color-flagged-main);
}

.card-safe {
  border-color: var(--color-safe-main);
  background: linear-gradient(135deg, var(--bg-surface) 0%, var(--color-safe-light) 100%);
}

.card-safe::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: var(--color-safe-main);
}
```

### 5.4 Badges & Status Indicators

```css
/* ═══════════════════════════════════════════════
   BADGE SYSTEM
   ═══════════════════════════════════════════════ */

.badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-1) var(--space-2-5);
  font-family: var(--font-body);
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  line-height: 1;
  border-radius: var(--radius-full);
  white-space: nowrap;
}

/* Status Badges */
.badge-flagged {
  background: var(--color-flagged-light);
  color: var(--color-danger-text);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.badge-safe {
  background: var(--color-safe-light);
  color: var(--color-success-text);
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.badge-borderline {
  background: var(--color-borderline-light);
  color: var(--color-warning-text);
  border: 1px solid rgba(251, 146, 60, 0.2);
}

.badge-pending {
  background: var(--color-slate-100);
  color: var(--color-slate-600);
  border: 1px solid var(--color-slate-200);
}

.badge-info {
  background: var(--color-info-light);
  color: var(--color-info-text);
  border: 1px solid rgba(59, 130, 246, 0.2);
}

/* Pulsing Badge (for alerts) */
.badge-pulse {
  position: relative;
}

.badge-pulse::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  background: inherit;
  opacity: 0;
  animation: badge-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes badge-pulse {
  0%, 100% { opacity: 0; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.1); }
}

/* Status Dot */
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-dot-flagged {
  background: var(--color-flagged-main);
  box-shadow: 0 0 0 3px var(--color-flagged-glow);
}

.status-dot-safe {
  background: var(--color-safe-main);
  box-shadow: 0 0 0 3px var(--color-safe-glow);
}

.status-dot-borderline {
  background: var(--color-borderline-main);
  box-shadow: 0 0 0 3px var(--color-borderline-glow);
}

/* Live Indicator */
.status-live {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.status-live .status-dot {
  animation: live-pulse 1.5s ease-in-out infinite;
}

@keyframes live-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
```

### 5.5 Score Visualization

```css
/* ═══════════════════════════════════════════════
   SCORE & METRICS VISUALIZATION
   ═══════════════════════════════════════════════ */

/* Score Card */
.score-card {
  background: var(--bg-surface);
  border: 1px solid var(--color-slate-200);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.score-label {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-slate-500);
}

.score-value {
  font-family: var(--font-mono);
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  line-height: 1;
  font-feature-settings: 'tnum';
}

.score-value-low { color: var(--color-safe-dark); }
.score-value-medium { color: var(--color-warning-dark); }
.score-value-high { color: var(--color-danger-dark); }

/* Progress Bar */
.progress-bar {
  height: 8px;
  background: var(--color-slate-100);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.progress-bar-fill-low {
  background: linear-gradient(90deg, var(--color-safe-main) 0%, var(--color-safe-dark) 100%);
}

.progress-bar-fill-medium {
  background: linear-gradient(90deg, var(--color-warning-main) 0%, var(--color-warning-dark) 100%);
}

.progress-bar-fill-high {
  background: linear-gradient(90deg, var(--color-danger-main) 0%, var(--color-danger-dark) 100%);
}

/* Animated Progress */
.progress-bar-animated .progress-bar-fill {
  background-size: 200% 100%;
  animation: progress-shimmer 2s linear infinite;
}

@keyframes progress-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Circular Score */
.score-circle {
  position: relative;
  width: 120px;
  height: 120px;
}

.score-circle svg {
  transform: rotate(-90deg);
}

.score-circle-bg {
  fill: none;
  stroke: var(--color-slate-100);
  stroke-width: 8;
}

.score-circle-fill {
  fill: none;
  stroke-width: 8;
  stroke-linecap: round;
  transition: stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.score-circle-value {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-family: var(--font-mono);
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
}

/* Metric Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--space-4);
}

/* Risk Breakdown */
.risk-breakdown {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.risk-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.risk-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.risk-item-label {
  font-size: var(--text-sm);
  color: var(--color-slate-600);
}

.risk-item-value {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
}
```

---

## 6. PAGE-SPECIFIC DESIGNS

### 6.1 Login/Signup Pages

```css
/* ═══════════════════════════════════════════════
   AUTHENTICATION PAGES
   ═══════════════════════════════════════════════ */

.auth-page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
  background: var(--bg-base);
}

/* Left Side - Branding */
.auth-branding {
  background: linear-gradient(135deg, var(--color-primary-900) 0%, var(--color-slate-900) 100%);
  padding: var(--space-16);
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.auth-branding::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.5;
}

.auth-branding-content {
  position: relative;
  z-index: 1;
}

.auth-logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-12);
}

.auth-logo-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--color-primary-400) 0%, var(--color-primary-500) 100%);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-logo-text {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: white;
}

.auth-headline {
  font-family: var(--font-display);
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  color: white;
  line-height: var(--leading-tight);
  margin-bottom: var(--space-6);
}

.auth-tagline {
  font-size: var(--text-lg);
  color: var(--color-slate-300);
  line-height: var(--leading-relaxed);
  max-width: 400px;
}

.auth-features {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  margin-top: var(--space-12);
}

.auth-feature {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  color: var(--color-slate-300);
  font-size: var(--text-sm);
}

.auth-feature-icon {
  width: 24px;
  height: 24px;
  background: rgba(20, 184, 166, 0.2);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary-400);
}

/* Right Side - Form */
.auth-form-container {
  padding: var(--space-16);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.auth-form-wrapper {
  width: 100%;
  max-width: 400px;
}

.auth-form-header {
  margin-bottom: var(--space-8);
}

.auth-form-title {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: var(--color-slate-900);
  margin-bottom: var(--space-2);
}

.auth-form-subtitle {
  font-size: var(--text-base);
  color: var(--color-slate-500);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.auth-form-divider {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  margin: var(--space-6) 0;
}

.auth-form-divider::before,
.auth-form-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--color-slate-200);
}

.auth-form-divider-text {
  font-size: var(--text-sm);
  color: var(--color-slate-400);
}

.auth-form-footer {
  text-align: center;
  margin-top: var(--space-8);
}

.auth-form-footer-text {
  font-size: var(--text-sm);
  color: var(--color-slate-500);
}

.auth-form-footer-link {
  color: var(--color-primary-600);
  font-weight: var(--font-medium);
  text-decoration: none;
}

.auth-form-footer-link:hover {
  text-decoration: underline;
}

/* Mobile Responsive */
@media (max-width: 960px) {
  .auth-page {
    grid-template-columns: 1fr;
  }

  .auth-branding {
    display: none;
  }
}
```

### 6.2 Chat Interface

```css
/* ═══════════════════════════════════════════════
   CHAT INTERFACE
   ═══════════════════════════════════════════════ */

.chat-layout {
  display: grid;
  grid-template-columns: var(--sidebar-expanded) 1fr;
  height: 100vh;
  overflow: hidden;
}

/* Conversations Sidebar */
.chat-sidebar {
  background: var(--bg-surface);
  border-right: 1px solid var(--color-slate-200);
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.chat-sidebar-header {
  padding: var(--space-5) var(--space-4);
  border-bottom: 1px solid var(--color-slate-100);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chat-sidebar-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--color-slate-900);
}

.chat-sidebar-list {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-3);
}

/* Conversation Item */
.conversation-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.15s ease;
  margin-bottom: var(--space-1);
}

.conversation-item:hover {
  background: var(--bg-hover);
}

.conversation-item.active {
  background: var(--bg-selected);
}

.conversation-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 24px;
  background: var(--color-primary-500);
  border-radius: 0 2px 2px 0;
}

.conversation-icon {
  width: 36px;
  height: 36px;
  background: var(--color-primary-100);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary-600);
  flex-shrink: 0;
}

.conversation-content {
  flex: 1;
  min-width: 0;
}

.conversation-title {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-slate-900);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.conversation-preview {
  font-size: var(--text-xs);
  color: var(--color-slate-500);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Chat Main Area */
.chat-main {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  background: var(--bg-base);
}

/* Chat Header */
.chat-header {
  padding: var(--space-4) var(--space-6);
  background: var(--bg-surface);
  border-bottom: 1px solid var(--color-slate-200);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chat-header-info {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.chat-header-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--color-slate-900);
}

.chat-header-model {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-1) var(--space-2-5);
  background: var(--color-slate-100);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  color: var(--color-slate-600);
}

/* Messages Area */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* Message Bubble */
.message {
  display: flex;
  gap: var(--space-3);
  max-width: 720px;
  animation: message-appear 0.3s ease;
}

@keyframes message-appear {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-user {
  margin-left: auto;
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message-avatar-user {
  background: linear-gradient(135deg, var(--color-primary-500) 0%, var(--color-primary-600) 100%);
  color: white;
}

.message-avatar-ai {
  background: var(--color-slate-100);
  color: var(--color-slate-600);
}

.message-content {
  flex: 1;
}

.message-bubble {
  padding: var(--space-4) var(--space-5);
  border-radius: var(--radius-xl);
  line-height: var(--leading-relaxed);
}

.message-bubble-user {
  background: linear-gradient(135deg, var(--color-primary-500) 0%, var(--color-primary-600) 100%);
  color: white;
  border-bottom-right-radius: var(--radius-sm);
}

.message-bubble-ai {
  background: var(--bg-surface);
  color: var(--color-slate-700);
  border: 1px solid var(--color-slate-200);
  border-bottom-left-radius: var(--radius-sm);
}

.message-time {
  font-size: var(--text-xs);
  color: var(--color-slate-400);
  margin-top: var(--space-2);
  padding: 0 var(--space-1);
}

.message-user .message-time {
  text-align: right;
}

/* Typing Indicator */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-4) var(--space-5);
}

.typing-dot {
  width: 8px;
  height: 8px;
  background: var(--color-slate-400);
  border-radius: 50%;
  animation: typing-bounce 1.4s infinite ease-in-out both;
}

.typing-dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dot:nth-child(2) { animation-delay: -0.16s; }
.typing-dot:nth-child(3) { animation-delay: 0s; }

@keyframes typing-bounce {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.4;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Chat Input */
.chat-input-container {
  padding: var(--space-4) var(--space-6) var(--space-6);
  background: var(--bg-surface);
  border-top: 1px solid var(--color-slate-200);
}

.chat-input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: var(--space-3);
  background: var(--bg-base);
  border: 1px solid var(--color-slate-200);
  border-radius: var(--radius-xl);
  padding: var(--space-3);
  transition: all 0.2s ease;
}

.chat-input-wrapper:focus-within {
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.1);
}

.chat-input {
  flex: 1;
  border: none;
  background: transparent;
  resize: none;
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-slate-900);
  line-height: var(--leading-relaxed);
  max-height: 150px;
  padding: var(--space-1) var(--space-2);
}

.chat-input::placeholder {
  color: var(--color-slate-400);
}

.chat-input:focus {
  outline: none;
}

.chat-send-btn {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--color-primary-500) 0%, var(--color-primary-600) 100%);
  border: none;
  border-radius: var(--radius-lg);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.chat-send-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(20, 184, 166, 0.35);
}

.chat-send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* Medical Disclaimer */
.chat-disclaimer {
  text-align: center;
  padding: var(--space-3);
  font-size: var(--text-xs);
  color: var(--color-slate-400);
}
```

### 6.3 Admin Dashboard

```css
/* ═══════════════════════════════════════════════
   ADMIN DASHBOARD
   ═══════════════════════════════════════════════ */

.admin-layout {
  display: grid;
  grid-template-columns: var(--sidebar-admin) 1fr;
  height: 100vh;
  overflow: hidden;
  background: var(--bg-base);
}

/* Admin Sidebar */
.admin-sidebar {
  background: linear-gradient(180deg, var(--color-slate-900) 0%, var(--color-slate-800) 100%);
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.admin-sidebar-header {
  padding: var(--space-6);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-sidebar-logo {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.admin-sidebar-logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--color-primary-400) 0%, var(--color-primary-500) 100%);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.admin-sidebar-logo-text {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
  color: white;
}

.admin-sidebar-subtitle {
  font-size: var(--text-xs);
  color: var(--color-slate-400);
  margin-top: var(--space-1);
}

.admin-sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-4);
}

.admin-nav-section {
  margin-bottom: var(--space-6);
}

.admin-nav-section-title {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-slate-500);
  padding: var(--space-2) var(--space-3);
  margin-bottom: var(--space-2);
}

.admin-nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg);
  color: var(--color-slate-400);
  text-decoration: none;
  transition: all 0.15s ease;
  margin-bottom: var(--space-1);
  position: relative;
}

.admin-nav-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

.admin-nav-item.active {
  background: rgba(20, 184, 166, 0.15);
  color: var(--color-primary-400);
}

.admin-nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 24px;
  background: var(--color-primary-500);
  border-radius: 0 2px 2px 0;
}

.admin-nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.admin-nav-label {
  flex: 1;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
}

.admin-nav-badge {
  background: var(--color-danger-main);
  color: white;
  font-size: var(--text-2xs);
  font-weight: var(--font-bold);
  padding: var(--space-0-5) var(--space-2);
  border-radius: var(--radius-full);
  min-width: 20px;
  text-align: center;
  animation: badge-glow 2s ease-in-out infinite;
}

@keyframes badge-glow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
  50% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
}

.admin-sidebar-footer {
  padding: var(--space-4);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-user-info {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.05);
}

.admin-user-avatar {
  width: 36px;
  height: 36px;
  background: var(--color-primary-600);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: var(--font-semibold);
  font-size: var(--text-sm);
}

.admin-user-name {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: white;
}

.admin-user-role {
  font-size: var(--text-xs);
  color: var(--color-slate-400);
}

/* Admin Content Area */
.admin-content {
  height: 100vh;
  overflow-y: auto;
  padding: var(--space-8);
}

.admin-page-header {
  margin-bottom: var(--space-8);
}

.admin-page-title {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--color-slate-900);
  margin-bottom: var(--space-2);
}

.admin-page-description {
  font-size: var(--text-base);
  color: var(--color-slate-500);
}

/* Stats Cards */
.admin-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-5);
  margin-bottom: var(--space-8);
}

.admin-stat-card {
  background: var(--bg-surface);
  border: 1px solid var(--color-slate-200);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  position: relative;
  overflow: hidden;
}

.admin-stat-card::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, var(--color-primary-100) 0%, transparent 70%);
  opacity: 0.5;
  pointer-events: none;
}

.admin-stat-label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-slate-500);
  margin-bottom: var(--space-2);
}

.admin-stat-value {
  font-family: var(--font-mono);
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--color-slate-900);
  font-feature-settings: 'tnum';
}

.admin-stat-change {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  margin-top: var(--space-2);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
}

.admin-stat-change-up {
  color: var(--color-success-dark);
}

.admin-stat-change-down {
  color: var(--color-danger-dark);
}
```

---

## 7. ANIMATION SYSTEM

### 7.1 Keyframe Animations

```css
/* ═══════════════════════════════════════════════
   ANIMATION LIBRARY
   ═══════════════════════════════════════════════ */

/* Fade In */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Fade In Up */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Fade In Down */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Scale In */
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Slide In Right */
@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Slide In Left */
@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Pulse */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Spin */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Bounce */
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    transform: translateY(-25%);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}

/* Shake */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-4px); }
  20%, 40%, 60%, 80% { transform: translateX(4px); }
}

/* Shimmer (for loading states) */
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* Glow Pulse (for important elements) */
@keyframes glowPulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(20, 184, 166, 0.4);
  }
  50% {
    box-shadow: 0 0 0 12px rgba(20, 184, 166, 0);
  }
}
```

### 7.2 Animation Utilities

```css
/* ═══════════════════════════════════════════════
   ANIMATION UTILITIES
   ═══════════════════════════════════════════════ */

/* Animation Classes */
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

.animate-fade-in-up {
  animation: fadeInUp 0.4s ease-out;
}

.animate-fade-in-down {
  animation: fadeInDown 0.4s ease-out;
}

.animate-scale-in {
  animation: scaleIn 0.3s ease-out;
}

.animate-slide-in-right {
  animation: slideInRight 0.4s ease-out;
}

.animate-slide-in-left {
  animation: slideInLeft 0.4s ease-out;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

.animate-bounce {
  animation: bounce 1s infinite;
}

.animate-shake {
  animation: shake 0.5s ease-in-out;
}

/* Staggered Animation for Lists */
.stagger-children > * {
  opacity: 0;
  animation: fadeInUp 0.4s ease-out forwards;
}

.stagger-children > *:nth-child(1) { animation-delay: 0.05s; }
.stagger-children > *:nth-child(2) { animation-delay: 0.1s; }
.stagger-children > *:nth-child(3) { animation-delay: 0.15s; }
.stagger-children > *:nth-child(4) { animation-delay: 0.2s; }
.stagger-children > *:nth-child(5) { animation-delay: 0.25s; }
.stagger-children > *:nth-child(6) { animation-delay: 0.3s; }
.stagger-children > *:nth-child(7) { animation-delay: 0.35s; }
.stagger-children > *:nth-child(8) { animation-delay: 0.4s; }
.stagger-children > *:nth-child(9) { animation-delay: 0.45s; }
.stagger-children > *:nth-child(10) { animation-delay: 0.5s; }

/* Hover Transitions */
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.hover-scale {
  transition: transform 0.2s ease;
}

.hover-scale:hover {
  transform: scale(1.02);
}

/* Loading Skeleton */
.skeleton {
  background: linear-gradient(90deg,
    var(--color-slate-200) 25%,
    var(--color-slate-100) 50%,
    var(--color-slate-200) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-md);
}

.skeleton-text {
  height: 1em;
  margin-bottom: var(--space-2);
}

.skeleton-heading {
  height: 1.5em;
  width: 60%;
  margin-bottom: var(--space-4);
}

.skeleton-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-lg);
}
```

---

## 8. RESPONSIVE DESIGN

### 8.1 Breakpoints

```css
/* ═══════════════════════════════════════════════
   RESPONSIVE BREAKPOINTS
   ═══════════════════════════════════════════════ */

:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}

/* Mobile First Media Queries */
/* Small (sm) */
@media (min-width: 640px) { }

/* Medium (md) */
@media (min-width: 768px) { }

/* Large (lg) */
@media (min-width: 1024px) { }

/* Extra Large (xl) */
@media (min-width: 1280px) { }

/* 2X Large (2xl) */
@media (min-width: 1536px) { }
```

### 8.2 Responsive Layout Adjustments

```css
/* ═══════════════════════════════════════════════
   RESPONSIVE LAYOUTS
   ═══════════════════════════════════════════════ */

/* Mobile Layout */
@media (max-width: 1023px) {
  /* App Layout */
  .app-layout {
    grid-template-columns: 1fr;
    grid-template-rows: var(--navbar-height-mobile) 1fr;
    grid-template-areas:
      "navbar"
      "content";
  }

  .app-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 280px;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    z-index: 100;
  }

  .app-sidebar.open {
    transform: translateX(0);
  }

  /* Chat Layout */
  .chat-layout {
    grid-template-columns: 1fr;
  }

  .chat-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    z-index: 100;
  }

  .chat-sidebar.open {
    transform: translateX(0);
  }

  /* Admin Layout */
  .admin-layout {
    grid-template-columns: 1fr;
  }

  .admin-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 280px;
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    z-index: 100;
  }

  .admin-sidebar.open {
    transform: translateX(0);
  }

  .admin-content {
    padding: var(--space-5);
  }

  .admin-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  /* Auth Layout */
  .auth-page {
    grid-template-columns: 1fr;
  }

  .auth-branding {
    display: none;
  }

  .auth-form-container {
    padding: var(--space-6);
  }
}

/* Small Mobile */
@media (max-width: 479px) {
  .admin-stats-grid {
    grid-template-columns: 1fr;
  }

  .admin-page-title {
    font-size: var(--text-2xl);
  }

  .message {
    max-width: 100%;
  }
}
```

---

## 9. INTERACTION DETAIL PAGE

### 9.1 Five-Level Display Design

```css
/* ═══════════════════════════════════════════════
   INTERACTION DETAIL - 5 LEVEL VIEW
   ═══════════════════════════════════════════════ */

.interaction-detail {
  max-width: 1200px;
  margin: 0 auto;
}

.interaction-detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-8);
}

.interaction-id {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  color: var(--color-slate-500);
  background: var(--color-slate-100);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
}

/* Level Section */
.level-section {
  background: var(--bg-surface);
  border: 1px solid var(--color-slate-200);
  border-radius: var(--radius-xl);
  margin-bottom: var(--space-6);
  overflow: hidden;
  animation: fadeInUp 0.4s ease-out;
}

.level-section:nth-child(2) { animation-delay: 0.1s; }
.level-section:nth-child(3) { animation-delay: 0.2s; }
.level-section:nth-child(4) { animation-delay: 0.3s; }
.level-section:nth-child(5) { animation-delay: 0.4s; }
.level-section:nth-child(6) { animation-delay: 0.5s; }

.level-header {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-5) var(--space-6);
  background: var(--color-slate-50);
  border-bottom: 1px solid var(--color-slate-200);
}

.level-number {
  width: 32px;
  height: 32px;
  background: var(--color-primary-500);
  color: white;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: var(--font-bold);
}

.level-title {
  flex: 1;
}

.level-title h3 {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--color-slate-900);
}

.level-title p {
  font-size: var(--text-sm);
  color: var(--color-slate-500);
}

.level-content {
  padding: var(--space-6);
}

/* Level 1: Interaction Log */
.interaction-log-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.interaction-meta-item {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.interaction-meta-label {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-slate-500);
}

.interaction-meta-value {
  font-size: var(--text-sm);
  color: var(--color-slate-900);
  font-weight: var(--font-medium);
}

.interaction-meta-value.mono {
  font-family: var(--font-mono);
}

.interaction-content-box {
  background: var(--color-slate-50);
  border: 1px solid var(--color-slate-200);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  margin-top: var(--space-4);
}

.interaction-content-label {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-slate-500);
  margin-bottom: var(--space-3);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.interaction-content-text {
  font-size: var(--text-base);
  line-height: var(--leading-relaxed);
  color: var(--color-slate-700);
  white-space: pre-wrap;
}

/* Level 2: Record Analysis */
.topics-grid {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-bottom: var(--space-6);
}

.topic-tag {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-1-5) var(--space-3);
  background: var(--color-primary-50);
  color: var(--color-primary-700);
  border: 1px solid var(--color-primary-200);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
}

.flags-section {
  margin-top: var(--space-6);
}

.flags-section-title {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-slate-700);
  margin-bottom: var(--space-4);
}

.flags-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: var(--space-3);
}

.flag-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--bg-surface);
  border: 1px solid var(--color-slate-200);
  border-radius: var(--radius-lg);
  transition: all 0.15s ease;
}

.flag-item.flagged {
  background: var(--color-flagged-light);
  border-color: var(--color-flagged-main);
}

.flag-icon {
  width: 24px;
  height: 24px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.flag-icon-false {
  background: var(--color-slate-100);
  color: var(--color-slate-400);
}

.flag-icon-true {
  background: var(--color-flagged-main);
  color: white;
}

.flag-label {
  font-size: var(--text-sm);
  color: var(--color-slate-700);
}

.flag-item.flagged .flag-label {
  color: var(--color-danger-text);
  font-weight: var(--font-medium);
}

/* Level 3: Scoring */
.scores-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-5);
  margin-bottom: var(--space-6);
}

.score-card {
  background: var(--bg-surface);
  border: 1px solid var(--color-slate-200);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  text-align: center;
}

.score-card-value {
  font-family: var(--font-mono);
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  line-height: 1;
  margin-bottom: var(--space-3);
}

.score-card-value.low { color: var(--color-safe-dark); }
.score-card-value.medium { color: var(--color-warning-dark); }
.score-card-value.high { color: var(--color-danger-dark); }

.score-card-bar {
  height: 6px;
  background: var(--color-slate-100);
  border-radius: var(--radius-full);
  overflow: hidden;
  margin-bottom: var(--space-3);
}

.score-card-bar-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.score-card-label {
  font-size: var(--text-sm);
  color: var(--color-slate-600);
}

/* Overall Score Highlight */
.overall-score {
  background: linear-gradient(135deg, var(--color-slate-50) 0%, var(--bg-surface) 100%);
  border: 2px solid var(--color-slate-300);
  padding: var(--space-8);
  text-align: center;
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
}

.overall-score.flagged {
  background: linear-gradient(135deg, var(--color-flagged-light) 0%, var(--bg-surface) 100%);
  border-color: var(--color-flagged-main);
}

.overall-score-label {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-slate-500);
  margin-bottom: var(--space-4);
}

.overall-score-value {
  font-family: var(--font-mono);
  font-size: var(--text-6xl);
  font-weight: var(--font-extrabold);
  line-height: 1;
}

.overall-score-status {
  margin-top: var(--space-4);
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
}

.overall-score-status.flagged {
  background: var(--color-flagged-main);
  color: white;
}

.overall-score-status.safe {
  background: var(--color-safe-main);
  color: white;
}

/* Level 4: Explanation */
.explanation-content {
  background: var(--color-slate-50);
  border: 1px solid var(--color-slate-200);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  margin-bottom: var(--space-6);
}

.explanation-text {
  font-size: var(--text-base);
  line-height: var(--leading-relaxed);
  color: var(--color-slate-700);
}

.citations-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.citation-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-4);
  background: var(--bg-surface);
  border: 1px solid var(--color-slate-200);
  border-radius: var(--radius-lg);
}

.citation-icon {
  width: 36px;
  height: 36px;
  background: var(--color-info-light);
  color: var(--color-info-dark);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.citation-content {
  flex: 1;
}

.citation-title {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-slate-900);
  margin-bottom: var(--space-1);
}

.citation-meta {
  font-size: var(--text-xs);
  color: var(--color-slate-500);
}

.citation-score {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-info-dark);
  background: var(--color-info-light);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-md);
}

/* Level 5: Human Review */
.review-status {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-5);
  background: var(--color-slate-50);
  border: 1px solid var(--color-slate-200);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-6);
}

.review-label-badge {
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-lg);
  font-size: var(--text-lg);
  font-weight: var(--font-bold);
}

.review-label-badge.safe {
  background: var(--color-safe-light);
  color: var(--color-success-text);
  border: 1px solid var(--color-safe-main);
}

.review-label-badge.unsafe {
  background: var(--color-flagged-light);
  color: var(--color-danger-text);
  border: 1px solid var(--color-flagged-main);
}

.review-label-badge.borderline {
  background: var(--color-borderline-light);
  color: var(--color-warning-text);
  border: 1px solid var(--color-borderline-main);
}

.review-meta {
  flex: 1;
}

.review-reviewer {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-slate-900);
}

.review-timestamp {
  font-size: var(--text-sm);
  color: var(--color-slate-500);
}

.review-content-section {
  margin-top: var(--space-6);
}

.review-content-section h4 {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-slate-700);
  margin-bottom: var(--space-3);
}

.review-corrected-response {
  background: var(--color-safe-light);
  border: 1px solid var(--color-safe-main);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
}

.review-comments {
  background: var(--color-slate-50);
  border: 1px solid var(--color-slate-200);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
}

/* Pending Review State */
.pending-review {
  text-align: center;
  padding: var(--space-10);
}

.pending-review-icon {
  width: 64px;
  height: 64px;
  background: var(--color-warning-light);
  color: var(--color-warning-dark);
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--space-4);
}

.pending-review-text {
  font-size: var(--text-lg);
  font-weight: var(--font-medium);
  color: var(--color-slate-700);
  margin-bottom: var(--space-4);
}
```

---

## 10. IMPLEMENTATION CHECKLIST

### 10.1 CSS File Structure

```
frontend/src/styles/
├── variables.css          # All CSS custom properties
├── reset.css              # CSS reset/normalize
├── typography.css         # Typography system
├── animations.css         # Keyframe animations
├── utilities.css          # Utility classes
└── global.css             # Global styles (imports all above)

frontend/src/components/
└── [component]/
    ├── [Component].jsx
    └── [Component].css    # Component-scoped styles
```

### 10.2 Implementation Order

1. **Phase 1: Design Tokens**
   - [ ] Create variables.css with all color, spacing, typography tokens
   - [ ] Create reset.css
   - [ ] Set up font loading

2. **Phase 2: Base Components**
   - [ ] Button component with all variants
   - [ ] Input component with states
   - [ ] Card component
   - [ ] Badge component

3. **Phase 3: Layout Components**
   - [ ] App Layout shell
   - [ ] Sidebar (collapsible)
   - [ ] Navbar

4. **Phase 4: Auth Pages**
   - [ ] Login page with branding panel
   - [ ] Signup page

5. **Phase 5: Chat Interface**
   - [ ] Chat layout
   - [ ] Message components
   - [ ] Typing indicator
   - [ ] Input area

6. **Phase 6: Admin Dashboard**
   - [ ] Admin layout
   - [ ] Admin sidebar with badges
   - [ ] Stats cards
   - [ ] Interactions list
   - [ ] Interaction detail (5-level view)
   - [ ] Review interface

7. **Phase 7: Polish**
   - [ ] Add all animations
   - [ ] Responsive testing
   - [ ] Loading states
   - [ ] Error states
   - [ ] Empty states

---

## 11. VISUAL REFERENCE SUMMARY

### Color Quick Reference

| Use Case | Light Mode | Dark Mode |
|----------|------------|-----------|
| Primary Action | `#14b8a6` | `#2dd4bf` |
| Background | `#fafbfc` | `#0a0f1a` |
| Surface | `#ffffff` | `#111827` |
| Text Primary | `#0f172a` | `#f1f5f9` |
| Text Secondary | `#64748b` | `#94a3b8` |
| Border | `#e2e8f0` | `#1e293b` |
| Flagged | `#ef4444` | `#f87171` |
| Safe | `#22c55e` | `#4ade80` |
| Borderline | `#f59e0b` | `#fbbf24` |

### Typography Quick Reference

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Display | Cabinet Grotesk | 48px | Bold |
| Page Title | Cabinet Grotesk | 30px | Semibold |
| Section Title | Cabinet Grotesk | 20px | Semibold |
| Body | Satoshi | 16px | Regular |
| Small | Satoshi | 14px | Regular |
| Caption | Satoshi | 12px | Medium |
| Data | JetBrains Mono | 24px | Bold |

### Spacing Quick Reference

| Token | Value | Use Case |
|-------|-------|----------|
| `--space-2` | 8px | Tight gaps |
| `--space-3` | 12px | Component padding |
| `--space-4` | 16px | Standard gap |
| `--space-6` | 24px | Section padding |
| `--space-8` | 32px | Large sections |
| `--space-12` | 48px | Page margins |

---

**Document Status**: Complete
**Ready for Implementation**: Yes
**Design System Maturity**: Production-Grade

This document provides all specifications needed to implement a professional, production-grade UI for the Medical AI Anomaly Detection Platform.
