# AI Edge content team — how the agents work together

Account: Instagram **@aiedge.prompts** + Threads (same account). Niche: practical AI prompts & workflows, English, US audience.
Scheduler: Metricool, brand/blogId **8307772**, timezone **Europe/Kiev**. Personal account **maks_aurelius must never be touched**.
Owner notes (Ukrainian) live in the Obsidian vault on the owner's PC: `obsidian/Etsy/...`.

## Weekly pipeline (all times Europe/Kyiv)

| When | Agent | Reads | Writes |
|---|---|---|---|
| Daily 10:37 | 🔎 Trendwatcher (reference scout) | web, Reddit, Instagram/Threads/TikTok (built-in browser, view only) | `references/` + `obsidian/Etsy/Тренди/YYYY-MM-DD Тренди.md` |
| Sun 11:44 | Niche scout (products) | web | `obsidian/Etsy/Розвідка/...` |
| Sun 12:23 | 📊 Analyst | Metricool analytics | `obsidian/Etsy/Статистика/YYYY-MM-DD AI Edge.md` |
| Sun 13:07 | 🎬 Creative director | trends + analytics + product/campaign notes + past weeks | `plans/YYYY-wNN.json` (repo) + `obsidian/Etsy/Контент-план/YYYY-wNN.md` |
| Sun 14:17 | 🎨 Content maker | `plans/YYYY-wNN.json` | `posts/YYYY-wNN/*` + `posts/YYYY-wNN/manifest.json` (repo) |
| Sun 15:43 | 📅 Poster | `posts/YYYY-wNN/manifest.json` | Metricool schedule + `obsidian/Etsy/Сторінки/Тиждень NN — AI Edge.md` |

If an upstream file is missing, the agent does a reasonable version of that step itself and says so in its report.
Week NN = ISO week of the first publication day. The posting week runs from the day after the last scheduled post.

## Reference library: `references/` (built by the Trendwatcher, used by everyone)
The trendwatcher runs **every day** and looks for **small creators whose posts outperform their size** — the "outliers":
accounts with roughly 1k–50k followers in our niche (AI prompts, AI tools, ChatGPT tips, AI productivity, AI for work/career)
whose post/reel/thread got far more reach than usual for them (e.g. views ≥ 3× follower count, or ≥ 3× that creator's typical
post). Big accounts are only noted, not prioritised — small outliers prove the *format* works, not the audience size.

- `references/library.json` — one entry per reference:
  `{"id", "date_found", "platform", "url", "creator", "followers", "metric": "views|likes|comments", "value", "outlier_ratio",
    "format": "reel|carousel|single|thread|tiktok", "hook": "first line/slide, paraphrased", "benefit_shown": "before_after|chat_demo|list|comparison|story|other",
    "why_it_worked", "how_we_adapt", "used_in": []}`
  Numbers only if actually visible; otherwise `null` + `"metric_note": "not visible"`. Never invent metrics.
- `references/YYYY-MM-DD.md` — the day's finds, human-readable, with links.
- Store **links and our own analysis only** — never download or re-upload other people's images or videos.
- The creative director must cite reference `id`s in `source_trend`; the content maker opens those links before designing,
  and adds the post id to `used_in` once used.

## Control panel (where Maksym watches the team)
Every agent, at the end of each run, appends one line to `status/log.md` in this repo **and** to
`obsidian/Etsy/Сторінки/Пульт команди.md`:
`| YYYY-MM-DD HH:MM | <agent> | ✅/⚠️/❌ | what was done (1 line) | link to output |`

## Plan file: `plans/YYYY-wNN.json`
```json
{
  "week": "2026-w49", "theme": "…", "goal": "grow followers + drive Starter 10 downloads",
  "posts": [
    {"day": "2026-12-01", "time": "18:00", "format": "carousel|single|reel",
     "hook": "…", "slides": [{"type": "cover|before_after|chat_demo|steps|list|cta", "...": "..."}],
     "caption": "2–4 lines + 'Free Starter 10 → link in bio' + 3 hashtags", "alt": "…",
     "source_trend": "which trend/format inspired it (link)"}
  ],
  "stories": [
    {"day": "2026-12-01", "time": "12:30", "scenes": ["chat_demo:…", "before_after:…", "cta"], "seconds": 8}
  ]
}
```

## Manifest: `posts/YYYY-wNN/manifest.json`
```json
{"week": "2026-w49", "items": [
  {"kind": "post", "day": "2026-12-01", "time": "18:00", "media": ["posts/2026-w49/d1_1.jpg", "…"],
   "caption": "…", "alt": ["…"], "networks": ["instagram", "threads"]},
  {"kind": "story", "day": "2026-12-01", "time": "12:30", "media": ["posts/2026-w49/s1.mp4"], "networks": ["instagram"]}
]}
```
Media URL = `https://raw.githubusercontent.com/Makc9k/aiedge-media/main/<path>`.

## Creative rules (everyone)
1. **Show the benefit, don't describe it.** Every post/story demonstrates a transformation: before → after, chat demo with the real
   AI output, chaos → order, weak → strong. Text-only slides are allowed only as the hook or CTA.
2. Demos use **real outputs** (generate them, don't fake them) and keep the user's facts — never invent numbers, testimonials,
   sales counts, "studies show", or income promises.
3. Learn from trends = adapt **formats and hooks**, never copy someone's content, images or wording. Credit-free original work only.
4. Don't imitate real product UIs/brands (use the generic "AI chat" window from the engine). No celebrity photos.
5. Brand: bg #070B18, cyan #22D3EE, violet #A78BFA, green #34D399 (after), red #F87171 (before); Inter + DejaVu Sans Mono.
6. Stories: 1080×1920, important content between y=250 and y=1650; 5–12 s each; first second must already move.
   Feed: 1080×1350 (single or carousel up to 10 slides). Reels: 1080×1920, 15–40 s.
7. Every week: ≥4 posts carry the funnel line "Free Starter 10 → link in bio" (once the Gumroad link exists — check the
   product note `obsidian/Etsy/Продукти/AI Edge Prompt Pack.md`; before that use "Free prompt pack coming soon").
8. Check your own work: render contact sheets / preview frames and look at them before shipping. Fix overlaps and cut-off text.

## Voice: sound like a person, not a bot
If a **humanizer** skill is available in your session (e.g. `humanizer`, `humanize`, `humanize-ig`), run every caption,
hook and slide text through it before shipping. Either way, follow these rules — the creative director and the poster
both check them:
- Short, concrete sentences. Contractions (you'll, don't). Talk to one person ("you").
- One idea per post. Lead with the outcome the reader gets, not with how amazing AI is.
- Banned words/phrases: delve, unlock, unleash, elevate, game-changer, revolutionize, supercharge, seamless, robust,
  leverage, "in today's fast-paced world", "it's not just X, it's Y", "let's dive in", "here's the thing", "the best part?".
- No rule-of-three padding, no stacked adjectives, max 1 emoji per caption (0 is fine), max 1 em dash per caption.
- No fake urgency, no "everyone is talking about", no claims you can't show in the demo.
- Read it out loud test: if a friend wouldn't text it like that, rewrite it.

## Tools in this repo
- `tools/motion/engine.py` — animation engine (Canvas, easing, cards, chat window, bubbles, check/cross, underline, render()).
- `tools/motion/launch_v2.py` — reference scenes: `s1` chat/email demo, `s2` chaos→plan sorting, `s3` weak→strong rewrite,
  `s4` product reveal, `s5` CTA. Copy patterns from here.
- `tools/render_week_template.py` — static 1080×1350 post template.
- `tools/motion/assets/` — page renders of the Starter 10 PDF.
