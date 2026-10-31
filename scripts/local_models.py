#!/usr/bin/env python3
"""Builds local-models.json for DEV·TV's LOCAL MODELS channel.

Ollama's library has no public JSON feed, so this reads the newest-first
search page on ollama.com once a day (from a GitHub Action) and saves the
newest models. index.html then loads the JSON the same way it loads
spotlight.json. Standard library only: nothing to install.

The parser doesn't depend on Ollama's CSS classes or test attributes. It
finds each /library/<name> link, takes the text between it and the next
model link, and picks out sizes, abilities, pulls and "updated" from that.
"""
import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone

URL = "https://ollama.com/search?o=newest"
OUT = "local-models.json"
LIMIT = 20
CAPS = ["tools", "vision", "thinking", "embedding", "audio", "cloud"]


def chunks_to_text(chunk):
    """Visible text pieces of an HTML chunk, in order."""
    chunk = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", chunk, flags=re.S)
    parts = re.split(r"<[^>]+>", chunk)
    return [html.unescape(p).strip() for p in parts if html.unescape(p).strip()]


def main():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (DEV-TV local-models bot; github.com/shouvik12/devtv)"})
    page = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")

    links = list(re.finditer(r'href="/library/([A-Za-z0-9._-]+)"', page))
    models, seen = [], set()
    for i, m in enumerate(links):
        name = m.group(1)
        if name in seen:
            continue
        seen.add(name)
        # A card can link to its model more than once, so the card ends at
        # the next link to a *different* model, not just the next link.
        end = next((l.start() for l in links[i + 1:] if l.group(1) != name), len(page))
        # Start after the rest of the <a ...> tag, so its other attributes
        # (class="...") never get read as card text.
        tag_end = page.find(">", m.end())
        texts = chunks_to_text(page[tag_end + 1:end] if 0 <= tag_end < end else "")
        texts = [t for t in texts if "=" not in t and not t.startswith("class")]
        lower = [t.lower() for t in texts]

        caps = [c for c in CAPS if c in lower]
        # Sizes are lowercase (1.7b, 135m, e2b, 8x7b); pull counts are
        # uppercase (23.8K, 1.2M), so case tells them apart.
        sizes = [t for t in texts if re.fullmatch(r"(?:\d+x)?\d+(?:\.\d+)?[bm]|e\d+b", t)]
        pulls = next((t for t in texts if re.fullmatch(r"[\d.,]+[KMB]", t)), "")
        updated = ""
        # Ollama puts the exact date in a tooltip: title="Updated October 29, 2026".
        dm = re.search(r'title="Updated ([A-Z][a-z]+) (\d{1,2}), (\d{4})"', page[m.end():end])
        if dm:
            updated = dm.group(1)[:3] + " " + dm.group(2) + ", " + dm.group(3)
        # Exact download count is in a tooltip too: title="6,074 downloads".
        if not pulls:
            pm2 = re.search(r'title="([\d,]+) downloads?"', page[m.end():end])
            if pm2:
                pulls = pm2.group(1)
        if "--debug" in sys.argv and len(models) == 0:
            print("DEBUG", name, texts)
        for j, t in enumerate(lower):
            if not pulls and re.fullmatch(r"[\d.,]+\s*[kmb]?", t) and j + 1 < len(lower) and lower[j + 1].startswith("pull"):
                pulls = texts[j]
            pm = re.fullmatch(r"([\d.,]+\s*[kmb]?)\s+pulls?", t)
            if not pulls and pm:
                pulls = pm.group(1)
            um = re.search(r"(\d+\s+\w+\s+ago|yesterday|today|just now)", t)
            if not updated and um:
                updated = um.group(1)
        # The description is the longest piece of real prose in the card.
        prose = [t for t in texts if len(t) > 30 and t.lower() != name.lower()]
        desc = max(prose, key=len) if prose else ""

        # Cloud-only models can't be pulled and run locally.
        if not sizes and "cloud" in caps:
            continue
        models.append({
            "name": name,
            "description": desc,
            "capabilities": [c for c in caps if c != "cloud"],
            "sizes": sizes,
            "pulls": pulls,
            "updated": updated,
        })
        if len(models) >= LIMIT:
            break

    # Nothing found means the page changed or came back empty. Fail loudly
    # and keep yesterday's file instead of publishing an empty channel.
    if not models:
        sys.exit("No models parsed from " + URL + " (the page layout may have changed)")

    data = {
        "source": URL,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "models": models,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("Saved", len(models), "models to", OUT)
    for x in models[:5]:
        print(" -", x["name"], "|", ", ".join(x["sizes"]) or "-", "|", ", ".join(x["capabilities"]) or "-", "|", x["pulls"] or "-", "|", x["updated"] or "-")


if __name__ == "__main__":
    main()
