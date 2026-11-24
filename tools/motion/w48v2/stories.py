# -*- coding: utf-8 -*-
"""Stories 24–30.11 (12:30). Re-cut shots from the reels/carousels + story CTA. 1080x1920, safe zone 250–1650."""
from common import *
import r1_thanksgiving as r1, r2_email as r2, r3_blackfriday as r3, r4_dinners as r4, r5_monday as r5

CAR = OUT


def story_cta(line, tag=None):
    def f(t):
        im = bg(t + 3, a=CY, b=VIO)
        cta(im, t, 0, tag=tag, sub=line)
        return im
    return f


def still_anim(path, mode="pan", dur=6):
    src = Image.open(os.path.join(CAR, path)).convert("RGB")
    def f(t):
        im = bg(t, a=CY, b=VIO)
        if mode == "pan":      # full cheat-sheet, highlight sweeps cell by cell (numbers flash)
            im.paste(src, (0, 285))
            i = int(clamp((t - .3) / (dur - 1.0)) * 10 - 1e-6) if t > .3 else -1
            if i >= 0:
                col, row = i // 5, i % 5
                x, y = 40 + 30 + col * 470, 285 + 350 + 20 + row * 172
                lt = (t - .3) % ((dur - 1.0) / 10)
                ring = panel(470, 168, fill=(0, 0, 0), r=24, border=[CY, VIO, GREEN, AMBER, PINK][i % 5], bw=7,
                             glow=[CY, VIO, GREEN, AMBER, PINK][i % 5], glow_r=18, shadow=False)
                hole = ring.copy(); pd = ring.info["pad"]
                m = Image.new("L", hole.size, 255); ImageDraw.Draw(m).rounded_rectangle((pd + 7, pd + 7, pd + 463, pd + 161), 18, fill=0)
                hole.putalpha(Image.fromarray(np.minimum(np.array(hole.getchannel("A")), np.array(m))))
                put(im, hole, x + 235, y + 84, scale=1 + .06 * math.exp(-lt / .1))
        else:                  # pop the slide in
            s = slam(t, 0, .25) * .98
            put(im, src.convert("RGBA"), W / 2, 960, scale=s)
        return im
    return f


def seq(parts):
    """parts: (frame_fn, t0, t1, beats_src). Returns frame fn, total, beats."""
    total = sum(p[2] - p[1] for p in parts)
    starts, acc = [], 0
    for p in parts: starts.append(acc); acc += p[2] - p[1]
    beats = list(starts)
    for (fn, a, b, bsrc), s in zip(parts, starts):
        beats += [s + x - a for x in bsrc if a <= x < b]
    def f(t):
        for (fn, a, b, _), s in zip(parts, starts):
            if t < s + (b - a): return fn(a + t - s)
        fn, a, b, _ = parts[-1]; return fn(b)
    return f, total, sorted(set(beats)), starts[1:]


CTA_R = "Full prompt in today's Reel"
STORIES = {
    "s1_1124": [(r1.frame, 0, 3.2, r1.BEATS), (r1.frame, 8.3, 12.2, r1.BEATS), (story_cta(CTA_R, "PROMPT #10"), 0, 3.6, [0, .35, .65])],
    "s2_1125": [(still_anim("c1_1125_cheatsheet_1.jpg", "pan", 6.5), 0, 6.5, [0, 2, 4]),
                (story_cta("Full cheat sheet in today's post", "10 PROMPTS · 1 PAGE"), 0, 3.6, [0, .35, .65])],
    "s3_1126": [(r2.frame, 0, 1.6, r2.BEATS), (r2.frame, 5.3, 8.3, r2.BEATS), (r2.frame, 8.3, 11.6, r2.BEATS),
                (story_cta(CTA_R, "PROMPT #01"), 0, 3.6, [0, .35, .65])],
    "s4_1127": [(r3.frame, 0, 2.0, r3.BEATS), (r3.frame, 5.0, 8.6, r3.BEATS), (r3.frame, 9.0, 12.0, r3.BEATS),
                (story_cta(CTA_R, "PROMPT #09"), 0, 3.6, [0, .35, .65])],
    "s5_1128": [(still_anim("c2_1128_resume_1.jpg", "pop"), 0, 3.0, [0]), (still_anim("c2_1128_resume_4.jpg", "pop"), 0, 4.0, [0]),
                (still_anim("c2_1128_resume_5.jpg", "pop"), 0, 4.0, [0]),
                (story_cta("Full prompt in today's post", "PROMPT #05"), 0, 3.6, [0, .35, .65])],
    "s6_1129": [(r4.frame, 0, 1.5, r4.BEATS), (r4.frame, 4.1, 8.6, r4.BEATS), (r4.frame, 9.1, 12.6, r4.BEATS),
                (story_cta(CTA_R, "PROMPT #08"), 0, 3.6, [0, .35, .65])],
    "s7_1130": [(r5.frame, 0, 1.6, r5.BEATS), (r5.frame, 1.6, 7.2, r5.BEATS), (r5.frame, 7.2, 10.6, r5.BEATS),
                (story_cta(CTA_R, "PROMPT #03"), 0, 3.6, [0, .35, .65])],
}

if __name__ == "__main__":
    only = sys.argv[1:]
    for name, parts in STORIES.items():
        if only and name not in only: continue
        f, total, beats, cuts = seq(parts)
        render(os.path.join(OUT, f"{name}_story.mp4"), f, round(total, 2), beats, cuts)
        print(name, round(total, 1))
