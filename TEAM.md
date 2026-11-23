# AI Edge content team — how the agents work together

Account: Instagram **@aiedge.prompts** + Threads (same account). Niche: practical AI prompts & workflows, English, US audience.
Scheduler: Metricool, brand/blogId **8307772**, timezone **Europe/Kiev**. Personal account **maks_aurelius must never be touched**.
Owner notes (Ukrainian) live in the Obsidian vault on the owner's PC: `obsidian/Etsy/...`.

## Weekly pipeline (all times Europe/Kyiv)

| When | Agent | Reads | Writes |
|---|---|---|---|
| Sat 11:52 | 🔎 Trendwatcher | web, (optional) Instagram in the built-in browser, last swipe files | `obsidian/Etsy/Тренди/YYYY-MM-DD Тренди.md` |
| Sun 11:44 | Niche scout (products) | web | `obsidian/Etsy/Розвідка/...` |
| Sun 12:23 | 📊 Analyst | Metricool analytics | `obsidian/Etsy/Статистика/YYYY-MM-DD AI Edge.md` |
| Sun 13:07 | 🎬 Creative director | trends + analytics + product/campaign notes + past weeks | `plans/YYYY-wNN.json` (repo) + `obsidian/Etsy/Контент-план/YYYY-wNN.md` |
| Sun 14:17 | 🎨 Content maker | `plans/YYYY-wNN.json` | `posts/YYYY-wNN/*` + `posts/YYYY-wNN/manifest.json` (repo) |
| Sun 15:43 | 📅 Poster | `posts/YYYY-wNN/manifest.json` | Metricool schedule + `obsidian/Etsy/Сторінки/Тиждень NN — AI Edge.md` |

If an upstream file is missing, the agent does a reasonable version of that step itself and says so in its report.
Week NN = ISO week of the first publication day. The posting week runs from the day after the last scheduled post.

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

## Tools in this repo
- `tools/motion/engine.py` — animation engine (Canvas, easing, cards, chat window, bubbles, check/cross, underline, render()).
- `tools/motion/launch_v2.py` — reference scenes: `s1` chat/email demo, `s2` chaos→plan sorting, `s3` weak→strong rewrite,
  `s4` product reveal, `s5` CTA. Copy patterns from here.
- `tools/render_week_template.py` — static 1080×1350 post template.
- `tools/motion/assets/` — page renders of the Starter 10 PDF.
