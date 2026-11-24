# -*- coding: utf-8 -*-
"""AI Edge motion KIT v3 — bright, punchy brand motion (owner feedback 2026-11-23: "primitive and grey").

Sprite-based: every text/panel is rendered once (with glow / gradient fill) and cached, then
animated by position / scale / alpha. Camera layer adds zoom-punches and white flashes on beats.

    from kit import *
    def frame(t):                      # returns PIL RGB 1080x1920
        im = bg(t)                     # animated saturated glow background
        put(im, txt("HELLO", 120, grad=True, glow=CY), 540, 600, scale=pop(t, 0.2))
        return im
    render("out.mp4", frame, 15, beats=[0, 1.5, 3], flashes=[1.5])

New devices vs engine.py: glow/gradient text sprites, meme caption box (white box, black text),
fast AI typing with cursor, slam-in strips, red→green flip cards, orbiting chips, filling bars,
emoji sprites (Noto Color Emoji), zoom-punch camera + flash, silent AAC track for Instagram.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np, subprocess, math, os

W, H, FPS = 1080, 1920, 30
BG = (7, 11, 24); CY = (34, 211, 238); VIO = (167, 139, 250); GREEN = (52, 211, 153); RED = (248, 113, 113)
AMBER = (251, 191, 36); WHITE = (255, 255, 255); INK = (10, 12, 22); PANEL = (16, 22, 52); PANEL2 = (24, 32, 72)
PINK = (244, 114, 182)
# max on-screen width of a centred sprite body; with the camera zoom-punch (×1.075) it still stays inside 1080 px
SAFE_W = 960

FD = "/usr/share/fonts/opentype/inter/"
FONTS = {"black": FD + "Inter-Black.otf", "xb": FD + "Inter-ExtraBold.otf", "bold": FD + "Inter-Bold.otf",
         "sb": FD + "Inter-SemiBold.otf", "med": FD + "Inter-Medium.otf",
         "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
         "anton": "/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf",
         "sym": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"}
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
_fc, _cache = {}, {}


def font(w, size):
    k = (w, int(size))
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONTS.get(w, w), int(size))
    return _fc[k]


# ---------------- timing ----------------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, s, d): return clamp((t - s) / d) if d > 0 else float(t >= s)
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_io(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def back(x, s=2.2): x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, k): return a + (b - a) * k
def mix(a, b, k): k = clamp(k); return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))
def pop(t, s, d=.35): return back(prog(t, s, d))          # 0 -> overshoot -> 1
def slam(t, s, d=.22):                                     # big -> 1 (scale), for "hit" entrances
    k = prog(t, s, d); return 0 if t < s else lerp(1.9, 1.0, ease(k))
def out(t, s, d=.25): return 1 - ease(prog(t, s, d))


# ---------------- background ----------------
_grid = None
def _grid_layer():
    global _grid
    if _grid is None:
        g = Image.new("RGBA", (W + 80, H + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
        for x in range(0, W + 80, 80): d.line([(x, 0), (x, H + 80)], fill=(120, 150, 255, 16), width=2)
        for y in range(0, H + 80, 80): d.line([(0, y), (W + 80, y)], fill=(120, 150, 255, 16), width=2)
        _grid = g
    return _grid


_yy, _xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)
def bg(t, a=CY, b=VIO, c=None, energy=1.0, grid=True):
    """Saturated animated glow background (computed at 1/4 res, upscaled)."""
    acc = np.zeros((H // 4, W // 4, 3), np.float32) + np.array(BG, np.float32)
    blobs = [(a, .18 + .12 * math.sin(t * .7), .16 + .06 * math.cos(t * .5), 160, .75),
             (b, .84 + .08 * math.cos(t * .6), .82 + .07 * math.sin(t * .45), 180, .68),
             (c or b, .10 + .08 * math.sin(t * .5), .62 + .05 * math.cos(t * .4), 110, .45)]
    for col, fx, fy, r, inten in blobs:
        d2 = ((_xx - fx * W / 4) ** 2 + (_yy - fy * H / 4) ** 2) / (r * r)
        acc += np.exp(-d2)[..., None] * (np.array(col, np.float32) * inten * energy)
    im = Image.fromarray(np.clip(acc, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    if grid:
        off = int(t * 24) % 80
        g = _grid_layer().crop((off, off, off + W, off + H))
        im.paste(g, (0, 0), g)
    return im


# ---------------- sprites ----------------
def _gradient(w, h, c1=CY, c2=VIO, vertical=False):
    k = ("grad", w, h, c1, c2, vertical)
    if k not in _cache:
        n = h if vertical else w
        ramp = np.linspace(0, 1, max(n, 2), dtype=np.float32)[:, None]
        cols = (np.array(c1, np.float32) * (1 - ramp) + np.array(c2, np.float32) * ramp).astype(np.uint8)
        arr = np.repeat(cols[:, None, :], w, 1) if vertical else np.repeat(cols[None, :, :], h, 0).reshape(h, w, 3)
        _cache[k] = Image.fromarray(arr if vertical else arr)
    return _cache[k]


def txt(s, size, color=WHITE, w="black", glow=None, glow_r=22, grad=None, stroke=0, stroke_col=INK, glow_a=1.0):
    """Single-line text sprite (RGBA). grad=(c1,c2) gradient fill; glow=color halo."""
    k = ("txt", s, size, color, w, glow, glow_r, grad, stroke, stroke_col, glow_a)
    if k in _cache: return _cache[k]
    f = font(w, size)
    d0 = ImageDraw.Draw(Image.new("L", (1, 1)))
    l, tp, r, b = d0.textbbox((0, 0), s, font=f, stroke_width=stroke)
    pad = glow_r * 2 + 4 if glow else 6
    tw, th = r - l + pad * 2, b - tp + pad * 2
    mask = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(mask).text((pad - l, pad - tp), s, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
    out_ = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    if glow:
        halo = mask.filter(ImageFilter.GaussianBlur(glow_r)).point(lambda v: min(255, int(v * 1.6 * glow_a)))
        out_.paste(Image.new("RGBA", (tw, th), glow + (255,)), (0, 0), halo)
    if stroke:
        out_.paste(Image.new("RGBA", (tw, th), stroke_col + (255,)), (0, 0), mask)
        inner = Image.new("L", (tw, th), 0)
        ImageDraw.Draw(inner).text((pad - l, pad - tp), s, font=f, fill=255)
        mask = inner
    fill = _gradient(tw, th, *grad).convert("RGBA") if grad else Image.new("RGBA", (tw, th), color + (255,))
    out_.paste(fill, (0, 0), mask)
    _cache[k] = out_
    return out_


def emoji(ch, size):
    k = ("emoji", ch, size)
    if k not in _cache:
        f = ImageFont.truetype(EMOJI, 109)
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
        bb = im.getbbox() or (0, 0, 1, 1)
        im = im.crop(bb)
        sc = size / max(im.size)
        _cache[k] = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    return _cache[k]


def panel(w, h, fill=PANEL, r=36, border=None, bw=5, glow=None, glow_r=28, shadow=True):
    """Rounded panel sprite. border=(c1,c2) gradient ring or a single color; glow=color outer glow."""
    w, h = int(w), int(h)
    k = ("panel", w, h, fill, r, border, bw, glow, glow_r, shadow)
    if k in _cache: return _cache[k]
    pad = glow_r * 2 if (glow or shadow) else 2
    W2, H2 = w + pad * 2, h + pad * 2
    im = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    m = Image.new("L", (W2, H2), 0); ImageDraw.Draw(m).rounded_rectangle((pad, pad, pad + w, pad + h), r, fill=255)
    if shadow:
        sh = Image.new("L", (W2, H2), 0)
        ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 18, pad + w, pad + h + 18), r, fill=170)
        im.paste(Image.new("RGBA", (W2, H2), (0, 0, 0, 255)), (0, 0), sh.filter(ImageFilter.GaussianBlur(glow_r * .8)))
    if glow:
        gl = m.filter(ImageFilter.GaussianBlur(glow_r)).point(lambda v: min(255, int(v * 1.3)))
        im.paste(Image.new("RGBA", (W2, H2), glow + (255,)), (0, 0), gl)
    if border:
        bcol = _gradient(W2, H2, *border).convert("RGBA") if isinstance(border[0], tuple) else Image.new("RGBA", (W2, H2), border + (255,))
        im.paste(bcol, (0, 0), m)
        inner = Image.new("L", (W2, H2), 0)
        ImageDraw.Draw(inner).rounded_rectangle((pad + bw, pad + bw, pad + w - bw, pad + h - bw), max(4, r - bw), fill=255)
        im.paste(Image.new("RGBA", (W2, H2), fill + (255,)), (0, 0), inner)
    else:
        im.paste(Image.new("RGBA", (W2, H2), fill + (255,)), (0, 0), m)
    im.info["pad"] = pad
    _cache[k] = im
    return im


_luts = {}
def put(im, sp, cx, cy, scale=1.0, alpha=1.0, rot=0, anchor="c"):
    """Paste sprite centred at (cx, cy) (anchor 'c'), or top-left 'tl' / top-centre 'tc'."""
    if sp is None or scale <= 0.01 or alpha <= 0.01: return
    if SAFE_W and anchor == "c":           # judge 2026-11-24: zoom-punch must never push text past the frame edge
        body = sp.width - 2 * sp.info.get("pad", 0)
        if body * scale > SAFE_W: scale = SAFE_W / body
    s = sp
    if abs(scale - 1) > 0.004:
        s = sp.resize((max(1, int(sp.width * scale)), max(1, int(sp.height * scale))), Image.BILINEAR)
    if rot: s = s.rotate(rot, expand=True, resample=Image.BICUBIC)
    if alpha < 0.995:
        q = int(alpha * 40)
        if q not in _luts: _luts[q] = [int(v * q / 40) for v in range(256)]
        s = s.copy(); s.putalpha(s.getchannel("A").point(_luts[q]))
    if anchor == "c": x, y = cx - s.width / 2, cy - s.height / 2
    elif anchor == "tc": x, y = cx - s.width / 2, cy
    else: x, y = cx, cy
    im.paste(s, (int(x), int(y)), s)


def put_panel(im, sp, x, y, **kw):
    """Paste panel sprite so that its *body* (not glow pad) top-left is at (x, y)."""
    p = sp.info.get("pad", 0)
    put(im, sp, x - p, y - p, anchor="tl", **kw)


# ---------------- text blocks (drawn directly) ----------------
def wrap(text, f, width):
    d = ImageDraw.Draw(Image.new("L", (1, 1))); out_ = []
    for para in text.split("\n"):
        line = ""
        for wd in para.split(" "):
            tt = (line + " " + wd).strip()
            if d.textlength(tt, font=f) <= width or not line: line = tt
            else: out_.append(line); line = wd
        out_.append(line)
    return out_


def block(im, x, y, width, text, f, fill=WHITE, lh=1.3, chars=None, cursor=False, t=0, align="l", hl=None):
    """Wrapped text. chars = typing limit. hl={word_substring: color} colors whole lines' substrings. Returns bottom y."""
    d = ImageDraw.Draw(im)
    lines = wrap(text, f, width)
    step = int(f.size * lh)
    left = len(text) if chars is None else int(chars)
    yy = y; lastx = x
    for ln in lines:
        if left <= 0 and chars is not None: break
        show = ln[:left]; left -= len(ln) + 1
        xx = x if align == "l" else x + (width - d.textlength(ln, font=f)) / 2
        d.text((xx, yy), show, font=f, fill=fill)
        if hl:
            for sub, col in hl.items():
                i = show.find(sub)
                if i >= 0:
                    d.text((xx + d.textlength(show[:i], font=f), yy), sub, font=f, fill=col)
        lastx = xx + d.textlength(show, font=f); lasty = yy
        yy += step
    if cursor and int(t * 6) % 2 == 0 and chars is not None and chars < len(text):
        ly = yy - step
        d.rounded_rectangle((lastx + 6, ly + 4, lastx + 6 + f.size * .45, ly + f.size * 1.1), 4, fill=CY)
    return y + len(lines) * step


