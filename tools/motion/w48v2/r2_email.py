# -*- coding: utf-8 -*-
"""Reel 26.11 — Starter #01 messy email, two prompts. Structure of ref-20261123-03 ('from X to Y — two prompts':
result split first, step 1, step 2, back to before/after, CTA)."""
from common import *

MESSY = ("hey so I wanted to ask about maybe taking some days off around christmas, I know its busy and Jen is also off "
         "I think, but my family is flying in on the 22nd so I'd need like the 22-26 if possible, I can finish the Q4 "
         "report before, let me know sorry for the long msg")
P1 = ("Rewrite this email so it is clear and polite. Put my main request in the first sentence. Maximum 5 sentences. "
      "Keep all my facts and don't invent anything.")
A1 = ("Hi [Manager], could I take December 22–26 off? My family is flying in on the 22nd. I'll finish the Q4 report "
      "before I leave. I know it's a busy time and Jen may also be off, so I'm happy to talk through coverage. "
      "Thanks for considering it.")
P2 = "Make it warmer"
A2 = ("Hi [Manager], I hope your week is going well! Could I take December 22–26 off? My family is flying in on the "
      "22nd and I'd love to be there with them. I'll have the Q4 report done before I go. I know it's a busy stretch "
      "and Jen may be out too, so I'm glad to help plan coverage. Thank you for considering it!")
T_P1, T_P2, T_SPLIT, T_CTA, END = 1.6, 5.3, 8.3, 12.1, 14.5
HL_T = [T_SPLIT + .5, T_SPLIT + 1.5, T_SPLIT + 2.5]


def token_ranges(text, phrases):
    toks = text.split(" "); out_ = []
    for ph, col, s in phrases:
        pt = ph.split(" ")
        for i in range(len(toks)):
            if toks[i:i + len(pt)] == pt: out_.append((i, i + len(pt), col, s)); break
    return out_


def marked(im, x, y, width, text, f, fill, ranges, t, lh=1.25):
    """Text with marker highlights that sweep in (ranges of token indices)."""
    d = ImageDraw.Draw(im); toks = text.split(" "); step = int(f.size * lh)
    sp = d.textlength(" ", font=f); cx, cy = x, y
    pos = []
    for i, tk in enumerate(toks):
        w = d.textlength(tk, font=f)
        if cx + w > x + width and cx > x: cx = x; cy += step
        pos.append((cx, cy, w)); cx += w + sp
    for a, b, col, s in ranges:
        k = ease(prog(t, s, .3))
        if k <= 0: continue
        for i in range(a, b):
            px, py, w = pos[i]
            seg = clamp(k * (b - a) - (i - a))
            if seg > 0:
                d.rounded_rectangle((px - 6, py - 2, px + (w + sp) * seg, py + f.size * 1.18), 8, fill=mix(col, BG, .35))
    for i, tk in enumerate(toks):
        px, py, w = pos[i]
        d.text((px, py), tk, font=f, fill=fill)
    return cy + step


def split(im, t, s, hl=False):
    f = font("med", 44)
    kL, kR = ease(prog(t, s, .22)), ease(prog(t, s + .12, .22))
    # left: before
    hL = block_h(MESSY, f, 430, 1.25) + 130
    put_panel(im, panel(500, hL, fill=(58, 18, 30), r=34, border=RED, bw=5, glow=RED, glow_r=20, shadow=False), 25 - 520 * (1 - kL), 520)
    xL = 25 - 520 * (1 - kL)
    put(im, chip("BEFORE", 40, fg=BG, bg=RED), xL + 250, 575)
    rl = token_ranges(MESSY, [("maybe", RED, HL_T[0]), ("I think,", RED, HL_T[0] + .2), ("if possible,", RED, HL_T[1]),
                              ("sorry for the long msg", RED, HL_T[2])]) if hl else []
    marked(im, xL + 35, 640, 430, MESSY, f, (255, 225, 225), rl, t)
    # right: after
    hR = block_h(A2, f, 430, 1.25) + 130
    xR = 555 + 520 * (1 - kR)
    put_panel(im, panel(500, hR, fill=(10, 56, 46), r=34, border=GREEN, bw=5, glow=GREEN, glow_r=20, shadow=False), xR, 520)
    put(im, chip("AFTER", 40, fg=BG, bg=GREEN), xR + 250, 575)
    rr = token_ranges(A2, [("Could I take December 22–26 off?", CY, HL_T[0]), ("flying in on the 22nd", VIO, HL_T[1]),
                           ("Q4 report done", AMBER, HL_T[2])]) if hl else []
    marked(im, xR + 35, 640, 430, A2, f, WHITE, rr, t)


