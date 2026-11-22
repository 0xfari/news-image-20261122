#!/usr/bin/env python3
"""Render THE SUNDAY WORLD — one picture of Sunday 22 November 2026.

Every story below was verified against live reporting on 22 November 2026
(BBC, Reuters, Al Jazeera, AP via news wires). Nothing is invented: dates,
places and figures are as reported that day. All pictures are drawn in code
with PIL; no photographs, no copied artwork. Fonts are DejaVu, bundled in
fonts/ next to this script and loaded by a path relative to this file.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "fonts"

PAPER = (248, 244, 236)
INK = (22, 21, 19)
RED = (164, 31, 26)
NAVY = (23, 51, 73)
SEA = (29, 78, 107)
SEA_DARK = (18, 52, 74)
SAND = (217, 201, 163)
SAND_DARK = (198, 178, 132)
GOLD = (201, 162, 39)
GREY = (112, 107, 96)
RULE = (74, 68, 58)
WHITE = (250, 248, 243)
ORANGE = (214, 96, 32)
SMOKE = (120, 118, 112)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
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


def para(draw, x, y, text, fnt, fill, width, leading=None, max_lines=None):
    """Draw a wrapped paragraph; returns the y just below the last line."""
    leading = leading or int(fnt.size * 1.22)
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def dashed(draw, p0, p1, fill, width=2, dash=9, gap=6):
    """A dashed straight line between two points."""
    import math

    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    d = 0.0
    while d < length:
        end = min(d + dash, length)
        draw.line(
            [(p0[0] + ux * d, p0[1] + uy * d), (p0[0] + ux * end, p0[1] + uy * end)],
            fill=fill,
            width=width,
        )
        d = end + gap


def flame(draw, cx, cy, s):
    """A small flame: orange outer, gold inner."""
    draw.polygon(
        [
            (cx, cy - s),
            (cx + s * 0.55, cy - s * 0.1),
            (cx + s * 0.35, cy + s * 0.55),
            (cx - s * 0.35, cy + s * 0.55),
            (cx - s * 0.55, cy - s * 0.1),
        ],
        fill=ORANGE,
    )
    draw.polygon(
        [
            (cx, cy - s * 0.45),
            (cx + s * 0.28, cy),
            (cx, cy + s * 0.4),
            (cx - s * 0.28, cy),
        ],
        fill=GOLD,
    )


def smoke(draw, x, y, r):
    for i, rr in enumerate((r, r * 0.7, r * 0.45)):
        draw.ellipse(
            [x - rr, y - rr - i * r * 0.55, x + rr, y + rr - i * r * 0.55],
            fill=SMOKE,
        )


# ---------------------------------------------------------------- thumbnails
def thumb_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 90, 74))
    d.ellipse([x + w - 34, y + 8, x + w - 6, y + 36], fill=GOLD)  # sun
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(38, 58, 48))  # hall floor
    for yy in (y + 52, y + 70, y + 88):
        d.rectangle([x + 10, yy, x + w - 10, yy + 8], fill=(232, 226, 210))
        for i in range(4):
            cx = x + 20 + i * 24
            d.ellipse([cx - 4, yy - 10, cx + 4, yy - 2], fill=(30, 28, 26))
    d.rectangle([x + 8, y + 8, x + 30, y + 20], fill=RED)
    d.text((x + 11, y + 10), "COP31", font=font(SANS_B, 9), fill=WHITE)


def thumb_sparta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 84, 104))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA_DARK)
    d.polygon(
        [(x + 14, y + 58), (x + 86, y + 58), (x + 76, y + 74), (x + 24, y + 74)],
        fill=(40, 38, 34),
    )
    d.rectangle([x + 40, y + 40, x + 52, y + 58], fill=(40, 38, 34))
    d.rectangle([x + 58, y + 46, x + 66, y + 58], fill=(40, 38, 34))
    smoke(d, x + 46, y + 26, 9)
    flame(d, x + 46, y + 44, 11)
    d.text((x + 8, y + 6), "BALTIC SEA", font=font(SANS_B, 9), fill=WHITE)


def thumb_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 96, 122))
    d.polygon([(x + 50, y + 8), (x + 62, y + 22), (x + 50, y + 52), (x + 38, y + 22)],
              outline=WHITE, width=3)
    d.text((x + 44, y + 24), "N", font=font(SANS_B, 16), fill=WHITE)
    for cx, cy, s in ((x + 22, y + 74, 10), (x + 78, y + 66, 8)):
        d.polygon(
            [(cx - s, cy), (cx + s, cy), (cx + s * 2.2, cy - 3), (cx, cy - 6)],
            fill=(30, 30, 30),
        )
    dashed(d, (x + 6, y + 88), (x + 94, y + 88), WHITE, width=2)


def thumb_mexico(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 138, 74))
    d.polygon([(x, y + 62), (x + 34, y + 26), (x + 66, y + 62)], fill=(122, 84, 52))
    d.polygon([(x + 40, y + 62), (x + 72, y + 30), (x + 100, y + 62)], fill=(96, 64, 40))
    d.rectangle([x, y + 62, x + w, y + h], fill=(222, 190, 138))
    d.ellipse([x + 40, y + 70, x + 60, y + 90], fill=GOLD)
    d.text((x + 46, y + 74), "★", font=font(SANS_B, 13), fill=INK)


def thumb_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(74, 92, 96))
    d.polygon([(x, y + 66), (x + 30, y + 18), (x + 58, y + 66)], fill=(52, 62, 58))
    d.polygon([(x + 40, y + 66), (x + 72, y + 26), (x + 100, y + 66)], fill=(44, 52, 50))
    d.polygon([(x + 24, y + 26), (x + 30, y + 18), (x + 36, y + 26)], fill=WHITE)
    d.rectangle([x, y + 66, x + w, y + h], fill=(88, 80, 66))
    pts = [(x + 6, y + 88), (x + 20, y + 88), (x + 28, y + 76), (x + 36, y + 96),
           (x + 46, y + 82), (x + 60, y + 88), (x + 94, y + 88)]
    d.line(pts, fill=RED, width=3)


def thumb_hartha(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(88, 84, 76))
    for cx in (x + 26, x + 62):
        d.polygon(
            [(cx - 14, y + 88), (cx - 10, y + 44), (cx + 10, y + 44), (cx + 14, y + 88)],
            fill=(210, 204, 190),
        )
        d.ellipse([cx - 10, y + 42, cx + 10, y + 50], fill=(210, 204, 190))
    smoke(d, x + 62, y + 30, 8)
    flame(d, x + 62, y + 46, 9)
    d.rectangle([x, y + 88, x + w, y + h], fill=(52, 48, 42))


def thumb_manipur(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(126, 58, 52))
    d.rectangle([x + 34, y + 34, x + 66, y + 90], fill=(232, 226, 210))
    d.rectangle([x + 42, y + 22, x + 58, y + 34], fill=(232, 226, 210))
    d.rectangle([x + 38, y + 52, x + 62, y + 74], fill=RED)
    d.polygon([(x + 76, y + 22), (x + 92, y + 50), (x + 60, y + 50)], fill=GOLD)
    d.text((x + 74, y + 34), "!", font=font(SANS_B, 16), fill=INK)


def thumb_florida(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(96, 116, 128))
    for cx in (x + 24, x + 62):
        d.polygon([(cx - 18, y + 52), (cx, y + 34), (cx + 18, y + 52)], fill=(150, 60, 44))
        d.rectangle([cx - 14, y + 52, cx + 14, y + 72], fill=(228, 220, 204))
    d.rectangle([x, y + 72, x + w, y + h], fill=(38, 90, 116))
    d.line([(x, y + 72), (x + w, y + 72)], fill=WHITE, width=2)
    for xx in (x + 14, x + 46, x + 78):
        d.line([(xx, y + 12), (xx - 3, y + 22)], fill=(200, 214, 224), width=2)


def thumb_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(34, 40, 46))
    d.line([(x + 10, y + 14), (x + 10, y + 86)], fill=GREY, width=2)
    d.line([(x + 10, y + 86), (x + 92, y + 86)], fill=GREY, width=2)
    pts = [(x + 14, y + 30), (x + 32, y + 38), (x + 48, y + 34),
           (x + 64, y + 56), (x + 78, y + 66), (x + 90, y + 80)]
    d.line(pts, fill=(214, 64, 48), width=4)
    d.polygon([(x + 90, y + 80), (x + 82, y + 74), (x + 84, y + 84)], fill=(214, 64, 48))
    d.text((x + 12, y + 6), "S&P −5.1%", font=font(SANS_B, 11), fill=WHITE)


# ---------------------------------------------------------------- hero map
def hero_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # Iran coast along the top, Arabian peninsula along the bottom-left.
    d.polygon(
        [(x, y), (x + w, y), (x + w, y + 34), (x + 640, y + 52),
         (x + 470, y + 30), (x + 300, y + 48), (x + 150, y + 30), (x, y + 44)],
        fill=SAND,
    )
    d.polygon(
        [(x, y + h), (x, y + 118), (x + 150, y + 96), (x + 250, y + 128),
         (x + 330, y + 150), (x + 300, y + h)],
        fill=SAND,
    )
    # Bahrain island
    d.ellipse([x + 268, y + 96, x + 292, y + 118], fill=SAND_DARK)
    d.ellipse([x + 276, y + 102, x + 284, y + 110], fill=RED)
    # Strait of Hormuz narrows, right side
    d.polygon(
        [(x + 700, y + 40), (x + 760, y + 30), (x + 800, y + 60), (x + 760, y + 92),
         (x + 700, y + 84)],
        fill=SAND_DARK,
    )
    # Tankers on the water with fire
    for tx, ty in ((x + 560, y + 128), (x + 700, y + 148)):
        d.rectangle([tx - 34, ty - 8, tx + 34, ty + 8], fill=(40, 38, 34))
        d.rectangle([tx - 10, ty - 18, tx + 8, ty - 8], fill=(40, 38, 34))
        smoke(d, tx, ty - 26, 8)
        flame(d, tx, ty - 14, 10)
    # Missile arcs from the top coast toward Bahrain and the tankers
    dashed(d, (x + 430, y + 52), (x + 282, y + 100), GOLD, width=3)
    dashed(d, (x + 560, y + 48), (x + 560, y + 118), GOLD, width=3)
    dashed(d, (x + 700, y + 44), (x + 700, y + 138), GOLD, width=3)
    # Labels
    lab = font(SANS_B, 14)
    d.text((x + 14, y + 10), "IRAN", font=lab, fill=NAVY)
    d.text((x + 16, y + 148), "SAUDI ARABIA", font=lab, fill=NAVY)
    d.text((x + 308, y + 88), "BAHRAIN", font=font(SANS_B, 12), fill=WHITE)
    d.text((x + 640, y + 96), "STRAIT OF HORMUZ", font=lab, fill=WHITE)
    d.text((x + 800, y + 150), "GULF OF OMAN", font=lab, fill=WHITE)
    d.text((x + 500, y + 158), "TWO TANKERS HIT", font=font(SANS_B, 12), fill=WHITE)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24
    CW = W - 2 * M  # 976

    # ---- masthead
    name = font(SERIF_B, 62)
    d.text((W // 2, 14), "THE SUNDAY WORLD", font=name, fill=INK, anchor="ma")
    hrule(d, M, W - M, 88, fill=INK, width=3)
    hrule(d, M, W - M, 93, fill=INK, width=1)
    date_f = font(SANS_B, 16)
    d.text(
        (W // 2, 100),
        "SUNDAY, 22 NOVEMBER 2026  ·  THE DAY'S WORLD NEWS IN ONE PICTURE",
        font=date_f,
        fill=INK,
        anchor="ma",
    )

    # ---- hero
    hy = 128
    map_h = 176
    hero_h = 296
    hero_map(d, M, hy, CW, map_h)
    d.rectangle([M, hy + map_h, M + CW, hy + hero_h], fill=NAVY)
    d.text(
        (M + 16, hy + map_h + 8),
        "THE GULF — WAR AT SEA",
        font=font(SANS_B, 15),
        fill=GOLD,
    )
    d.text(
        (M + 16, hy + map_h + 30),
        "IRAN STRIKES ACROSS THE GULF",
        font=font(SERIF_B, 36),
        fill=WHITE,
    )
    para(
        d, M + 16, hy + map_h + 72,
        "Bahrain says an Iranian attack set fire to a civilian industrial site, with no "
        "injuries. Tehran claims it hit US bases; two tankers were struck near the "
        "Strait of Hormuz.",
        font(SANS, 17), WHITE, CW - 32, leading=20, max_lines=2,
    )

    # ---- story grid: 3 columns x 3 rows
    stories = [
        ("CLIMATE · ANTALYA", "COP31 in overtime as new draft aims to avert collapse",
         "Talks run into a second day past deadline, split over fossil fuels and "
         "funding for poorer nations.", thumb_cop31),
        ("THE BALTIC", "Freighter Sparta II on fire after suspected drone strike",
         "Crew evacuated in the Gulf of Finland as firefighters battle the blaze.",
         thumb_sparta),
        ("NATO · WARSAW", "Poland accuses Russia of airspace violation",
         "NATO chief Rutte, in Warsaw: the alliance will defend every inch of "
         "Polish territory.", thumb_poland),
        ("MEXICO", "FBI most-wanted drug lord captured in shoot-out",
         "Fausto Isidro, “El Chapo Isidro”, seized in a raid; eleven people "
         "were killed in the operation.", thumb_mexico),
        ("PERU", "Magnitude 6.7 quake shakes the Andes",
         "Fifteen injured in the Junín region; no deaths reported after the "
         "tremor.", thumb_peru),
        ("IRAQ", "Fire at Basra power station kills four",
         "Blaze at the Hartha plant injures 35; the cause is not yet known, "
         "state media say.", thumb_hartha),
        ("INDIA", "Toxic alcohol kills eleven in Manipur",
         "More than 180 people in hospital after drinking bootleg liquor, "
         "the chief minister says.", thumb_manipur),
        ("UNITED STATES", "Florida floods break a 73-year river record",
         "The St Johns River tops its 1953 mark near Cocoa; flooding may "
         "last into January.", thumb_florida),
        ("MARKETS", "Stocks suffer worst week since April 2025",
         "Traders now price in a near-certain Fed quarter-point rate rise in "
         "December; oil eases near $93.", thumb_markets),
    ]
    gy = 448
    col_w = (CW - 24) // 3  # 317
    row_h, row_gap = 148, 10
    for i, (kicker, title, deck, thumb) in enumerate(stories):
        col, row = i % 3, i // 3
        cx = M + col * (col_w + 12)
        cy = gy + row * (row_h + row_gap)
        d.text((cx, cy), kicker, font=font(SANS_B, 12), fill=RED)
        thumb(d, cx, cy + 20, 100, 100)
        tx = cx + 112
        para(d, tx, cy + 20, title, font(SANS_B, 19), INK, col_w - 112,
             leading=23, max_lines=3)
        # deck sits under the title, right of the thumbnail
        title_lines = wrap(d, title, font(SANS_B, 19), col_w - 112)
        dy = cy + 20 + len(title_lines) * 23 + 4
        para(d, tx, dy, deck, font(SANS, 13), (52, 50, 46), col_w - 112,
             leading=16, max_lines=4)
        if col < 2:
            d.line([(cx + col_w + 6, cy), (cx + col_w + 6, cy + row_h - 12)],
                   fill=(198, 192, 178), width=1)

    # ---- also today strip
    sy = 924
    hrule(d, M, W - M, sy, fill=INK, width=2)
    d.text((M, sy + 8), "ALSO TODAY", font=font(SANS_B, 14), fill=RED)
    para(
        d, M + 118, sy + 8,
        "FBI probes an apparent hack of its criminal database  •  Houthi missiles "
        "fired at Riyadh intercepted  •  Geneva talks on “killer robots” end with "
        "no treaty  •  Spain heads to a snap election on 29 November  •  SoftBank "
        "shelves a $1 trillion SK Hynix buyout",
        font(SANS, 14), INK, CW - 118, leading=18, max_lines=3,
    )
    hrule(d, M, W - M, 988, fill=INK, width=2)

    # ---- footer
    d.text(
        (W // 2, 996),
        "Drawn from live reporting of Sunday 22 November 2026 · THE SUNDAY WORLD · "
        "All pictures drawn in code — no photographs",
        font=font(SANS, 12), fill=GREY, anchor="ma",
    )

    out = ROOT / "entry.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
