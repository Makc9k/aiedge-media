# -*- coding: utf-8 -*-
"""Reel 29.11 — Starter #08 dinners + shopping list. Structure of ref-20261123-01 (@tech.bit0):
'Stop guessing…' + the finished bright result card first, then the input, then the card builds, then a 2nd output."""
from common import *

SEGS = ["Create a 5-day dinner plan for ", ("2 people", CY), ". Budget: ", ("$70", GREEN), ". Time per meal: max ",
        ("30 minutes", AMBER), ". We don't eat: ", ("pork, mushrooms", PINK), ". Then give me one shopping list grouped by store section."]
DAYS = [("MON", "Sheet-pan lemon chicken", "30", "🍋"), ("TUE", "Black bean tacos", "20", "🌮"),
        ("WED", "Garlic butter shrimp pasta", "20", "🍤"), ("THU", "One-pot turkey chili", "30", "🌶️"),
        ("FRI", "Teriyaki salmon rice bowls", "25", "🐟")]
SHOP = [("Produce", "lemons · potatoes · green beans · onions · garlic · spinach · broccoli · avocado · limes · cilantro", GREEN, "🥦"),
        ("Meat & seafood", "chicken thighs · ground turkey · salmon", RED, "🍗"),
        ("Frozen", "shrimp · corn", CY, "🧊"),
        ("Pantry", "black beans · kidney beans · diced tomatoes · spaghetti · rice · teriyaki sauce · chili powder · tortillas", AMBER, "🥫"),
        ("Dairy", "butter · shredded cheese · sour cream", VIO, "🧈")]
T_CHAT, T_BUILD, T_SHOP, T_CTA, END = 1.5, 4.1, 9.1, 13.0, 15.0
TILE_T = [T_BUILD + .35 + i * .9 for i in range(5)]
SHOP_T = [T_SHOP + .3 + i * .6 for i in range(5)]


