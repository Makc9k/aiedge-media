# -*- coding: utf-8 -*-
"""2026-11-24 story 12:35 'prompt hint' (pre-mortem, same prompt as the 18:00 Reel; ref-20261123-10)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "w48v2"))
from kit import *
from common import wcard
from scene_phone_input import input_bar

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "posts", "daily", "2026-11-24")
P = "Imagine this already failed. What went wrong?"


def story(t):
    im = bg(t + 1, a=RED if t < 3.9 else GREEN, b=VIO)
    put(im, strip("Before any big plan, type this:", 980, 58, RED), W / 2 - 400 * (1 - ease(prog(t, 0, .25))), 500)
    n = (t - .8) * 26
    input_bar(im, t, typed=P, chars=n, y_bottom=930, x=30, w=1020, size=56)
    if t >= 2.7:
        put(im, txt("“already failed”", 104, RED, w="black", glow=RED, glow_r=26, glow_a=.9), W / 2, 1100, scale=slam(t, 2.7, .22))
        put(im, txt("AI lists what breaks first", 54, WHITE, w="bold"), W / 2, 1215, alpha=prog(t, 3.0, .25))
    if t >= 3.9:
        put(im, wcard("Then ask for fixes for the top 3", w=920, col=GREEN, size=64, weight="xb", fill_k=.6, pad=40, icon="✅"),
            W / 2, 1400, scale=slam(t, 3.9, .22))
        put(im, chip("Full demo at 18:00 · @aiedge.prompts", 48, fg=BG, bg=CY, glow=CY, padx=34), W / 2, 1590, scale=pop(t, 4.3, .3))
    return im


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    if sys.argv[1:] == ["stills"]:
        stills(story, [.3, 1.8, 3.2, 5.4], "/tmp/s1124.jpg")
    else:
        render(os.path.join(OUT, "story_1124_1235_hint.mp4"), story, 6.0, [0, .25, 2.7, 3.9, 4.3], [2.7, 3.9])
