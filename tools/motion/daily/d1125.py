# -*- coding: utf-8 -*-
"""2026-11-25 — Reel 'LinkedIn headline x5' + stories 12:30 / 12:35.
Structure of ref-20261124-01 (@prompt.editor3, phone chat screen recording): the same input stays attached in the
message bar, a short command is typed on the keyboard, results reveal one by one, ~1.3 s each.
Voice: ElevenLabs 'Liam' (tts_out/2026-11-25_reel.mp3, tightened by build_vo_1125.py). Cuts follow voice segments."""
import sys, os, json, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "w48v2"))
from kit import *
from common import header, cta, wcard
from scene_phone_input import attach_card, input_bar, keyboard

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "..", "posts", "daily", "2026-11-25")
VO = json.load(open(os.path.join(HERE, "assets", "vo_1125.json")))

BEFORE = "Marketing Coordinator at a dental group"
TYPED = "Rewrite my headline 5 ways…"
RES = [("RESULTS-FIRST", CY, "Keeping 6 dental offices in front of their patients through email and social"),
       ("RECRUITER KEYWORDS", VIO, "Marketing Coordinator | Email Marketing · Newsletters · Social Media Management | Healthcare"),
       ("MEMORABLE", GREEN, "I write the emails your dentist sends. All 6 offices."),
       ("FREELANCE", CY, "I run newsletters and social media for dental practices, so the team can stay with patients"),
       ("PLAIN + CONFIDENT", VIO, "Marketing Coordinator. I run email and social for 6 dental offices.")]
PROMPT = ("My headline: [title]. What I actually do: [one line]. Rewrite it 5 ways: results-first, recruiter keywords, "
          "memorable, for freelance clients, plain + confident. Max 120 characters each. "
          "Don't add numbers I didn't give you.")

T_TYPE = VO["one"][0] - .1          # keyboard up, typing
T_SEND = VO["five"][0]              # send + "5 versions"
T_R = [VO[f"r{i}"][0] for i in range(1, 6)]
T_STACK = VO["pick"][0]
T_TAP = T_STACK + .75
T_CTA = VO["cta"][0] - .35          # cta() slams "Free Starter 10" at +.35
END = round(VO["total"] + 1.2, 2)


def attached(struck=1.0):
    return attach_card(BEFORE, w=560, struck=struck, size=44)


def result_card(i, w=960, size=60):
    lab, col, text = RES[i]
    return wcard(text, w=w, col=col, size=size, weight="xb", fill_k=.6, pad=40)


def hook(im, t):
    put(im, txt("Your LinkedIn headline", 84, grad=(CY, VIO), glow=CY, glow_r=20, glow_a=.7), W / 2, 330, scale=slam(t, 0, .2))
    put(im, chip("5 upgrades · 1 prompt", 50, fg=BG, bg=AMBER, glow=AMBER), W / 2, 445, scale=pop(t, .15, .3))
    # before card (red), struck through, shrinks a little
    st = ease(prog(t, .35, .4))
    red = wcard(BEFORE, w=940, col=RED, size=70, weight="xb", fill_k=.55, pad=38)
    put(im, chip("BEFORE", 44, fg=BG, bg=RED), W / 2, 560, scale=pop(t, 0, .25))
    rk = lerp(1.0, .92, ease(prog(t, .8, .3)))
    put_panel_c(im, red, W / 2, 720, rk)
    strike_card(im, BEFORE, 940, 70, 38, W / 2, 720, rk, st)
    # best version punches in
    if t >= .8:
        put(im, chip("AFTER · 1 of 5", 44, fg=BG, bg=GREEN, glow=GREEN), W / 2, 905, scale=pop(t, .8, .25))
        put_panel_c(im, result_card(2, size=70), W / 2, 1110, slam(t, .85, .22))
    input_bar(im, t, attached=attached(st), placeholder="Message AI…", y_bottom=1640)


