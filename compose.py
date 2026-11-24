#!/usr/bin/env python3
"""THE DAWN LEDGER — NI23 G4 final2 (@ethpumped).

One day in print: Monday 23 November 2026. Lead (pool #19): Nepal PM
Balendra Shah holds bilateral talks with PM Modi in Delhi. Trio: #19 +
#7 COP31 ends without a deal in Antalya + #25 India declare on 720/9.

Fleet-schema source for the margin checker: grid / NUMS / TL / BRIEFS /
dc / PINS literals, lead() + mini() card painters, dotted_map().
1024x1024, peach dawn paper, black ink, orange accent, flat drawings.
Variant A: 3 leads on top, 4-col grid, numbers + map row, ALSO band.
Variant B: 2 leads + numbers rail, wide third lead, grid, map cell.
Counts are computed from the data, so the kicker can never lie.
PIL is local-only; the submitted program (main.py) is stdlib copy-only.
"""

import math
import sys
from collections import Counter

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024
M = 14
CW = W - 2 * M

PEACH = (252, 231, 205)
PEACH2 = (250, 219, 178)
PAPER = (255, 248, 236)
INK = (18, 16, 14)
ORANGE = (214, 96, 18)
ORANGE_D = (168, 66, 8)
RED = (178, 34, 22)
GREY = (96, 88, 80)
LINE = (60, 52, 44)

REGIONS = {
    "SOUTH ASIA": (196, 84, 20),
    "EUROPE": (38, 92, 150),
    "MIDDLE EAST": (150, 44, 44),
    "NORTH AMERICA": (44, 120, 92),
    "SOUTHEAST ASIA": (120, 74, 160),
    "AFRICA": (176, 128, 20),
    "GLOBAL": (90, 90, 96),
}


def pf(size):   # masthead face: PlayfairDisplay-Black
    return ImageFont.truetype(FONT_DIR + "PlayfairDisplay-Black.ttf", size)


def fb(size):   # headline face
    return ImageFont.truetype(FONT_DIR + "PlayfairDisplay-Bold.ttf", size)


def fr(size):   # deck / body face
    return ImageFont.truetype(FONT_DIR + "Archivo.ttf", size)


def fsr(size):  # brief face
    return ImageFont.truetype(FONT_DIR + "Archivo.ttf", size)


