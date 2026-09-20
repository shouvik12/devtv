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

![DEV·TV screenshot](./assets/screenshot.png)

_Real capture: headless Chromium loaded `index.html`, tuned to the GitHub channel, and this is what came back live. GitHub is the channel shown here because it's the only one this particular capture environment could reach; the other four render identically in layout, just with each channel's own color and data._

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

![In-app reader](./assets/screenshot-reader.png)

_Real capture of the reader opening a GitHub README. It happened to hit a live rate limit (`403`) from this repo's own testing volume when the screenshot was taken, which is actually a decent look at the app's real error handling: a clear message plus a working "Open original source" fallback, rather than a broken page._

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

![Channel settings panel](./assets/screenshot-settings.png)

_The ⚙ panel: real ON/OFF labels per channel, plus live NO SIGNAL indicators for whichever channels this particular capture environment couldn't reach._

## 📱 Mobile

The layout is responsive below 640px: channel buttons resize to fit three per row, the WATCH/STOP button takes its own full-width row, round buttons grow to a 44px minimum touch target, and the footer hint swaps from keyboard shortcuts to tap instructions.

![Mobile layout](./assets/screenshot-mobile.png)

_Real capture at a 390×844 viewport, the same headless run as above._

## 🚀 Getting it running

This is one HTML file. No install, no dependencies, no account.

### On desktop (Chrome, Safari, Firefox, Edge, any browser)

1. **Download `index.html`**: on this repo's GitHub page, click the green **Code** button → **Download ZIP** (or just open [index.html](./index.html) and use the "Download raw file" button).
2. Find it in your Downloads folder.
3. **Open it**: double-click it, or drag it straight into an open browser window, or right-click it → **Open with** → your browser of choice.

```bash
open index.html        # macOS
start index.html        # Windows
xdg-open index.html     # Linux
```

That's it. It runs entirely in the browser, nothing to install.

### On mobile

Opening a local HTML file on a phone isn't really practical the way double-clicking it is on desktop, phones don't give you the same drag-and-drop file access. The easy path on mobile is to open a **hosted** version instead of a local file:

- If it's already deployed (see **Deploying it** below), just open that link in Chrome or Safari on your phone like any normal website.
- If it isn't deployed yet, **[Netlify Drop](https://app.netlify.com/drop)** takes about 10 seconds from a laptop and gives you a real URL you can then open on your phone.

The app itself is responsive and touch-friendly below 640px wide, so once it's loaded from a real URL, it works the same as on desktop.

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
- The `RELEASES` channel makes 6 requests per refresh (one per tracked project) against `api.github.com`, same host as the `GITHUB` channel. Combined, the GitHub-backed channels use 7 requests per 10-minute refresh cycle, which is 42 requests/hour at the default rate. GitHub's unauthenticated core API allows 60 requests/hour/IP, so that leaves roughly 18/hour of headroom for interactive README reads before the shared limit is hit. If it is hit, the affected channel or reader shows a clear error rather than breaking the rest of the app. Note that this limit is tied to the originating IP, so multiple people behind the same public IP (an office, a shared network) share the same budget.
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
