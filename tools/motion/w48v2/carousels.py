# -*- coding: utf-8 -*-
"""Carousels 25.11 (cheat-sheet, ref-20261123-08) and 28.11 (stop-X-say-Y, ref-20261123-11). 1080x1350."""
from common import *
CH = 1350
ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
PAPER = (248, 249, 253)


def cbg(seed=0.0, a=CY, b=VIO, c=None):
    return bg(seed, a=a, b=b, c=c).crop((0, 285, 1080, 285 + CH))


def handle(im, i, n):
    d = ImageDraw.Draw(im)
    d.text((60, CH - 78), "@aiedge.prompts", font=font("bold", 34), fill=WHITE)
    s = f"{i}/{n}"; f = font("bold", 34)
    d.text((W - 60 - d.textlength(s, font=f), CH - 78), s, font=f, fill=(200, 215, 255))


def center_txt(im, s, size, y, **kw):
    put(im, txt(s, size, **kw), W / 2, y)


# ---------------- carousel 1: cheat sheet ----------------
SHEET = [("Messy email", "Ask in line 1, max 5 sentences, keep my facts"),
         ("Follow-up", "Under 60 words, end with one yes/no question"),
         ("Week plan", "Sort: urgent / important / later / delete, max 4 h focus a day"),
         ("Scary task", "Steps of 25 min, first one under 5 min"),
         ("Resume", "Results not duties, write [add number] if missing"),
         ("New topic", "Analogy, real explanation, 3 myths, 3 quiz Qs"),
         ("Post ideas", "30 hooks: 10 tips, 10 myths, 10 personal"),
         ("Dinners", "5-day plan + shopping list by aisle"),
         ("Hard choice", "Table vs my priorities + 3 questions"),
         ("Pre-mortem", "It failed in 6 months. Top 10 reasons + fixes")]
NUMCOL = [CY, VIO, GREEN, AMBER, PINK]


def c1_s1():
    im = cbg(1.0, a=CY, b=VIO)
    put(im, chip("SCREENSHOT THIS", 34, fg=BG, bg=AMBER, glow=AMBER), W / 2, 80)
    center_txt(im, "10 AI PROMPTS", 104, 190, w="black", grad=(CY, VIO), glow=CY, glow_r=18, glow_a=.6)
    center_txt(im, "for your boring stuff", 60, 290, w="xb", color=WHITE)
    x0, y0, x1, y1 = 40, 350, 1040, 1250
    sp = panel(x1 - x0, y1 - y0, fill=PAPER, r=30, glow=(80, 140, 255), glow_r=26, shadow=False)
    put_panel(im, sp, x0, y0)
    d = ImageDraw.Draw(im)
    for yy in range(y0 + 40, y1 - 10, 45): d.line([(x0 + 20, yy), (x1 - 20, yy)], fill=(222, 230, 246), width=2)
    cw, chh = (x1 - x0 - 60) / 2, (y1 - y0 - 40) / 5
    for i, (nm, sh) in enumerate(SHEET):
        col, row = i // 5, i % 5
        cx, cy = x0 + 30 + col * cw, y0 + 20 + row * chh
        nc = NUMCOL[i % 5]
        d.rounded_rectangle((cx + 6, cy + 14, cx + 86, cy + 76), 18, fill=nc)
        ns = f"{i + 1:02d}"; nf = font("black", 38)
        d.text((cx + 46 - d.textlength(ns, font=nf) / 2, cy + 22), ns, font=nf, fill=BG)
        d.text((cx + 102, cy + 18), nm, font=font("black", 38), fill=INK)
        block(im, cx + 102, cy + 68, cw - 120, "“" + sh + "”", font("sb", 27), (55, 65, 100), 1.22)
        if col == 0: d.line([(x0 + 30 + cw - 5, cy + 20), (x0 + 30 + cw - 5, cy + chh - 10)], fill=(210, 218, 238), width=2)
    handle(im, 1, 3)
    return im


WEEKS = [("URGENT", RED, ["pay electric bill (10 min)", "finish client deck (3 h)", "read contract (1 h)"]),
         ("IMPORTANT", VIO, ["reply to 14 emails (1.5 h)", "plan mom's birthday (45 min)", "call dentist (10 min)", "gym x3 (after work)"]),
         ("CAN WAIT", CY, ["update LinkedIn (45 min)", "fix bike (1 h)"]),
         ("DELETE / MOVE", PINK, ["clean garage → the weekend"])]