def arb(size):
    return ImageFont.truetype(FONT_DIR + "Archivo-Bold.ttf", size)


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def txt(d, x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def fit1(d, s, font, maxw):
    while s and d.textlength(s, font=font) > maxw:
        s = s[:-1]
    return s


# ---------------- flat illustrations ----------------

def illus(d, kind, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    if kind == "hands":
        d.rectangle([x + 2, y + 3, x + 11, y + s - 4], fill=(230, 90, 30))
        d.rectangle([x + s - 11, y + 3, x + s - 2, y + s - 4], fill=(40, 110, 60))
        d.arc([x + 8, y + 5, x + s - 8, y + s + 6], 20, 160, fill=INK, width=2)
        d.ellipse([cx - 3, cy + 3, cx + 3, cy + 9], fill=ORANGE)
    elif kind == "globe":
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=(38, 92, 150), width=2)
        d.line([cx - 13, cy, cx + 13, cy], fill=(38, 92, 150), width=2)
        d.line([cx, cy - 13, cx, cy + 13], fill=(38, 92, 150), width=2)
    elif kind == "bat":
        d.polygon([(x + 5, y + s - 4), (x + 13, y + 4), (x + 19, y + 7),
                   (x + 11, y + s - 2)], fill=(150, 100, 40))
        d.ellipse([x + s - 15, y + 5, x + s - 6, y + 14], fill=RED)
    elif kind == "flame":
        d.polygon([(cx, y + 3), (cx + 9, y + s - 3), (cx - 9, y + s - 3)], fill=ORANGE)
        d.polygon([(cx, y + 10), (cx + 4, y + s - 3), (cx - 4, y + s - 3)], fill=(240, 170, 40))
    elif kind == "drone":
        d.line([x + 4, y + 5, x + s - 4, y + s - 5], fill=INK, width=2)
        d.ellipse([cx - 5, cy - 3, cx + 5, cy + 3], fill=GREY)
        for ex, ey in ((x + 2, y + 2), (x + s - 8, y + 2), (x + 2, y + s - 7), (x + s - 8, y + s - 7)):
            d.ellipse([ex, ey, ex + 6, ey + 5], outline=INK, width=1)
    elif kind == "child":
        d.rectangle([x + 2, y + s - 8, x + s - 2, y + s - 4], fill=GREY)
        d.polygon([(x + 3, y + s - 8), (x + 12, y + 5), (x + 19, y + s - 8)], fill=(120, 110, 100))
        d.ellipse([cx - 4, cy - 2, cx + 4, cy + 6], fill=(240, 190, 130))
    elif kind == "ship":
        d.polygon([(x + 2, y + s - 7), (x + s - 2, y + s - 7),
                   (x + s - 8, y + s - 2), (x + 8, y + s - 2)], fill=INK)
        d.rectangle([cx - 7, y + 7, cx + 5, y + s - 9], fill=GREY)
        d.polygon([(cx - 2, y + 1), (cx + 4, y + 7), (cx, y + 7)], fill=ORANGE)
    elif kind == "scales":
        d.line([cx, y + 4, cx, y + s - 4], fill=INK, width=2)
        d.line([x + 5, y + 7, x + s - 5, y + 7], fill=INK, width=2)
        d.polygon([(x + 5, y + 7), (x + 1, y + 16), (x + 9, y + 16)], outline=INK, width=1)
        d.polygon([(x + s - 5, y + 7), (x + s - 9, y + 16), (x + s - 1, y + 16)], outline=INK, width=1)
    elif kind == "ballot":
        d.rectangle([x + 5, cy, x + s - 5, y + s - 3], outline=INK, width=2)
        d.rectangle([x + 8, y + 4, x + s - 8, cy - 2], outline=INK, width=1)
        d.line([cx - 3, cy + 3, cx, cy + 7], fill=(38, 92, 150), width=2)
        d.line([cx, cy + 7, cx + 6, cy], fill=(38, 92, 150), width=2)
    elif kind == "gold":
        for i, bx in enumerate(range(x + 3, x + s - 10, 10)):
            d.rectangle([bx, y + s - 7 - i, bx + 8, y + s - 3], fill=(212, 160, 32))
        d.polygon([(x + s - 11, y + 4), (x + s - 3, y + 11), (x + s - 11, y + 11)], fill=RED)
    elif kind == "march":
        for i, ox in enumerate(range(x + 3, x + s - 6, 9)):
            d.ellipse([ox, y + 6 + (i % 2) * 3, ox + 6, y + 12 + (i % 2) * 3], fill=INK)
            d.line([ox + 3, y + 12 + (i % 2) * 3, ox + 3, y + s - 3], fill=INK, width=2)
        d.rectangle([x + 2, y + 1, x + 20, y + 6], fill=ORANGE)
    elif kind == "tennis":
        d.ellipse([x + 3, y + 3, x + 19, y + 19], outline=INK, width=2)
        d.line([x + 15, y + 15, x + s - 3, y + s - 2], fill=INK, width=2)
        d.ellipse([x + s - 14, y + 4, x + s - 5, y + 13], fill=(150, 190, 40))
    else:
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(240, 170, 40))
        for a in range(0, 360, 60):
            d.line([cx + 8 * math.cos(math.radians(a)), cy + 8 * math.sin(math.radians(a)),
                    cx + 11 * math.cos(math.radians(a)), cy + 11 * math.sin(math.radians(a))],
                   fill=ORANGE, width=2)


