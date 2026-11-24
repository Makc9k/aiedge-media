# -*- coding: utf-8 -*-
"""Shared bits for week 2026-w48 v2 reels/stories (built on kit.py)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from kit import *

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "..", "posts", "2026-w48-v2")


def header(im, t, s, text, size=76, grad=(CY, VIO), glow=CY, y=600, d=.3):
    """Section header that slams in."""
    if t < s: return
    put(im, txt(text, size, grad=grad, glow=glow, glow_r=20, glow_a=.7), W / 2, y, scale=slam(t, s, d), alpha=prog(t, s, .12))


def label(im, t, s, text, y, size=50, fg=INK, bg=CY):
    if t < s: return
    sp = chip(text, size, fg=fg, bg=bg, glow=bg)
    put(im, sp, W / 2, y, scale=pop(t, s, .3))


def cta(im, t, s, tag=None, prompt=None, line2="link in bio", sub=None):
    """End card. tag = 'PROMPT #10', prompt = text shown in a card (optional)."""
    lt = t - s
    if lt < 0: return
    y = 300
    if tag:
        put(im, chip(tag, 46, fg=BG, bg=AMBER, glow=AMBER), W / 2, y + 40, scale=pop(t, s, .3)); y += 120
    if prompt:
        f = font("sb", 44); hh = block_h(prompt, f, 840, 1.28) + 70
        sp = panel(960, hh, fill=(14, 20, 50), r=36, border=(CY, VIO), bw=4, glow=(60, 80, 200), glow_r=24)
        k = ease(prog(t, s + .1, .3))
        put_panel(im, sp, 60, y + 60 * (1 - k), alpha=k)
        if k > .5:
            block(im, 120, y + 35 + 60 * (1 - k), 840, prompt, f, (230, 245, 255), 1.28)
        y += hh + 70
    else:
        y += 160
    put(im, txt("Free Starter 10", 108, grad=(CY, VIO), glow=CY, glow_r=26, glow_a=.8), W / 2, y + 70,
        scale=slam(t, s + .35, .25), alpha=prog(t, s + .35, .1))
    put(im, chip("→  " + line2, 58, fg=BG, bg=GREEN, glow=GREEN, padx=40, pady=18), W / 2, y + 220, scale=pop(t, s + .65, .35))
    if sub:
        put(im, txt(sub, 46, (210, 225, 255), w="sb"), W / 2, y + 340, alpha=prog(t, s + .9, .25))
    put(im, txt("@aiedge.prompts", 50, WHITE, w="bold", glow=VIO, glow_r=14, glow_a=.6), W / 2, 1600, alpha=prog(t, s + 1.0, .3))


def word_caption(im, t, s, e, text, y=1560, size=58, col=WHITE, hl=None):
    """Word-by-word caption (each word pops) between s and e."""
    if t < s or t > e: return
    words = text.split(); n = len(words)
    f = font("black", size); d = ImageDraw.Draw(im)
    shown = max(1, min(n, int((t - s) / max(.12, (e - s - .4) / n)) + 1))
    line = " ".join(words[:shown])
    tw = d.textlength(line, font=f)
    x = (W - tw) / 2
    for i, wd in enumerate(words[:shown]):
        c = (hl or {}).get(wd.strip(".,!?"), col)
        sp = txt(wd, size, c, w="black", stroke=6, stroke_col=INK)
        ww = d.textlength(wd, font=f)
        sc = pop(t, s + i * (e - s - .4) / n, .2) if i == shown - 1 else 1
        put(im, sp, x + ww / 2, y, scale=sc)
        x += ww + d.textlength(" ", font=f)


def wcard(text, w=960, col=VIO, icon=None, size=44, num=None, fill_k=.62, weight="bold", fg=WHITE, pad=30):
    """Wrapped-text card sprite with colored border + glow; icon = emoji, num = number badge."""
    k = ("wcard", text, w, col, icon, size, num, fill_k, weight, fg, pad)
    if k in kit_cache(): return kit_cache()[k]
    f = font(weight, size)
    lead = 0
    if icon or num is not None: lead = int(size * 1.9)
    tw = w - pad * 2 - lead
    th = block_h(text, f, tw, 1.28)
    hh = max(th, int(size * 1.5)) + pad * 2
    p = panel(w, hh, fill=mix(col, BG, fill_k), r=32, border=col, bw=5, glow=col, glow_r=16, shadow=False).copy()
    pp = p.info["pad"]
    if icon:
        e = emoji(icon, int(size * 1.35)); p.paste(e, (pp + pad, pp + (hh - e.height) // 2), e)
    elif num is not None:
        d = ImageDraw.Draw(p); r = int(size * .75); cx, cy = pp + pad + r, pp + hh // 2
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
        nf = font("black", size); s = str(num)
        d.text((cx - d.textlength(s, font=nf) / 2, cy - size * .62), s, font=nf, fill=BG)
    block(p, pp + pad + lead, pp + pad + max(0, (int(size * 1.5) - th) // 2), tw, text, f, fg, 1.28)
    p.info["pad"] = pp; p.info["h"] = hh
    kit_cache()[k] = p
    return p


def kit_cache():
    import kit
    return kit._cache