def frame(t):
    im = bg(t, a=CY, b=GREEN if t >= T_SPLIT else VIO, c=RED if t < T_P1 else None)
    if t < T_P1:
        put(im, txt("Messy → yes-worthy", 88, grad=(RED, GREEN), glow=CY, glow_r=18, glow_a=.5), W / 2, 330, scale=slam(t, 0, .2))
        put(im, chip("2 PROMPTS", 52, fg=BG, bg=AMBER, glow=AMBER), W / 2, 440, scale=pop(t, .25, .3))
        split(im, t, 0.0)
    elif t < T_SPLIT:
        two = t >= T_P2
        put(im, chip("PROMPT 2" if two else "PROMPT 1", 56, fg=BG, bg=VIO if two else CY, glow=VIO if two else CY), W / 2, 330,
            scale=pop(t, T_P2 if two else T_P1, .3))
        put(im, txt("Make it warmer" if two else "Clear + ask first", 64, w="black"), W / 2, 445, scale=slam(t, T_P2 if two else T_P1 + .1, .2))
        x0, y0, x1, y1 = chat_frame(im, 40, 530, 1000, 1110)
        f = font("med", 44); wb = x1 - x0
        if not two:
            n = (t - T_P1 - .1) * 140
            yb = bubble(im, x0 + 60, y0, wb - 60, P1, f, "user", chars=max(0, n), t=t)
            if n > len(P1):
                put_panel(im, chip("+ your messy draft attached", 40, fg=WHITE, bg=(90, 30, 45)), x0 + 60, yb + 18)
                n2 = (t - (T_P1 + .2 + len(P1) / 140)) * 135
                if n2 > 0: bubble(im, x0, yb + 120, wb - 40, A1, f, "ai", chars=n2, t=t)
        else:
            yb = bubble(im, x0 + 360, y0, wb - 360, P2, f, "user", chars=max(0, (t - T_P2 - .05) * 45), t=t)
            n2 = (t - T_P2 - .5) * 150
            if n2 > 0:
                bubble(im, x0, yb + 30, wb - 40, A2, f, "ai", chars=n2, t=t)
    elif t < T_CTA:
        put(im, txt("Ask first. Facts kept.", 80, grad=(CY, GREEN), glow=GREEN, glow_r=18, glow_a=.6), W / 2, 330, scale=slam(t, T_SPLIT, .2))
        tags = [("Ask in line 1", CY), ("Dates kept", VIO), ("Q4 report kept", AMBER)]
        for i, (tg, col) in enumerate(tags):
            if t >= HL_T[i]:
                put(im, chip(tg, 40, fg=BG, bg=col, glow=col), 190 + i * 350, 440, scale=pop(t, HL_T[i], .3))
        split(im, t, T_SPLIT, hl=True)
    else:
        cta(im, t, T_CTA, tag="PROMPT #01 · MESSY → CLEAR", prompt=P1 + "\n[paste your draft]",
            sub="Then: “Make it warmer”")
    return im


BEATS = [0, .25, T_P1, 2.9, 4.2, T_P2, 5.8, 7.0, T_SPLIT] + HL_T + [T_CTA, T_CTA + .35, T_CTA + .65]
FLASH = [T_P1, T_P2, T_SPLIT, T_CTA]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        stills(frame, [.9, 4.6, 7.9, 9.0, 11.6, 14.0], "/tmp/r2_stills.jpg")
    else:
        render(os.path.join(OUT, "r2_1126_messy_email.mp4"), frame, END, BEATS, FLASH)
