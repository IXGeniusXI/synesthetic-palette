# Design System — Synesthetic Palette

<!-- impeccable:design-schema 1 -->

## 🎨 Palette (Deep Synesthetic Theme)

A minimalist, high-contrast dark palette designed to make color swatches pop off the screen with absolute clarity while maintaining an immersive, premium gallery aesthetic.

| Token | Color Name | HEX | Role | OKLCH |
| :--- | :--- | :--- | :--- | :--- |
| `--bg-abyss` | Deep Abyss | `#050B14` | Page Background | `0.08, 0.03, 240` |
| `--bg-surface` | Midnight Surface | `#0D1527` | Cards / Container surfaces | `0.13, 0.04, 244` |
| `--bg-glass` | Aero Glass | `rgba(24, 35, 60, 0.4)` | Floating components / Backdrops | `0.20, 0.05, 242` |
| `--accent-green` | Vivid Synesthesia Green | `#00FF66` | Primary Accent / Interactive | `0.86, 0.28, 142` |
| `--accent-cyan` | Neon Cyan | `#00F0FF` | Secondary Highlight / Tooltips | `0.78, 0.22, 196` |
| `--text-primary` | Polar Mist | `#E6ECF8` | Main Headings & Body | `0.92, 0.02, 240` |
| `--text-muted` | Subdued Slate | `#7C8B9E` | Secondary/Meta text & borders | `0.58, 0.04, 242` |

---

## 🔤 Typography

Our typeface pairings contrast technical precision (Mono) with organic elegance (Serif) to reflect the hybrid nature of AI-curated and human-designed aesthetics.

*   **Display Font:** `Instrument Serif` (Google Fonts). Used for large headings and emotional callouts.
    *   *Usage Rule:* Set in large sizes (48px+), frequently in *italics* (`font-style: italic`), with letter-spacing set to `-0.02em` for an elegant, editorial, fashion-house feel.
*   **Body & UI Font:** `Plus Jakarta Sans` or system `system-ui`. Used for control elements, descriptions, and dashboard metrics.
    *   *Usage Rule:* High legibility, medium weight (500) for UI labels, tight letter-spacing (`-0.011em`).
*   **Data & Swatches Font:** `Geist Mono` or system mono. Used for HEX codes, RGB strings, metrics, and prompts.
    *   *Usage Rule:* Highly readable, uppercase swatches, letter-spacing `0.05em`.

---

## 📐 Layout & Spacing

*   **Grid System:** Flexible grid using CSS Grid and Flexbox. Spacing uses a strict 8px/4px base.
*   **Outer Page Margins:** `min(4vw, 48px)` for robust breathing room.
*   **Cards Padding:** `24px` on desktop, `16px` on mobile.
*   **Border Radius:**
    *   Containers & Cards: `16px` (`--radius-lg`)
    *   Buttons & Badges: `8px` (`--radius-sm`)

---

## 💫 Transitions & Interactive States

*   **Default Easing:** `cubic-bezier(0.16, 1, 0.3, 1)` (Ultra-smooth ease-out custom curve).
*   **Hover States:**
    *   Interactive elements (Buttons, Swatches) transform slightly up by `-2px` with a subtle glow shadow of `--accent-green`.
    *   Swatches reveal a copy icon on hover with a fluid fade-in (`opacity: 1`, transition `0.2s`).
*   **Glassmorphism Backdrop Filter:** `backdrop-filter: blur(12px) saturate(180%)`.

---

## 🛠️ Design System CSS (Vanilla)

```css
:root {
  --bg-abyss: #050b14;
  --bg-surface: #0d1527;
  --bg-glass: rgba(24, 35, 60, 0.4);
  --accent-green: #00ff66;
  --accent-cyan: #00f0ff;
  --text-primary: #e6ecf8;
  --text-muted: #7c8b9e;

  --font-display: 'Instrument Serif', serif;
  --font-sans: 'Plus Jakarta Sans', system-ui, sans-serif;
  --font-mono: 'Geist Mono', 'Space Mono', monospace;

  --radius-lg: 16px;
  --radius-md: 12px;
  --radius-sm: 8px;

  --transition-smooth: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  --shadow-glow: 0 0 20px rgba(0, 255, 102, 0.15);
}
```
