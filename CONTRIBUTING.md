# Contributing to DEV·TV

Thanks for wanting to add to this. Before opening a PR, read the constraints below, they're not suggestions, they're what makes this project what it is.

## The rules that can't bend

- **One HTML file.** No build step, no framework, no npm packages, no second file except the license and README. If your change needs a bundler, it doesn't belong here.
- **No backend, ever.** Every channel is a direct `fetch()` from the browser. If a source needs a server-held API key or a token exchange that has no CORS support, it's not a candidate, no matter how good the data is. See the "Sources considered and ruled out" table in the README before proposing one, it's likely already been checked.
- **No AI-generated or AI-summarized content.** Every story shown is real source data, fetched live, not rewritten. This is a hard line, not a style preference.
- **Real data only.** No mock stories, no placeholder content in a merged PR. If a channel's API is temporarily down while you're building, that's fine locally, but the PR should work against the real endpoint.

## Proposing a new channel

Open an issue first, before writing code. Include:

1. **The source and its API.** Link the docs.
2. **Proof it works from a browser with no key.** Paste the result of running a real `fetch()` against it from your browser's console, or a screenshot of the Network tab showing a 200 response with no `Authorization` header. "The docs say it's keyless" isn't proof, CORS support and no-key access are two different things, and only testing both confirms it.
3. **What "trending" or "new" means for this source**, if relevant. Some APIs sort by relevance, some by date, some don't sort at all, be explicit about which you're using and why.

If a maintainer confirms it's viable, then send the PR.

## Code style

- Match what's already there: no semicolons-optional inconsistency, no mixed indentation, no new global variables beyond what's already declared near the top of the `<script>` block.
- Comments should explain *why*, not *what*. The existing code has a lot of these, e.g. why a limit is 6 requests or why a regex is shaped the way it is, follow that pattern.
- Keep the CRT/retro-TV feel in mind for anything visual. New UI should look like it was always part of the set, not bolted on.

## Testing your change

There's no test suite, this is intentionally a single static file. Instead:

1. Open `index.html` directly in a browser (`open index.html` / `start index.html` / `xdg-open index.html`).
2. Exercise the channel(s) you touched: let it run a full rotation, open the reader on a few stories, toggle it off/on in `⚙`, check it survives a `SIGNAL LOST` state if you can force one (e.g. by briefly going offline).
3. Check the browser console for errors you introduced.
4. If your change touches a channel that shares the GitHub rate limit (`GITHUB` or `RELEASES`), be mindful while testing, you're spending from the same 60/hour/IP budget documented in the README.

## Submitting the PR

- Keep it focused. One channel, one fix, one feature, not a grab-bag.
- Update the README if your change affects the channel table, the controls table, the "Tech notes" request-count math, or the "Sources considered and ruled out" list.
- Describe what you tested and how, since there's no CI to lean on.

## What won't be merged

- Anything requiring a backend, an API key held server-side, or a paid tier of an API.
- AI-generated summaries or rewrites of source content.
- A new file, a build tool, or a framework dependency.
- Tracking, analytics, or anything that phones home beyond the channel's own source API.

If you're not sure whether an idea fits, open an issue and ask before building it.
