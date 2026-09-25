# Roadmap

Synesthetic Palette is being rebuilt for the Nebius x NVIDIA Global AI Hackathon 2026
(Personal AI track). Submission target: 27 October 2026. Hard deadline: 30 October, 18:00 CET.

The v0 in this repository is a scaffold: a chat and a text-to-palette call. The goal of the
rebuild is a product that turns any sensory input into a usable, verified design system.

## Product thesis

1. **Synesthesia, literally.** Input is not only a text brief. Sound (analysed in the browser
   with the Web Audio API), images (read by a vision model) and words all become palette,
   type pairing and motion curve.
2. **The model proposes, color science verifies.** Nemotron drafts the palette through tool
   calls; deterministic OKLCH code checks contrast (WCAG 2.2 and APCA), gamut and harmony,
   then hands failures back to the model to revise. No palette ships unverified.
3. **Personal AI that learns taste.** Every approval and rejection becomes memory. Memory
   lives in the user's browser (IndexedDB), can be exported and deleted in one click, and
   the backend stays stateless.
4. **A weekly drop with sources.** Trend research grounded by Tavily, every claim linked.
5. **Output that designers actually paste.** CSS variables, Tailwind theme, W3C design
   tokens (Figma), Adobe ASE, Procreate swatches, and live previews on real layouts.

## Model routing (Nebius Token Factory)

| Job | Model |
|---|---|
| Co-pilot chat, streaming | `nvidia/Nemotron-3_5-Lightning` |
| Cheap routing and memory summaries | `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B` |
| Palette agent and weekly drop drafting | `nvidia/nemotron-3-super-120b-a12b` |
| Weekly drop final critique | `nvidia/Nemotron-3-Ultra-550b-a55b` |
| Taste memory embeddings | `Qwen/Qwen3-Embedding-8B` |
| Reading reference images | `openbmb/MiniCPM-V-4_5` |

## Milestones

| # | Window | Milestone |
|---|---|---|
| M0 | 25–27 Sep | Repository, CI, baseline, model router |
| M1 | 28 Sep – 6 Oct | Engine: palette agent, color science validator, exports. **Scope freeze 6 Oct** |
| M2 | 7–13 Oct | Senses and memory: sound, image, taste memory, weekly drop pipeline |
| M3 | 14–20 Oct | Interface: full redesign with motion, live previews, deploy |
| M4 | 21–27 Oct | Proof: latency benchmarks, README, demo video under 3 minutes, submission |

---
© 2026 Eugenio Santiago. MIT licensed code; brand and written material may not be copied
without permission.
