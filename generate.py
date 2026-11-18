#!/usr/bin/env python3
"""Generate entry.png: a one-page newspaper front page summing up the world
news of Tuesday 17 November 2026. All stories are real events reported that
day (BBC, AP, Reuters, Al Jazeera, ABC News, Just Security). Output: 1024x1024
PNG, well under the 1 MiB gate limit. Run: python3 generate.py"""
import math
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (26, 26, 26)
RED = (179, 38, 30)
BLUE = (29, 78, 137)
GOLD = (176, 132, 24)
GREY = (90, 88, 82)
LIGHT = (232, 226, 214)
SEA = (52, 110, 150)
SKY = (214, 230, 240)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning list of lines fitting width px."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=4, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


# ---------------- icons (flat, drawn in a coloured disc) ----------------
def icon_bridge(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 52, 44))
    # sea
    d.rectangle([cx - r, cy + r * 0.45, cx + r, cy + r * 0.62], fill=SEA)
    # deck, broken in the middle
    d.rectangle([cx - r * 0.82, cy + r * 0.28, cx - r * 0.12, cy + r * 0.38], fill=(255, 255, 255))
    d.rectangle([cx + r * 0.12, cy + r * 0.28, cx + r * 0.82, cy + r * 0.38], fill=(255, 255, 255))
    # towers
    for tx in (-0.62, 0.62):
        d.rectangle([cx + r * tx - 3, cy - r * 0.55, cx + r * tx + 3, cy + r * 0.3], fill=(255, 255, 255))
    # cables
    d.line([cx - r * 0.62, cy - r * 0.55, cx - r * 0.12, cy + r * 0.28], fill=(255, 255, 255), width=2)
    d.line([cx + r * 0.62, cy - r * 0.55, cx + r * 0.12, cy + r * 0.28], fill=(255, 255, 255), width=2)
    # explosion burst in the gap
    bx, by = cx, cy - r * 0.05
    for ang in range(0, 360, 45):
        import math
        x2 = bx + r * 0.42 * math.cos(math.radians(ang))
        y2 = by + r * 0.42 * math.sin(math.radians(ang))
        d.line([bx, by, x2, y2], fill=(255, 200, 40), width=4)
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(255, 200, 40))
    # smoke
    d.ellipse([cx - r * 0.35, cy - r * 0.75, cx - r * 0.05, cy - r * 0.45], fill=(200, 200, 200))
    d.ellipse([cx + r * 0.05, cy - r * 0.85, cx + r * 0.35, cy - r * 0.55], fill=(220, 220, 220))


def icon_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE)
    d.ellipse([cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.62], outline=(255, 255, 255), width=3)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=3)
    d.ellipse([cx - r * 0.28, cy - r * 0.62, cx + r * 0.28, cy + r * 0.62], outline=(255, 255, 255), width=3)
    d.ellipse([cx + r * 0.45, cy - r * 0.75, cx + r * 0.75, cy - r * 0.45], fill=(255, 200, 40))


def icon_tanker(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(20, 90, 110))
    # hull
    d.polygon([(cx - r * 0.75, cy + r * 0.1), (cx + r * 0.75, cy + r * 0.1),
               (cx + r * 0.55, cy + r * 0.5), (cx - r * 0.55, cy + r * 0.5)], fill=(255, 255, 255))
    d.rectangle([cx - r * 0.45, cy - r * 0.25, cx + r * 0.1, cy + r * 0.1], fill=(255, 200, 40))
    d.rectangle([cx + r * 0.25, cy - r * 0.1, cx + r * 0.55, cy + r * 0.1], fill=(255, 255, 255))
    # explosion
    import math
    bx, by = cx + r * 0.45, cy - r * 0.45
    for ang in range(0, 360, 45):
        x2 = bx + r * 0.35 * math.cos(math.radians(ang))
        y2 = by + r * 0.35 * math.sin(math.radians(ang))
        d.line([bx, by, x2, y2], fill=(255, 120, 40), width=4)
    d.ellipse([bx - 8, by - 8, bx + 8, by + 8], fill=(255, 200, 40))
    # waves
    for wy in (0.62, 0.78):
        d.arc([cx - r * 0.8, cy + r * wy - 8, cx - r * 0.2, cy + r * wy + 8], 0, 180, fill=(255, 255, 255), width=3)
        d.arc([cx + r * 0.1, cy + r * wy - 8, cx + r * 0.7, cy + r * wy + 8], 0, 180, fill=(255, 255, 255), width=3)


def icon_bank(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(60, 90, 60))
    d.polygon([(cx - r * 0.7, cy - r * 0.1), (cx, cy - r * 0.62), (cx + r * 0.7, cy - r * 0.1)], fill=(255, 255, 255))
    for i in range(3):
        x = cx + (i - 1) * r * 0.42
        d.rectangle([x - 6, cy - r * 0.05, x + 6, cy + r * 0.55], fill=(255, 255, 255))
    d.rectangle([cx - r * 0.72, cy + r * 0.55, cx + r * 0.72, cy + r * 0.68], fill=(255, 255, 255))
    # lightning bolt (the bug that broke it)
    d.polygon([(cx + r * 0.55, cy - r * 0.75), (cx + r * 0.3, cy - r * 0.1),
               (cx + r * 0.48, cy - r * 0.1), (cx + r * 0.25, cy + r * 0.45),
               (cx + r * 0.55, cy - r * 0.15), (cx + r * 0.38, cy - r * 0.15)],
              fill=(255, 200, 40))


