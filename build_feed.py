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
   <link>{BASE}/#ep{ep['num']:03d}</link>
   <pubDate>{ep['date']}</pubDate>
   <itunes:duration>{fmt_dur(ep['duration'])}</itunes:duration>
   <itunes:episode>{ep['num']}</itunes:episode>
   <itunes:episodeType>full</itunes:episodeType>
   <itunes:image href="{BASE}/{ep["image"]}"/>
   <itunes:explicit>no</itunes:explicit>
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
  <itunes:explicit>no</itunes:explicit>
  <itunes:type>episodic</itunes:type>
  <image><url>{BASE}/cover.jpg</url><title>{html.escape(show['title'])}</title><link>{BASE}/</link></image>
{chr(10).join(items)}
 </channel>
</rss>
"""
    open(os.path.join(HERE, "feed.xml"), "w", encoding="utf-8").write(feed)
    def prompt_html(e):
        if not e.get("prompt"):
            return ""
        num = f'{e["num"]:03d}'
        return (
            f'<div class="ep-prompt" id="prompt-ep{num}"><div class="prompt-head"><b>פרומפט להטמעה</b>'
            f'<button class="copy-btn" type="button" data-target="pc{num}">העתקה</button></div>'
            f'<code id="pc{num}">{html.escape(e["prompt"])}</code></div>'
        )
    rows = "\n".join(
        f'<li dir="rtl" id="ep{e["num"]:03d}"><div class="ep-head"><img class="ep-cover" src="episodes/ep{e["num"]:03d}-cover.jpg" alt="עטיפת פרק {e["num"]:03d}" loading="lazy"><b>פרק {e["num"]:03d}</b><span class="ep-title">{html.escape(e["title"])}</span></div>'
        f'<p class="ep-sum">{html.escape(e["summary"])}</p>'
        + prompt_html(e) +
        f'<audio controls preload="none" src="episodes/{e["file"]}"></audio></li>'
        for e in reversed(eps))
    page = f"""<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(show['title'])} | {html.escape(show.get('tagline', show['description']))}</title>
