# -*- coding: utf-8 -*-
"""Phone chat 'screen recording' device (ref-20261124-01 @prompt.editor3): the SAME input stays attached
in the message bar (like a photo thumbnail), a short prompt is typed on an on-screen keyboard, send tap,
results reveal one by one. Generic UI only (no real product look).

    from scene_phone_input import input_bar, keyboard, attach_card
    y_top = input_bar(im, t, attached=attach_card("Marketing Coordinator…"), typed="Rewrite my…", chars=n, sent=False)
    keyboard(im, t, y=1440, pressed=n)          # key flashes while typing
"""
from kit import *

KEYS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]


def attach_card(text, w=300, col=RED, struck=0.0, size=34):
    """Small 'attachment thumbnail' with the user's input (red = before). struck 0..1 draws a strike line."""
    f = font("bold", size); th = block_h(text, f, w - 40, 1.2)
    hh = th + 40
    sp = panel(w, hh, fill=mix(col, BG, .55), r=22, border=col, bw=4, shadow=False).copy()
    pd = sp.info["pad"]
    block(sp, pd + 20, pd + 20, w - 40, text, f, (255, 230, 230), 1.2)
    if struck > 0:
        d = ImageDraw.Draw(sp)
        lines = wrap(text, f, w - 40); step = int(size * 1.2)
        tot = sum(d.textlength(l, font=f) for l in lines); left = tot * struck
        for i, l in enumerate(lines):
            lw = d.textlength(l, font=f); seg = min(lw, left); left -= lw
            if seg <= 0: break
            yy = pd + 20 + i * step + size * .62
            d.line((pd + 16, yy, pd + 24 + seg, yy), fill=RED, width=7)
    sp.info["pad"] = pd; sp.info["h"] = hh
    return sp


def input_bar(im, t, attached=None, typed="", chars=None, sent=False, y_bottom=1420, x=40, w=1000, placeholder="Message AI…", size=44):
    """Message bar anchored at its bottom edge. Returns the bar's top y."""
    f = font("med", size); lh_ = int(size * 1.27)
    ah = attached.info["h"] + 30 if attached is not None else 0
    txt_ = typed if not sent else ""
    shown = txt_ if chars is None else txt_[:int(max(0, chars))]
    lines = wrap(shown or placeholder, f, w - 200)[-3:]
    hh = 40 + ah + len(lines) * lh_ + 24
    y0 = y_bottom - hh
    put_panel(im, panel(w, hh, fill=(22, 30, 66), r=44, border=(CY, VIO), bw=3, glow=(40, 80, 170), glow_r=18, shadow=False), x, y0)
    if attached is not None:
        put_panel(im, attached, x + 30, y0 + 24)
    d = ImageDraw.Draw(im); yy = y0 + 28 + ah
    for l in lines:
        d.text((x + 40, yy), l, font=f, fill=WHITE if shown else (150, 165, 210)); yy += lh_
    if shown and chars is not None and chars < len(txt_) and int(t * 6) % 2 == 0:
        lx = x + 40 + d.textlength(lines[-1], font=f)
        d.rounded_rectangle((lx + 6, yy - lh_ + 4, lx + 26, yy - 6), 4, fill=CY)
    # send button
    bx, by = x + w - 92, y_bottom - 92
    pressed = sent and t % 100 < 9e9
    d.ellipse((bx, by, bx + 72, by + 72), fill=GREEN if shown or sent else (60, 70, 110))
    d.polygon([(bx + 24, by + 18), (bx + 56, by + 36), (bx + 24, by + 54)], fill=BG)
    return y0


def keyboard(im, t, y=1440, pressed=None, alpha=1.0, text=""):
    """Generic on-screen keyboard (3 rows + space). pressed = char index typed so far -> flashes that key."""
    if alpha <= 0.01: return
    layer = Image.new("RGBA", (W, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.rounded_rectangle((20, 0, W - 20, 228), 30, fill=(14, 19, 44, 245))
    cur = None
    if pressed is not None and text and 0 <= int(pressed) < len(text): cur = text[int(pressed)].lower()
    kf = font("sb", 34)
    for r, row in enumerate(KEYS):
        kw = 92; gap = 8; tot = len(row) * kw + (len(row) - 1) * gap; x0 = (W - tot) / 2
        for i, ch in enumerate(row):
            xx = x0 + i * (kw + gap); yy = 14 + r * 54
            on = (ch == cur)
            d.rounded_rectangle((xx, yy, xx + kw, yy + 46), 10, fill=CY if on else (38, 48, 92))
            d.text((xx + kw / 2 - d.textlength(ch, font=kf) / 2, yy + 4), ch, font=kf, fill=BG if on else (215, 225, 255))
    on = cur == " "
    d.rounded_rectangle((300, 14 + 3 * 54, 780, 14 + 3 * 54 + 46), 10, fill=CY if on else (38, 48, 92))
    put(im, layer, W / 2, y + 115, alpha=alpha)