def icon_rocket(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 60, 120))
    # body tilted
    d.polygon([(cx - r * 0.15, cy - r * 0.7), (cx + r * 0.2, cy - r * 0.55),
               (cx + r * 0.05, cy + r * 0.15), (cx - r * 0.3, cy), ], fill=(255, 255, 255))
    d.polygon([(cx - r * 0.3, cy), (cx + r * 0.05, cy + r * 0.15),
               (cx - r * 0.15, cy + r * 0.35), (cx - r * 0.45, cy + r * 0.2)], fill=(255, 120, 40))
    d.ellipse([cx - r * 0.35, cy + r * 0.3, cx - r * 0.05, cy + r * 0.6], fill=(255, 200, 40))
    d.ellipse([cx + r * 0.45, cy - r * 0.75, cx + r * 0.75, cy - r * 0.45], fill=(255, 255, 255))
    d.ellipse([cx + r * 0.52, cy - r * 0.68, cx + r * 0.68, cy - r * 0.52], fill=(255, 200, 40))


def icon_chip(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(30, 60, 110))
    s = r * 0.55
    d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=8, fill=(255, 255, 255))
    for i in (-1, 0, 1):
        d.line([cx + i * s * 0.55, cy - s - 10, cx + i * s * 0.55, cy - s], fill=(255, 255, 255), width=4)
        d.line([cx + i * s * 0.55, cy + s, cx + i * s * 0.55, cy + s + 10], fill=(255, 255, 255), width=4)
        d.line([cx - s - 10, cy + i * s * 0.55, cx - s, cy + i * s * 0.55], fill=(255, 255, 255), width=4)
        d.line([cx + s, cy + i * s * 0.55, cx + s + 10, cy + i * s * 0.55], fill=(255, 255, 255), width=4)
    d.rounded_rectangle([cx - s * 0.45, cy - s * 0.45, cx + s * 0.45, cy + s * 0.45], radius=5, fill=BLUE)
    d.text((cx, cy), "AI", font=font(F_SANSB, 22), fill=(255, 255, 255), anchor="mm")


def icon_jet(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(140, 40, 40))
    # simple jet silhouette, nose to upper right
    d.polygon([(cx - r * 0.7, cy + r * 0.15), (cx + r * 0.1, cy - r * 0.45),
               (cx + r * 0.75, cy - r * 0.55), (cx + r * 0.35, cy - r * 0.05),
               (cx + r * 0.7, cy + r * 0.35), (cx + r * 0.3, cy + r * 0.25),
               (cx - r * 0.1, cy + r * 0.55), (cx - r * 0.25, cy + r * 0.3)],
              fill=(255, 255, 255))
    d.ellipse([cx - r * 0.75, cy - r * 0.55, cx - r * 0.4, cy - r * 0.2], fill=(255, 200, 40))


ICONS = {"bridge": icon_bridge, "globe": icon_globe, "tanker": icon_tanker,
         "bank": icon_bank, "rocket": icon_rocket, "chip": icon_chip, "jet": icon_jet}

# ---------------- page ----------------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 36  # margin

