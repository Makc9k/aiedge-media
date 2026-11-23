# tools

`render_week_template.py` — Pillow renderer for a week of AI Edge posts (1080×1350).
Brand: bg #070B18, cyan #22D3EE, violet #A78BFA, fonts Inter (Black/SemiBold/Medium) + DejaVu Sans Mono for prompt cards.
Handle on images: @aiedge.prompts.

To make a new week: copy the script, change the 7 post blocks (tag, title, body, prompt card),
set the output folder to `posts/<year>-w<ISO week>/`, run it, check the contact sheet, commit, push.
Rules: only real, checkable prompting techniques; no invented statistics; no income promises.