# ---------------- data (pool ni23-pool.md only) ----------------
# grid tuples: (num, region, topic, src, head, deck, kind)
grid = [
    (19, "SOUTH ASIA", "DIPLOMACY", "ObserverVoice, 23 Nov",
     "Nepal's Shah Meets Modi in Delhi",
     "PM Balendra Shah held bilateral talks with PM Modi in Delhi, 22–23 Nov.", "hands"),
    (7, "EUROPE", "CLIMATE", "BBC / AP, 23 Nov",
     "COP31 Ends Without a Deal",
     "COP31 closed in Antalya with no pact; Türkiye's draft omitted fossil fuels.", "globe"),
    (25, "SOUTH ASIA", "CRICKET", "ObserverVoice, 23 Nov",
     "India Declare on Record 720/9",
     "720/9 declared at Wellington — highest Test total ever made in New Zealand.", "bat"),
    (1, "MIDDLE EAST", "WAR AT SEA", "AP live, 23 Nov",
     "Tankers Burn in Hormuz Strait",
     "Tankers ablaze as Iran–US war widens into the Gulf.", "flame"),
    (2, "MIDDLE EAST", "WAR", "AP/AFP wires, 23 Nov",
     "IRGC Claims Radars Hit",
     "IRGC says two Patriot radars hit at a US base in Bahrain.", "drone"),
    (12, "EUROPE", "WAR", "BBC, 23 Nov",
     "Kyiv Boy Alive From Rubble",
     "Boy, 7, freed after a Russian strike on Kyiv; six killed.", "child"),
    (13, "EUROPE", "WAR", "JagranJosh, 23 Nov",
     "14 Missing, Zelenskiy Says",
     "14 missing after a drone hit Kyiv region, Zelenskiy said.", "drone"),
    (9, "EUROPE", "SEA INCIDENT", "BBC, 23 Nov",
     "Russian Ship Still Burns",
     "Russian cargo ship still burns off Finland, in the Gulf.", "ship"),
    (24, "SOUTHEAST ASIA", "WORLD COURT", "Guardian/NYT wires, 23 Nov",
     "ICJ: Myanmar Guilty",
     "Genocide ruling on Rohingya campaign; 700,000+ fled in 2017.", "scales"),
    (43, "NORTH AMERICA", "POLITICS", "BBC, 23 Nov",
     "Democrats' Majority: 258–173",
     "Biggest House majority since 1992; NC seat confirmed it.", "ballot"),
    (34, "GLOBAL", "MONEY", "ObserverVoice, 23 Nov",
     "Gold Slides to $3,538",
     "Down over $2,000 from the 2026 record of $5,595 an ounce.", "gold"),
    (15, "EUROPE", "PROTEST", "JagranJosh, 23 Nov",
     "Thousands March in Lisbon",
     "Thousands in Lisbon, Portugal marched over living costs.", "march"),
    (48, "EUROPE", "TENNIS", "BBC, 23 Nov",
     "Alcaraz Wins First ATP Finals",
     "Beat Zverev for his first ATP Finals crown in Turin.", "tennis"),
]
META = {19: ("DELHI, INDIA", "REPORTED"), 7: ("ANTALYA, TÜRKIYE", "OFFICIAL"),
        25: ("WELLINGTON, NZ", "REPORTED"), 1: ("STRAIT OF HORMUZ", "REPORTED"),
        2: ("BAHRAIN", "CLAIM"), 12: ("KYIV, UKRAINE", "REPORTED"),
        13: ("KYIV REGION", "ON RECORD"), 9: ("OFF FINLAND", "ONGOING"),
        24: ("THE HAGUE", "OFFICIAL"), 43: ("WASHINGTON, US", "REPORTED"),
        34: ("WORLD MARKETS", "REPORTED"), 15: ("LISBON, PORTUGAL", "REPORTED"),
        48: ("TURIN, ITALY", "REPORTED")}
NUMS = [("720/9d", "India record (#25)"),
        ("258–173", "House majority (#43)"),
        ("$3,538", "Gold ounce (#34)"),
        ("₹28,000 cr", "Tata pipe sale (#32)"),
        ("65.9%", "IndiGo share (#33)"),
        ("14", "Missing Kyiv (#13)")]
TL = [("00:02Z", "UN AI talks go on"),
      ("02:00Z", "Albanese on COP31"),
      ("AM", "Shah–Modi talks, Delhi"),
      ("MIDDAY", "Kyiv boy freed"),
      ("PM", "India 720/9d"),
      ("LATE", "COP31 ends")]