def strike_card(im, text, w, size, pad, cx, cy, sc, st, weight="xb", width=10):
    """Strike-through drawn over a wcard's own text lines (progress st 0..1 across all lines)."""
    if st <= 0: return
    f = font(weight, size); d = ImageDraw.Draw(im)
    lines = wrap(text, f, w - pad * 2); step = int(size * 1.28)
    th = max(len(lines) * step, int(size * 1.5)); hh = th + pad * 2
    top = cy - hh * sc / 2; left = sum(d.textlength(l, font=f) for l in lines) * st
    for i, l in enumerate(lines):
        lw = d.textlength(l, font=f); seg = min(lw, left); left -= lw
        if seg <= 0: break
        x0 = cx - (w / 2 - pad) * sc; yy = top + (pad + i * step + size * .62) * sc
        d.line((x0 - 6, yy, x0 + seg * sc + 6, yy), fill=RED, width=width)


def put_panel_c(im, sp, cx, cy, scale=1.0, alpha=1.0):
    put(im, sp, cx, cy, scale=scale, alpha=alpha)


def typing(im, t):
    n = (t - T_TYPE - .1) * 38
    sent = t >= T_SEND
    if not sent:
        put(im, txt("One prompt.", 104, grad=(CY, VIO), glow=CY, glow_r=22, glow_a=.7), W / 2, 360, scale=slam(t, T_TYPE + .05, .2))
        put(im, txt("Same input. Short command.", 50, (215, 228, 255), w="bold"), W / 2, 470, alpha=prog(t, T_TYPE + .2, .2))
        f72 = font("black", 88)
        block(im, 80, 600, 920, TYPED, f72, WHITE, 1.2, chars=max(0, n), cursor=True, t=t)
        ky = lerp(1700, 1420, ease(prog(t, T_TYPE, .25)))
        keyboard(im, t, y=ky, pressed=n, text=TYPED)
        input_bar(im, t, attached=attached(), typed=TYPED, chars=n, y_bottom=ky - 15)
    else:
        put(im, txt("5 better versions", 96, grad=(GREEN, CY), glow=GREEN, glow_r=22, glow_a=.7), W / 2, 340, scale=slam(t, T_SEND, .2))
        # user message bubble in chat
        k = ease(prog(t, T_SEND, .25))
        f = font("bold", 50)
        bw = 620
        yb = 470 + 60 * (1 - k)
        put_panel(im, attached(), W - 60 - 560, yb, alpha=k)
        bubble(im, W - 60 - bw, yb + 155, bw, TYPED, f, "user")
        # AI typing dots
        dots = int((t - T_SEND) * 8) % 4
        for i in range(3):
            c = CY if i < dots else (70, 85, 140)
            ImageDraw.Draw(im).ellipse((90 + i * 60, 900, 130 + i * 60, 940), fill=c)
        put(im, chip("writing 5 versions…", 44, fg=WHITE, bg=(40, 52, 110)), 520, 920, alpha=k)
        input_bar(im, t, attached=None, placeholder="Message AI…", y_bottom=1640)


def reveals(im, t):
    i = max(j for j in range(5) if t >= T_R[j])
    lab, col, text = RES[i]
    put(im, chip(f"{i + 1}/5 · {lab}", 54, fg=BG, bg=col, glow=col, padx=36), W / 2, 340, scale=pop(t, T_R[i], .28))
    # progress dots
    d = ImageDraw.Draw(im)
    for j in range(5):
        cx = W / 2 - 120 + j * 60; c = RES[j][1] if j <= i else (60, 70, 110)
        d.ellipse((cx - 14, 440 - 14, cx + 14, 440 + 14), fill=c)
    # previous card flies up & fades
    if i > 0 and t - T_R[i] < .25:
        k = ease(prog(t, T_R[i], .25))
        put(im, result_card(i - 1), W / 2, 860 - 300 * k, alpha=1 - k, scale=1 - .2 * k)
    big = 1.12 if i == 2 else 1.0
    put(im, result_card(i), W / 2, 860, scale=slam(t, T_R[i], .22) * big)
    if i == 2 and t - T_R[i] > .2:
        put(im, emoji("🔥", 90), W / 2 + 430, 700, scale=pop(t, T_R[i] + .2, .3))
    put(im, txt("Max 120 characters · no made-up numbers", 44, (200, 215, 255), w="sb"), W / 2, 1200, alpha=prog(t, T_R[0] + .2, .3))
    input_bar(im, t, attached=attached(), placeholder="Same input, still attached", y_bottom=1640)


