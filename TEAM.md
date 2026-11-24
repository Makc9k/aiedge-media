# AI Edge content team — how the agents work together

Account: Instagram **@aiedge.prompts** + Threads (same account). Niche: practical AI prompts & workflows, English, US audience.
Scheduler: Metricool, brand/blogId **8307772**, timezone **Europe/Kiev**. Personal account **maks_aurelius must never be touched**.
Owner notes (Ukrainian) live in the Obsidian vault on the owner's PC: `obsidian/Etsy/...`.

## Daily pipeline (all times Europe/Kyiv) — the team works EVERY day

**Schedule rule:** the owner's PC is on from ~09:00 during the day, so the whole chain runs 09:02–15:37. These times override any times written in an agent's own prompt.

**Daily quota per publishing day:** 1 Instagram Reel (18:00) + 3 Threads posts (15:30, 19:30, 22:30) + 2 stories (12:30, 12:35).
Each day the chain prepares the missing items for today (slots ≥2 h ahead) and fully for tomorrow.

| When | Agent | Reads | Writes |
|---|---|---|---|
| Daily 09:02 | 🔎 Scout | web, Reddit, Instagram/Threads/TikTok (view only), Buzzfy | `references/library.json`, `references/YYYY-MM-DD.md` (section «Для директора сьогодні»), `obsidian/Etsy/Тренди/` |
| Daily 09:47 | 📊 Analyst | Metricool, Buzzfy, Gumroad (view only) | `status/goal.json` progress, `obsidian/Etsy/Статистика/YYYY-MM-DD AI Edge.md` («Рекомендації для директора») |
| Daily 10:23 | 🎬 Creative director | scout + analyst + judge reports | `plans/daily/YYYY-MM-DD.json` (date = publish day) + `obsidian/Etsy/Контент-план/YYYY-MM-DD.md` |
| Daily 11:07 | 🎨 Content maker | `plans/daily/*.json` | `posts/daily/YYYY-MM-DD/*` + `manifest.json` |
| Daily 12:37 | 📅 Poster | `posts/daily/*/manifest.json` + Threads texts from plans | Metricool schedule + `obsidian/Etsy/Сторінки/Розклад AI Edge.md` |
| Daily 15:37 | ⚖️ Judge | everything changed in 24 h + tomorrow's quota in Metricool | `obsidian/Etsy/Сторінки/Суддя/YYYY-MM-DD.md` |
| Sun 11:44 | 🧭 Niche scout (products) | web | `obsidian/Etsy/Розвідка/...` |

The director must apply the latest analyst «Рекомендації для директора» and judge «Для креативного директора».
If an upstream file is missing, the agent waits briefly (git pull every 5 min), then does a reasonable version itself and marks ⚠️.
Threads posts: plain text ≤500 chars (optionally 1 image); 3 different types per day (useful prompt/tip with real result · opinion/question that invites replies · mini before/after or list); only one of the three carries the Starter 10 link.

## Transition 24–30 Nov (old content → new)
- Posts scheduled in Metricool for 24–30.11 BEFORE 2026-11-23 21:00 (media from `campaign/` or `posts/2026-w48/`) are **OLD STYLE** (owner rejected them).
- Director: for each day 24–30.11 take the Reel/carousel from `plans/2026-w48-v2.json` (already planned with breakdowns) into `plans/daily/YYYY-MM-DD.json`; add the 3 Threads posts and stories.
- Poster: when the new item for a slot is ready, move the OLD-STYLE post in that slot to draft (`updateScheduledPost` draft: true, never delete), then schedule the new one. If the new item is not ready, leave the old one.

