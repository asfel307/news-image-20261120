#!/usr/bin/env python3
"""Render the 20 November 2026 world-news front page as a 1024x1024 PNG.

No network, no downloaded assets: every glyph comes from the local DejaVu
fonts and every pictogram is drawn with Pillow primitives.

Run:  python3 render.py
Writes entry.png next to this file.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# ---------------------------------------------------------------- palette ---
PAPER = (247, 242, 231)      # ivory newsprint
INK = (30, 27, 22)           # near-black ink
BRICK = (166, 58, 42)        # brick-red accent
TEAL = (46, 110, 106)        # single secondary colour
MUTED = (107, 101, 90)       # grey-brown for kickers / captions
RULE = (30, 27, 22)
PANEL = (240, 234, 219)      # slightly darker paper for pictogram panels
CARD_LINE = (198, 188, 168)  # hairline around cards

W = H = 1024
MARGIN = 40


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return font("DejaVuSerif.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in `width` px."""
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


def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ------------------------------------------------------------- pictograms ---
# Each draws inside the box (x0, y0, x1, y1) with ink / brick / teal only.

def pic_drone(d, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # rotor arms
    d.line([x0 + 14, y0 + 26, x1 - 14, y1 - 26], fill=INK, width=5)
    d.line([x1 - 14, y0 + 26, x0 + 14, y1 - 26], fill=INK, width=5)
    # rotor discs
    for rx, ry in ((x0 + 22, y0 + 30), (x1 - 22, y0 + 30),
                   (x0 + 22, y1 - 30), (x1 - 22, y1 - 30)):
        d.ellipse([rx - 16, ry - 5, rx + 16, ry + 5], outline=INK, width=3)
        d.ellipse([rx - 3, ry - 3, rx + 3, ry + 3], fill=BRICK)
    # body
    d.rounded_rectangle([cx - 34, cy - 20, cx + 34, cy + 20],
                        radius=14, fill=TEAL, outline=INK, width=3)
    d.ellipse([cx - 12, cy - 9, cx + 12, cy + 9], fill=PAPER, outline=INK, width=2)
    # payload slung below
    d.line([cx, cy + 20, cx, cy + 34], fill=INK, width=3)
    d.polygon([(cx - 12, cy + 34), (cx + 12, cy + 34), (cx, cy + 48)],
              fill=BRICK, outline=INK)
    # motion dashes
    for i, yy in enumerate((y0 + 12, y0 + 24)):
        d.line([x0 + 6 + i * 8, yy, x0 + 30 + i * 8, yy], fill=BRICK, width=3)


def pic_chart(d, box):
    x0, y0, x1, y1 = box
    # axes
    d.line([x0 + 12, y0 + 12, x0 + 12, y1 - 12], fill=INK, width=3)
    d.line([x0 + 12, y1 - 12, x1 - 8, y1 - 12], fill=INK, width=3)
    # faint grid
    for gy in (y0 + 30, y0 + 48, y0 + 66):
        d.line([x0 + 12, gy, x1 - 8, gy], fill=CARD_LINE, width=1)
    # plunging line
    pts = [(x0 + 16, y0 + 20), (x0 + 32, y0 + 26), (x0 + 48, y0 + 24),
           (x0 + 62, y0 + 42), (x0 + 76, y0 + 40), (x0 + 88, y0 + 66)]
    d.line(pts, fill=BRICK, width=5, joint="curve")
    # arrowhead at the end
    ex, ey = pts[-1]
    d.polygon([(ex, ey + 12), (ex - 12, ey - 2), (ex + 2, ey - 12)],
              fill=BRICK)
    # down-arrow badge
    d.ellipse([x1 - 30, y0 + 6, x1 - 6, y0 + 30], fill=BRICK)
    d.text((x1 - 25, y0 + 8), "↓", font=sans_b(18), fill=PAPER)


def pic_tower(d, box):
    x0, y0, x1, y1 = box
    # two buildings, the tall one struck
    d.rectangle([x0 + 14, y0 + 40, x0 + 44, y1 - 10], fill=TEAL, outline=INK, width=3)
    d.rectangle([x0 + 50, y0 + 12, x0 + 80, y1 - 10], fill=INK, outline=INK, width=3)
    for wy in range(y0 + 22, y1 - 18, 11):
        d.rectangle([x0 + 57, wy, x0 + 64, wy + 5], fill=PAPER)
        d.rectangle([x0 + 67, wy, x0 + 74, wy + 5], fill=PAPER)
    for wy in range(y0 + 48, y1 - 18, 11):
        d.rectangle([x0 + 21, wy, x0 + 28, wy + 5], fill=PAPER)
        d.rectangle([x0 + 31, wy, x0 + 38, wy + 5], fill=PAPER)
    # impact burst at the top of the tall tower
    bx, by = x0 + 65, y0 + 14
    for dx, dy in ((-18, -12), (0, -17), (18, -12), (-20, 0), (20, 0),
                   (-14, 9), (14, 9)):
        d.line([bx, by, bx + dx, by + dy], fill=BRICK, width=4)
    d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=BRICK, outline=INK, width=2)
    # ground
    d.line([x0 + 6, y1 - 10, x1 - 6, y1 - 10], fill=INK, width=3)


