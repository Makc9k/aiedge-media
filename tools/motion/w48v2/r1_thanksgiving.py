# -*- coding: utf-8 -*-
"""Reel 24.11 — Pre-mortem Thanksgiving. Structure of ref-20261123-10 (meme caption box over screen,
result visible under the caption from frame 0, then the chat, then the list, then fixes, CTA)."""
from common import *

PROMPT = ("Imagine it's 6 months from now and my first time hosting Thanksgiving dinner for 8 people failed. "
          "List the 10 most likely reasons why. Then for the top 3, suggest what I can do now to prevent them.")
REASONS = [("Turkey still frozen on Thursday", "🧊"), ("Every dish needs the oven", "🔥"),
           ("Guest can't eat half the menu", "🥗"), ("Turkey late, sides go cold", "⏰"),
           ("3 new recipes on the day", "📖"), ("Panic gravy at the last minute", "🫠"),
           ("A key ingredient forgotten", "🛒"), ("Not enough chairs or plates", "🪑"),
           ("Host stuck in the kitchen", "🍳"), ("No fridge room for leftovers", "📦")]
FIXES = [("Turkey still frozen", "Thaw it in cold water, about 30 min per pound. Change the water every 30 min."),
         ("Every dish needs the oven", "Write an oven schedule. Move sides to the stovetop, slow cooker or the day before."),
         ("No one asked about diets", "Text every guest today: “Anything you don't eat?”")]
T_CHAT, T_LIST, T_FIX, T_CTA, END = 1.0, 3.3, 8.3, 12.3, 15.0
LIST_T = [T_LIST + .35 + i * .44 for i in range(10)]
FIX_T = [T_FIX + .5 + i * .95 for i in range(3)]


def caption(im, t):
    if t >= T_CTA: return
    a = 1 - prog(t, T_CTA - .2, .2)
    meme_box(im, "I asked AI why my\nThanksgiving failed|🦃", 262, size=62, alpha=a, scale=slam(t, 0, .18) if t < .2 else 1)
    put(im, txt("(it hasn't happened yet)", 46, CY, w="bold", glow=CY, glow_r=12, glow_a=.5), W / 2, 500,
        alpha=a * prog(t, .35, .2))


def frame(t):
    im = bg(t, a=(249, 115, 22) if t < T_FIX else GREEN, b=VIO, energy=1.0)
    if t < T_CHAT:                                   # result first: reason #1 slams in
        put(im, chip("AI's #1 reason", 50, fg=BG, bg=RED, glow=RED), W / 2, 700, scale=pop(t, .05, .25))
        sp = panel(960, 420, fill=mix(RED, BG, .45), r=44, border=RED, bw=6, glow=RED, glow_r=34, shadow=False)
        put_panel(im, sp, 60, 800, alpha=1)
        put(im, emoji("🧊", 150), W / 2, 930, scale=pop(t, .12, .3))
        put(im, txt("The turkey is still", 70, w="black"), W / 2, 1075, scale=slam(t, .0, .2))
        put(im, txt("frozen on Thursday", 70, w="black"), W / 2, 1155, scale=slam(t, .08, .2))
        put(im, txt("…and that's only reason one", 52, (255, 225, 225), w="xb"), W / 2, 1330, alpha=prog(t, .4, .2))
        put(im, chip("9 more →", 50, fg=BG, bg=AMBER, glow=AMBER), W / 2, 1460, scale=pop(t, .55, .25))
    elif t < T_LIST:                                 # chat: prompt types fast
        x0, y0, x1, y1 = chat_frame(im, 60, 600, 960, 900)
        f = font("sb", 50)
        n = int((t - T_CHAT - .1) * 120)
        yb = bubble(im, x0 + 40, y0, x1 - x0 - 40, PROMPT, f, "user", chars=max(0, n), t=t)
        if n > len(PROMPT):
            k = t - (T_CHAT + .1 + len(PROMPT) / 120)
            d = ImageDraw.Draw(im)
            for i in range(3):
                r = 12 + 6 * math.sin(k * 14 - i)
                d.ellipse((x0 + 40 + i * 50 - r, yb + 70 - r, x0 + 40 + i * 50 + r, yb + 70 + r), fill=VIO)
    elif t < T_FIX:                                  # 10 reasons slam in
        header(im, t, T_LIST, "10 ways it goes wrong", 74, grad=(RED, AMBER), glow=RED, y=600)
        for i, (r, ic) in enumerate(REASONS):
            if t < LIST_T[i]: break
            sp = strip(r, 960, 44, RED, num=i + 1, icon=ic, h=84)
            put_panel(im, sp, 60 + 400 * (1 - ease(prog(t, LIST_T[i], .16))), 690 + i * 94, alpha=prog(t, LIST_T[i], .1))
    elif t < T_CTA:                                  # top 3 flip red -> green
        header(im, t, T_FIX, "…and how to stop the top 3", 66, grad=(GREEN, CY), glow=GREEN, y=600)
        f = font("bold", 44)
        for i, (prob, fix) in enumerate(FIXES):
            y = 690 + i * 300
            appear = T_FIX + .1 + i * .12
            if t < appear: continue
            ys, flipped = flip_scale(t, FIX_T[i], .4)
            if not flipped:
                sp = strip(prob, 960, 48, RED, num=i + 1, h=110)
                put(im, squash(sp, ys), W / 2, y + 55, alpha=prog(t, appear, .12))
            else:
                hh = block_h(fix, f, 790) + 60
                card = Image.new("RGBA", (W, hh + 80), (0, 0, 0, 0))
                p = panel(960, hh, fill=mix(GREEN, BG, .62), r=36, border=GREEN, bw=5, glow=GREEN, glow_r=18, shadow=False)
                card.paste(p, (60 - p.info["pad"], 40 - p.info["pad"]), p)
                ic = check_icon(78); card.paste(ic, (90, 40 + (hh - 78) // 2), ic)
                block(card, 196, 70, 790, fix, f, WHITE, 1.3)
                put(im, squash(card, ys), W / 2, y + hh / 2, alpha=1)
    else:
        cta(im, t, T_CTA, tag="PROMPT #10 · PRE-MORTEM", prompt=PROMPT, sub="10 prompts like this, free PDF")
    caption(im, t)
    return im


BEATS = [0, T_CHAT, 2.2, T_LIST] + LIST_T[::2] + [T_FIX] + FIX_T + [T_CTA, T_CTA + .35, T_CTA + .65]
FLASH = [T_CHAT, T_LIST, T_FIX, T_CTA]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        stills(frame, [.3, 2.4, 6.0, 8.0, 11.8, 14.5], "/tmp/r1_stills.jpg")
    else:
        render(os.path.join(OUT, "r1_1124_thanksgiving_premortem.mp4"), frame, END, BEATS, FLASH, shake=[0.02])