def tile(day, dish, mins, ic, w=960, h=172, col=CY):
    k = ("tile", day, dish, mins)
    c = kit_cache()
    if k in c: return c[k]
    p = panel(w, h, fill=(20, 30, 70), r=36, border=(col, VIO), bw=4, glow=(40, 120, 200), glow_r=16, shadow=False).copy()
    pp = p.info["pad"]; d = ImageDraw.Draw(p)
    e = emoji(ic, 104); p.paste(e, (pp + 28, pp + (h - e.height) // 2), e)
    d.text((pp + 160, pp + 26), day, font=font("black", 40), fill=CY)
    d.text((pp + 160, pp + 80), dish, font=font("xb", 48), fill=WHITE)
    bw = 150
    d.rounded_rectangle((pp + w - bw - 24, pp + 26, pp + w - 24, pp + 86), 30, fill=GREEN)
    s = mins + " min"; f = font("black", 40)
    d.text((pp + w - 24 - bw / 2 - d.textlength(s, font=f) / 2, pp + 32), s, font=f, fill=BG)
    p.info["pad"] = pp
    c[k] = p
    return p


def guide(im, t, start, y0=560, slam_in=False):
    """The 5-day guide card; tiles appear at TILE_T (or all at once when slam_in)."""
    put(im, txt("5-Day Dinner Guide", 74, grad=(AMBER, PINK), glow=AMBER, glow_r=18, glow_a=.6), W / 2, y0, scale=slam(t, start, .2) if slam_in else 1)
    for i, (dy, dish, m, ic) in enumerate(DAYS):
        st = start + .05 * i if slam_in else TILE_T[i]
        if t < st: continue
        sp = tile(dy, dish, m, ic)
        put(im, sp, W / 2, y0 + 150 + i * 196, scale=pop(t, st, .3))


def fields(im, t, s):
    """Prompt with bracket fields filled one after another."""
    f = font("med", 46); d = ImageDraw.Draw(im)
    x0, y, x, width, step = 90, 760, 90, 900, 64
    for gi, seg in enumerate(SEGS):
        if isinstance(seg, str):
            for wd in seg.split(" "):
                if not wd: x += d.textlength(" ", font=f); continue
                ww = d.textlength(wd + " ", font=f)
                if x + ww > x0 + width: x = x0; y += step
                d.text((x, y), wd, font=f, fill=(225, 240, 255)); x += ww
        else:
            val, col = seg; idx = gi // 2
            st = s + .35 + idx * .5
            n = int(clamp((t - st) / .3) * len(val))
            shown = val[:n] if n > 0 else "     "
            ww = d.textlength(shown, font=font("xb", 46)) + 30
            if x + ww > x0 + width: x = x0; y += step
            box_col = col if n > 0 else (60, 70, 110)
            d.rounded_rectangle((x, y - 4, x + ww, y + 56), 14, fill=mix(box_col, BG, .25) if n > 0 else (40, 50, 90), outline=box_col, width=3)
            d.text((x + 15, y), shown, font=font("xb", 46), fill=BG if n > 0 else WHITE)
            x += ww + 12


_pb = []
def print_bottom(y):
    if not _pb: _pb.append(y); print("shop bottom", y)


def frame(t):
    im = bg(t, a=AMBER if t < T_CHAT or t >= T_BUILD else CY, b=PINK if t < T_SHOP else GREEN, c=VIO)
    if t < T_CHAT:
        put(im, txt("Stop guessing", 96, w="black", glow=PINK, glow_r=16, glow_a=.5), W / 2, 300, scale=slam(t, 0, .18))
        put(im, txt("what's for dinner", 84, grad=(AMBER, PINK), glow=AMBER, glow_r=16, glow_a=.5), W / 2, 410, scale=slam(t, .15, .18))
        guide(im, t, 0.05, y0=560, slam_in=True)
    elif t < T_BUILD:
        put(im, txt("Fill 4 brackets", 92, grad=(CY, GREEN), glow=CY, glow_r=18, glow_a=.6), W / 2, 380, scale=slam(t, T_CHAT, .2))
        put(im, chip("PROMPT #08", 50, fg=BG, bg=AMBER, glow=AMBER), W / 2, 500, scale=pop(t, T_CHAT + .1, .3))
        x0, y0, x1, y1 = chat_frame(im, 40, 600, 1000, 640)
        fields(im, t, T_CHAT)
    elif t < T_SHOP:
        put(im, txt("5 dinners, ≤30 min each", 70, w="black", glow=CY, glow_r=14, glow_a=.5), W / 2, 330, scale=slam(t, T_BUILD, .2))
        guide(im, t, T_BUILD, y0=470)
    elif t < T_CTA:
        put(im, txt("1 shopping list, by aisle", 70, w="black", glow=GREEN, glow_r=14, glow_a=.5), W / 2, 330, scale=slam(t, T_SHOP, .2))
        y = 420
        for i, (sec, items, col, ic) in enumerate(SHOP):
            sp = wcard(items, 960, col, icon=ic, size=44, fill_k=.6, pad=26)
            hd = chip(sec, 40, fg=BG, bg=col)
            if t >= SHOP_T[i]:
                k = ease(prog(t, SHOP_T[i], .2)); dx = 600 * (1 - k) * (1 if i % 2 else -1)
                put_panel(im, sp, 60 + dx, y + 34, alpha=prog(t, SHOP_T[i], .1))
                put_panel(im, hd, 90 + dx, y)
            y += sp.info["h"] + 34 + 20
        if t > SHOP_T[-1]: print_bottom(y)
    else:
        cta(im, t, T_CTA, tag="PROMPT #08 · DINNERS + LIST", sub="Save it for Sunday")
        put(im, emoji("🔖", 150), W / 2, 1330, scale=pop(t, T_CTA + .9, .35), rot=8 * math.sin(t * 6))
    return im


BEATS = [0, .15, T_CHAT] + [T_CHAT + .35 + i * .5 for i in range(4)] + [T_BUILD] + TILE_T + [T_SHOP] + SHOP_T + [T_CTA, T_CTA + .35, T_CTA + .65]
FLASH = [T_CHAT, T_BUILD, T_SHOP, T_CTA]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        stills(frame, [.8, 3.6, 8.6, 12.8, 13.4, 14.8], "/tmp/r4_stills.jpg")
    else:
        render(os.path.join(OUT, "r4_1129_dinner_plan.mp4"), frame, END, BEATS, FLASH)
