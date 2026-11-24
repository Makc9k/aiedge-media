# -*- coding: utf-8 -*-
"""Reel 27.11 — Starter #09 hard decision (Black Friday laptop). Structure of ref-20261123-02:
question hook with objects popping in, one input typed, then several outputs revealed one after another."""
from common import *

PROMPT = ("I'm deciding between [A] buying the discounted laptop on Black Friday now ($200 off) and [B] keeping my "
          "5-year-old laptop and waiting. What matters most to me: fast photo exports for my side gig, a tight budget, "
          "not wasting money. Compare them in a table against my priorities, list what I might be overlooking, and ask "
          "me 3 questions that would make the choice clearer.")
TABLE = [("Fast exports", ("✓ big jump", GREEN), ("✗ stays slow", RED)),
         ("Tight budget", ("✗ money out now", RED), ("✓ no spend", GREEN)),
         ("Not wasting money", ("? only if $200 off is a real discount", AMBER), ("? old laptop may fail at a bad time", AMBER))]
MISSING = [("More RAM or an SSD in your old laptop might fix exports for less", "🔧"),
           ("Check the price history: is “$200 off” a real discount?", "📉"),
           ("Return window and warranty length", "🧾"),
           ("Software or accessories you'd also need to buy", "🔌")]
QUEST = ["How long does one export take now, and what does that time cost your gig?",
         "Can you pay for it without going into debt?",
         "What specs does your editing app actually recommend?"]
T_CHAT, T_TAB, T_MISS, T_Q, T_CTA, END = 2.0, 5.0, 9.0, 12.0, 14.3, 16.0
CELL_T = [T_TAB + .45 + i * .5 for i in range(6)]
MISS_T = [T_MISS + .35 + i * .6 for i in range(4)]
Q_T = [T_Q + .3 + i * .55 for i in range(3)]


def table(im, t):
    f = font("bold", 44); fh = font("black", 46)
    cols = [(60, 300), (370, 320), (700, 320)]
    y = 700
    d = ImageDraw.Draw(im)
    for (x, w), hd, col in zip(cols, ["Priority", "A: buy now", "B: wait"], [WHITE, CY, VIO]):
        d.rounded_rectangle((x, y, x + w - 10, y + 84), 22, fill=mix(col, BG, .55) if col != WHITE else (40, 48, 90))
        d.text((x + 22, y + 14), hd, font=fh, fill=WHITE)
    y += 100
    for r, (pri, a, b) in enumerate(TABLE):
        hh = max(block_h(pri, f, 260), block_h(a[0], f, 270), block_h(b[0], f, 270)) + 40
        d.rounded_rectangle((60, y, 350, y + hh), 22, fill=(32, 40, 84))
        block(im, 82, y + 20, 260, pri, f, WHITE)
        for j, (txt_, col) in enumerate([a, b]):
            ci = r * 2 + j; x, w = cols[j + 1]
            if t < CELL_T[ci]: continue
            k = pop(t, CELL_T[ci], .3)
            flash = 1 - prog(t, CELL_T[ci], .35)
            cell = panel(w - 10, hh, fill=mix(mix(col, BG, .45), WHITE, .5 * flash), r=22, border=col, bw=4, glow=col, glow_r=14, shadow=False)
            put(im, cell, x + (w - 10) / 2, y + hh / 2, scale=k)
            if k > .8:
                block(im, x + 20, y + 20, w - 50, txt_, f, WHITE)
        y += hh + 16


