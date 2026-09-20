# DEV·TV

**The developer internet, broadcast.**

A full-screen "TV" for the developer internet. Instead of checking GitHub, Hacker News, DEV, and Hugging Face separately, open one channel-surfable broadcast and let it run.

Keep coding. Keep an eye on the developer world.

---

## What it is

DEV·TV is a single self-contained HTML page — no build step, no server, no backend, no accounts. It pulls live data straight from public APIs in your own browser and presents it as a TV broadcast: one story on screen at a time, auto-rotating, with NOW/NEXT/LATER, a channel ident on every switch, a ticker, and real static when you change channels.

It is not a dashboard and not another feed aggregator. It shows a few curated items per channel and moves on, the way a TV station programs a schedule instead of dumping every wire story on screen at once.

## Channels

| # | Channel | Source | What it shows |
|---|---------|--------|----------------|
| 01 | **GitHub** | `api.github.com` | Repositories created in the last 7 days, sorted by stars — a "rising repository" heuristic since GitHub's Trending page has no official API |
| 02 | **Hacker News** | `hacker-news.firebaseio.com` | Current front-page stories |
| 03 | **DEV** | `dev.to/api` | Top articles from the last 7 days |
| 04 | **Hugging Face** | `huggingface.co/api` | Trending models, ranked by Hugging Face's own momentum score |

Every story links to its real source. Clicking a story opens an in-app reader instead of a new tab — full article body for DEV.to, the repo's README for GitHub, the model card for Hugging Face, and the self-post text for Hacker News (link posts have no article text on HN itself, so those show a short note plus a link out instead of faking content).

## Controls

- **← / →** or **number keys (1–4)** — change channel
- **Space** — pause / resume
- **▶ WATCH** — Auto Pilot: cycles through stories, then channels, on repeat
- **⚙** — toggle channels on/off (at least one must stay on)
- **Speed button (1× / 2× / 3× / 0.5×)** — controls how long each story stays on screen
- **⏻** — power off (screen goes to NO SIGNAL)
- **Esc** — close the in-app reader

## Running it

This is one HTML file. No install, no dependencies.

```bash
# just open it
open index.html        # macOS
start index.html        # Windows
xdg-open index.html     # Linux
```

Or double-click it in a file browser.

### Why it has to run as a real page, not inside a sandboxed preview

Every channel here does a live `fetch()` to a third-party API from your browser. Some sandboxed environments (embedded previews, some "artifact" runtimes) block outbound requests to arbitrary domains by content security policy — in that context every channel fails identically with a generic `Failed to fetch`, regardless of which API it's calling. Opening the file directly, or hosting it as a normal static page, removes that restriction entirely; it behaves like any other webpage making a `fetch()` call.

## Deploying it

It's a static file, so any static host works. No config needed.

- **Netlify Drop** — go to [app.netlify.com/drop](https://app.netlify.com/drop) and drag `index.html` in. Live in seconds, no account required for a one-off deploy.
- **GitHub Pages** — push this repo, then enable Pages in the repo's Settings → Pages, pointing at the `main` branch root. `index.html` is already named correctly for this.
- **Cloudflare Pages / Vercel** — same drag-and-drop or CLI deploy flow.

## Tech notes

- Vanilla HTML/CSS/JS. No framework, no build tooling, no npm packages.
- All state (enabled channels, playback speed) is kept in `localStorage`, scoped per browser/origin.
- Markdown from fetched READMEs/articles is rendered through a small, deliberately limited converter (headers, bold, italic, inline code, links). Input is HTML-escaped before any markup is reapplied, so nothing fetched from an external source can inject real HTML into the page.
- Each channel refreshes independently every 10 minutes. A channel that fails shows `SIGNAL LOST` with the underlying error, without affecting the other channels.

## What's deliberately not here yet

Kept out of scope for the same reason a v1 TV network doesn't launch with 40 channels:

- User accounts, personalization, or a recommendation engine
- AI-generated summaries — every story is real source data, not a rewrite
- A backend of any kind (several candidate sources — Reddit, Product Hunt, X, LinkedIn — were evaluated and ruled out specifically because they require one; see below)
- Community-created channels
- More than a handful of channels total

## Sources considered and ruled out

For transparency, since this took real investigation to confirm:

| Source | Status |
|---|---|
| Reddit | Public JSON endpoints are being locked down; real OAuth exists but its token-exchange step has no CORS support (confirmed against `ssl.reddit.com/api/v1/access_token`) — would require a backend to hold the exchange server-side |
| Product Hunt | GraphQL API requires an OAuth token that can't safely live in client-side code |
| X / Twitter | No free tier that can read data at all as of the 2026 pricing overhaul — pay-per-request from the first call |
| LinkedIn | Real API access is partner-gated (manual approval, months-long, often rejected); no path for an individual developer |
| Medium | Official API discontinued — no path to credentials, free or paid |
| arXiv | Tested live: API is real and keyless, but `export.arxiv.org` does not appear to support CORS for browser `fetch()` — removed after confirming `Failed to fetch` while every other channel succeeded in the same session |

## License

MIT — see [LICENSE](./LICENSE).
