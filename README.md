<div align="center">

# 📺 DEV·TV

### The developer internet, broadcast.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![No backend](https://img.shields.io/badge/backend-none-brightgreen)]()
[![Single file](https://img.shields.io/badge/build%20step-none-brightgreen)]()
[![Channels](https://img.shields.io/badge/channels-5%20live-orange)]()
[![Mobile friendly](https://img.shields.io/badge/mobile-friendly-blue)]()

A full-screen "TV" for the developer internet. Instead of checking GitHub, Hacker News, DEV, Hugging Face, and release notes separately, open one channel-surfable broadcast and let it run.

**Keep coding. Keep an eye on the developer world.**

</div>

---

### 🖼️ Screenshot

> _Drop a real screenshot or GIF of your running instance at `assets/screenshot.png` and it'll render here automatically: `![DEV·TV screenshot](./assets/screenshot.png)`._

Until then, here's what's actually on screen. Note it's playing by default, the way a real TV already has something on when you turn it on:

```
┌──────────────────────────────────────────────────────────┐
│  ● ON AIR  01  GITHUB                          ▪▪▪▪       │
│                                                             │
│  RISING REPOSITORY                                         │
│  browser-use/jev-ultrafast                                 │
│  10,584 stars · created 3d ago                              │
│  i. am. speed.                                              │
│  ▸ click to read in DEV·TV                                  │
│                                                             │
│  NOW    browser-use/jev-ultrafast                          │
│  NEXT   tamaratran/fast-jev-compaction                     │
│  LATER  robbietilton/Compositor                            │
│                                                             │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  HF: prism-ml/Ternary-Bonsai  •  REL: React v19.2.0  •  …  │
└──────────────────────────────────────────────────────────┘
[❚❚ STOP] [01 GH][02 HN][03 DEV][04 HF][05 REL] [1×][⏻ green]
```

---

## What it is

DEV·TV is a single self-contained HTML page. No build step, no server, no backend, no accounts. It pulls live data straight from public APIs in your own browser and presents it as a real TV broadcast: one story on screen at a time, auto-rotating, with NOW/NEXT/LATER, a channel ident on every switch, a ticker, real per-pixel static on power-on and every channel change, and a CRT-style collapse/expand animation when you power it off and on.

It is **not** a dashboard and **not** another feed aggregator. It shows a few curated items per channel and moves on, the way a TV station programs a schedule instead of dumping every wire story on screen at once.

## 📡 Channels

| # | Channel | Source | What it shows |
|---|---------|--------|----------------|
| 01 | **GitHub** | `api.github.com` | Repositories created in the last 7 days, sorted by stars. A "rising repository" heuristic, since GitHub's Trending page has no official API |
| 02 | **Hacker News** | `hacker-news.firebaseio.com` | Current front-page stories |
| 03 | **DEV** | `dev.to/api` | Top articles from the last 7 days |
| 04 | **Hugging Face** | `huggingface.co/api` | Trending models, ranked by Hugging Face's own momentum score |
| 05 | **Releases** | `api.github.com` | Real version releases for the stacks people actually google to stay current: React, Vue, TypeScript, Node.js, Python, Rust |

Every story links to its real source. Click a story and it opens in an in-app reader right on the TV, no new tab:

- **DEV.to**: the full article body
- **GitHub**: the repo's actual README
- **Hugging Face**: the model's README / model card
- **Releases**: the real release notes, already fetched, no extra request
- **Hacker News**: full text for self-posts (Ask HN / Show HN); link posts have no article text on HN itself, so those show a short note plus a link out instead of faking content

Markdown from fetched content renders through a small, deliberately limited converter (headers, bold, italic, inline code, links). Input is HTML-escaped before any markup is reapplied, so nothing fetched from an external source can inject real HTML into the page.

## 🎛️ Controls

| Key / Button | Action |
|---|---|
| `←` `→` or `1`–`5` | Change channel. Doesn't interrupt playback either way |
| `❚❚ STOP` / `▶ WATCH` | Playing is the default, like turning on a real TV. STOP freezes on whatever story is currently showing; WATCH resumes from there |
| `⚙` | Toggle channels on/off. Each shows an explicit **ON** / **OFF** label, not just a switch position (at least one channel must stay on) |
| Speed button | `1×` `2×` `3×` `0.5×`, how long each story stays on screen |
| `⛶` | Fullscreen toggle |
| `⏻` | Power. Green glow means on, dim gray means off, tooltip tells you which way it'll flip. Powering off plays a real CRT-style collapse (screen squishes to a line, then a dot, then dark); powering on reverses it |
| `Esc` | Close the in-app reader |

Static (real per-pixel noise, not a CSS texture) plays continuously on first load until you pick a channel, and briefly on every channel change afterward, like actually tuning a signal.

## 📱 Mobile

The layout is responsive below 640px: channel buttons resize to fit three per row, the WATCH/STOP button takes its own full-width row, round buttons grow to a 44px minimum touch target, and the footer hint swaps from keyboard shortcuts to tap instructions. Nothing here has been tested on a real device by an AI, though. If something looks cramped on your phone, it's worth a closer look.

## 🚀 Running it

This is one HTML file. No install, no dependencies.

```bash
open index.html        # macOS
start index.html        # Windows
xdg-open index.html     # Linux
```

Or just double-click it in a file browser.

### ⚠️ Why it has to run as a real page, not inside a sandboxed preview

Every channel does a live `fetch()` to a third-party API from your browser. Some sandboxed environments (embedded previews, "artifact" runtimes) block outbound requests to arbitrary domains via content security policy. In that context every channel fails identically with a generic `Failed to fetch`, regardless of which API it's calling. Opening the file directly, or hosting it as a normal static page, removes that restriction. It behaves like any other webpage making a `fetch()` call.

## ☁️ Deploying it

It's a static file, so any static host works. No config needed.

- **[Netlify Drop](https://app.netlify.com/drop)**: drag `index.html` in. Live in seconds, no account required.
- **GitHub Pages**: push this repo, then enable Pages in **Settings → Pages**, pointing at the `main` branch root. `index.html` is already named correctly for this.
- **Cloudflare Pages / Vercel**: same drag-and-drop or CLI deploy flow.

## 🔧 Tech notes

- Vanilla HTML/CSS/JS. No framework, no build tooling, no npm packages.
- All state (enabled channels, playback speed) lives in `localStorage`, scoped per browser/origin.
- Each channel refreshes independently every 10 minutes, regardless of playback state. A channel that fails shows `SIGNAL LOST` with the underlying error, without affecting the others.
- The `RELEASES` channel makes 6 requests per refresh (one per tracked project) against `api.github.com`, same host as the `GITHUB` channel. GitHub's unauthenticated core API allows 60 requests/hour/IP; this app stays comfortably under that even with both channels and occasional README reads.
- The power-on/off transition is a real CSS keyframe animation (`scale` + `filter: brightness/contrast`) on the screen element, not a fade. It genuinely collapses to a line and a dot, CRT-style.

## 🚫 What's deliberately not here yet

Kept out of scope for the same reason a v1 TV network doesn't launch with 40 channels:

- User accounts, personalization, or a recommendation engine
- AI-generated summaries: every story is real source data, not a rewrite
- A backend of any kind (several candidate sources, Reddit, Product Hunt, X, LinkedIn, Discord, were evaluated and ruled out specifically because they require one; see below)
- Community-created channels
- More than a handful of channels total

## 🔍 Sources considered and ruled out

For transparency, since this took real investigation to confirm:

| Source | Status |
|---|---|
| **Reddit** | Public JSON endpoints are being locked down; real OAuth exists but its token-exchange step has no CORS support (confirmed against `ssl.reddit.com/api/v1/access_token`). Would need a backend to hold the exchange server-side |
| **Product Hunt** | GraphQL API requires an OAuth token that can't safely live in client-side code |
| **X / Twitter** | No free tier that can read data at all as of the 2026 pricing overhaul. Pay-per-request from the first call |
| **LinkedIn** | Real API access is partner-gated (manual approval, months-long, often rejected). No path for an individual developer |
| **Medium** | Official API discontinued. No path to credentials, free or paid |
| **Discord** | OAuth/bot-token required for everything; no global "trending" concept even with a token; CORS explicitly unsupported |
| **arXiv** | Tested live: API is real and keyless, but `export.arxiv.org` does not appear to support CORS for browser `fetch()`. Removed after confirming `Failed to fetch` while every other channel succeeded in the same session |

## 📄 License

MIT, see [LICENSE](./LICENSE).