def stack(im, t):
    put(im, txt("Pick the one", 92, grad=(CY, VIO), glow=CY, glow_r=20, glow_a=.7), W / 2, 315, scale=slam(t, T_STACK, .2))
    put(im, txt("that sounds like you", 66, WHITE, w="black"), W / 2, 410, scale=slam(t, T_STACK + .12, .2))
    y = 500
    for j in range(5):
        sp = wcard(RES[j][2], w=980, col=RES[j][1], size=44, weight="bold", fill_k=.62, pad=26, num=j + 1)
        h = sp.info["h"]
        k = ease(prog(t, T_STACK + j * .06, .25))
        sc = 1.0
        if j == 2 and t >= T_TAP:
            sc = 1 + .05 * ease(prog(t, T_TAP, .2))
            put_panel(im, panel(980, h, fill=(0, 0, 0), r=32, border=GREEN, bw=8, glow=GREEN, glow_r=30, shadow=False), 50, y)
        put(im, sp, W / 2 + 400 * (1 - k), y + h / 2, scale=sc, alpha=k)
        if j == 2 and t >= T_TAP - .2:
            put(im, emoji("👆", 110), 985, y + h + 30 - 30 * ease(prog(t, T_TAP - .2, .2)))
        y += h + 22


def frame(t):
    if t < T_TYPE:
        im = bg(t, a=RED, b=GREEN, c=VIO); hook(im, t)
    elif t < T_R[0]:
        im = bg(t, a=CY, b=VIO); typing(im, t)
    elif t < T_STACK:
        i = max(j for j in range(5) if t >= T_R[j])
        im = bg(t, a=RES[i][1], b=VIO if RES[i][1] != VIO else CY); reveals(im, t)
    elif t < T_CTA:
        im = bg(t, a=GREEN, b=CY); stack(im, t)
    else:
        im = bg(t, a=CY, b=VIO)
        cta(im, t, T_CTA, tag="LINKEDIN HEADLINE ×5", prompt=PROMPT)
    return im


BEATS = [0, .35, .85, T_TYPE, T_SEND] + T_R + [T_STACK, T_TAP, T_CTA + .35, T_CTA + .65]
FLASH = [.85, T_SEND] + T_R + [T_STACK, T_CTA + .35]
SHAKE = [T_R[2]]


# ---------------- stories ----------------
def story_1230(t):
    """6 s: red card struck (moving from frame 0) → green line zoom-punches → '4 more versions at 18:00'."""
    im = bg(t + 1, a=RED if t < 1.5 else GREEN, b=VIO)
    put(im, chip("LINKEDIN HEADLINE", 54, fg=BG, bg=AMBER, glow=AMBER, padx=36), W / 2, 360, scale=pop(t, 0, .25))
    k = ease(prog(t, 1.35, .3))
    if k < 1:
        put(im, txt("Yours right now:", 74, WHITE, w="black"), W / 2, 560, alpha=1 - k, scale=slam(t, 0, .2))
    yR = lerp(800, 560, k); rk = lerp(lerp(1.06, 1.0, ease(prog(t, 0, .4))), .9, k)
    put(im, wcard(BEFORE, w=920, col=RED, size=76, weight="xb", fill_k=.55, pad=40), W / 2, yR, scale=rk, alpha=1 - .35 * k)
    strike_card(im, BEFORE, 920, 76, 40, W / 2, yR, rk, ease(prog(t, .15, 1.0)), width=13)
    if .5 <= t < 1.5:
        put(im, txt("One prompt fixes this ↓", 66, grad=(CY, GREEN), glow=CY, glow_r=16, glow_a=.6), W / 2, 1180,
            scale=slam(t, .5, .2), alpha=1 - k)
    if t >= 1.5:
        put(im, chip("ONE PROMPT LATER", 50, fg=BG, bg=GREEN, glow=GREEN, padx=34), W / 2, 790, scale=pop(t, 1.5, .25))
        put(im, wcard(RES[2][2], w=960, col=GREEN, size=76, weight="xb", fill_k=.6, pad=44), W / 2, 1040, scale=slam(t, 1.6, .22))
    if t >= 4.0:
        put(im, txt("4 more versions at 18:00", 74, grad=(CY, VIO), glow=CY, glow_r=18, glow_a=.7), W / 2, 1360, scale=slam(t, 4.0, .2))
        put(im, chip("one prompt · @aiedge.prompts", 48, fg=WHITE, bg=(40, 52, 110), padx=32), W / 2, 1490, scale=pop(t, 4.3, .3))
    return im


