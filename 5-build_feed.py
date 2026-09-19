#!/usr/bin/env python3
"""Regenerate feed.xml + index.html for the Musagim podcast from episodes.json.
Daily update: add the new mp3 to episodes/, append an entry to episodes.json
(with real byte size + duration), run this script, push."""
import json, html, os, sys

BASE = "https://avigdor-instinct.github.io/musagim"
HERE = os.path.dirname(os.path.abspath(__file__))

def fmt_dur(s):
    s = int(round(s)); return f"{s//3600:02d}:{(s%3600)//60:02d}:{s%60:02d}"

def main():
    data = json.load(open(os.path.join(HERE, "episodes.json"), encoding="utf-8"))
    show = data["show"]; eps = data["episodes"]
    items = []
    for ep in reversed(eps):  # newest first
        t = html.escape(ep["title"]); d = html.escape(ep["summary"])
        items.append(f"""  <item>
   <title>{t}</title>
   <description>{d}</description>
   <itunes:title>{t}</itunes:title>
   <itunes:summary>{d}</itunes:summary>
   <enclosure url="{BASE}/episodes/{ep['file']}" length="{ep['size']}" type="audio/mpeg"/>
   <guid isPermaLink="false">musagim-ep{ep['num']:03d}</guid>
   <pubDate>{ep['date']}</pubDate>
   <itunes:duration>{fmt_dur(ep['duration'])}</itunes:duration>
   <itunes:episode>{ep['num']}</itunes:episode>
   <itunes:episodeType>full</itunes:episodeType>
   <itunes:explicit>false</itunes:explicit>
  </item>""")
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom">
 <channel>
  <title>{html.escape(show['title'])}</title>
  <link>{BASE}/</link>
  <atom:link href="{BASE}/feed.xml" rel="self" type="application/rss+xml"/>
  <language>{show['language']}</language>
  <copyright>© 2026 {html.escape(show['author'])}</copyright>
  <description>{html.escape(show['description'])}</description>
  <itunes:author>{html.escape(show['author'])}</itunes:author>
  <itunes:summary>{html.escape(show['description'])}</itunes:summary>
  <itunes:owner><itunes:name>{html.escape(show['author'])}</itunes:name><itunes:email>{show['email']}</itunes:email></itunes:owner>
  <itunes:image href="{BASE}/cover.jpg"/>
  <itunes:category text="{show['category']}"/>
  <itunes:explicit>false</itunes:explicit>
  <image><url>{BASE}/cover.jpg</url><title>{html.escape(show['title'])}</title><link>{BASE}/</link></image>
{chr(10).join(items)}
 </channel>
</rss>
"""
    open(os.path.join(HERE, "feed.xml"), "w", encoding="utf-8").write(feed)
    rows = "\n".join(
        f'<li dir="rtl"><b>פרק {e["num"]:03d}</b> · {html.escape(e["title"])} '
        f'<audio controls preload="none" src="episodes/{e["file"]}"></audio></li>'
        for e in reversed(eps))
    page = f"""<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(show['title'])}</title>
<style>body{{font-family:system-ui,sans-serif;background:#f5efe3;color:#1a1a1a;max-width:640px;margin:2rem auto;padding:0 1rem;line-height:1.6}}
img.cover{{width:180px;border-radius:12px}}audio{{width:100%;margin-top:4px}}li{{margin-bottom:1.2rem}}code{{background:#ece4d2;padding:2px 6px;border-radius:6px;direction:ltr;display:inline-block}}</style></head>
<body><img class="cover" src="cover.jpg" alt="עטיפת הפודקאסט">
<h1>{html.escape(show['title'])}</h1><p>{html.escape(show['description'])}</p>
<p>להאזנה באפל פודקאסטס או כל אפליקציית פודקאסטים: מוסיפים לפי כתובת ה-RSS:<br><code>{BASE}/feed.xml</code></p>
<ol>{rows}</ol></body></html>"""
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    # sanity: verify every referenced mp3 exists with the declared size
    ok = True
    for ep in eps:
        p = os.path.join(HERE, "episodes", ep["file"])
        if not os.path.exists(p): print("MISSING", p); ok = False
        elif os.path.getsize(p) != ep["size"]:
            print("SIZE MISMATCH", ep["file"], os.path.getsize(p), "!=", ep["size"]); ok = False
    print("feed.xml + index.html written,", "all files OK" if ok else "FILE PROBLEMS")

if __name__ == "__main__":
    main()
