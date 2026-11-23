# -*- coding: utf-8 -*-
"""Launch stories v2 — visual demos of real results (not text on a background)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from engine import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
PAGES = sys.argv[2] if len(sys.argv) > 2 else "pages"   # folder with page PNGs of the Starter PDF


def header(c, t, tag, title, tag_col=VIO):
    c.pill(0, 250, tag, F(ISB, 32), tag_col, (24, 20, 52), k=prog(t, 0, .4), center=True)
    c.text_c(330, title, F(IB, 64), WHITE, prog(t, .15, .45), dy=30)


# ---------------- S1: messy email -> clear email ----------------
MESSY = ("Hi Sarah, hope you're doing well! So I was looking at the project stuff from last week and there were a few "
         "things, also the client called again about the timeline which I think we discussed before? Anyway I was "
         "wondering if maybe you could possibly send me the updated budget file at some point if that's ok, they kind "
         "of need it before the Thursday meeting I think. Thanks so much!!")
CLEAN = ("Hi Sarah,\nCould you send me the updated budget file before Thursday's meeting? The client needs it for that "
         "meeting.\nThey also called again about the timeline, so let's discuss that separately.\nThanks!")
USER_PROMPT = "Rewrite this email so it's clear and polite. Main request first. Max 5 sentences. Don't invent anything.\n[email pasted]"
N_MESSY = len(MESSY.split())


def paper(c, box, title, text, font, col_border=None, k=1.0, underlines=()):
    """box = (x0, y0, x1, _) — height is computed from the text. Returns bottom y."""
    x0, y0, x1, _ = box
    lines = wrap(c.d, text, font, x1 - x0 - 72)
    step = int(font.size * 1.42)
    y1 = y0 + 96 + len(lines) * step + 30
    c.card((x0, y0, x1, y1), fill=PAPER, outline=col_border, width=5 if col_border else 3)
    c.d.text((x0 + 36, y0 + 26), title, font=F(ISB, 28), fill=(107, 120, 150))
    c.d.line([(x0 + 36, y0 + 74), (x1 - 36, y0 + 74)], fill=(220, 226, 238), width=2)
    for i, ln in enumerate(lines):
        c.d.text((x0 + 36, y0 + 96 + i * step), ln, font=font, fill=INK)
    # map character ranges to lines (single-paragraph text)
    starts, pos = [], 0
    joined = " ".join(lines)
    for ln in lines:
        starts.append(pos); pos += len(ln) + 1
    for (needle, kk) in underlines:
        a = joined.find(needle)
        if a < 0 or kk <= 0: continue
        b = a + len(needle)
        segs = []
        for i, ln in enumerate(lines):
            s0, s1_ = starts[i], starts[i] + len(ln)
            lo, hi = max(a, s0), min(b, s1_)
            if lo < hi: segs.append((i, lo - s0, hi - s0))
        total = sum(e - st for _, st, e in segs) or 1
        done = 0
        for i, st, e in segs:
            seg_k = clamp((kk * total - done) / (e - st))
            done += e - st
            ln = lines[i]
            xa = x0 + 36 + c.d.textlength(ln[:st], font=font)
            xb = x0 + 36 + c.d.textlength(ln[:e], font=font)
            c.underline(xa, xb, y0 + 96 + i * step + font.size * 1.18, seg_k)
    return y1


def s1(c, t):
    header(c, t, "FREE PROMPT · LIVE DEMO", "Messy email → clear email")
    f_body = F(IM, 36)
    # phase A: before
    if t < 4.0:
        out = ease(prog(t, 3.4, .6))
        k = ease(prog(t, .3, .5))
        y = 470 + 60 * (1 - k) - 900 * out
        c.pill(80, y - 6, "BEFORE", F(IB, 28), RED, (60, 20, 30), k=k)
        bottom = paper(c, (60, y + 60, 1020, 0), "To: Sarah   ·   Subject: (no subject)", MESSY, f_body,
                       underlines=[("send me the updated budget file", prog(t, 1.3, .5)),
                                   ("at some point", prog(t, 1.9, .4))])
        tags = [("Main request buried in the middle", 1.3), ("Vague: “at some point”", 1.9), (f"{N_MESSY} words, mostly filler", 2.5)]
        for i, (tg, st) in enumerate(tags):
            kk = prog(t, st, .35)
            if kk > 0:
                yy = bottom + 50 + i * 92
                c.cross(110, yy + 32, 26, kk)
                c.text(156, yy + 8, tg, F(ISB, 40), WHITE, kk)
    # phase B: chat
    if 3.6 <= t < 8.9:
        k = ease(prog(t, 3.6, .5)) * (1 - ease(prog(t, 8.4, .5)))
        y0 = 460 + 120 * (1 - k)
        inner = chat_window(c, (50, y0, 1030, y0 + 1180))
        x0, iy, x1, _ = inner
        uy = bubble(c, x1 - 780, iy, 780, USER_PROMPT, F(MONO, 30), "user", chars=(t - 4.0) * 70)
        if t > 5.4:
            c.d.ellipse((x0, uy + 40, x0 + 54, uy + 94), fill=CY)
            c.d.text((x0 + 13, uy + 46), "✦", font=F(SYM, 32), fill=BG)
            n = (t - 5.6) * 62
            bubble(c, x0 + 70, uy + 34, 840, CLEAN, F(IM, 36), "ai", chars=n, cursor=n < len(CLEAN))
        if k < 1 and t > 8.4:
            pass
    # phase C: after
    if t >= 8.6:
        k = ease(prog(t, 8.6, .5))
        y = 470 + 60 * (1 - k)
        c.pill(80, y - 6, "AFTER", F(IB, 28), GREEN, (14, 52, 44), k=k)
        bottom = paper(c, (60, y + 60, 1020, 0), "To: Sarah   ·   Subject: Budget file before Thursday", CLEAN, f_body, col_border=GREEN)
        n_clean = len(CLEAN.split())
        checks = [("Main request in sentence 1", 9.1), (f"{n_clean} words instead of {N_MESSY}", 9.5), ("Same facts, nothing invented", 9.9)]
        for i, (tg, st) in enumerate(checks):
            kk = prog(t, st, .4)
            yy = bottom + 50 + i * 92
            c.check(110, yy + 32, 28, kk)
            c.text(160, yy + 8, tg, F(ISB, 42), WHITE, kk)
        c.text_c(1600, "This prompt is in the free Starter 10", F(ISB, 40), CY, prog(t, 10.6, .5))


# ---------------- S2: to-do chaos -> week plan ----------------
TASKS = [  # text, minutes, day index (0-4) or -1 = delete
    ("Finish Q4 report", 120, 0), ("Reply to landlord", 10, 0), ("Book dentist", 5, 1), ("Clean inbox", 30, 1),
    ("Gym", 60, 2), ("Call mom", 20, 2), ("Friday slides", 90, 3), ("Fix bike", 45, 4),
    ("Re-watch old webinar", 0, -1), ("Reorganize desktop", 0, -1)]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
NOTE_COLS = [(254, 240, 138), (167, 243, 208), (191, 219, 254), (251, 207, 232), (253, 230, 138)]
random.seed(7)
SCATTER = [(random.randint(90, 640), random.randint(470, 1300), random.uniform(-12, 12)) for _ in TASKS]


def fmt(m): return f"{m//60}h {m%60:02d}m" if m >= 60 else f"{m}m"


def note_img(text, col, w=330, h=150, chip=None):
    im = Image.new("RGBA", (w + 20, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 14, w + 10, h + 14), 16, fill=(0, 0, 0, 90))
    d.rounded_rectangle((6, 6, w + 4, h + 4), 16, fill=col)
    lines = wrap(d, text, F(IBOLD, 36), w - 40)
    for i, ln in enumerate(lines[:2]):
        d.text((26, 24 + i * 44), ln, font=F(IBOLD, 36), fill=INK)
    if chip:
        cw = d.textlength(chip, font=F(ISB, 28)) + 28
        d.rounded_rectangle((26, h - 50, 26 + cw, h - 10), 18, fill=(11, 17, 36))
        d.text((40, h - 47), chip, font=F(ISB, 28), fill=CY)
    return im


NOTES = [note_img(tx, NOTE_COLS[i % 5], chip=fmt(m) if m else None) for i, (tx, m, d_) in enumerate(TASKS)]
ROW_Y0, ROW_H = 640, 170


def s2(c, t):
    header(c, t, "FREE PROMPT · LIVE DEMO", "To-do chaos → week plan")
    sort_start = 3.0
    kcol = ease(prog(t, 2.6, .6))
    totals = [0] * 5
    if kcol > 0:
        for i, dname in enumerate(DAYS):
            y = ROW_Y0 + i * ROW_H
            c.d.rounded_rectangle((50, y, 1030, y + ROW_H - 14), 22, fill=fade((16, 24, 52), kcol))
            c.text(78, y + 50, dname, F(IB, 46), WHITE, kcol)
        c.d.rounded_rectangle((260, 1530, 820, 1630), 24, fill=fade((60, 20, 30), kcol))
        c.text_c(1558, "Delete — not worth it", F(ISB, 40), RED, kcol)
    slot = [0] * 5
    for i, (tx, m, day) in enumerate(TASKS):
        sx, sy, rot = SCATTER[i]
        jitter = 6 * math.sin(t * 7 + i) if t < sort_start else 0
        appear = back(prog(t, .3 + i * .12, .35))
        k = ease_io(prog(t, sort_start + i * .22, .7))
        if day >= 0:
            tx_ = 210 + 155 + slot[day] * 300
            ty_ = ROW_Y0 + day * ROW_H + (ROW_H - 14) / 2
            slot[day] += 1
            scale = lerp(1.0, 0.82, k)
            if k >= 1: totals[day] += m
        else:
            tx_, ty_ = 540, 1580
            scale = lerp(1.0, 0.25, k)
        cx = lerp(sx + 175, tx_, k) + jitter
        cy = lerp(sy + 85, ty_, k)
        vis = appear * (1 - (ease(prog(t, sort_start + i * .22 + .5, .3)) if day < 0 else 0))
        c.paste_scaled(NOTES[i], cx, cy, scale * vis, rot=lerp(rot, 0, k))
    if t < sort_start:
        c.text_c(1660, "10 things · no plan · stress", F(ISB, 42), RED, prog(t, 1.4, .4))
        if t > 2.2:
            pulse = .5 + .5 * math.sin(t * 10)
            c.pill(0, 1560, "✦  AI sorts it", F(IB, 40), BG, mix(CY, WHITE, pulse * .3), k=prog(t, 2.2, .3), center=True)
    for i in range(5):
        kk = prog(t, 6.2 + i * .15, .4)
        if kk > 0:
            y = ROW_Y0 + i * ROW_H
            txt = fmt(totals[i]) if totals[i] else "—"
            w = c.d.textlength(txt, font=F(IB, 36))
            c.text(1000 - w, y + 56, txt, F(IB, 36), GREEN, kk)
    c.text_c(1690, "Every day under 4 focused hours", F(ISB, 42), GREEN, prog(t, 7.2, .5))


# ---------------- S3: resume bullet ----------------
BEFORE_B = "Responsible for the company Instagram."
FACTS = ["posted daily", "built a content calendar", "1.2k → 4k followers"]
AFTER_B = "Grew the company Instagram from 1.2k to 4k followers by building a content calendar and posting daily."


def s3(c, t):
    header(c, t, "FREE PROMPT · LIVE DEMO", "Weak resume line → strong")
    k = ease(prog(t, .3, .5))
    y = 470 + 40 * (1 - k)
    c.card((60, y, 1020, y + 420), fill=PAPER)
    c.d.text((100, y + 30), "EXPERIENCE", font=F(IB, 30), fill=(107, 120, 150))
    c.d.text((100, y + 80), "Marketing Assistant · Bright Co.", font=F(IBOLD, 40), fill=INK)
    fb = F(IM, 40)
    c.d.text((100, y + 160), "•", font=fb, fill=INK)
    strike = prog(t, 3.0, .5)
    if t < 3.6:
        c.d.text((140, y + 160), BEFORE_B, font=fb, fill=mix(INK, (170, 178, 196), strike))
        w = c.d.textlength(BEFORE_B, font=fb)
        c.underline(140, 140 + w, y + 214, prog(t, 1.0, .5))
        if strike > 0:
            c.d.line([(140, y + 184), (140 + w * ease(strike), y + 184)], fill=RED, width=5)
        c.pill(140, y + 250, "a duty, not a result", F(ISB, 30), RED, (254, 226, 226), k=prog(t, 1.3, .4))
    else:
        n = (t - 3.7) * 55
        c.block(140, y + 160, 840, AFTER_B, fb, INK, chars=n, cursor=n < len(AFTER_B))
    # facts
    c.text(80, y + 470, "Your facts:", F(ISB, 38), MUT, prog(t, 1.7, .4))
    x, fy = 80, y + 530
    for i, fct in enumerate(FACTS):
        kk = prog(t, 1.9 + i * .3, .35)
        tw = c.d.textlength(fct, font=F(ISB, 34)) + 48
        if x + tw > 1000: x, fy = 80, fy + 76
        nx = c.pill(x, fy, fct, F(ISB, 34), CY, (8, 51, 68), k=kk)
        x = (nx or x + tw) + 16
    checks = [("Result first, not a duty", 6.0), ("Only your real numbers", 6.4), ("Strong action verb", 6.8)]
    for i, (tg, st) in enumerate(checks):
        kk = prog(t, st, .4)
        yy = y + 760 + i * 92
        c.check(110, yy + 32, 28, kk)
        c.text(160, yy + 8, tg, F(ISB, 42), WHITE, kk)


# ---------------- S4: product reveal ----------------
PAGE_IMGS = []


def load_pages():
    for n in ["p1.png", "p3.png", "p4.png"]:
        p = os.path.join(PAGES, n)
        PAGE_IMGS.append(Image.open(p).convert("RGB"))


def s4(c, t):
    c.text_c(260, "All 10 prompts. One free PDF.", F(IB, 60), WHITE, prog(t, 0, .4), dy=30)
    fan = ease_io(prog(t, .6, 1.0))
    specs = [(-10, -190, 1), (10, 190, 2), (0, 0, 0)]
    for rot, dx, idx in specs:
        img = PAGE_IMGS[idx]
        h = 820
        sc = h / img.height * back(prog(t, .2, .6), 1.2)
        c.paste_scaled(img.resize((int(img.width * h / img.height), h)), 540 + dx * fan, 900 + abs(dx) * .15 * fan,
                       sc * img.height / h, rot=rot * fan)
    kb = prog(t, 1.6, .4)
    if kb > 0:
        b = Image.new("RGBA", (330, 130), (0, 0, 0, 0))
        dd = ImageDraw.Draw(b)
        dd.rounded_rectangle((0, 0, 329, 129), 65, fill=CY)
        dd.text((62, 14), "FREE", font=F(IB, 88), fill=BG)
        c.paste_scaled(b, 820, 470, back(kb), rot=-8)
    c.text_c(1450, "Copy · fill the [brackets] · done", F(ISB, 44), MUT, prog(t, 2.2, .5))
    c.text_c(1520, "Works with any AI chat", F(ISB, 44), MUT, prog(t, 2.5, .5))


# ---------------- S5: CTA ----------------
def s5(c, t):
    bob = 26 * math.sin(t * 5)
    k = prog(t, .2, .4)
    if k > 0:
        cx, y = 540, 420 + bob
        c.d.polygon([(cx, y - 70), (cx - 80, y + 20), (cx + 80, y + 20)], fill=fade(CY, ease(k)))
        c.d.rectangle((cx - 26, y + 20, cx + 26, y + 140), fill=fade(CY, ease(k)))
    c.text_c(680, "Get the Starter 10", F(IB, 100), WHITE, prog(t, .1, .4), dy=30)
    c.text_c(810, "free — link in bio", F(IB, 100), CY, prog(t, .4, .4), dy=30)
    c.pill(0, 1000, "@aiedge.prompts", F(IB, 60), WHITE, (18, 26, 56), padx=48, pady=26, k=prog(t, .9, .4), center=True)
    mini = [("Clear emails", 1.3), ("Week plan in 2 min", 1.5), ("Stronger resume", 1.7)]
    for i, (m, st) in enumerate(mini):
        kk = prog(t, st, .4)
        c.check(330, 1250 + i * 86 + 30, 24, kk)
        c.text(372, 1250 + i * 86 + 8, m, F(ISB, 42), WHITE, kk)


if __name__ == "__main__":
    which = sys.argv[3].split(",") if len(sys.argv) > 3 else ["1", "2", "3", "4", "5"]
    load_pages()
    jobs = {"1": ("story1_email_demo", s1, 11.5, [2.8, 7.4, 10.8]), "2": ("story2_week_demo", s2, 9.5, [1.8, 4.2, 8.5]),
            "3": ("story3_resume_demo", s3, 8.5, [2.0, 7.6]), "4": ("story4_reveal", s4, 6, [4.5]),
            "5": ("story5_cta", s5, 5, [3.5])}
    for k in which:
        name, fn, secs, prev = jobs[k]
        rc = render(os.path.join(OUT, name + ".mp4"), fn, secs, preview_at=prev)
        print(name, rc)