def block_h(text, f, width, lh=1.3): return len(wrap(text, f, width)) * int(f.size * lh)


def meme_box(im, text, y, size=62, alpha=1.0, scale=1.0):
    """White meme caption box (reference device): black bold text, centred, each line its own box."""
    f = font("xb", size); lines = text.split("\n"); d = ImageDraw.Draw(im)
    lh = int(size * 1.42)
    layer = Image.new("RGBA", (W, len(lines) * lh + 60), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    for i, l in enumerate(lines):
        segs = l.split("|")      # "text|🦃" -> emoji appended
        tw = d.textlength(segs[0], font=f) + (size * 1.1 if len(segs) > 1 else 0)
        x = (W - tw) / 2; yy = 20 + i * lh
        ld.rounded_rectangle((x - 30, yy - 6, x + tw + 30, yy + size * 1.3), 20, fill=(255, 255, 255, 255))
        ld.text((x, yy + 2), segs[0], font=f, fill=INK)
        if len(segs) > 1:
            e = emoji(segs[1], int(size * .95)); layer.paste(e, (int(x + tw - size * .98), int(yy + 4)), e)
    put(im, layer, W / 2, y + layer.height / 2 - 20, scale=scale, alpha=alpha)


def chip(s, size=44, fg=INK, bg=CY, w="xb", padx=28, pady=14, glow=None):
    k = ("chip", s, size, fg, bg, w, padx, pady, glow)
    if k in _cache: return _cache[k]
    f = font(w, size); d = ImageDraw.Draw(Image.new("L", (1, 1)))
    tw = int(d.textlength(s, font=f)); hh = int(size * 1.2) + pady * 2
    p = panel(tw + padx * 2, hh, fill=bg, r=hh // 2, glow=glow, glow_r=18, shadow=False).copy()
    pad = p.info["pad"]
    ImageDraw.Draw(p).text((pad + padx, pad + pady + size * .02), s, font=f, fill=fg)
    p.info["pad"] = pad
    _cache[k] = p
    return p


def chat_frame(im, x, y, w, h, title="AI chat", k=1.0):
    """Generic AI chat window (no real product UI)."""
    sp = panel(w, h, fill=(11, 16, 40), r=40, border=(CY, VIO), bw=4, glow=(40, 90, 180), glow_r=30)
    put_panel(im, sp, x, y, alpha=k)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x + 4, y + 4, x + w - 4, y + 96), 36, fill=(20, 28, 66))
    d.rectangle((x + 4, y + 60, x + w - 4, y + 96), fill=(20, 28, 66))
    d.ellipse((x + 32, y + 26, x + 76, y + 70), fill=CY)
    d.text((x + 42, y + 24), "✦", font=font("sym", 32), fill=BG)
    d.text((x + 96, y + 24), title, font=font("bold", 40), fill=WHITE)
    for i, col in enumerate([RED, AMBER, GREEN]):
        d.ellipse((x + w - 150 + i * 40, y + 38, x + w - 128 + i * 40, y + 60), fill=col)
    return (x + 36, y + 130, x + w - 36, y + h - 30)