<meta name="description" content="{html.escape(show['title'])} - {html.escape(show['description'])}">
<link rel="alternate" type="application/rss+xml" title="RSS" href="feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;800&display=swap" rel="stylesheet">
<style>
:root{{--cream:#f5efe1;--ink:#1c1a17;--teal:#4f8f7d;--teal-dark:#3a6e60;--paper:#efe7d3}}
*{{box-sizing:border-box}}
body{{font-family:'Heebo',system-ui,sans-serif;background:var(--cream);color:var(--ink);margin:0;line-height:1.65}}
.wrap{{max-width:680px;margin:0 auto;padding:0 1.25rem}}
header.hero{{text-align:center;padding:3.5rem 1.25rem 2.5rem;border-bottom:3px solid var(--ink)}}
header.hero img.cover{{width:min(300px,70vw);border-radius:14px;box-shadow:6px 6px 0 var(--ink);border:2px solid var(--ink)}}
h1{{font-size:2.9rem;font-weight:800;margin:1.6rem 0 0.2rem;letter-spacing:-0.5px}}
.tagline{{font-size:1.35rem;font-weight:600;color:var(--teal-dark);margin:0 0 1.2rem}}
.pitch{{max-width:34rem;margin:0 auto 0.6rem;font-size:1.08rem}}
.disclosure{{font-size:0.9rem;color:#5a5548;margin:0.6rem auto 0;max-width:34rem}}
.subscribe{{background:var(--paper);border:2px solid var(--ink);border-radius:14px;box-shadow:5px 5px 0 var(--ink);padding:1.4rem 1.5rem;margin:2.2rem 0;text-align:right}}
.subscribe summary{{margin:0;font-size:1.35rem;font-weight:800;cursor:pointer;list-style:none}}
.subscribe summary::-webkit-details-marker{{display:none}}
.subscribe summary::before{{content:"▸ ";color:var(--teal-dark)}}
.subscribe[open] summary::before{{content:"▾ "}}
.subscribe[open] summary{{margin-bottom:0.7rem}}
.btn{{display:inline-block;background:var(--teal);color:#fff;border:2px solid var(--ink);border-radius:10px;box-shadow:3px 3px 0 var(--ink);padding:0.55rem 1.1rem;font-weight:600;text-decoration:none;font-size:1rem;margin:0.3rem 0 0.3rem 0.6rem;transition:transform .05s}}
.btn:active{{transform:translate(2px,2px);box-shadow:1px 1px 0 var(--ink)}}
.btn.rss{{background:var(--ink)}}
.subscribe ol{{margin:0.6rem 0 0.2rem;padding-right:1.2rem}}
.feed-url{{display:block;direction:ltr;text-align:left;background:#fff;border:2px dashed var(--teal);border-radius:8px;padding:0.5rem 0.8rem;margin-top:0.7rem;font-family:ui-monospace,monospace;font-size:0.92rem;word-break:break-all}}
section.eps{{padding:0.5rem 0 3.5rem}}
section.eps h2{{font-size:1.5rem;font-weight:800;border-bottom:3px solid var(--teal);display:inline-block;padding-bottom:0.15rem}}
ol.episodes{{list-style:none;padding:0;margin:1.2rem 0 0}}
ol.episodes li{{background:#fbf7ec;border:2px solid var(--ink);border-radius:12px;padding:1rem 1.2rem;margin-bottom:1.1rem}}
.ep-head{{display:flex;gap:0.6rem;align-items:center;flex-wrap:wrap}}
.ep-cover{{width:64px;height:64px;border-radius:10px;border:2px solid var(--ink)}}
.ep-head b{{color:var(--teal-dark)}}
.ep-title{{font-weight:600;font-size:1.05rem}}
.ep-sum{{margin:0.3rem 0 0.6rem;font-size:0.95rem;color:#45413a}}
.ep-prompt{{background:var(--paper);border:2px dashed var(--teal);border-radius:10px;padding:0.7rem 0.9rem;margin:0.5rem 0 0.8rem}}
.prompt-head{{display:flex;justify-content:space-between;align-items:center;margin-bottom:0.3rem}}
.prompt-head b{{color:var(--teal-dark)}}
.ep-prompt code{{display:block;font-family:inherit;font-size:0.92rem;white-space:pre-wrap;line-height:1.6}}
.copy-btn{{background:var(--teal);color:#fff;border:2px solid var(--ink);border-radius:8px;padding:0.15rem 0.7rem;font-family:inherit;font-size:0.85rem;font-weight:600;cursor:pointer}}
.copy-btn:active{{transform:translate(1px,1px)}}
.suggest{{background:#fbf7ec;border:2px solid var(--ink);border-radius:12px;padding:1.1rem 1.3rem;margin:1.4rem 0 1.8rem}}
.suggest h2{{font-size:1.35rem;font-weight:800;color:var(--teal-dark);margin:0 0 0.3rem}}
.suggest p.hint{{margin:0 0 0.8rem;font-size:0.95rem;color:#45413a}}
.suggest textarea{{width:100%;min-height:90px;border:2px solid var(--ink);border-radius:10px;padding:0.6rem 0.8rem;font-family:inherit;font-size:1rem;background:#fff;resize:vertical;box-sizing:border-box}}
.suggest input.nick{{width:100%;max-width:280px;border:2px solid var(--ink);border-radius:10px;padding:0.45rem 0.8rem;font-family:inherit;font-size:0.95rem;background:#fff;margin-top:0.6rem;box-sizing:border-box}}
.suggest .hp{{position:absolute;right:-9999px;opacity:0;height:0;overflow:hidden}}
.suggest button{{margin-top:0.7rem;cursor:pointer;font-family:inherit}}
.suggest .s-msg{{margin:0.5rem 0 0;font-weight:600;font-size:0.95rem}}
.suggest .s-msg.ok{{color:var(--teal-dark)}}
.suggest .s-msg.err{{color:#b3402e}}
audio{{width:100%}}
footer{{text-align:center;font-size:0.85rem;color:#5a5548;padding:1.5rem 0 2.5rem;border-top:2px solid var(--paper)}}
footer a{{color:var(--teal-dark)}}
</style></head>
<body>
<header class="hero">
<img class="cover" src="cover.jpg" alt="עטיפת הפודקאסט {html.escape(show['title'])}">
<h1>{html.escape(show['title'])}</h1>
<p class="tagline">{html.escape(show.get('tagline', show['description']))}</p>
<p class="pitch">מיני-פודקאסט יומי בעברית: בכל פרק חמש דקות - מושג אחד מעולמות הטכנולוגיה, הסוכנים והבילדרות, מוסבר בגובה העיניים, בזמן שלוקח לשתות קפה.</p>
<p class="disclosure">התוכנית מופקת ומוגשת באמצעות בינה מלאכותית וקול סינתטי.</p>
</header>
<div class="wrap">
<details class="subscribe" id="subscribe">
<summary>איך מנויים?</summary>
<a class="btn" href="feed.xml">מנוי ב-RSS</a>
<a class="btn rss" href="https://podcasts.apple.com" target="_blank" rel="noopener">Apple Podcasts</a>
<a class="btn" href="https://patreon.com/in_agent_lingo_heb" target="_blank" rel="noopener">Patreon</a>
<a class="btn rss" href="https://www.linkedin.com/in/eshel-karp" target="_blank" rel="noopener">LinkedIn</a>
<p style="margin:0.9rem 0 0.2rem"><b>מנוי ב-Apple Podcasts לפי כתובת:</b></p>
<ol>
<li>ב-Mac: באפליקציית Podcasts לפתוח את התפריט <b>File</b> ולבחור <b>Add Show by URL</b> (האזנה לתוכנית לפי כתובת)</li>
<li>ב-iPhone: להדביק את הכתובת באפליקציית פודקאסטים כמו Overcast או Pocket Casts, או לסנכרן מה-Mac</li>
<li>להדביק את כתובת ההזנה:</li>
</ol>
<span class="feed-url">{BASE}/feed.xml</span>
</details>
<section class="suggest" id="suggest">
<h2>תיבת הצעות</h2>
<p class="hint">יש מושג שבא לכם שנסביר בפרק? כתבו כאן - כל הצעה נקראת.</p>
<textarea id="s-text" maxlength="1000" placeholder="למשל: מה זה בעצם סוכן AI?"></textarea>
<input class="nick" id="s-nick" maxlength="60" placeholder="שם או כינוי (לא חובה)">
<input class="hp" id="s-hp" type="text" tabindex="-1" autocomplete="off" aria-hidden="true">
<button class="btn" id="s-send" type="button">שליחת הצעה</button>
<p class="s-msg" id="s-msg"></p>
</section>
<section class="eps">
<h2>פרקים</h2>
<ol class="episodes">{rows}</ol>
</section>
</div>
<footer>
<p>{html.escape(show['title'])} · <a href="feed.xml">RSS</a> · <a href="https://patreon.com/in_agent_lingo_heb">Patreon</a> · <a href="https://www.linkedin.com/in/eshel-karp">LinkedIn</a></p>
</footer>
<script>
document.addEventListener('click',function(ev){{
  var b=ev.target.closest('.copy-btn'); if(!b) return;
  var c=document.getElementById(b.dataset.target); if(!c) return;
  if(navigator.clipboard) navigator.clipboard.writeText(c.innerText);
  b.textContent='הועתק!'; setTimeout(function(){{b.textContent='העתקה'}},2000);
}});
document.getElementById('s-send').addEventListener('click',function(){{
  var msg=document.getElementById('s-msg'), btn=document.getElementById('s-send');
  var text=document.getElementById('s-text').value.trim();
  if(text.length<3){{msg.className='s-msg err';msg.textContent='כותבים קודם הצעה קטנה';return}}
  btn.disabled=true; msg.className='s-msg'; msg.textContent='שולח...';
  fetch('https://bilshon-suggest.vercel.app/api/suggest',{{method:'POST',headers:{{'Content-Type':'application/json'}},
    body:JSON.stringify({{text:text,nick:document.getElementById('s-nick').value.trim(),hp:document.getElementById('s-hp').value}})}})
  .then(function(r){{return r.json()}}).then(function(d){{
    if(d.ok){{msg.className='s-msg ok';msg.textContent='תודה! ההצעה נקלטה';document.getElementById('s-text').value='';document.getElementById('s-nick').value=''}}
    else{{msg.className='s-msg err';msg.textContent='משהו לא עבד - נסו שוב'}}
    btn.disabled=false;
  }}).catch(function(){{msg.className='s-msg err';msg.textContent='אין חיבור - נסו שוב בעוד רגע';btn.disabled=false}});
}});
</script></body></html>"""
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