BRIEFS = [
    "#3 Houthi missile at Saudi intercepted",
    "#5 UN: keep negotiating lethal AI arms",
    "#6 US declassifies more UFO footage",
    "#10 Russia-bound ship towed in Finland",
    "#11 Benghazi blast — suspected drone",
    "#14 UK–EU reset deal: Burnham, 'landmark'",
    "#16 Myanmar: ASEAN ruling unfair",
    "#17 Cameroon ex-rebels, broken vows",
    "#18 Escaped lion scares Turkish town",
    "#20 India, Bulgaria discuss IMEC",
    "#21 Guru Nanak Jayanti celebrated",
    "#22 UP: blackout drills in 75 districts",
    "#23 Fire UPDATE: 7 bags, 50 missing",
    "#26 India chase win, NZ 119/2",
    "#27 India win ODI series NZ 3–2",
    "#28 Anupama defends IBSF title",
    "#29 World chess title grips fans",
    "#31 Kota pilgrim bus tragedy: 9 dead",
    "#32 Tata Steel pipe sale: ₹28,000 crore",
    "#33 SpiceJet audit call; IndiGo 65.9%",
    "#36 Modi opens IIT Patna AI Centre",
    "#37 Amit Shah: ₹4,000 cr Arunachal",
    "#41 Google: $5m for IIT Kharagpur AI",
    "#42 India–EU pact set for 16 Dec",
    "#44 Trump hits Schumer, Dem push",
    "#45 US Army explosives, Iowa",
    "#46 FBI probes hack of justice database",
    "#47 Miley Cyrus marries Maxx Morando",
]
BRIEF_REGIONS = ["MIDDLE EAST", "GLOBAL", "NORTH AMERICA", "EUROPE", "AFRICA",
                 "EUROPE", "SOUTHEAST ASIA", "AFRICA", "EUROPE", "EUROPE",
                 "SOUTH ASIA", "SOUTH ASIA", "SOUTHEAST ASIA", "SOUTH ASIA",
                 "SOUTH ASIA", "SOUTH ASIA", "GLOBAL", "SOUTH ASIA",
                 "SOUTH ASIA", "SOUTH ASIA", "SOUTH ASIA", "SOUTH ASIA",
                 "SOUTH ASIA", "EUROPE", "NORTH AMERICA", "NORTH AMERICA",
                 "NORTH AMERICA", "NORTH AMERICA"]
dc = ("Xi–Trump–Putin summit, 19 Nov · Poland missiles incident, 20 Nov · "
      "SpiceJet fundraise, 18 Nov · Hyderabad bomb emails, 21 Nov · "
      "Paolo Bulgari dies, 22 Nov · Indonesia candy-factory fire itself, 22 Nov · "
      "Bolsonaro in ICU, 22 Nov · S. Korea minister resigns, 22 Nov")
PINS = [(19, 168, 62), (7, 128, 50), (25, 208, 104), (1, 138, 62),
        (2, 133, 58), (12, 122, 40), (13, 126, 36), (9, 118, 30),
        (24, 172, 76), (43, 30, 44), (34, 112, 54), (15, 92, 50),
        (48, 108, 46)]
COUNTS = Counter([c[1] for c in grid] + BRIEF_REGIONS)
TOTAL = len(grid) + len(BRIEFS)
NREG = len(COUNTS)


# ---------------- page furniture ----------------