def c1_s2():
    im = cbg(2.0, a=GREEN, b=VIO)
    put(im, chip("#03 IN ACTION", 40, fg=BG, bg=GREEN, glow=GREEN), W / 2, 90)
    center_txt(im, "Messy list in → sorted week out", 54, 190, w="black", color=WHITE, glow=GREEN, glow_r=12, glow_a=.4)
    sp = wcard("pay electric bill, finish client deck, call dentist, reply to 14 emails, gym x3, fix bike, plan mom's birthday, clean garage, read contract, update LinkedIn",
               960, RED, size=34, fill_k=.55, pad=26)
    put(im, chip("YOUR LIST", 30, fg=BG, bg=RED), 150, 268)
    put_panel(im, sp, 60, 300)
    y = 300 + sp.info["h"] + 30
    put(im, txt("↓", 70, GREEN, w="sym", glow=GREEN, glow_r=10), W / 2, y + 20); y += 70
    colw = 470
    for i, (nm, col, items) in enumerate(WEEKS):
        cx = 60 + (i % 2) * (colw + 20)
        yy = y + (i // 2) * 330
        p = panel(colw, 310, fill=mix(col, BG, .7), r=28, border=col, bw=4, glow=col, glow_r=12, shadow=False)
        put_panel(im, p, cx, yy)
        put_panel(im, chip(nm, 30, fg=BG, bg=col), cx + 20, yy + 18)
        block(im, cx + 24, yy + 90, colw - 48, "\n".join(items), font("sb", 32), WHITE, 1.3)
    handle(im, 2, 3)
    return im


def c1_s3():
    im = cbg(3.0, a=CY, b=PINK)
    center_txt(im, "Want the full prompts?", 64, 140, w="black", color=WHITE)
    pg = Image.open(os.path.join(ASSETS, "p3.png")).convert("RGBA")
    pg = pg.resize((int(pg.width * 620 / pg.height), 620), Image.LANCZOS)
    fr = Image.new("RGBA", (pg.width + 16, pg.height + 16), (255, 255, 255, 255)); fr.paste(pg, (8, 8), pg)
    gl = panel(fr.width, fr.height, fill=WHITE, r=8, glow=CY, glow_r=40, shadow=False)
    put(im, gl, W / 2, 560, rot=-4); put(im, fr, W / 2, 560, rot=-4)
    put(im, txt("Free Starter 10", 100, grad=(CY, VIO), glow=CY, glow_r=22, glow_a=.7), W / 2, 960)
    put(im, chip("→  link in bio", 54, fg=BG, bg=GREEN, glow=GREEN, padx=40, pady=16), W / 2, 1090)
    center_txt(im, "Copy-paste versions + a pro tip for each", 38, 1190, w="sb", color=(220, 230, 255))
    handle(im, 3, 3)
    return im


# ---------------- carousel 2: resume ----------------
BEFORE = ["Responsible for the company's 3 social media accounts", "Answered customer emails", "Helped with onboarding new hires"]
AFTER = ["Managed the company's 3 social media accounts, growing followers by [add number]% in [add timeframe].",
         "Resolved [add number] customer emails per week, keeping replies under [add number] hours.",
         "Trained and onboarded [add number] new hires, shortening their ramp-up by [add number] weeks."]
P05 = ("Rewrite these resume bullet points to show results, not duties. Use strong action verbs. Only use numbers I gave "
       "you — if a number would help but is missing, write [add number] instead of inventing one.\n\n[paste bullets]")


def gradient_bg(c1, c2):
    g = Image.new("RGB", (W, CH))
    a = np.linspace(0, 1, CH)[:, None, None]; b = np.linspace(0, 1, W)[None, :, None]
    k = np.clip(a * .6 + b * .4, 0, 1)
    arr = np.array(c1) * (1 - k) + np.array(c2) * k
    return Image.fromarray(arr.astype(np.uint8))


def chips_text(im, x, y, width, text, f, fill, chipcol=CY, lh=1.34, glow=False):
    """Text where [bracketed] parts become glowing chips."""
    d = ImageDraw.Draw(im); step = int(f.size * lh); cx = x
    import re
    parts = re.split(r"(\[[^\]]+\])", text)
    toks = []
    for p in parts:
        if p.startswith("["): toks.append((p, True))
        else:
            for li, seg in enumerate(p.split("\n")):
                if li: toks.append(("\n", None))
                toks += [(w, False) for w in seg.split(" ") if w]
    sp = d.textlength(" ", font=f)
    for tk, isc in toks:
        if isc is None:
            cx = x; y += step; continue
        if not isc and tk[0] in "%.,;:" and cx > x: cx -= sp + 2
        w = d.textlength(tk, font=f) + (16 if isc else 0)
        if cx + w > x + width and cx > x: cx = x; y += step
        if isc:
            if glow:
                g = panel(int(w), int(f.size * 1.25), fill=chipcol, r=12, glow=chipcol, glow_r=14, shadow=False)
                put_panel(im, g, cx - 4, y - 4); d = ImageDraw.Draw(im)
            else:
                d.rounded_rectangle((cx - 4, y - 4, cx + w - 4, y + f.size * 1.21), 12, fill=chipcol)
            d.text((cx + 4, y), tk, font=f, fill=BG)
        else:
            d.text((cx, y), tk, font=f, fill=fill)
        cx += w + sp
    return y + step


def chips_h(width, text, f, lh=1.34):
    scratch = Image.new("RGB", (W, 2000))
    return chips_text(scratch, 0, 0, width, text, f, WHITE, lh=lh)


def c2_s1():
    im = gradient_bg((76, 29, 149), (8, 145, 178))
    ov = Image.new("RGBA", (W, CH), (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle((0, 0, W, CH), fill=(7, 11, 24, 70)); im.paste(ov, (0, 0), ov)
    put(im, txt("STOP TELLING AI", 112, WHITE, w="black", glow=(0, 0, 0), glow_r=18, glow_a=.5), W / 2, 330)
    s = txt("“FIX MY RESUME”", 104, (255, 235, 235), w="black", glow=RED, glow_r=20, glow_a=.7)
    put(im, s, W / 2, 500)
    d = ImageDraw.Draw(im)
    d.line([(W / 2 - s.width / 2 + 30, 515), (W / 2 + s.width / 2 - 30, 490)], fill=RED, width=14)
    put(im, chip("TYPE THIS INSTEAD  →", 62, fg=BG, bg=GREEN, glow=GREEN, padx=46, pady=22), W / 2, 760)
    center_txt(im, "One prompt. Duties become results.", 46, 930, w="bold", color=WHITE)
    center_txt(im, "Swipe →", 44, 1130, w="xb", color=(220, 250, 255))
    handle(im, 1, 6)
    return im


def c2_s2():
    im = cbg(5.0, a=RED, b=VIO)
    put(im, chip("WHAT YOU GET", 40, fg=BG, bg=RED, glow=RED), W / 2, 110)
    center_txt(im, "You type “fix my resume”…", 58, 220, w="black", color=WHITE)
    x0, y0, x1, y1 = chat_frame(im, 60, 300, 960, 640)
    bubble(im, x0 + 420, y0, x1 - x0 - 420, "fix my resume", font("sb", 40), "user")
    weak = "Results-driven professional with a proven track record of managing social media and delivering excellent customer service."
    yb = bubble(im, x0, y0 + 120, x1 - x0 - 40, weak, font("med", 40), "ai")
    for i, w_ in enumerate(["buzzwords", "no numbers", "could be anyone"]):
        put(im, chip("✗ " + w_, 44, fg=WHITE, bg=RED, glow=RED), W / 2, 1020 + i * 0, alpha=0)
    for i, w_ in enumerate(["✗  buzzwords", "✗  no numbers", "✗  could be anyone"]):
        put(im, chip(w_, 46, fg=WHITE, bg=RED, glow=RED), W / 2, 1010 + i * 92)
    handle(im, 2, 6)
    return im


def c2_s3():
    im = cbg(6.0, a=CY, b=VIO)
    put(im, chip("TYPE THIS INSTEAD", 40, fg=BG, bg=GREEN, glow=GREEN), W / 2, 110)
    center_txt(im, "Prompt #05 · Resume bullet upgrade", 48, 210, w="black", color=WHITE)
    f = font("mono", 38)
    hh = block_h(P05, f, 860, 1.42) + 90
    put_panel(im, panel(960, hh, fill=(12, 18, 44), r=32, border=(CY, VIO), bw=5, glow=(60, 90, 220), glow_r=28), 60, 300)
    d = ImageDraw.Draw(im)
    for i, col in enumerate([RED, AMBER, GREEN]): d.ellipse((100 + i * 36, 330, 122 + i * 36, 352), fill=col)
    chips_text(im, 110, 380, 860, P05, f, (230, 245, 255), chipcol=CY, lh=1.42)
    center_txt(im, "Copy it. Paste your bullets under it.", 44, 300 + hh + 80, w="bold", color=(220, 250, 255))
    handle(im, 3, 6)
    return im


def c2_s4():
    im = cbg(7.0, a=RED, b=GREEN)
    put(im, chip("DUTIES → RESULTS", 40, fg=BG, bg=AMBER, glow=AMBER), W / 2, 100)
    y = 180
    for b_, a_ in zip(BEFORE, AFTER):
        sb = wcard(b_, 960, RED, size=34, fill_k=.55, pad=22, weight="sb")
        put_panel(im, sb, 60, y); y += sb.info["h"] + 8
        put(im, txt("↓", 46, GREEN, w="sym"), W / 2, y + 16); y += 40
        sa = Image.new("RGBA", (1, 1))
        hh = chips_h(880, a_, font("bold", 36)) + 40
        put_panel(im, panel(960, hh, fill=mix(GREEN, BG, .6), r=28, border=GREEN, bw=4, glow=GREEN, glow_r=12, shadow=False), 60, y)
        chips_text(im, 100, y + 22, 880, a_, font("bold", 36), WHITE, chipcol=CY)
        y += hh + 34
    handle(im, 4, 6)
    return im


def c2_s5():
    im = cbg(8.0, a=CY, b=(37, 99, 235))
    center_txt(im, "You fill the numbers.", 76, 170, w="black", color=WHITE, glow=CY, glow_r=14, glow_a=.5)
    center_txt(im, "AI doesn't invent them.", 76, 270, w="black", grad=(CY, GREEN), glow=CY, glow_r=14, glow_a=.5)
    y = 400
    for a_ in AFTER:
        hh = chips_h(860, a_, font("bold", 38), 1.4) + 46
        put_panel(im, panel(960, hh, fill=(14, 22, 54), r=28, border=(CY, VIO), bw=4, shadow=False), 60, y)
        chips_text(im, 110, y + 25, 860, a_, font("bold", 38), WHITE, chipcol=CY, lh=1.4, glow=True)
        y += hh + 30
    center_txt(im, "Real numbers are what recruiters notice.", 40, y + 50, w="sb", color=(220, 240, 255))
    handle(im, 5, 6)
    return im


def c2_s6():
    im = cbg(9.0, a=VIO, b=CY)
    put(im, chip("PROMPT #05 + 9 MORE", 42, fg=BG, bg=AMBER, glow=AMBER), W / 2, 260)
    put(im, txt("Free Starter 10", 110, grad=(CY, VIO), glow=CY, glow_r=24, glow_a=.75), W / 2, 470)
    put(im, chip("→  link in bio", 60, fg=BG, bg=GREEN, glow=GREEN, padx=44, pady=18), W / 2, 640)
    center_txt(im, "Save this for your next application", 46, 780, w="bold", color=WHITE)
    pg = Image.open(os.path.join(ASSETS, "p4.png")).convert("RGBA")
    pg = pg.resize((int(pg.width * 400 / pg.height), 400), Image.LANCZOS)
    fr = Image.new("RGBA", (pg.width + 12, pg.height + 12), (255, 255, 255, 255)); fr.paste(pg, (6, 6), pg)
    put(im, panel(fr.width, fr.height, fill=WHITE, r=6, glow=VIO, glow_r=34, shadow=False), W / 2, 1060, rot=4)
    put(im, fr, W / 2, 1060, rot=4)
    handle(im, 6, 6)
    return im


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sets = {"c1_1125_cheatsheet": [c1_s1, c1_s2, c1_s3], "c2_1128_resume": [c2_s1, c2_s2, c2_s3, c2_s4, c2_s5, c2_s6]}
    for name, fns in sets.items():
        ims = []
        for i, fn in enumerate(fns):
            im = fn().convert("RGB"); p = os.path.join(OUT, f"{name}_{i + 1}.jpg"); im.save(p, quality=93); ims.append((i + 1, im))
        contact([(i, im) for i, im in ims], f"/tmp/{name}_sheet.jpg")
        print(name, len(ims))
