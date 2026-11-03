#!/usr/bin/env python3
"""DEVTube fetcher: ranks YouTube videos recommended across DEV.to articles and comments.

Usage (from the devtv repo root):  python3 scripts/devtube.py
Output: devtube.json (ranked), .devtube-cache/ (raw API responses, so reruns are fast)
"""
import argparse, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

API = "https://dev.to/api"
UA = {"User-Agent": "DEVTube/0.1 (github.com/shouvik12)"}
DEV_HEADERS = {**UA, "Accept": "application/vnd.forem.api-v1+json"}
CACHE = ".devtube-cache"
DELAY = 0.4

YT_PATTERNS = [
    # DEV liquid tag: {% youtube VIDEO_ID %}
    re.compile(r"\{%\s*youtube\s+[\"']?([A-Za-z0-9_-]{11})", re.I),
    # Plain links and iframes: watch?v=, youtu.be/, embed/, shorts/, live/
    re.compile(r"(?:youtube(?:-nocookie)?\.com/(?:watch\?(?:[^\s\"'<>]*?[&;])?v=|embed/|live/|v/)"
               r"|youtu\.be/)([A-Za-z0-9_-]{11})", re.I),
]


def get(url, headers, retries=5):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 404):
                return None
            wait = 2 ** attempt * 2
            print(f"  HTTP {e.code}, retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)
        except (urllib.error.URLError, TimeoutError):
            time.sleep(2 ** attempt)
    return None


def cached(kind, key, url, headers=DEV_HEADERS):
    path = os.path.join(CACHE, kind, f"{key}.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    data = get(url, headers)
    time.sleep(DELAY)
    if data is not None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f)
    return data


TS = re.compile(r"(?:youtube(?:-nocookie)?\.com/\S*?|youtu\.be/)([A-Za-z0-9_-]{11})\S*?[?&#](?:t|start)=(?:(\d+)h)?(?:(\d+)m)?(\d+)s?", re.I)


def video_ids(text):
    ids = set()
    for p in YT_PATTERNS:
        ids.update(p.findall(text or ""))
    return ids


def timestamps(text):
    """{video_id: [seconds, ...]} for links like ?t=760 or &t=12m40s."""
    out = {}
    for vid, h, m, sec in TS.findall(text or ""):
        out.setdefault(vid, []).append(int(h or 0) * 3600 + int(m or 0) * 60 + int(sec))
    return out


def real_text(html):
    """Words in a comment once tags and links are removed. Spam is usually just a link."""
    t = re.sub(r"<[^>]+>", " ", html or "")
    t = re.sub(r"https?://\S+", " ", t)
    return len(t.split())


def walk(comments):
    for c in comments or []:
        yield c
        yield from walk(c.get("children"))


def main():
    global DELAY
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=365, help="top articles from the last N days")
    ap.add_argument("--pages", type=int, default=1, help="pages of articles to scan")
    ap.add_argument("--per-page", type=int, default=1000)
    ap.add_argument("--top", type=int, default=300, help="videos to keep in output")
    ap.add_argument("--delay", type=float, default=0.4)
    args = ap.parse_args()
    DELAY = args.delay

    videos = {}  # id -> {"people": set, "sources": []}
    stats = {"articles": 0, "comments": 0, "words": 0, "links": 0, "authors": set(), "commenters": set(), "oldest": None}

    def add(vid, person, source, text=""):
        v = videos.setdefault(vid, {"people": set(), "sources": [], "starts": []})
        v["starts"] += timestamps(text).get(vid, [])
        v["people"].add(person)
        v["sources"].append(source)

    for page in range(1, args.pages + 1):
        url = f"{API}/articles?top={args.days}&per_page={args.per_page}&page={page}"
        articles = get(url, DEV_HEADERS) or []
        print(f"Page {page}: {len(articles)} articles")
        for i, meta in enumerate(articles, 1):
            aid, title, aurl = meta["id"], meta["title"], meta["url"]
            author = meta["user"]["username"]
            tags = meta.get("tag_list") or []
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",") if t.strip()]
            ctx = {"article_title": title, "article_url": aurl, "tags": tags}

            full = cached("articles", aid, f"{API}/articles/{aid}") or {}
            stats["articles"] += 1
            stats["authors"].add(author)
            stats["words"] += len((full.get("body_markdown") or "").split())
            pub = (meta.get("published_at") or "")[:10]
            if pub and (not stats["oldest"] or pub < stats["oldest"]):
                stats["oldest"] = pub
            for vid in video_ids(full.get("body_markdown")):
                add(vid, author, {**ctx, "type": "article", "by": author, "url": aurl}, full.get("body_markdown"))

            if meta.get("comments_count", 0) > 0:
                comments = cached("comments", aid, f"{API}/comments?a_id={aid}") or []
                for c in walk(comments):
                    who = (c.get("user") or {}).get("username", "unknown")
                    stats["comments"] += 1
                    stats["commenters"].add(who)
                    stats["words"] += len(re.sub(r"<[^>]+>", " ", c.get("body_html") or "").split())
                    curl = f"https://dev.to/{who}/comment/{c.get('id_code', '')}"
                    if real_text(c.get("body_html")) < 8:
                        continue  # link-only comment: usually spam or self-promo
                    for vid in video_ids(c.get("body_html")):
                        add(vid, who, {**ctx, "type": "comment", "by": who, "url": curl}, c.get("body_html"))

            if i % 100 == 0:
                print(f"  {i} articles scanned, {len(videos)} videos found")

    stats["links"] = sum(len(v["sources"]) for v in videos.values())
    people = stats["authors"] | stats["commenters"]
    recommenders = set().union(*(v["people"] for v in videos.values())) if videos else set()

    # Rank by number of distinct people recommending, then total mentions
    ranked = sorted(videos.items(), key=lambda kv: (len(kv[1]["people"]), len(kv[1]["sources"])), reverse=True)

    out = []
    for vid, v in ranked:
        if len(out) >= args.top:
            break
        watch = f"https://www.youtube.com/watch?v={vid}"
        oembed = cached("oembed", vid, "https://www.youtube.com/oembed?format=json&url="
                        + urllib.parse.quote(watch, safe=""), headers=UA)
        if not oembed:  # removed or private video
            continue
        out.append({
            "id": vid,
            "title": oembed.get("title"),
            "channel": oembed.get("author_name"),
            "thumbnail": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
            "url": watch,
            # Most-cited moment: the timestamp people linked to most often.
            "start": max(set(v["starts"]), key=v["starts"].count) if v["starts"] else 0,
            "people": len(v["people"]),
            "mentions": len(v["sources"]),
            "sources": v["sources"],
        })

    with open("devtube.json", "w") as f:
        summary = {
            "articles_scanned": stats["articles"],
            "comments_scanned": stats["comments"],
            "words_read": stats["words"],
            "developers_scanned": len(people),
            "video_recommendations": stats["links"],
            "unique_videos": len(videos),
            "developers_recommending": len(recommenders),
            "videos_on_channel": len(out),
            "oldest_article": stats["oldest"],
        }
        json.dump({"generated": time.strftime("%Y-%m-%d"), "stats": summary, "videos": out}, f, indent=2)
    print(f"Done: {len(out)} videos written to devtube.json\n")
    for k, v in summary.items():
        print(f"  {k.replace('_', ' '):26} {v:,}" if isinstance(v, int) else f"  {k.replace('_', ' '):26} {v}")


if __name__ == "__main__":
    main()
