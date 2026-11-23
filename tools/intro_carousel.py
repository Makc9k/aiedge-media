# -*- coding: utf-8 -*-
"""Intro / 'meet AI Edge' carousel, 6 slides 1080x1350."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "motion"))
from engine import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "intro"
AVATAR = sys.argv[2] if len(sys.argv) > 2 else "avatars/avatar_ai_edge.png"
SW, SH = 1080, 1350
os.makedirs(OUT, exist_ok=True)


def slide(n, total=6):
    c = Canvas(0, 3.0 + n, SW, SH)
    c.d.text((70, 66), "AI EDGE", font=F(IB, 30), fill=CY)
    s = f"{n}/{total}"
    c.d.text((SW - 70 - c.d.textlength(s, font=F(ISB, 30)), 68), s, font=F(ISB, 30), fill=MUT)
    return c


def footer(c, text="Swipe →"):
    c.d.line([(70, SH - 120), (SW - 70, SH - 120)], fill=LINE, width=2)
    c.d.text((70, SH - 92), "@aiedge.prompts", font=F(ISB, 32), fill=WHITE)
    w = c.d.textlength(text, font=F(ISB, 32))
    c.d.text((SW - 70 - w, SH - 92), text, font=F(ISB, 32), fill=CY)


def title(c, y, parts, size=84):
    """parts: list of (text, color) on lines separated by '\n' entries."""
    x = 70
    for txt, col in parts:
        if txt == "\n":
            y += int(size * 1.12); x = 70; continue
        c.d.text((x, y), txt, font=F(IB, size), fill=col)
        x += c.d.textlength(txt, font=F(IB, size))
    return y + int(size * 1.12)


# 1 — cover
c = slide(1)
av = Image.open(AVATAR).convert("RGB").resize((300, 300), Image.LANCZOS)
mask = Image.new("L", (300, 300), 0); ImageDraw.Draw(mask).ellipse((0, 0, 299, 299), fill=255)
c.d.ellipse((60, 170, 380, 490), outline=CY, width=4)
c.im.paste(av, (70, 180), mask)
c.d = ImageDraw.Draw(c.im)
y = title(c, 560, [("Hi, I'm ", WHITE), ("AI Edge", CY), (" 👋".replace(" 👋", ""), WHITE)], 104)
c.block(70, y + 20, 900, "I turn AI into time you get back.", F(IB, 56), WHITE)
c.block(70, y + 120, 900, "One copy-paste prompt a day — and I show you exactly what it does, before → after.", F(IM, 40), MUT)
footer(c)
c.im.save(f"{OUT}/1.jpg", quality=93)

# 2 — what you get
c = slide(2)
y = title(c, 170, [("What you'll get", WHITE), ("\n", None), ("here", CY)], 88)
rows = [("1 prompt a day", "Copy it, fill the [brackets], paste into any AI chat."),
        ("Live demos", "Real before → after results, not promises."),
        ("Free tools", "Prompt packs and templates you can keep.")]
y += 40
for i, (a, b) in enumerate(rows):
    c.card((70, y, SW - 70, y + 230), fill=CARD)
    c.d.ellipse((110, y + 60, 210, y + 160), fill=(8, 51, 68))
    c.d.text((143, y + 70), str(i + 1), font=F(IB, 64), fill=CY)
    c.d.text((250, y + 52), a, font=F(IB, 50), fill=WHITE)
    c.block(250, y + 122, 700, b, F(IM, 34), MUT)
    y += 260
footer(c)
c.im.save(f"{OUT}/2.jpg", quality=93)

# 3 — demo email before/after
MESSY = "Hi Sarah, hope you're well! So I was looking at the project stuff… anyway could you maybe send the updated budget file at some point if that's ok, they kind of need it before Thursday I think. Thanks so much!!"
CLEAN = "Hi Sarah, could you send me the updated budget file before Thursday's meeting? The client needs it for that meeting. Thanks!"
c = slide(3)
title(c, 150, [("One prompt. ", WHITE), ("Real result.", CY)], 70)
c.pill(70, 280, "BEFORE", F(IB, 28), RED, (60, 20, 30))
c.card((70, 340, SW - 70, 640), fill=PAPER)
c.block(110, 372, 860, MESSY, F(IM, 33), (90, 98, 120))
c.d.line([(110, 600), (520, 600)], fill=RED, width=4)
c.d.ellipse((508, 664, 572, 728), fill=CY)
c.d.text((524, 668), "↓", font=F(SYM, 46), fill=BG)
c.pill(70, 690, "AFTER", F(IB, 28), GREEN, (14, 52, 44))
c.card((70, 750, SW - 70, 990), fill=PAPER, outline=GREEN, width=5)
c.block(110, 782, 860, CLEAN, F(IM, 36), INK)
for i, tg in enumerate(["Request in sentence 1", "Same facts, half the words"]):
    c.check(100, 1050 + i * 70 + 26, 24, 1.0)
    c.d.text((142, 1050 + i * 70 + 4), tg, font=F(ISB, 38), fill=WHITE)
footer(c)
c.im.save(f"{OUT}/3.jpg", quality=93)

# 4 — demo week plan
c = slide(4)
title(c, 150, [("Chaos ", RED), ("→ ", WHITE), ("plan", GREEN)], 80)
c.block(70, 255, 940, "Paste a messy to-do list. Get a realistic week.", F(IM, 38), MUT)
notes = ["Q4 report", "Landlord", "Dentist", "Inbox", "Gym", "Call mom", "Slides", "Fix bike"]
cols = [(254, 240, 138), (167, 243, 208), (191, 219, 254), (251, 207, 232)]
random.seed(4)
for i, nt in enumerate(notes):  # chaos pile
    x, yy, r = random.randint(80, 330), random.randint(350, 560), random.uniform(-14, 14)
    im = Image.new("RGBA", (220, 100), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
    dd.rounded_rectangle((0, 0, 219, 99), 14, fill=cols[i % 4]); dd.text((18, 30), nt, font=F(IBOLD, 32), fill=INK)
    im = im.rotate(r, expand=True, resample=Image.BICUBIC)
    c.im.paste(im, (x, yy), im)
c.d = ImageDraw.Draw(c.im)
c.d.text((560, 470), "→", font=F(SYM, 90), fill=CY)
plan = [("Mon", ["Q4 report", "Landlord"], "2h 10m"), ("Tue", ["Dentist", "Inbox"], "35m"), ("Wed", ["Gym", "Call mom"], "1h 20m"),
        ("Thu", ["Slides"], "1h 30m"), ("Fri", ["Fix bike"], "45m")]
y = 700
for d_, items, tot in plan:
    c.d.rounded_rectangle((70, y, SW - 70, y + 92), 18, fill=CARD)
    c.d.text((100, y + 24), d_, font=F(IB, 38), fill=WHITE)
    x = 220
    for j, it in enumerate(items):
        w = c.d.textlength(it, font=F(IBOLD, 30)) + 40
        c.d.rounded_rectangle((x, y + 18, x + w, y + 74), 12, fill=cols[(len(it) + j) % 4])
        c.d.text((x + 20, y + 28), it, font=F(IBOLD, 30), fill=INK)
        x += w + 14
    w = c.d.textlength(tot, font=F(IB, 32))
    c.d.text((SW - 100 - w, y + 28), tot, font=F(IB, 32), fill=GREEN)
    y += 106
footer(c)
c.im.save(f"{OUT}/4.jpg", quality=93)

# 5 — rules
c = slide(5)
y = title(c, 170, [("My 3 rules", WHITE)], 88)
rules = [("No hype.", "If a prompt doesn't save real time, it doesn't get posted."),
         ("No fake numbers.", "Demos use real outputs. Your facts stay your facts."),
         ("Copy-paste ready.", "Every prompt works in any AI chat, today.")]
y += 50
for a, b in rules:
    c.check(110, y + 36, 34, 1.0)
    c.d.text((170, y), a, font=F(IB, 54), fill=WHITE)
    c.block(170, y + 76, 820, b, F(IM, 38), MUT)
    y += 270
footer(c)
c.im.save(f"{OUT}/5.jpg", quality=93)

# 6 — CTA
c = slide(6)
y = title(c, 200, [("Start here", WHITE), ("\n", None), ("→ follow + save", CY)], 92)
c.card((70, y + 60, SW - 70, y + 380), fill=CARD, outline=CY)
c.d.text((120, y + 100), "Coming soon", font=F(ISB, 34), fill=VIO)
c.d.text((120, y + 150), "Free Starter 10", font=F(IB, 76), fill=WHITE)
c.block(120, y + 250, 840, "10 copy-paste prompts for email, planning, career & more.", F(IM, 36), MUT)
c.block(70, y + 450, 940, "Next: the prompt that turns any messy email into a clear one.", F(ISB, 42), WHITE)
footer(c, "Follow ⚡".replace("⚡", "").strip() + " →")
c.im.save(f"{OUT}/6.jpg", quality=93)

ims = [Image.open(f"{OUT}/{i}.jpg").resize((360, 450)) for i in range(1, 7)]
sh = Image.new("RGB", (3 * 370 + 10, 2 * 460 + 10), "#444")
for i, im in enumerate(ims):
    sh.paste(im, (10 + (i % 3) * 370, 10 + (i // 3) * 460))
sh.save(f"{OUT}_sheet.png")
print("ok")