def masthead(d):
    d.rectangle([0, 0, W, 24], fill=INK)
    txt(d, M, 4, "THE DAWN LEDGER", arb(14), fill=PEACH)
    kick = "%d STORIES · %d REGIONS · EVERY ONE FROM 23 NOVEMBER 2026" % (TOTAL, NREG)
    txt(d, W - M, 4, kick, arb(14), fill=PEACH, anchor="ra")
    txt(d, W // 2, 28, "Monday 23 November 2026", pf(54), fill=INK, anchor="ma")
    txt(d, W // 2, 88, "THE  DAWN  LEDGER", pf(33), fill=ORANGE_D, anchor="ma")
    sub = ("Nepal's Shah meets Modi in Delhi  ·  COP31 ends without a deal  ·  "
           "India declare on a record 720/9")
    txt(d, W // 2, 126, sub, arb(15), fill=INK, anchor="ma")
    d.line([M, 150, W - M, 150], fill=INK, width=3)
    x = M
    for name, col in REGIONS.items():
        if name not in COUNTS:
            continue
        label = "%s %d" % (name, COUNTS[name])
        wd = d.textlength(label, font=arb(13)) + 16
        d.rectangle([x, 155, x + wd, 173], fill=col)
        txt(d, x + 8, 157, label, arb(13), fill=(255, 255, 255))
        x += wd + 6
    y = 179
    txt(d, M, y, "THE DAY IN UTC", arb(13), fill=ORANGE_D)
    x = M + 112
    for t, ev in TL:
        txt(d, x, y, t, arb(12), fill=ORANGE_D)
        ew = d.textlength(t, font=arb(12)) + 5
        txt(d, x + ew, y, ev, fr(12), fill=INK)
        x += ew + d.textlength(ev, font=fr(12)) + 14
    d.line([M, 198, W - M, 198], fill=LINE, width=2)
    return 204


def _frame(d, c, x, y, w):
    num, region, topic, src, head, deck, kind = c
    loc, status = META[num]
    d.rectangle([x, y, x + w, y + 19], fill=REGIONS[region])
    txt(d, x + 6, y + 3, fit1(d, "#%d %s" % (num, loc), arb(12),
        w - d.textlength(status, font=arb(12)) - 24), arb(12), fill=(255, 255, 255))
    txt(d, x + w - 6, y + 3, status, arb(12), fill=(255, 255, 255), anchor="ra")
    illus(d, kind, x + w - 40, y + 23, 32)
    txt(d, x + 7, y + 23, region + " · " + topic, arb(11), fill=ORANGE_D)
    return head, deck, src


def lead(d, c, x, y, w, h):
    """Big trio card: headline fb(30), deck fr(15)."""
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=LINE, width=2)
    head, deck, src = _frame(d, c, x, y, w)
    tf = fb(30)
    tlines = wrap(d, head, tf, w - 14)
    flines = wrap(d, deck, fr(15), w - 14)
    assert len(tlines) <= 2 and len(flines) <= 2, (head, tlines, flines)
    ly = y + 37
    for ln in tlines:
        txt(d, x + 7, ly, ln, tf, fill=INK)
        ly += 33
    fy = y + h - 50
    for ln in flines:
        txt(d, x + 7, fy, ln, fr(15), fill=INK)
        fy += 18
    txt(d, x + 7, y + h - 15, "Source: " + src, fsr(11), fill=GREY)


def mini(d, c, x, y, w, h):
    """Grid card: headline fb(28), deck fr(15)."""
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=LINE, width=2)
    head, deck, src = _frame(d, c, x, y, w)
    tf = fb(28)
    tlines = wrap(d, head, tf, w - 14)
    flines = wrap(d, deck, fr(15), w - 14)
    assert len(tlines) <= 2 and len(flines) <= 2, (head, tlines, flines)
    ly = y + 37
    for ln in tlines:
        txt(d, x + 7, ly, ln, tf, fill=INK)
        ly += 30
    fy = y + h - 50
    for ln in flines:
        txt(d, x + 7, fy, ln, fr(15), fill=INK)
        fy += 18
    txt(d, x + 7, y + h - 15, "Source: " + src, fsr(11), fill=GREY)


def numbers_box(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PEACH2, outline=LINE, width=2)
    txt(d, x + 9, y + 5, "THE DAY IN NUMBERS", arb(14), fill=ORANGE_D)
    cw2 = (w - 18) // 2
    for i, (big, small) in enumerate(NUMS):
        cx = x + 9 + (i % 2) * cw2
        cy = y + 28 + (i // 2) * ((h - 32) // 3)
        txt(d, cx, cy, big, fb(19), fill=INK)
        txt(d, cx, cy + 24, fit1(d, small, fr(11), cw2 - 4), fr(11), fill=INK)


def dotted_map(d, x, y, w, h):
    """Dotted world map; dots mark the story numbers of the main cards."""
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=LINE, width=2)
    txt(d, x + 9, y + 5, "WHERE IT HAPPENED", arb(13), fill=ORANGE_D)
    txt(d, x + w - 9, y + 5, "dots mark the story numbers", fr(11), fill=GREY, anchor="ra")
    blobs = [(18, 34, 52, 26), (44, 66, 20, 34), (86, 30, 66, 22), (96, 52, 46, 30),
             (98, 84, 30, 26), (140, 36, 74, 48), (182, 92, 26, 18)]
    sx = (w - 16) / 230.0
    sy = (h - 52) / 118.0
    for bx, by, bw, bh in blobs:
        for gx in range(int(bw / 6)):
            for gy in range(int(bh / 6)):
                px = x + 8 + (bx + gx * 6) * sx
                py = y + 26 + (by - 24 + gy * 6) * sy
                d.ellipse([px, py, px + 2.2, py + 2.2], fill=(175, 155, 128))
    for num, mx, my in PINS:
        px = x + 8 + mx * sx
        py = y + 26 + (my - 24) * sy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=ORANGE)
        txt(d, px, py - 6, str(num), arb(10), fill=(255, 255, 255), anchor="ma")
    ly = y + h - 17
    lx = x + 9
    short = {"SOUTH ASIA": "S. Asia", "EUROPE": "Europe",
             "MIDDLE EAST": "M. East", "NORTH AMERICA": "N. Am."}
    for name, col in list(REGIONS.items())[:4]:
        d.rectangle([lx, ly + 1, lx + 9, ly + 10], fill=col)
        txt(d, lx + 12, ly, short[name], fr(10), fill=INK)
        lx += 12 + d.textlength(short[name], font=fr(10)) + 9


