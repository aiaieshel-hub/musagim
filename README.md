# בלשון סוכנים (Bilshon Sochnim)

Personal Hebrew mini-podcast. Static site + RSS feed served by GitHub Pages.

- Feed: https://aiaieshel-hub.github.io/musagim/feed.xml
- Home: https://aiaieshel-hub.github.io/musagim/

## Publishing a new episode (daily)

1. Convert the voice note: `ffmpeg -i epXXX.ogg -codec:a libmp3lame -b:a 96k -ac 1 -ar 44100 episodes/epXXX-slug.mp3`
2. Get duration (`ffprobe -show_entries format=duration -of csv=p=0`) and byte size (`stat -c%s`).
3. Append the episode to `episodes.json` (num, file, title, RFC-822 date with +0300, duration seconds, size bytes, summary).
4. Run `python3 build_feed.py` - it regenerates `feed.xml` + `index.html` and verifies sizes.
5. Commit + push. Pages redeploys in ~1 minute.

Git access: fine-grained PAT `musagim-feed-publisher` (vault: "GitHub PAT - musagim repo publisher", expires 2026-12-18, Contents RW on this repo only).
Web uploads via github.com rename staged files with numeric prefixes - use git, or fix names after.

Note: each episode entry must include a `prompt` field (the episode's apply-prompt, Hebrew). It renders as a copyable 'פרומפט להטמעה' box in the episode card on the site and is also appended to the summary.

## Draft / re-publish workflow (approved 2026-09-19)
Episodes carry a `status` field in episodes.json: `published` or `draft`.
Only `published` episodes are written to feed.xml and index.html (draft mp3s/covers stay in episodes/, unlisted).
Re-publish rule: an episode returns to `published` only after the user writes his application notes for it in the learning system.
The apply-prompt rewrite (new 8-part brief + 6/6 check standard) is NOT synced to the site until the user approves the 5 review batches.

## Sourcing rule (user instruction, 2026-09-22)
"בלי אוטוטיוזדיי. משם רק נושאים והשראה. למידה אתה מביא ממקורות פתוחים."
AutoTuesday may be used for topics and inspiration only. Learning content for episodes must come from open sources. Applies to all future episode production.
