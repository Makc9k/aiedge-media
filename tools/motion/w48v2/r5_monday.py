# -*- coding: utf-8 -*-
"""Reel 30.11 — Starter #03 weekly plan. Structure of ref-20261123-06 ('X killed Y' cover: bold headline, one word
in red marker, crossed-out sticker, FREE badge; then motion-graphic explainer: central node + orbiting items,
word-by-word captions)."""
from common import *

PROMPT = ("Here is my to-do list. Sort it into: urgent, important, can wait, delete. Estimate the time for each item. "
          "Then build a Monday–Friday plan with a maximum of 4 hours of focused work per day.\n[paste your list]")
TASKS = ["electric bill", "client deck", "dentist", "14 emails", "gym x3", "fix bike", "mom's birthday", "garage",
         "contract", "LinkedIn"]
BUCKETS = [("URGENT", RED, [("electric bill", "10m"), ("client deck", "3h"), ("contract", "1h")]),
           ("IMPORTANT", VIO, [("14 emails", "1.5h"), ("mom's bday", "45m"), ("dentist call", "10m"), ("gym x3", "after work")]),
           ("CAN WAIT", CY, [("LinkedIn", "45m"), ("fix bike", "1h")]),
           ("DELETE / MOVE", PINK, [("garage → weekend", "")])]
WEEK = [("MON", 3.33, "3h 20m", "bill · client deck · dentist"), ("TUE", 2.5, "2h 30m", "contract · emails"),
        ("WED", 1.5, "1h 30m", "mom's birthday plan · LinkedIn"), ("THU", 1.0, "1h", "fix bike"),
        ("FRI", 0.0, "buffer", "anything that slipped")]
T_ORB, T_SORT, T_WEEK, T_CTA, END = 1.6, 4.1, 7.2, 11.2, 14.0
DAY_T = [T_WEEK + .4 + i * .6 for i in range(5)]
SLOT = {}
for bi, (_, _, items) in enumerate(BUCKETS):
    for ii, (nm, _) in enumerate(items): SLOT[nm] = (bi, ii)
ALIAS = {"electric bill": "electric bill", "client deck": "client deck", "dentist": "dentist call", "14 emails": "14 emails",
         "gym x3": "gym x3", "fix bike": "fix bike", "mom's birthday": "mom's bday", "garage": "garage → weekend",
         "contract": "contract", "LinkedIn": "LinkedIn"}


def sticky(t):
    k = ("sticky",)
    c = kit_cache()
    if k not in c:
        p = Image.new("RGBA", (360, 360), (0, 0, 0, 0)); d = ImageDraw.Draw(p)
        d.rectangle((10, 10, 350, 350), fill=(253, 224, 71))
        d.text((40, 40), "to-do.txt", font=font("black", 48), fill=INK)
        for i in range(5): d.line([(40, 130 + i * 44), (320 - (i % 2) * 70, 130 + i * 44)], fill=(120, 100, 20), width=8)
        c[k] = p
    return c[k]