## Audio follows the reference (owner's rule 2026-11-24)
- Scout: for every Reel/TikTok reference add `"audio"`: `trending_song` (name it if visible) / `voiceover` / `original_sound` / `music_bed` / `no_audio`, plus `"audio_note"` (what the sound does: beat drops on the reveal, voice explains the prompt, etc.). Only what you actually see/hear on the page; else `null`.
- Director: copy the reference's audio into the plan (`breakdown.audio`, and for songs a search term in `audio_search`). Timing of cuts should match the beat when the reference does that.
- Maker / Poster implement it:
  - `trending_song` → Poster attaches Instagram library music in Metricool: `instagramData.audioConfiguration = {"audioId": "<numeric id or exact song title>"}` (Reels only). If Metricool rejects it (account not connected via a Facebook Page) → schedule without it, mark ⚠️ and write the exact error in the report. Never bake copyrighted songs into the file.
  - `voiceover` → ElevenLabs is ALLOWED (owner, 2026-11-24) through the local voice worker on the owner's PC — never open or print `elevenlabs_key.txt`.
    1. Write a job file into the connected folder `C:\ft_userdata\viral\tts_queue\<id>.json` (device tools; in device_bash it is `$HOME/mnt/ft_userdata/viral/tts_queue/`): `{"id": "<date>_reel", "text": "<script, English, natural spoken style>", "voice": "<optional name from tts_out/_voices.json>", "lang": "en"}`.
    2. Poll every 30 s (max 10 min) for `tts_out/<id>.json`. If `ok` is true, use `tts_out/<id>.mp3` (copy it into the cloud workspace with device_stage_files) and cut the video to the voice. If `fallback: true`, the free edge-tts voice was used — still OK, but say so in the report.
    3. If nothing appears in 10 min, the worker is not running (PC off or `start_tts.cmd` not started): ship with big on-screen text instead and mark ⚠️.
    Keep the voice consistent across Reels. **Brand voice: `Liam - Energetic, Social Media Creator`** (american male, social media) — pass it as `"voice"` in every job. Worker verified working 2026-11-24 (engine elevenlabs, model eleven_multilingual_v2).
  - `music_bed` → bake a track into the file only if its licence for commercial social use is verified; put the source URL + licence in `manifest.json`. If not verifiable → no music.
  - Stories: audio can only be baked into the file (no library music via API).

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

## Mission Control site (`hq/`)
One-off missions (extra runs ordered by the owner) are listed in `status/missions.json` and shown as «Current mission» with live status. Your log line marks your step done (matched by your agent name, time ≥ step start). The last agent of a mission sets `"active": null` when the mission is complete.
Public dashboard at https://makc9k.github.io/aiedge-media/hq/ reads `status/log.md`, `status/agents.json`, `status/goal.json` and `references/library.json` live.
The 📊 Analyst appends a progress entry to `status/goal.json` every Sunday (same numbers as «🎯 Ціль місяця»): `{"date","ig","threads","followers_gain","leads","sales"}`. If you add an agent, add it to `status/agents.json`.