def also_box(d, x, y, w, h, cols=4):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=LINE, width=2)
    txt(d, x + 9, y + 4, "ALSO ON MONDAY — STORIES 14 TO %d" % TOTAL, arb(13), fill=ORANGE_D)
    colw = (w - 18) // cols
    rows = (len(BRIEFS) + cols - 1) // cols
    pitch = min(15, (h - 26) // rows)
    for i, s in enumerate(BRIEFS):
        cx = x + 9 + (i // rows) * colw
        cy = y + 24 + (i % rows) * pitch
        txt(d, cx, cy, fit1(d, s, fsr(13), colw - 6), fsr(13), fill=INK)


def bottom_bands(d, y):
    d.rectangle([M, y, W - M, y + 27], fill=(252, 238, 232), outline=RED, width=1)
    lines = wrap(d, "DATE CHECK — NOT 23 NOVEMBER NEWS: " + dc, fr(11), CW - 14)
    assert len(lines) == 2, lines
    txt(d, M + 7, y + 2, lines[0], fr(11), fill=INK)
    txt(d, M + 7, y + 14, lines[1], fr(11), fill=INK)
    fy = y + 31
    d.line([M, fy, W - M, fy], fill=INK, width=2)
    txt(d, M, fy + 5,
        "HOW SURE: REPORTED = carried by the named wire or paper · CLAIM = one side's account, "
        "labelled as such · ONGOING = still developing · OFFICIAL / ON RECORD = an authority's own words.",
        fr(11), fill=INK)
    txt(d, M, fy + 20,
        "Every story happened, or was first reported, on Monday 23 November 2026. "
        "Contested claims are attributed.  Original drawings.",
        arb(11), fill=INK)


def build(variant):
    img = Image.new("RGB", (W, H), PEACH)
    d = ImageDraw.Draw(img)
    top = masthead(d)
    gap = 6
    ch = 150
    leadh = 156
    if variant == "A":
        lw = (CW - 2 * gap) // 3
        for i, c in enumerate(grid[:3]):
            lead(d, c, M + i * (lw + gap), top, lw, leadh)
        y = top + leadh + gap
        gw = (CW - 3 * gap) // 4
        for i, c in enumerate(grid[3:11]):
            mini(d, c, M + (i % 4) * (gw + gap), y + (i // 4) * (ch + gap), gw, ch)
        y += 2 * (ch + gap)
        mini(d, grid[11], M, y, gw, ch)
        mini(d, grid[12], M + gw + gap, y, gw, ch)
        numbers_box(d, M + 2 * (gw + gap), y, gw, ch)
        dotted_map(d, M + 3 * (gw + gap), y, gw, ch)
        y += ch + gap
        also_box(d, M, y, CW, 117)
        bottom_bands(d, y + 123)
    else:
        lw = (CW - 2 * gap) // 3
        lead(d, grid[0], M, top, lw, leadh)
        lead(d, grid[1], M + lw + gap, top, lw, leadh)
        numbers_box(d, M + 2 * (lw + gap), top, lw, leadh)
        y = top + leadh + gap
        gw = (CW - 3 * gap) // 4
        lead(d, grid[2], M, y, 2 * gw + gap, ch)
        mini(d, grid[3], M + 2 * (gw + gap), y, gw, ch)
        mini(d, grid[4], M + 3 * (gw + gap), y, gw, ch)
        y += ch + gap
        for i, c in enumerate(grid[5:9]):
            mini(d, c, M + i * (gw + gap), y, gw, ch)
        y += ch + gap
        for i, c in enumerate(grid[9:12]):
            mini(d, c, M + i * (gw + gap), y, gw, ch)
        dotted_map(d, M + 3 * (gw + gap), y, gw, ch)
        y += ch + gap
        mini(d, grid[12], M, y, gw, ch)
        also_box(d, M + gw + gap, y, CW - gw - gap, ch, cols=3)
        bottom_bands(d, y + ch + gap)
    return img


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ni23g4-final2-A.png"
    im = build(which)
    if "--final" in sys.argv:
        im = im.convert("P", palette=Image.ADAPTIVE, colors=192)
    im.save(out, optimize=True)
    print(out, im.size, "stories", TOTAL, "regions", NREG, dict(COUNTS))