# masthead
d.text((W // 2, 26), "THE WORLD IN ONE DAY", font=font(F_SERIF, 52), fill=INK, anchor="ma")
d.rectangle([M, 92, W - M, 96], fill=INK)
d.text((W // 2, 104), "TUESDAY  •  17 NOVEMBER 2026", font=font(F_SERIF, 36), fill=RED, anchor="ma")
d.text((W // 2, 152), "The day's world news — in one picture",
       font=font(F_SANS, 22), fill=GREY, anchor="ma")
d.rectangle([M, 188, W - M, 192], fill=INK)

# ---- lead story: Kerch Bridge ----
LY = 202
IH = 132
# illustration band: sea + bridge, full width
d.rectangle([M, LY, W - M, LY + IH], fill=SKY)
d.rectangle([M, LY + 96, W - M, LY + IH], fill=SEA)
# bridge deck with a broken gap in the middle
d.rectangle([M + 30, LY + 52, W // 2 - 46, LY + 64], fill=(60, 60, 60))
d.rectangle([W // 2 + 46, LY + 52, W - M - 30, LY + 64], fill=(60, 60, 60))
for tx in (M + 150, M + 330, W - M - 330, W - M - 150):
    d.rectangle([tx - 6, LY + 4, tx + 6, LY + 64], fill=(60, 60, 60))
    d.line([tx - 6, LY + 4, tx - 90, LY + 52], fill=(60, 60, 60), width=3)
    d.line([tx + 6, LY + 4, tx + 90, LY + 52], fill=(60, 60, 60), width=3)
# falling span + burst + smoke at the gap
d.polygon([(W // 2 - 40, LY + 64), (W // 2 + 40, LY + 64),
           (W // 2 + 18, LY + 96), (W // 2 - 18, LY + 96)], fill=(90, 90, 90))
bx, by = W // 2, LY + 32
for ang in range(0, 360, 30):
    d.line([bx, by, bx + 42 * math.cos(math.radians(ang)), by + 42 * math.sin(math.radians(ang))],
           fill=(255, 170, 30), width=6)
d.ellipse([bx - 15, by - 15, bx + 15, by + 15], fill=(255, 200, 40))
d.ellipse([bx - 66, by - 30, bx - 20, by + 6], fill=(210, 210, 210))
d.ellipse([bx + 22, by - 38, bx + 70, by - 2], fill=(225, 225, 225))
# waves
for wx in range(M + 20, W - M - 40, 90):
    d.arc([wx, LY + 104, wx + 60, LY + 124], 0, 180, fill=(255, 255, 255), width=3)

d.text((M, LY + 140), "UKRAINE  •  RUSSIA  —  LEAD STORY", font=font(F_SANSB, 21), fill=RED)
d.text((M, LY + 166), "Kerch Bridge hit — road span collapses",
       font=font(F_SERIF, 36), fill=INK)
draw_wrapped(d, M, LY + 212,
             "Ukraine struck the bridge linking Russia to occupied Crimea in what "
             "Zelenskyy called an \u201cunprecedented operation\u201d. Moscow vowed to rebuild it.",
             font(F_SANS, 23), W - 2 * M, leading=5, max_lines=2)
d.rectangle([M, LY + 270, W - M, LY + 272], fill=INK)

# ---- grid: 2 rows x 3 cols ----
stories = [
    ("globe", "ASIA  •  DIPLOMACY", "Trump lands in Manila",
     "Signs a trade statement with Thailand at the ASEAN summit; three-way talks with Xi and Putin due in Shenzhen."),
    ("tanker", "MIDDLE EAST", "Two tankers \u201chit mines\u201d",
     "Iran says the ships caught fire in the Strait of Hormuz; a third US carrier arrives in the region."),
    ("bank", "MARKETS", "Banking bug halts JPMorgan",
     "A software fault slowed online banking, branches and Zelle payments. Not a cyberattack."),
    ("rocket", "SPACE", "Vulcan rocket fails",
     "Amazon\u2019s 40 Leo internet satellites were destroyed minutes after Sunday\u2019s launch."),
    ("chip", "TECH  •  EARNINGS", "Nvidia reports after bell",
     "Its first earnings since Jensen Huang stepped down as chief executive."),
    ("jet", "ASIA  •  SECURITY", "Japan scrambles jets",
     "Tokyo protests after two suspected Russian aircraft entered its airspace."),
]
GY = LY + 286
CW, CH = (W - 2 * M - 2 * 18) // 3, 178
for i, (icon, kicker, head, body) in enumerate(stories):
    r, c = divmod(i, 3)
    x0 = M + c * (CW + 18)
    y0 = GY + r * (CH + 12)
    if c:
        d.line([x0 - 9, y0 + 6, x0 - 9, y0 + CH - 6], fill=LIGHT, width=2)
    if r:
        d.line([x0, y0 - 6, x0 + CW, y0 - 6], fill=LIGHT, width=2)
    ICONS[icon](d, x0 + 32, y0 + 32, 32)
    d.text((x0 + 74, y0 + 10), kicker, font=font(F_SANSB, 17), fill=RED)
    draw_wrapped(d, x0 + 74, y0 + 32, head, font(F_SERIF, 24), CW - 74, leading=2, max_lines=2)
    draw_wrapped(d, x0, y0 + 92, body, font(F_SANS, 18), CW, leading=3, max_lines=3)

# ---- ticker: also on 17 November ----
TY = GY + 2 * CH + 12 + 6
d.rectangle([M, TY, W - M, TY + 84], fill=INK)
d.text((M + 16, TY + 8), "ALSO ON 17 NOVEMBER", font=font(F_SANSB, 20), fill=(255, 200, 40))
draw_wrapped(d, M + 16, TY + 36,
             "UK sanctions Israeli settlement firms  •  D\u00e9pardieu pleads guilty in Paris  •  "
             "West urges Israel to open Gaza aid crossings  •  Houthis advance in Yemen",
             font(F_SANS, 18), W - 2 * M - 32, fill=(255, 255, 255), leading=3, max_lines=2)

# ---- footer ----
FY = TY + 96
d.text((W // 2, FY), "Sources: BBC  •  AP  •  Reuters  •  Al Jazeera  •  ABC News  •  Just Security",
       font=font(F_SANS, 18), fill=GREY, anchor="ma")
d.text((W // 2, FY + 26), "Every event above was reported on Tuesday 17 November 2026.",
       font=font(F_SANSB, 18), fill=GREY, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png")
