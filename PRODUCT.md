# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack
Vite + React (TypeScript) with Vanilla CSS (Frontend); FastAPI + Python (Backend) with Nebius Token Factory (`nvidia/Nemotron-3_5-Lightning`).

## Users
Creative professionals, graphic designers, motion designers, illustrators, and small creative/art studios who need trend intelligence and palette generation every week but are priced out of enterprise forecasting platforms like WGSN.

## Product Purpose
Synesthetic Palette is a personal AI design co-pilot that democratizes trend forecasting and palette/sensory generation. Every Monday it releases a "trend drop" consisting of color palettes, typography pairings, and aesthetic briefs, and provides an active, persistent AI Co-pilot under the "Personal AI" track to help designers brainstorm and customize palettes.

## Positioning
An affordable, accessible, and highly aesthetic trend-forecasting and palette co-pilot built specifically for the day-to-day visual decisions of designers, utilizing local persistence, fast open models (NVIDIA), and web grounding (Tavily).

## Operating Context
Designers working on active branding, motion design, or UI projects on their local machines. They use the web dashboard to browse trends, copy HEX/RGB/OKLCH values, download CSS/Figma variables, and chat with their aesthetic assistant to explore design combinations.

## Capabilities and Constraints
- **Weekly Drops:** Monday color palette, typography pairing, and concept justification.
- **Interactive Co-pilot:** Always-on chat with system-prompted design director personality.
- **Dynamic Palette Generator:** Takes a brief and outputs structured JSON swatches.
- **Local Persistence:** History and saved swatches are stored locally (SQLite/JSON on backend, LocalStorage on frontend).
- **Technological constraint:** Calls must run through the Nebius Token Factory API and use an NVIDIA track model (e.g., `nvidia/Nemotron-3_5-Lightning`).

## Brand Commitments
- **Name:** Synesthetic Palette
- **Tone & Voice:** Professional, inspiring, direct, visual, artistic, and sophisticated (Eugenio's style).
- **Aesthetic:** Minimalist, high-contrast, modern dark mode, fluid transitions, and precise typography spacing.

## Evidence on Hand
Draft submission texts and structural plans are mapped out in `eg-private-local/shipaton-textos-submissao.md`.

## Product Principles
1. **Design First:** The interface itself must feel like a work of art—polished, responsive, and visually impeccable.
2. **Actionable Utility:** Every color, font, or insight must be easy to copy, export, and use immediately in design software.
3. **Control & Security:** User data, project details, and saved preferences are owned and kept local by the user.

## Accessibility & Inclusion
Accessible contrast ratios for color text overlays, keyboard-navigable palette copying, and semantic HTML structure.
