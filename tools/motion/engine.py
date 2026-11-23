# -*- coding: utf-8 -*-
"""AI Edge motion engine — Pillow + ffmpeg. 1080x1920 (stories/reels) or 1080x1350.

Usage:
    from engine import *
    def scene(c, t):            # c = Canvas for this frame, t = seconds
        c.title(...)
    render("out.mp4", scene, seconds=8)

Design: dark #070B18 background with drifting grid, cyan #22D3EE accent, violet #A78BFA secondary,
green #34D399 for "after/fixed", red #F87171 for "before/problem". Fonts: Inter + DejaVu Sans Mono.
Instagram safe zone for stories: keep important content between y=250 and y=1650.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess, math, random, os

W, H, FPS = 1080, 1920, 30
BG = (7, 11, 24); CY = (34, 211, 238); VIO = (167, 139, 250); MUT = (159, 179, 217)
CARD = (15, 22, 48); LINE = (30, 42, 74); WHITE = (255, 255, 255)
GREEN = (52, 211, 153); RED = (248, 113, 113); AMBER = (251, 191, 36); PAPER = (246, 248, 252); INK = (11, 17, 36)

FD = "/usr/share/fonts/opentype/inter/"
IB, ISB, IM = FD + "Inter-Black.otf", FD + "Inter-SemiBold.otf", FD + "Inter-Medium.otf"
IBOLD = FD + "Inter-Bold.otf" if os.path.exists(FD + "Inter-Bold.otf") else ISB
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SYM = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_fc = {}


def F(path, size):
    k = (path, int(size))
    if k not in _fc:
        _fc[k] = ImageFont.truetype(path, int(size))
    return _fc[k]


# ---------- timing ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, start, dur): return clamp((t - start) / dur) if dur > 0 else float(t >= start)
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_io(x): x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def back(x, s=1.7): x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, k): return a + (b - a) * k
def mix(c1, c2, k): return tuple(int(lerp(c1[i], c2[i], clamp(k))) for i in range(3))
def fade(col, k): return mix(BG, col, k)


def wrap(d, text, font, width):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split(" "):
            tt = (line + " " + w).strip()
            if d.textlength(tt, font=font) <= width or not line:
                line = tt
            else:
                out.append(line); line = w
        out.append(line)
    return out


_shadow = {}
def shadow(w, h, r=28, blur=26, alpha=150):
    k = (w, h, r, blur, alpha)
    if k not in _shadow:
        pad = blur * 2
        s = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
        ImageDraw.Draw(s).rounded_rectangle((pad, pad + 14, pad + w, pad + h + 14), r, fill=(0, 0, 0, alpha))
        _shadow[k] = (s.filter(ImageFilter.GaussianBlur(blur)), pad)
    return _shadow[k]


class Canvas:
    def __init__(self, f, t, w=W, h=H, grid=True):
        self.f, self.t, self.w, self.h = f, t, w, h
        self.im = Image.new("RGB", (w, h), BG)
        self.d = ImageDraw.Draw(self.im)
        if grid:
            off = (f * 1.2) % 60
            for x in range(0, w + 60, 60):
                self.d.line([(x - off, 0), (x - off, h)], fill=(11, 17, 36))
            for y in range(0, h + 60, 60):
                self.d.line([(0, y - off), (w, y - off)], fill=(11, 17, 36))
            # soft glow blob
            gx, gy = w * 0.5 + 220 * math.sin(t * 0.4), h * 0.35 + 160 * math.cos(t * 0.33)
            for r, a in [(520, 10), (380, 14), (240, 18)]:
                self.d.ellipse((gx - r, gy - r, gx + r, gy + r), fill=mix(BG, (14, 60, 80), a / 60))

    # ----- text -----
    def text_c(self, y, text, font, fill, k=1.0, dy=0):
        if k <= 0: return
        w = self.d.textlength(text, font=font)
        self.d.text(((self.w - w) / 2, y + dy * (1 - ease(k))), text, font=font, fill=fade(fill, ease(k)))

    def text(self, x, y, text, font, fill, k=1.0):
        if k <= 0: return
        self.d.text((x, y), text, font=font, fill=fade(fill, ease(k)))

    def block(self, x, y, width, text, font, fill, lh=1.38, chars=None, cursor=False):
        """Draw wrapped text; chars limits visible characters (typing). Returns bottom y."""
        if chars is not None:
            text = text[:max(0, int(chars))]
        lines = wrap(self.d, text, font, width) if text else [""]
        step = int(font.size * lh)
        for i, ln in enumerate(lines):
            self.d.text((x, y + i * step), ln, font=font, fill=fill)
        if cursor and (self.f // 8) % 2 == 0:
            lw = self.d.textlength(lines[-1], font=font)
            yy = y + (len(lines) - 1) * step
            self.d.rectangle((x + lw + 4, yy + 4, x + lw + 4 + font.size * 0.5, yy + font.size * 1.1), fill=CY)
        return y + len(lines) * step

    def block_h(self, width, text, font, lh=1.38):
        return len(wrap(self.d, text, font, width)) * int(font.size * lh)

    # ----- shapes -----
    def card(self, box, fill=CARD, r=28, outline=None, width=3, shadow_on=True):
        x0, y0, x1, y1 = [int(v) for v in box]
        if shadow_on and x1 > x0 and y1 > y0:
            s, pad = shadow(x1 - x0, y1 - y0, r)
            self.im.paste(s, (x0 - pad, y0 - pad), s)
            self.d = ImageDraw.Draw(self.im)
        self.d.rounded_rectangle((x0, y0, x1, y1), r, fill=fill, outline=outline, width=width)

    def pill(self, x, y, text, font, fg, bg, padx=24, pady=12, k=1.0, center=False):
        if k <= 0: return
        tw = self.d.textlength(text, font=font)
        if center: x = (self.w - tw) / 2 - padx
        self.d.rounded_rectangle((x, y, x + tw + padx * 2, y + font.size + pady * 2), (font.size + pady * 2) // 2,
                                 fill=fade(bg, ease(k)))
        self.d.text((x + padx, y + pady - font.size * 0.08), text, font=font, fill=fade(fg, ease(k)))
        return x + tw + padx * 2

    def check(self, cx, cy, r, k, col=GREEN):
        if k <= 0: return
        s = back(k)
        rr = r * s
        self.d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=col)
        if k > 0.3:
            kk = ease((k - 0.3) / 0.7)
            p1, p2, p3 = (cx - r * .45, cy), (cx - r * .1, cy + r * .38), (cx + r * .5, cy - r * .35)
            if kk < .4:
                pts = [p1, (lerp(p1[0], p2[0], kk / .4), lerp(p1[1], p2[1], kk / .4))]
            else:
                q = (kk - .4) / .6
                pts = [p1, p2, (lerp(p2[0], p3[0], q), lerp(p2[1], p3[1], q))]
            self.d.line(pts, fill=BG, width=max(3, int(r * .22)), joint="curve")

    def cross(self, cx, cy, r, k, col=RED):
        if k <= 0: return
        rr = r * back(k)
        self.d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=col)
        a = r * .35 * ease(k)
        self.d.line([(cx - a, cy - a), (cx + a, cy + a)], fill=BG, width=max(3, int(r * .2)))
        self.d.line([(cx - a, cy + a), (cx + a, cy - a)], fill=BG, width=max(3, int(r * .2)))

    def underline(self, x0, x1, y, k, col=RED, width=5, wavy=True):
        if k <= 0: return
        xe = lerp(x0, x1, ease(k))
        if wavy:
            pts = [(x, y + 4 * math.sin((x - x0) / 9)) for x in range(int(x0), int(xe) + 1, 3)]
            if len(pts) > 1: self.d.line(pts, fill=col, width=width)
        else:
            self.d.line([(x0, y), (xe, y)], fill=col, width=width)

    def paste_scaled(self, img, cx, cy, scale, rot=0):
        if scale <= 0.01: return
        im = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.LANCZOS)
        if rot:
            im = im.convert("RGBA").rotate(rot, expand=True, resample=Image.BICUBIC)
        if im.mode != "RGBA": im = im.convert("RGBA")
        self.im.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)
        self.d = ImageDraw.Draw(self.im)

    def progress_dots(self, n, i, y=1700):
        for j in range(n):
            x = self.w / 2 + (j - (n - 1) / 2) * 34
            self.d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=CY if j == i else LINE)


def chat_window(c, box, title="AI chat", k=1.0):
    """Generic AI chat window frame (not imitating any real product). Returns inner content box."""
    x0, y0, x1, y1 = box
    c.card(box, fill=(12, 18, 40), outline=LINE)
    c.d.rounded_rectangle((x0, y0, x1, y0 + 84), 28, fill=(18, 26, 56))
    c.d.rectangle((x0, y0 + 50, x1, y0 + 84), fill=(18, 26, 56))
    c.d.ellipse((x0 + 30, y0 + 24, x0 + 66, y0 + 60), fill=CY)
    c.d.text((x0 + 39, y0 + 22), "✦", font=F(SYM, 28), fill=BG)
    c.d.text((x0 + 84, y0 + 24), title, font=F(ISB, 34), fill=WHITE)
    return (x0 + 30, y0 + 110, x1 - 30, y1 - 30)


def bubble(c, x, y, width, text, font, who="user", chars=None, cursor=False):
    """Chat bubble; who='user' (right, cyan tint) or 'ai' (left, dark). Returns bottom y."""
    pad = 26
    shown = text if chars is None else text[:max(0, int(chars))]
    tw = width - pad * 2
    h = max(c.block_h(tw, text, font), int(font.size * 1.38)) + pad * 2
    if who == "user":
        fill, col = (8, 51, 68), (220, 248, 255)
    else:
        fill, col = (24, 32, 64), WHITE
    c.d.rounded_rectangle((x, y, x + width, y + h), 26, fill=fill)
    c.block(x + pad, y + pad, tw, shown, font, col, cursor=cursor)
    return y + h


def render(path, scene, seconds, w=W, h=H, preview_at=None, music=None):
    n = int(seconds * FPS)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-"]
    if music and os.path.exists(music):
        cmd += ["-i", music, "-af", f"afade=t=out:st={seconds-1}:d=1", "-shortest"]
    else:
        cmd += ["-f", "lavfi", "-t", str(seconds), "-i", "anullsrc=r=44100:cl=stereo", "-shortest"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    prev = preview_at if preview_at is not None else [seconds * 0.85]
    prev_frames = {int(s * FPS): i for i, s in enumerate(prev)}
    for f in range(n):
        c = Canvas(f, f / FPS, w, h)
        scene(c, f / FPS)
        if f in prev_frames:
            c.im.save(path.replace(".mp4", f"_p{prev_frames[f]}.jpg"), quality=85)
        p.stdin.write(c.im.tobytes())
    p.stdin.close(); p.wait()
    return p.returncode