def bubble(im, x, y, w, text, f, who="user", chars=None, t=0, lh=1.28):
    pad = 28
    lines = wrap(text, f, w - pad * 2)
    if chars is None: nl = len(lines)
    else:
        nl, acc = 0, 0
        for ln in lines:
            if acc >= max(1, int(chars)): break
            nl += 1; acc += len(ln) + 1
    hh = max(1, nl) * int(f.size * lh) + pad * 2
    fill = (10, 70, 92) if who == "user" else (30, 38, 84)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x, y, x + w, y + hh), 30, fill=fill, outline=CY if who == "user" else VIO, width=3)
    block(im, x + pad, y + pad, w - pad * 2, text, f, (225, 250, 255) if who == "user" else WHITE, lh, chars, True, t)
    return y + hh


def strip(text, w, size=46, col=RED, num=None, fg=WHITE, h=None, icon=None):
    """Bright full-saturation strip with number badge (cached)."""
    k = ("strip", text, w, size, col, num, fg, h, icon)
    if k in _cache: return _cache[k]
    f = font("xb", size); hh = h or int(size * 1.9)
    dark = mix(col, BG, .42)
    p = panel(w, hh, fill=dark, r=hh // 3, border=col, bw=4, glow=col, glow_r=16, shadow=False).copy()
    pad = p.info["pad"]; d = ImageDraw.Draw(p)
    x = pad + 22
    if num is not None:
        d.rounded_rectangle((x, pad + 12, x + hh - 24, pad + hh - 12), (hh - 24) // 3, fill=col)
        ns = str(num); nf = font("black", int(size * .9))
        d.text((x + (hh - 24 - d.textlength(ns, font=nf)) / 2, pad + (hh - nf.size * 1.2) / 2), ns, font=nf, fill=BG)
        x += hh + 4
    if icon:
        e = emoji(icon, int(size * 1.1)); p.paste(e, (int(x), int(pad + (hh - e.height) / 2)), e); x += e.width + 18
    d.text((x, pad + (hh - size * 1.2) / 2), text, font=f, fill=fg)
    p.info["pad"] = pad
    _cache[k] = p
    return p


def flip_scale(t, s, d=.4):
    """Card flip: returns (yscale, flipped) — squashes to 0 then reopens."""
    k = prog(t, s, d)
    if k < .5: return 1 - ease_io(k * 2) * 1.0, False
    return ease_io((k - .5) * 2), True


def squash(sp, ys):
    if ys >= .999: return sp
    return sp.resize((sp.width, max(1, int(sp.height * ys))), Image.BILINEAR)


def check_icon(size, col=GREEN, kind="check"):
    k = ("icon", size, col, kind)
    if k in _cache: return _cache[k]
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((0, 0, size - 1, size - 1), fill=col)
    if kind == "check":
        d.line([(size * .27, size * .52), (size * .44, size * .69), (size * .74, size * .33)], fill=BG, width=max(4, size // 8), joint="curve")
    elif kind == "cross":
        a, b = size * .32, size * .68
        d.line([(a, a), (b, b)], fill=BG, width=max(4, size // 8)); d.line([(a, b), (b, a)], fill=BG, width=max(4, size // 8))
    else:
        f = font("black", int(size * .7)); d.text(((size - d.textlength("?", font=f)) / 2, size * .08), "?", font=f, fill=BG)
    _cache[k] = im
    return im


# ---------------- camera + render ----------------
def camera(im, t, beats=(), flashes=(), shake=()):
    z = 1.0
    for b in beats:
        if 0 <= t - b < .5: z = max(z, 1 + .075 * math.exp(-(t - b) / .11))
    dx = dy = 0
    for s in shake:
        if 0 <= t - s < .3:
            a = 14 * math.exp(-(t - s) / .08); dx = a * math.sin(t * 90); dy = a * math.cos(t * 77)
    if z > 1.001 or dx or dy:
        cw, ch = W / z, H / z
        x0, y0 = (W - cw) / 2 + dx, (H - ch) / 2 + dy
        im = im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
    for fl in flashes:
        if 0 <= t - fl < .18:
            a = .55 * math.exp(-(t - fl) / .05)
            im = Image.blend(im, Image.new("RGB", (W, H), WHITE), a)
    return im


def render(path, frame_fn, seconds, beats=(), flashes=(), shake=(), w=W, h=H, sheet=6):
    """Render to mp4 (H.264 + silent AAC stereo, required by Instagram). Saves a 6-frame contact sheet."""
    n = int(round(seconds * FPS))
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(FPS),
           "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-map", "0:v", "-map", "1:a", "-t", f"{n / FPS:.3f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high",
           "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    picks = {int(n * (i + .5) / sheet): i for i in range(sheet)}
    shots = []
    for f in range(n):
        t = f / FPS
        im = camera(frame_fn(t), t, beats, flashes, shake)
        if f in picks: shots.append((t, im.copy()))
        p.stdin.write(im.convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    contact(shots, path.rsplit(".", 1)[0] + "_sheet.jpg")
    return p.returncode


def contact(shots, out_path, cols=3):
    tw = 360; th = int(tw * shots[0][1].height / shots[0][1].width)
    rows = math.ceil(len(shots) / cols)
    sh = Image.new("RGB", (cols * (tw + 12) + 12, rows * (th + 52) + 12), (30, 30, 30)); d = ImageDraw.Draw(sh)
    for i, (t, im) in enumerate(shots):
        x, y = 12 + (i % cols) * (tw + 12), 12 + (i // cols) * (th + 52)
        sh.paste(im.resize((tw, th), Image.LANCZOS), (x, y + 40))
        d.text((x, y + 4), f"t={t:.1f}s", font=font("bold", 28), fill=WHITE)
    sh.save(out_path, quality=88)


def stills(frame_fn, times, out_path):
    contact([(t, frame_fn(t)) for t in times], out_path)