def pic_baseball(d, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2 - 4, (y0 + y1) // 2 - 10
    # ball
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=PAPER,
              outline=INK, width=4)
    # seams: two short arcs hugging the left and right edges
    d.arc([cx - 44, cy - 30, cx + 4, cy + 30], start=300, end=60,
          fill=BRICK, width=3)
    d.arc([cx - 4, cy - 30, cx + 44, cy + 30], start=120, end=240,
          fill=BRICK, width=3)
    for t in range(4):
        a = math.radians(250 + t * 35)
        x = cx - 22 + 6 * math.cos(a)
        y = cy + 22 * math.sin(a)
        d.line([x - 3, y - 3, x + 3, y + 3], fill=BRICK, width=2)
    # small star for the hits record
    sx, sy = x0 + 12, y0 + 12
    d.polygon([(sx, sy - 6), (sx + 2, sy - 1), (sx + 7, sy - 1),
               (sx + 3, sy + 2), (sx + 5, sy + 7), (sx, sy + 4),
               (sx - 5, sy + 7), (sx - 3, sy + 2), (sx - 7, sy - 1),
               (sx - 2, sy - 1)], fill=BRICK)


def pic_shield(d, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    # shield outline, leaving room for the vote tally below it
    d.polygon([(cx - 32, y0 + 6), (cx + 32, y0 + 6), (cx + 32, y0 + 36),
               (cx, y1 - 28), (cx - 32, y0 + 36)], fill=TEAL, outline=INK, width=3)
    # two base markers inside
    for mx, my in ((cx - 13, y0 + 26), (cx + 13, y0 + 26)):
        d.ellipse([mx - 6, my - 6, mx + 6, my + 6], fill=PAPER, outline=INK, width=2)
        d.ellipse([mx - 2, my - 2, mx + 2, my + 2], fill=BRICK)
    # dome arc above the shield
    d.arc([cx - 38, y0 - 6, cx + 38, y0 + 30], start=180, end=360,
          fill=BRICK, width=4)
    # vote tally, centred under the shield
    tally = "109–0"
    tw = d.textlength(tally, font=sans_b(18))
    d.text((cx - tw / 2, y1 - 22), tally, font=sans_b(18), fill=INK)


def pic_boat(d, box):
    x0, y0, x1, y1 = box
    # hull
    d.polygon([(x0 + 12, y0 + 48), (x1 - 12, y0 + 48), (x1 - 26, y0 + 72),
               (x0 + 26, y0 + 72)], fill=BRICK, outline=INK, width=3)
    # mast + sail
    mx = (x0 + x1) // 2
    d.line([mx, y0 + 48, mx, y0 + 12], fill=INK, width=3)
    d.polygon([(mx + 2, y0 + 14), (mx + 2, y0 + 46), (mx + 30, y0 + 46)],
              fill=PAPER, outline=INK, width=2)
    # lifebuoy
    d.ellipse([x0 + 10, y0 + 10, x0 + 34, y0 + 34], fill=PAPER,
              outline=BRICK, width=5)
    d.ellipse([x0 + 17, y0 + 17, x0 + 27, y0 + 27], outline=BRICK, width=3)
    # waves
    for wy in (y0 + 80, y0 + 90):
        d.arc([x0 + 4, wy - 7, x0 + 40, wy + 7], start=180, end=360,
              fill=TEAL, width=3)
        d.arc([x0 + 44, wy - 7, x0 + 80, wy + 7], start=180, end=360,
              fill=TEAL, width=3)


# ------------------------------------------------------------------ layout ---
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    y = 30
    kicker = "ONE DAY  ·  SIX STORIES  ·  AROUND THE WORLD"
    kw = d.textlength(kicker, font=sans_b(17))
    d.text(((W - kw) / 2, y), kicker, font=sans_b(17), fill=BRICK)
    y += 30
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=serif_b(64))
    d.text(((W - tw) / 2, y), title, font=serif_b(64), fill=INK)
    y += 82
    date = "Friday, 20 November 2026"
    dw = d.textlength(date, font=serif(26))
    d.text(((W - dw) / 2, y), date, font=serif(26), fill=INK)
    y += 44
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=4)
    d.line([MARGIN, y + 7, W - MARGIN, y + 7], fill=RULE, width=1)
    y += 20

    # ---- lead story ----------------------------------------------------
    lead_x, lead_w = MARGIN, 600
    d.text((lead_x, y), "LEAD STORY", font=sans_b(17), fill=BRICK)
    y += 26
    headline = "UK pledges 1,000+ long-range drones for Ukraine"
    lines = wrap(d, headline, serif_b(42), lead_w)
    y = text_block(d, (lead_x, y), lines, serif_b(42), INK, 50)
    y += 8
    deck = ("PM Andy Burnham announced a £260m package in Berlin at the "
            "Coalition of the Willing meeting. The drones fly 1,000+ km — "
            "London to Berlin — and carry heavy warheads. The package also "
            "has maritime, logistical and surveillance drones; 80%+ of "
            "funding is spent in the UK.")
    lines = wrap(d, deck, sans(20), lead_w)
    y = text_block(d, (lead_x, y), lines, sans(20), INK, 28)
    # lead pictogram panel, right of the text
    px0, py0 = 668, 206
    px1, py1 = W - MARGIN, 500
    d.rectangle([px0, py0, px1, py1], fill=PANEL, outline=CARD_LINE, width=2)
    d.rectangle([px0, py0, px1, py0 + 34], fill=BRICK)
    cap = "1,000+ KM RANGE"
    cw = d.textlength(cap, font=sans_b(17))
    d.text(((px0 + px1 - cw) / 2, py0 + 7), cap, font=sans_b(17), fill=PAPER)
    pic_drone(d, (px0 + 34, py0 + 52, px1 - 34, py1 - 34))
    d.text((px0 + 14, py1 - 30), "£260m package  ·  Berlin",
           font=sans(16), fill=MUTED)

    # rule under the lead
    ly = 532
    d.line([MARGIN, ly, W - MARGIN, ly], fill=RULE, width=2)

    # ---- five story cards ----------------------------------------------
    cards = [
        ("MARKETS", "Taiwan stocks plunge 2,200 points",
         "Below 37,000 — lowest since mid-April — after shedding "
         "7,000+ points in a week. Five rescue measures unveiled.",
         pic_chart),
        ("MIDDLE EAST", "Houthi strikes hit Saudi Arabia",
         "Four targets claimed, including Riyadh's tallest skyscraper, "
         "damaged. Foreign investors were warned to leave.",
         pic_tower),
        ("SPORT", "Trump pardons Pete Rose",
         "All-time hits leader — 4,256 hits — pardoned posthumously. "
         "His 1990 tax case; Hall of Fame vote next December 2027.",
         pic_baseball),
        ("ARCTIC", "Denmark ratifies Greenland deal, 109–0",
         "The US gains two bases, including “Golden Dome” missile "
         "defence. Danish sovereignty and Greenlanders' "
         "self-determination reaffirmed.",
         pic_shield),
        ("MIGRATION", "Migrant boat capsizes off Senegal",
         "About 100 people were aboard off Yenne; dozens are missing "
         "and the search continues. 11,000+ reached the Canary "
         "Islands in the first half of November.",
         pic_boat),
    ]

    gap = 16
    top_w = (W - 2 * MARGIN - 2 * gap) // 3          # 304
    bot_w = (W - 2 * MARGIN - gap) // 2              # 464
    row1_y, row1_h = 550, 200
    row2_y, row2_h = 766, 200

    def card(x, y, w, h, kicker_text, title_text, body_text, pic):
        d.rectangle([x, y, x + w, y + h], fill=PAPER,
                    outline=CARD_LINE, width=2)
        d.rectangle([x, y, x + w, y + 5], fill=BRICK)
        pad = 14
        # pictogram panel, top-left
        ps = 84
        d.rectangle([x + pad, y + 18, x + pad + ps, y + 18 + ps],
                    fill=PANEL, outline=CARD_LINE, width=1)
        pic(d, (x + pad, y + 18, x + pad + ps, y + 18 + ps))
        # kicker + headline to the right of the pictogram
        tx = x + pad + ps + 12
        tw2 = x + w - pad - tx
        d.text((tx, y + 18), kicker_text, font=sans_b(15), fill=TEAL)
        tlines = wrap(d, title_text, sans_b(20), tw2)
        text_block(d, (tx, y + 38), tlines[:3], sans_b(20), INK, 24)
        # body under the pictogram row
        by = y + 18 + ps + 8
        blines = wrap(d, body_text, sans(17), w - 2 * pad)
        text_block(d, (x + pad, by), blines[:4], sans(17), INK, 22)

    for i in range(3):
        k, t, b, p = cards[i]
        card(MARGIN + i * (top_w + gap), row1_y, top_w, row1_h, k, t, b, p)
    for j in range(2):
        k, t, b, p = cards[3 + j]
        card(MARGIN + j * (bot_w + gap), row2_y, bot_w, row2_h, k, t, b, p)

    # ---- footer ----------------------------------------------------------
    fy = 984
    d.line([MARGIN, fy - 12, W - MARGIN, fy - 12], fill=RULE, width=1)
    foot = "Sources: GOV.UK · BBC · Reuters · AP · TASS · AFP · Folketing record"
    fw = d.textlength(foot, font=sans(16))
    d.text(((W - fw) / 2, fy), foot, font=sans(16), fill=MUTED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = render()
    print("wrote", path, os.path.getsize(path), "bytes")
