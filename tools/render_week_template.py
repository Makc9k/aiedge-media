"""AI Edge — week 1 posts, 1080x1350."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1350
BG, CYAN, VIO, TXT, MUT, CARD = "#070B18", "#22D3EE", "#A78BFA", "#FFFFFF", "#9FB3D9", "#0F1630"
IB = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
ISB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
IM = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
HANDLE = "@aiedge.prompts"
M = 90
F = lambda p, s: ImageFont.truetype(p, s)


def wrap(d, text, font, width):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split(" "):
            t = (line + " " + w).strip()
            if d.textlength(t, font=font) <= width:
                line = t
            else:
                out.append(line)
                line = w
        out.append(line)
    return out


def base(tag, n):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    # subtle grid
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill="#0B1124")
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill="#0B1124")
    d.rounded_rectangle((M, 80, M + d.textlength(tag, font=F(ISB, 28)) + 44, 132), 26, outline=CYAN, width=2)
    d.text((M + 22, 88), tag, font=F(ISB, 28), fill=CYAN)
    d.text((W - M - d.textlength(n, font=F(ISB, 28)), 90), n, font=F(ISB, 28), fill=MUT)
    # footer
    d.line([(M, H - 120), (W - M, H - 120)], fill="#1E2A4A", width=2)
    d.text((M, H - 92), "⚡", font=F("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 34), fill=CYAN)
    d.text((M + 48, H - 92), HANDLE, font=F(ISB, 32), fill=TXT)
    s = "Save for later →"
    d.text((W - M - d.textlength(s, font=F(IM, 30)), H - 90), s, font=F(IM, 30), fill=MUT)
    return im, d


def title(d, y, text, size=88, hl=None):
    f = F(IB, size)
    for line in wrap(d, text, f, W - 2 * M):
        x = M
        for i, word in enumerate(line.split(" ")):
            col = CYAN if hl and word.strip(".,:?!").lower() in hl else TXT
            d.text((x, y), word, font=f, fill=col)
            x += d.textlength(word + " ", font=f)
        y += int(size * 1.1)
    return y


def body(d, y, text, size=40, col=MUT, font=IM, width=None):
    f = F(font, size)
    for line in wrap(d, text, f, width or (W - 2 * M)):
        d.text((M, y), line, font=f, fill=col)
        y += int(size * 1.4)
    return y


def prompt_card(d, y, text, label="PROMPT — copy it", size=34):
    f = F(MONO, size)
    lines = wrap(d, text, f, W - 2 * M - 80)
    h = 90 + len(lines) * int(size * 1.45) + 30
    d.rounded_rectangle((M, y, W - M, y + h), 24, fill=CARD, outline="#1E2A4A", width=2)
    d.text((M + 40, y + 32), label, font=F(ISB, 26), fill=VIO)
    yy = y + 90
    for l in lines:
        d.text((M + 40, yy), l, font=f, fill="#E6F6FB")
        yy += int(size * 1.45)
    return y + h


os.makedirs("ai_week1", exist_ok=True)

# 01 — prompt formula
im, d = base("PROMPT BASICS", "01/07")
y = title(d, 200, "Better prompts have 4 parts.", 96, {"4"})
y += 60
rows = [("ROLE", "Who should the AI be?", "“Act as a senior copywriter…”"),
        ("TASK", "What exactly to do?", "“Write 3 subject lines…”"),
        ("CONTEXT", "What does it need to know?", "“For a $9 budget planner, US moms…”"),
        ("FORMAT", "How should the answer look?", "“A table: line · why it works”")]
for k, q, ex in rows:
    d.rounded_rectangle((M, y, W - M, y + 170), 22, fill=CARD)
    d.text((M + 36, y + 30), k, font=F(IB, 40), fill=CYAN)
    d.text((M + 300, y + 32), q, font=F(ISB, 36), fill=TXT)
    d.text((M + 300, y + 92), ex, font=F(IM, 30), fill=MUT)
    y += 192
im.save("ai_week1/01_mon.jpg", quality=92)

# 02 — let AI interview you
im, d = base("PROMPT TRICK", "02/07")
y = title(d, 200, "Let the AI interview you first.", 92, {"interview"})
y = body(d, y + 30, "Vague request = generic answer. Make it ask for the details it’s missing before it writes anything.")
y = prompt_card(d, y + 50, "Before you answer, ask me up to 5 questions you need to do this really well. Wait for my answers, then do the task: [your task]")
body(d, y + 50, "Works for: cover letters, plans, ads, emails, code.", 36, TXT, ISB)
im.save("ai_week1/02_tue.jpg", quality=92)

# 03 — messy email
im, d = base("WORKFLOW", "03/07")
y = title(d, 200, "Messy email → clear email in 10 seconds.", 88, {"clear"})
y = prompt_card(d, y + 50, "Rewrite this email so it is clear and polite. Put the main request in the first sentence. Max 5 sentences. Keep my facts, don't invent anything.\n\n[paste your email]")
body(d, y + 50, "The last line matters: tell it not to invent facts.", 36, TXT, ISB)
im.save("ai_week1/03_wed.jpg", quality=92)

# 04 — examples beat adjectives
im, d = base("PROMPT RULE", "04/07")
y = title(d, 200, "Show examples. Skip the adjectives.", 92, {"examples"})
y += 40
d.rounded_rectangle((M, y, W - M, y + 200), 22, fill=CARD, outline="#3B1F2B", width=2)
d.text((M + 36, y + 26), "✗", font=F("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36), fill="#F87171"); d.text((M + 80, y + 28), "WEAK", font=F(IB, 34), fill="#F87171")
d.text((M + 36, y + 96), "“Write a catchy, fun, engaging caption.”", font=F(IM, 36), fill=TXT)
y += 230
d.rounded_rectangle((M, y, W - M, y + 330), 22, fill=CARD, outline="#164E58", width=2)
d.text((M + 36, y + 26), "✓", font=F("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36), fill=CYAN); d.text((M + 80, y + 28), "STRONG", font=F(IB, 34), fill=CYAN)
f = F(IM, 34)
yy = y + 90
for l in wrap(d, "“Write 5 captions in the style of these two:\n1) [your best caption]\n2) [another one you like]”", f, W - 2 * M - 72):
    d.text((M + 36, yy), l, font=f, fill=TXT)
    yy += 48
body(d, y + 370, "AI copies patterns better than it guesses taste.", 36, MUT, IM)
im.save("ai_week1/04_thu.jpg", quality=92)

# 05 — self-critique
im, d = base("QUALITY BOOST", "05/07")
y = title(d, 200, "Make the AI criticise its own draft.", 90, {"criticise"})
y = body(d, y + 30, "First drafts are average. One extra message makes them sharper.")
y = prompt_card(d, y + 50, "List the 3 weakest points of your answer above, honestly. Then rewrite it fixing all 3.")
body(d, y + 50, "Use it on anything that matters before you hit send.", 36, TXT, ISB)
im.save("ai_week1/05_fri.jpg", quality=92)

# 06 — weekly planning
im, d = base("WEEKEND WORKFLOW", "06/07")
y = title(d, 200, "Plan your whole week in 2 minutes.", 90, {"2"})
y = prompt_card(d, y + 50, "Here is my to-do list. Sort it into: urgent, important, can wait, delete. Estimate time for each. Then build a Mon–Fri plan with max 4 hours of focused work per day.\n\n[paste your list]")
body(d, y + 50, "You decide. The AI just does the sorting.", 36, TXT, ISB)
im.save("ai_week1/06_sat.jpg", quality=92)

# 07 — recap + CTA
im, d = base("WEEK 1 RECAP", "07/07")
y = title(d, 200, "6 prompts to save this week:", 92, {"6"})
y += 30
for i, t in enumerate(["4-part prompt formula", "Let AI interview you", "Messy → clear email", "Examples > adjectives", "Self-critique pass", "2-minute week plan"], 1):
    d.text((M, y), f"0{i}", font=F(IB, 44), fill=CYAN)
    d.text((M + 100, y + 4), t, font=F(ISB, 42), fill=TXT)
    y += 80
y += 40
d.rounded_rectangle((M, y, W - M, y + 170), 26, fill=CYAN)
d.text((M + 44, y + 30), "Free AI prompt pack — coming soon", font=F(IB, 40), fill=BG)
d.text((M + 44, y + 96), "Follow so you don't miss it ⚡".replace("⚡", ""), font=F(ISB, 34), fill=BG)
im.save("ai_week1/07_sun.jpg", quality=92)

# contact sheet
ims = [Image.open(f"ai_week1/{n}") for n in sorted(os.listdir("ai_week1")) if n.endswith(".jpg")]
sheet = Image.new("RGB", (4 * 360 + 50, 2 * 450 + 30), "#222")
for i, p in enumerate(ims):
    sheet.paste(p.resize((360, 450)), (10 + (i % 4) * 370, 10 + (i // 4) * 460))
sheet.save("ai_week1_sheet.png")
print("ok", len(ims))