def bucket_xy(bi):
    return (60 + (bi % 2) * 490, 540 + (bi // 2) * 500)


def frame(t):
    im = bg(t, a=CY, b=VIO, c=(37, 99, 235) if t < T_ORB else None)
    if t < T_ORB:
        put(im, chip("FREE PROMPT", 46, fg=BG, bg=GREEN, glow=GREEN), W / 2, 300, scale=pop(t, .05, .3))
        put(im, txt("AI killed your", 100, w="black", glow=CY, glow_r=14, glow_a=.4), W / 2, 440, scale=slam(t, 0, .18))
        put(im, txt("Monday", 150, grad=(CY, VIO), glow=CY, glow_r=22, glow_a=.6), W / 2, 590, scale=slam(t, .15, .18))
        put(im, txt("panic", 220, RED, w="anton", stroke=7, stroke_col=WHITE, glow=RED, glow_r=30, glow_a=.7), W / 2, 810, scale=slam(t, .35, .2), rot=-6)
        sh = 10 * math.sin(t * 40) * (1 if t > .7 else 0)
        put(im, sticky(t), W / 2 + sh, 1260, scale=pop(t, .55, .3), rot=7)
        k = ease(prog(t, .9, .25))
        if k > 0:
            d = ImageDraw.Draw(im)
            d.line([(370, 1090), (370 + 340 * k, 1090 + 340 * k)], fill=RED, width=26)
            if k > .5: d.line([(710, 1090), (710 - 340 * (k - .5) * 2, 1090 + 340 * (k - .5) * 2)], fill=RED, width=26)
    elif t < T_WEEK:
        sorting = t >= T_SORT
        put(im, txt("Paste the mess" if not sorting else "Sorted + timed", 92, grad=(CY, VIO) if not sorting else (GREEN, CY),
                    glow=CY, glow_r=18, glow_a=.6), W / 2, 380, scale=slam(t, T_SORT if sorting else T_ORB, .2))
        cx, cy = W / 2, 1050
        if sorting:
            for bi, (nm, col, items) in enumerate(BUCKETS):
                x, y = bucket_xy(bi)
                k = prog(t, T_SORT + bi * .1, .25)
                put_panel(im, panel(470, 475, fill=mix(col, BG, .72), r=34, border=col, bw=5, glow=col, glow_r=18, shadow=False), x, y, alpha=k)
                put(im, chip(nm, 40, fg=BG, bg=col), x + 235, y + 50, scale=pop(t, T_SORT + bi * .1, .3))
        node_k = 1 - prog(t, T_SORT, .3)
        if node_k > 0:
            r = 130 + 8 * math.sin(t * 8)
            put(im, panel(int(r * 2), int(r * 2), fill=CY, r=int(r), glow=CY, glow_r=40, shadow=False), cx, cy, scale=node_k * pop(t, T_ORB, .3))
            put(im, txt("AI", 110, BG, w="black"), cx, cy, scale=node_k * pop(t, T_ORB, .3))
        for i, tk in enumerate(TASKS):
            ang = i / len(TASKS) * math.tau + (t - T_ORB) * 1.3
            ox, oy = cx + 320 * math.cos(ang), cy + 470 * math.sin(ang)
            nm = ALIAS[tk]; bi, ii = SLOT[nm]
            if sorting:
                kk = ease_io(prog(t, T_SORT + .3 + i * .1, .45))
                bx, by = bucket_xy(bi)
                tx, ty = bx + 235, by + 135 + ii * 88
                x, y = lerp(ox, tx, kk), lerp(oy, ty, kk)
                est = BUCKETS[bi][2][ii][1]
                label = nm + (f"  {est}" if est and kk >= 1 else "")
                col = BUCKETS[bi][1] if kk > .5 else WHITE
                sp = chip(label, 44, fg=BG, bg=col)
                if kk >= 1 and bi == 3:
                    sp = chip(label, 44, fg=BG, bg=PINK)
                put(im, sp, x, y)
            else:
                put(im, chip(tk, 44, fg=BG, bg=WHITE, glow=CY), ox, oy, scale=pop(t, T_ORB + .05 * i, .3))
    elif t < T_CTA:
        put(im, txt("Max 4 h focus a day", 86, grad=(GREEN, CY), glow=GREEN, glow_r=18, glow_a=.6), W / 2, 380, scale=slam(t, T_WEEK, .2))
        d = ImageDraw.Draw(im)
        x0, x1 = 230, 1000
        top = 520
        lim = x0 + (x1 - x0) * 1.0
        for i, (day, hrs, lab, what) in enumerate(WEEK):
            y = top + i * 214
            k = prog(t, DAY_T[i], .5)
            if t < DAY_T[i] - .05: continue
            put(im, chip(day, 46, fg=BG, bg=CY if i < 4 else AMBER), 125, y + 42, scale=pop(t, DAY_T[i], .25))
            d.rounded_rectangle((x0, y + 10, x1, y + 76), 33, fill=(28, 36, 80))
            frac = hrs / 4.0
            if hrs > 0:
                xe = x0 + (x1 - x0) * frac * ease(k)
                if xe > x0 + 66:
                    put_panel(im, panel(int(xe - x0), 66, fill=GREEN, r=33, glow=GREEN, glow_r=14, shadow=False), x0, y + 10)
            sp = txt(lab, 46, WHITE if hrs == 0 else BG, w="black")
            if k > .4: put(im, sp, x0 + 30 + sp.width / 2, y + 43)
            if k > .5: d.text((x0, y + 96), what, font=font("bold", 44), fill=(225, 235, 255))
        # 4h limit line
        for yy in range(500, top + 5 * 214 - 40, 36):
            d.line([(lim, yy), (lim, yy + 18)], fill=RED, width=6)
        put(im, chip("4 h", 40, fg=WHITE, bg=RED), lim - 40, 470 + 0 * 30, alpha=prog(t, T_WEEK + .2, .2))
    else:
        cta(im, t, T_CTA, tag="PROMPT #03 · WEEKLY PLAN", prompt=PROMPT, sub="You make the final call")
    if T_ORB <= t < T_CTA:
        if t < T_SORT: word_caption(im, t, T_ORB + .2, T_SORT, "10 tasks. Zero order.", y=1585, hl={"Zero": RED})
        elif t < T_WEEK: word_caption(im, t, T_SORT + .2, T_WEEK, "Sorted and timed in seconds.", y=1585, hl={"seconds": GREEN})
        else: word_caption(im, t, T_WEEK + .3, T_CTA, "Gym stays after work.", y=1585, hl={"Gym": AMBER})
    return im


BEATS = [0, .15, .35, .55, .9, T_ORB, 2.6, 3.4, T_SORT] + [T_SORT + .3 + i * .2 for i in range(0, 10, 2)] + [T_WEEK] + DAY_T + [T_CTA, T_CTA + .35, T_CTA + .65]
FLASH = [T_ORB, T_SORT, T_WEEK, T_CTA]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        stills(frame, [1.2, 3.0, 5.0, 6.8, 10.5, 13.8], "/tmp/r5_stills.jpg")
    else:
        render(os.path.join(OUT, "r5_1130_monday_plan.mp4"), frame, END, BEATS, FLASH, shake=[.4, .9])