**Director: mandatory items for week 2026-w49** (owner's request):
1. (POSTPONED until real progress is visible on the site) Reel «I built 7 AI agents that run my Instagram»: screen recording of the live site (pipeline animation → agent cards with countdowns → reference wall → goal rings). Only real numbers from the site, no invented results. Hook in first 2 s. CTA: comment PROMPTS / free Starter 10.
2. Weekly series «Week N: +X followers, Y downloads, Z sales» built from `status/goal.json` (real numbers only, even if small).

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

## What sells (owner feedback 2026-11-23: "primitive and grey, I wouldn't buy from this")
- Every Reel = ONE prompt that gives the viewer a vivid, personal result in ~10 s (model: @tech.bit0 selfie → glasses/colors/haircut, 36×). About the viewer, not about us.
- Bright, high-contrast frames; no grey fog/washed-out looks; a visual "hit" (zoom-punch / reveal) every 1–2 s; result shown in the first 3 s.
- Do NOT post content about our agents/site until it shows real progress (e.g. +50 followers or first sales). Empty dashboards = anti-proof.
- Higgsfield (AI-generated cinematic shots + voice) will be connected after the owner's payday; until then use real screen captures of prompt results + bright brand motion.

## Reference-driven production (owner's rule: references decide the format, templates only decide the colors)
Templates/engine give **brand style only** (colors, fonts, safe zones). The **structure of every post comes from its reference**.
1. Director: for each post, open the reference (`source_trend` → `references/library.json` → url) and write a `breakdown` in the plan:
   `{"hook_seconds": 1.5, "hook_mechanic": "…", "shots": [{"t": "0-1.5", "what": "…", "text_on_screen": "…"}], "cut_rhythm": "cut every ~1 s",
   "visual_device": "screen recording | split before/after | chat demo | meme caption | list reveal | face/hand + overlay", "payoff_at": "…", "cta_style": "…"}`.
   Use `social-media-skills:viral-reverse-engineering` for the breakdown. If the reference can't be opened, pick another one — no breakdown, no post.
2. Maker: rebuild **the same structure** (timing, number of shots, rhythm, where text sits, the visual device) with our own content and brand.
   If the engine lacks that device (e.g. meme caption over screen recording, fog/blur transition, zoom-punch on a word) — add a new scene to `tools/motion/` first.
   Real screen recordings are allowed and preferred when the reference uses them: record our own pages (Mission Control site, Gumroad pages) with Playwright screencast (see `tools/motion/record_site.py`).
3. Variety check: in one week no two posts may share the same `visual_device` + layout. The Judge flags violations.
4. In `manifest.json` each item gets `"reference_match": "what we copied structurally / what we changed"`.

## Plugins & connectors — who uses what
Verified 2026-11-23 (status/plugin_check.md): scheduled runs DO have humanizer, social-media-skills, marketing, buzzfy, virlo skills and apify/buzzfy/Metricool tools (no Virlo MCP server yet). Use a tool only if it is actually available in your session (check first); otherwise fall back to web search / the
built-in browser and say so in your report. **Apify is switched OFF by the owner (2026-11-23): do not use it.** Max ~1 paid Virlo run per agent run once Virlo is connected.

| Agent | Primary tools |
|---|---|
| 🔎 Scout | **Virlo** (`virlo`, `trend-scout`, `creator-deep-dive`; rank by weighted virality ln(views/followers)×ln(followers)), `social-media-skills:viral-reverse-engineering`, `trend-jacking` |
| 📊 Analyst | Metricool, **Buzzfy** `instagram-audit` / `reel-checkup`, `social-media-skills:analytics-and-reporting`, `marketing:performance-report` |
| 🎬 Creative director | `virlo:short-form-trend-research`, `social-media-skills:batch-content-plan`, `content-pillars`, `hook-writer`, `campaign-and-launch-planning` |
| 🎨 Content maker | `social-media-skills:carousel-writer`, `reels-script`, `story-writer`, `before-after-and-transformation`, `instagram-reels-publishing`, `platform-specs-and-validation`, `humanizer` |
| 📅 Poster | Metricool, `social-media-skills:caption-writer`, `instagram-seo`, `threads-post`, `humanizer` |

## Verify before telling the owner (owner's standing rule)
Before giving Maksym any instruction, price, limit, menu path or claim about a tool/platform: check it first
(official help page, the tool's own response, or by looking at the screen in the built-in browser). If you could
not verify something, say so plainly ("не перевірено") instead of presenting it as fact. Never invent UI steps.

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

## 🔇 Silent browsing (all agents, added 2026-11-24)
The built-in browser runs on the owner's PC and its sound goes to his headphones. After EVERY page open/navigation in the browser (Instagram, Threads, TikTok, YouTube, Reddit, any page with media) immediately run javascript_tool:
`document.querySelectorAll('video,audio').forEach(m=>{m.muted=true;m.pause();}); new MutationObserver(()=>document.querySelectorAll('video,audio').forEach(m=>{m.muted=true;m.pause();})).observe(document.documentElement,{childList:true,subtree:true});`
Never play videos with sound. Read views/followers/hooks from page text or screenshots. Prefer WebFetch/search over the browser when it is enough.

## 🔊 Audio is mandatory (owner rule, 2026-11-24) — overrides any "silent AAC" / "no_audio" above
- EVERY Reel and EVERY story must have audible sound. `"audio": "no_audio"` is no longer allowed in plans; silent fallback is forbidden.
- Default when the reference sound is unknown or is a licensed song we can't use: brand voice **Liam** voiceover via the local TTS worker (job in `C:\ft_userdata\viral\tts_queue\`, result in `tts_out\`). Reel: voice reads the hook + key beats, cuts land on voice beats. Story: 1 short line (3–6 s) in Liam's voice.
- If the TTS worker does not answer in 10 min: do NOT ship silent. Mark ⚠️ in the panel and tell the poster to hold that item.
- Maker check before push: `ffmpeg -i file.mp4 -af volumedetect -f null -` → mean_volume must be above −35 dB. Write the value in manifest (`"mean_volume_db"`).
- Poster check before scheduling: same volumedetect on the file; if mean_volume ≤ −35 dB (silent) — do not schedule, mark ❌ for the maker.