def frame(t):
    im = bg(t, a=CY if t < T_MISS else PINK, b=PINK if t < T_CHAT else ((37, 99, 235) if T_MISS <= t < T_CTA else VIO), c=AMBER if t < T_CHAT else None)
    if t < T_CHAT:
        put(im, txt("Buy the Black Friday", 84, w="black", glow=PINK, glow_r=16, glow_a=.5), W / 2, 380, scale=slam(t, 0, .2))
        put(im, txt("deal… or not?", 110, grad=(AMBER, PINK), glow=AMBER, glow_r=20, glow_a=.6), W / 2, 500, scale=slam(t, .3, .2))
        put(im, emoji("💻", 380), W / 2, 960 + 18 * math.sin(t * 5), scale=pop(t, .45, .45))
        put(im, chip("$200 OFF", 72, fg=WHITE, bg=RED, glow=RED, padx=36), 780, 760, scale=pop(t, .8, .35), rot=-12)
        put(im, chip("A  buy now", 54, fg=BG, bg=CY, glow=CY), 290, 1330, scale=pop(t, 1.1, .3))
        put(im, chip("B  keep the old one", 54, fg=BG, bg=VIO, glow=VIO), 700, 1450, scale=pop(t, 1.35, .3))
    elif t < T_TAB:
        put(im, chip("ONE PROMPT", 56, fg=BG, bg=CY, glow=CY), W / 2, 360, scale=pop(t, T_CHAT, .3))
        x0, y0, x1, y1 = chat_frame(im, 40, 470, 1000, 1170)
        n = (t - T_CHAT - .1) * 160
        bubble(im, x0 + 20, y0, x1 - x0 - 20, PROMPT, font("med", 44), "user", chars=max(0, n), t=t,)
    elif t < T_MISS:
        put(im, txt("Table vs YOUR priorities", 70, grad=(CY, VIO), glow=CY, glow_r=16, glow_a=.6), W / 2, 420, scale=slam(t, T_TAB, .2))
        put(im, chip("1", 56, fg=BG, bg=CY, glow=CY), W / 2, 570, scale=pop(t, T_TAB + .1, .3))
        table(im, t)
    elif t < T_Q:
        put(im, txt("What you might be missing", 68, grad=(VIO, PINK), glow=VIO, glow_r=16, glow_a=.6), W / 2, 420, scale=slam(t, T_MISS, .2))
        put(im, chip("2", 56, fg=BG, bg=VIO, glow=VIO), W / 2, 570, scale=pop(t, T_MISS + .1, .3))
        y = 680
        for i, (m, ic) in enumerate(MISSING):
            sp = wcard(m, 960, VIO, icon=ic)
            if t >= MISS_T[i]:
                put_panel(im, sp, 60 + 500 * (1 - ease(prog(t, MISS_T[i], .18))), y, alpha=prog(t, MISS_T[i], .1))
            y += sp.info["h"] + 26
    elif t < T_CTA:
        put(im, txt("3 questions back to you", 70, grad=(CY, GREEN), glow=CY, glow_r=16, glow_a=.6), W / 2, 420, scale=slam(t, T_Q, .2))
        put(im, chip("3", 56, fg=BG, bg=GREEN, glow=GREEN), W / 2, 570, scale=pop(t, T_Q + .1, .3))
        y = 690
        for i, q in enumerate(QUEST):
            sp = wcard(q, 960, CY, num=i + 1, size=48)
            if t >= Q_T[i]:
                put(im, sp, W / 2, y + sp.info["h"] / 2, scale=pop(t, Q_T[i], .3))
            y += sp.info["h"] + 34
        put(im, txt("The call is still yours.", 56, WHITE, w="xb"), W / 2, 1560, alpha=prog(t, Q_T[2] + .4, .3))
    else:
        cta(im, t, T_CTA, tag="PROMPT #09 · HARD DECISION", sub="Works for any A-or-B choice")
        for i, (c_, col) in enumerate([("Table", CY), ("Blind spots", VIO), ("3 questions", GREEN)]):
            put(im, chip(c_, 44, fg=BG, bg=col, glow=col), 215 + i * 325, 1330, scale=pop(t, T_CTA + 1.0 + i * .12, .3))
    return im


BEATS = [0, .3, .45, .8, 1.1, 1.35, T_CHAT, 3.5, T_TAB] + CELL_T + [T_MISS] + MISS_T + [T_Q] + Q_T + [T_CTA, T_CTA + .35, T_CTA + .65]
FLASH = [T_CHAT, T_TAB, T_MISS, T_Q, T_CTA]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        stills(frame, [1.6, 4.0, 8.6, 11.8, 13.9, 15.6], "/tmp/r3_stills.jpg")
    else:
        render(os.path.join(OUT, "r3_1127_blackfriday_decision.mp4"), frame, END, BEATS, FLASH, shake=[.8])