HINT = "Don't add numbers I didn't give you."
def story_1235(t):
    """6 s: 'Prompt hint' chip → line types into a chat bar → fake stat crossed out → CTA."""
    im = bg(t + 2, a=VIO, b=CY)
    put(im, chip("PROMPT HINT", 62, fg=BG, bg=AMBER, glow=AMBER, padx=44), W / 2, 380, scale=pop(t, 0, .3))
    put(im, txt("End every rewrite with:", 70, WHITE, w="black"), W / 2, 510, scale=slam(t, .15, .2))
    n = (t - .45) * 24
    input_bar(im, t, typed=HINT, chars=n, y_bottom=850, x=30, w=1020, size=52)
    if t >= 2.4:
        put(im, chip("without it, AI may write:", 46, fg=WHITE, bg=(90, 30, 45), padx=30), W / 2, 960, scale=pop(t, 2.4, .25))
        fake = "“Grew patient bookings by 300%”"
        put(im, wcard(fake, w=920, col=RED, size=64, weight="xb", fill_k=.55, pad=40), W / 2, 1120, scale=slam(t, 2.5, .2))
        strike_card(im, fake, 920, 64, 40, W / 2, 1120, 1.0, ease(prog(t, 3.0, .4)), width=12)
        if t >= 3.2:
            put(im, chip("MADE-UP STAT", 46, fg=BG, bg=RED, glow=RED), W / 2 + 260, 1230, scale=pop(t, 3.2, .25), rot=-6)
    if t >= 4.0:
        put(im, txt("Stops made-up stats", 82, grad=(GREEN, CY), glow=GREEN, glow_r=18, glow_a=.7), W / 2, 1380, scale=slam(t, 4.0, .2))
        put(im, chip("Free Starter 10 → link in bio", 52, fg=BG, bg=GREEN, glow=GREEN, padx=36), W / 2, 1510, scale=pop(t, 4.3, .3))
        put(im, txt("@aiedge.prompts", 46, WHITE, w="bold"), W / 2, 1610, alpha=prog(t, 4.6, .3))
    return im


def mux(video, audio):
    tmp = video + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", audio, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-af", "apad", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, video)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    what = sys.argv[1:] or ["reel", "s1", "s2"]
    if "stills" in what:
        stills(frame, [.4, 1.6, 3.0, 4.0, 7.4, 12.2], "/tmp/r1125_stills.jpg")
        stills(story_1230, [.3, 1.0, 2.2, 4.8], "/tmp/s1125a.jpg"); stills(story_1235, [.4, 1.8, 3.5, 5.2], "/tmp/s1125b.jpg")
    if "reel" in what:
        p = os.path.join(OUT, "reel_1125_linkedin_headline.mp4")
        render(p, frame, END, BEATS, FLASH, SHAKE); mux(p, os.path.join(HERE, "assets", "vo_1125.m4a"))
    if "s1" in what:
        render(os.path.join(OUT, "story_1125_1230_teaser.mp4"), story_1230, 6.0, [0, 1.5, 1.6, 4.3], [1.6])
    if "s2" in what:
        render(os.path.join(OUT, "story_1125_1235_hint.mp4"), story_1235, 6.0, [0, .15, 2.5, 3.1, 4.1], [2.5, 4.1])
