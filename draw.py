#!/usr/bin/env python3
"""news-image-20261122 — 'THE DAILY ORBIT': Sunday 22 November 2026 in one image.

Dense broadsheet-style news poster drawn with Pillow. Fully deterministic:
no randomness, no timestamps, no network. Fonts are bundled in fonts/
next to this file. Output: $MAKEFUN_OUTPUT_DIR/entry.png when that
variable is set, else /output/entry.png when /output exists, otherwise
entry.png next to this file. 1024x1024, < 1 MiB.
"""
import os
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- constants
W, H = 1024, 1024
M = 24                      # page margin
CW = W - 2 * M              # content width

PAPER = (247, 243, 233)
PANEL = (253, 251, 245)
INK = (26, 24, 20)
GRAY = (88, 82, 72)
HAIR = (168, 160, 144)
RED = (178, 30, 30)
DRED = (138, 20, 20)
NAVY = (24, 42, 74)
GREEN = (22, 92, 54)
GOLD = (146, 108, 20)

HERE = os.path.dirname(os.path.abspath(__file__))
# Font resolution order: the fonts/ directory bundled next to this file
# first (the grader image has no system Noto fonts), then the system
# font directory, then Pillow's built-in default as a last resort.
FONT_DIRS = (os.path.join(HERE, "fonts"), "/usr/share/fonts/truetype/noto")
SERIF_BLACK = "NotoSerifDisplay-Black.ttf"
SERIF_XB = "NotoSerifDisplay-ExtraBold.ttf"
SERIF_B = "NotoSerifDisplay-Bold.ttf"
SANS_CB = "NotoSans-CondensedBold.ttf"
SANS_CSB = "NotoSans-CondensedSemiBold.ttf"
SANS_CM = "NotoSans-CondensedMedium.ttf"
SANS_C = "NotoSans-Condensed.ttf"

_cache = {}


def F(name, size):
    key = (name, size)
    if key not in _cache:
        font = None
        for d in FONT_DIRS:
            p = os.path.join(d, name)
            if os.path.isfile(p):
                font = ImageFont.truetype(p, size)
                break
        if font is None:
            font = ImageFont.load_default()
        _cache[key] = font
    return _cache[key]


# ---------------------------------------------------------------- helpers
def tw(d, text, font):
    return d.textlength(text, font=font)


def fit(d, text, path, max_w, start, floor=8):
    """Largest font size <= start whose text fits max_w."""
    s = start
    while s > floor and tw(d, text, F(path, s)) > max_w:
        s -= 1
    return F(path, s)


def tracked(d, xy, text, font, fill, track=2):
    """Draw letterspaced text; returns total width."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += tw(d, ch, font) + track
    return x - track - xy[0]


def tracked_w(d, text, font, track=2):
    return sum(tw(d, ch, font) for ch in text) + track * (len(text) - 1)


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(d, xy, text, font, fill, max_w, leading, max_lines=None):
    """Draw wrapped text; returns y after the block."""
    x, y = xy
    lines = wrap(d, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def rule(d, x0, x1, y, fill=INK, wdt=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


# ---------------------------------------------------------------- content
RED_STRIP = ("RUSSIAN MISSILES FALL ON POLAND \u2014 NATO VOWS TO DEFEND "
             "\u2018EVERY INCH\u2019  \u2022  CLIMATE TALKS DEADLOCKED  \u2022  "
             "WALL STREET CRASHES")

STATS = [
    ("3", "OBJECTS DOWN IN POLAND\n2 MISSILES + 1 JET DRONE"),
    ("$120B", "ADAPTATION TARGET A YEAR\nDROPPED FROM COP31 DRAFT"),
    ("-10%", "NASDAQ\u2019S WEEK \u2014 ITS WORST\nSINCE MARCH 2020"),
    ("7", "STRAIGHT DOWN DAYS FOR\nTHE S&P 500 \u2014 A 2020 FIRST"),
    ("1.5\u00b0C", "OVERSHOOT OF PARIS LIMIT\nCONCEDED IN COP TEXT"),
    ("-23%", "NVIDIA\u2019S WEEK \u2014 ITS WORST\nSINCE 2008"),
]

HEROES = [
    dict(
        accent=NAVY, kick="WARSAW \u2022 NATO \u2022 EASTERN FLANK",
        head="NATO: \u2018EVERY INCH OF POLAND WILL BE DEFENDED\u2019",
        body=("Two Russian missiles and a jet drone crashed in south-east "
              "Poland on Friday. In Warsaw on Saturday, NATO chief Mark Rutte "
              "pledged: \u201cI can guarantee NATO will defend every inch of "
              "Polish territory.\u201d No casualties. PM Tusk called it an "
              "intentional provocation; NATO\u2019s North Atlantic Council "
              "meets Monday in Brussels."),
        foot="Kh-101 wreckage confirmed at Nowy Lipowiec \u2022 Article 4 not invoked",
    ),
    dict(
        accent=GREEN, kick="ANTALYA \u2022 COP31 CLIMATE SUMMIT",
        head="CLIMATE TALKS DEADLOCK OVER TWO WORDS: FOSSIL FUELS",
        body=("COP31 ran past its Friday deadline with no deal. The latest "
              "draft deletes every mention of fossil fuels and drops the "
              "$120bn-a-year adaptation target for 2035. Some 130 nations "
              "demand transition language; oil states refuse. The EU says "
              "better no deal than a weak one. The 1.5\u00b0C overshoot is "
              "conceded in the text."),
        foot="Turkey\u2019s \u201835 by 35\u2019 electrification pledge survives",
    ),
    dict(
        accent=DRED, kick="NEW YORK \u2022 MARKETS IN FREEFALL",
        head="WALL STREET\u2019S WORST WEEK SINCE THE PANDEMIC",
        body=("Friday: S&P -3.7%, Nasdaq -5.3%, Nvidia -14% as "
              "the AI trade cracked. The S&P fell seven straight days and "
              "slid into correction; chip stocks lost 17% in the week, "
              "their worst since 2001. The fear gauge VIX closed at 35.9."),
        foot=None,  # bar chart instead
    ),
]

BARS = [("S&P 500", -8.6), ("NASDAQ", -10.0), ("DOW", -8.0), ("NVIDIA", -22.9)]

CARDS = [
    ("TRUMP EYES NUCLEAR SUMMIT",
     "Open to a trilateral meeting with Putin and Xi on nuclear disarmament, he says."),
    ("KYIV: BRIDGE STRIKE \u2018FAIR\u2019",
     "Zelensky cites 109 Russian air attacks on Ukraine\u2019s bridges before the Crimea strike."),
    ("DENMARK ACCUSES MOSCOW",
     "Copenhagen says Russia plotted to murder a US-Ukrainian rapper."),
    ("FINLAND PROBES AIR BREACH",
     "Russian helicopter strayed 4.1 km inside; Russian cargo ship ablaze in the Gulf."),
    ("IRAN STRIKE HITS BAHRAIN",
     "Industrial facility struck; air defences intercepted a second attack \u2014 Reuters."),
    ("HORMUZ SHIPPING ATTACKED",
     "Two UKMTO reports: unknown projectiles hit a vessel\u2019s stern and engine room."),
    ("HEGSETH MEMO CHILLS CANADA",
     "Secret memo limits US\u2013Canada defence relations, the Washington Post reports."),
    ("FBI PROBES NCIC HACK",
     "Agents investigate an alleged breach of the US national criminal database."),
    ("MEXICO NABS \u2018EL CHAPO ISIDRO\u2019",
     "Cartel boss Meza Flores, on the FBI\u2019s 10 Most Wanted, held after a shootout."),
    ("EU\u2013INDONESIA DEAL SIGNED",
     "Brussels and Jakarta sign the CEPA trade pact and an investment agreement."),
    ("EU FLOATS \u20ac1.78TN BUDGET",
     "Costa proposes the 2028\u201334 spending plan; leaders meet at a summit on 26\u201327 Nov."),
    ("LAGARDE TO LEAVE THE ECB",
     "Christine Lagarde steps down; the hunt for a new central bank chief begins."),
    ("DEMOCRATS RETAKE CONGRESS",
     "US midterm results hand both chambers of Congress back to the Democrats."),
    ("NORWAY VOIDS OIL LICENCES",
     "Supreme Court rules the climate-disputed drilling licences invalid."),
    ("NIGERIA BOAT DISASTER",
     "Rescuers recover 24 bodies after a boat capsizes, emergency agency NEMA says."),
    ("AL-SHABAAB AMBUSH CLAIM",
     "Militants claim hundreds of Somali soldiers killed in an ambush."),
    ("KENYA EBOLA PATIENT HOME",
     "Last patient discharged; the DR Congo death toll passes 5,300."),
    ("GHANA\u2019S HERITAGE NOTES",
     "New banknote series honours Kwame Nkrumah and Kofi Annan."),
    ("ALCARAZ INTO ATP FINAL",
     "Spaniard fights back past Shelton to set up a title match with Zverev."),
    ("FRANCE BEAT ARGENTINA",
     "Les Bleus reach the Nations Championship final vs South Africa; Australia beat Wales."),
    ("BOURNEMOUTH BEAT FOREST",
     "Evanilson scores for a sixth straight game; Coventry edge Palace 3\u20132."),
    ("GTA 6: CRITICS 99, FANS 5.6",
     "Rockstar\u2019s epic tops critic charts but is review-bombed by users on Metacritic."),
    ("ASSET SEIZURE LAW PASSED",
     "Indonesia\u2019s new law lets the state seize assets from Rp1 billion."),
    ("JAKARTA WAGE TOPS NATION",
     "2027 minimum: Jakarta Rp6,136,941; Bali jumps 42.15%; Bekasi Rp6,480,058 highest."),
    ("GREEN SM BIKE SHUTS DOWN",
     "The e-bike service stopped on 20 Nov; partner balances and units being returned."),
    ("TRAIN HITS MINIBUS, BURNS",
     "Siantar Express locomotive catches fire after a collision in Simalungun."),
    ("GUNS N\u2019 ROSES ROCK GBK",
     "MRT and TransJakarta ran past midnight for the Jakarta concert crowd."),
]

ALSO = ("ALSO: Rover Idefix launches toward the moons of Mars \u2022 jewellery "
        "scion Paolo Bulgari dies \u2022 IMOS 2026 motor show runs 20\u201329 Nov "
        "at ICE BSD \u2022 242,482 part-time PPPK teachers go full-time in 2027")

DATECHECK = ("Every story on this page was reported on 21\u201322 November 2026 "
             "and cross-checked against wire reports (Reuters, AP, BBC) on "
             "Sunday 22 November 2026. Market figures are Friday\u2019s close, "
             "20 November.")

# Dot-matrix world map: (row) -> list of (col_start, col_end) land spans.
MAP_ROWS = [
    [(8, 14), (18, 24), (28, 33), (58, 106)],
    [(4, 36), (54, 64), (66, 108)],
    [(6, 34), (53, 62), (64, 106)],
    [(8, 33), (52, 64), (66, 104)],
    [(10, 32), (52, 66), (68, 100), (102, 104)],
    [(12, 30), (50, 68), (70, 80), (84, 98)],
    [(13, 24), (50, 67), (74, 79), (82, 95)],
    [(15, 20), (51, 66), (75, 78), (83, 92)],
    [(31, 42), (53, 65), (84, 86), (89, 91), (93, 96)],
    [(32, 43), (55, 64), (86, 90), (93, 97)],
    [(33, 43), (56, 63), (89, 100)],
    [(34, 42), (57, 62), (90, 99)],
    [(35, 41), (58, 61), (91, 98)],
    [(36, 40), (104, 105)],
    [(37, 39)],
    [(37, 38)],
]
# (col, row): Warsaw, Antalya, New York, Mexico City, Bahrain, Nigeria,
# Kenya, Jakarta, Buenos Aires
PINS = [(58, 3), (63, 4), (29, 4), (15, 6), (71, 6), (54, 8), (63, 9),
        (88, 9), (38, 12)]


# ---------------------------------------------------------------- drawing
def masthead(d):
    y = 16
    rule(d, M, W - M, y, INK, 3)
    rule(d, M, W - M, y + 5, INK, 1)
    y += 12
    # side notes
    f_side = F(SANS_CSB, 11)
    d.text((M, y + 8), "GLOBAL EDITION", font=f_side, fill=GRAY)
    rtxt = "No. 327 \u2022 PRICE: ONE IMAGE"
    d.text((W - M - tw(d, rtxt, f_side), y + 8), rtxt, font=f_side, fill=GRAY)
    # paper name
    name = "THE DAILY ORBIT"
    fn = fit(d, name, SERIF_BLACK, 560, 54)
    d.text(((W - tw(d, name, fn)) / 2, y), name, font=fn, fill=INK)
    y += 48
    # giant date
    date = "SUNDAY 22 NOVEMBER 2026"
    fd_ = fit(d, date, SERIF_BLACK, CW, 64)
    d.text(((W - tw(d, date, fd_)) / 2, y), date, font=fd_, fill=INK)
    y += 58
    rule(d, M, W - M, y, INK, 1)
    rule(d, M, W - M, y + 3, INK, 3)
    return y + 8


def red_strip(d, y):
    h = 30
    d.rectangle([M, y, W - M, y + h], fill=RED)
    fs = fit(d, RED_STRIP, SANS_CB, CW - 20, 17)
    d.text(((W - tw(d, RED_STRIP, fs)) / 2, y + 5), RED_STRIP, font=fs,
           fill=(255, 250, 240))
    return y + h + 4


def world_strip(d, y):
    h = 26
    d.rectangle([M, y, W - M, y + h], fill=INK)
    f1 = F(SANS_CB, 15)
    d.text((M + 10, y + 4), "THE WORLD IN ONE DAY", font=f1,
           fill=(255, 250, 240))
    f2 = F(SANS_CSB, 12)
    t = "30 STORIES \u2022 SIX CONTINENTS \u2022 ONE PAGE"
    d.text((W - M - 10 - tw(d, t, f2), y + 6), t, font=f2, fill=(230, 224, 208))
    return y + h + 6


def stats_strip(d, y):
    n = len(STATS)
    gap = 8
    bw = (CW - gap * (n - 1)) / n
    f_num = F(SERIF_XB, 25)
    f_lab = F(SANS_CSB, 9)
    rule(d, M, W - M, y, HAIR, 1)
    y += 6
    for i, (num, lab) in enumerate(STATS):
        x = M + i * (bw + gap)
        if i:
            d.line([(x - gap / 2, y + 2), (x - gap / 2, y + 44)], fill=HAIR,
                   width=1)
        d.text((x, y), num, font=f_num, fill=DRED)
        ly = y + 30
        for ln in lab.split("\n"):
            d.text((x, ly), ln, font=f_lab, fill=GRAY)
            ly += 10.5
    y += 52
    rule(d, M, W - M, y, HAIR, 1)
    return y + 8


def star(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.34
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def hero(d, x, y, wdt, hgt, idx, spec):
    d.rectangle([x, y, x + wdt, y + hgt], fill=PANEL)
    d.rectangle([x, y, x + wdt, y + 5], fill=spec["accent"])
    # number badge
    d.rectangle([x + 10, y + 13, x + 34, y + 37], fill=spec["accent"])
    fn_ = F(SANS_CB, 17)
    num = str(idx + 1)
    d.text((x + 22 - tw(d, num, fn_) / 2, y + 16), num, font=fn_,
           fill=(255, 250, 240))
    fk = F(SANS_CB, 12)
    d.text((x + 42, y + 19), spec["kick"], font=fk, fill=spec["accent"])
    # headline
    fh = F(SERIF_B, 20)
    hy = block(d, (x + 10, y + 44), spec["head"], fh, INK, wdt - 20, 23, 3)
    rule(d, x + 10, x + wdt - 10, hy + 1, HAIR, 1)
    # body
    fb = F(SANS_C, 11)
    by = block(d, (x + 10, hy + 6), spec["body"], fb, (44, 41, 36),
               wdt - 20, 13.5)
    if idx == 0:
        rule(d, x + 10, x + wdt - 10, y + hgt - 38, HAIR, 1)
        star(d, x + wdt - 30, y + hgt - 20, 12, NAVY)
        ff = F(SANS_CM, 9)
        block(d, (x + 10, y + hgt - 32), spec["foot"], ff, GRAY, wdt - 52,
              11, 2)
    elif idx == 1:
        rule(d, x + 10, x + wdt - 10, y + hgt - 38, HAIR, 1)
        fbadge = F(SERIF_XB, 17)
        d.text((x + 10, y + hgt - 33), "35 BY 35", font=fbadge, fill=GREEN)
        ff = F(SANS_CM, 9)
        block(d, (x + 92, y + hgt - 30), spec["foot"], ff, GRAY, wdt - 102,
              11, 2)
    else:
        # weekly-loss bars
        fy = by + 6
        fl = F(SANS_CSB, 10)
        fv = F(SANS_CB, 10)
        d.text((x + 10, fy), "THE WEEK IN FULL:", font=fl, fill=GRAY)
        fy += 14
        maxv = 25.0
        for name, val in BARS:
            d.text((x + 10, fy), name, font=fl, fill=INK)
            bx = x + 76
            blen = (abs(val) / maxv) * (wdt - 140)
            d.rectangle([bx, fy + 2, bx + blen, fy + 10], fill=RED)
            vt = f"{val:.1f}%".replace("-", "-")
            d.text((bx + blen + 5, fy), vt, font=fv, fill=DRED)
            fy += 13
    d.rectangle([x, y, x + wdt, y + hgt], outline=HAIR, width=1)


def heroes(d, y):
    gap = 12
    wdt = (CW - 2 * gap) / 3
    hgt = 240
    for i, spec in enumerate(HEROES):
        hero(d, M + i * (wdt + gap), y, wdt, hgt, i, spec)
    return y + hgt + 10


def cards(d, y):
    cols, rows = 3, 9
    gap = 14
    wdt = (CW - (cols - 1) * gap) / cols
    rh = 41
    f_num = F(SANS_CB, 12)
    f_head = F(SANS_CB, 12)
    f_body = F(SANS_C, 9.5)
    for i, (head, body) in enumerate(CARDS):
        cx = M + (i % cols) * (wdt + gap)
        cy = y + (i // cols) * rh
        num = str(i + 4)
        d.rectangle([cx, cy + 1, cx + 17, cy + 18], fill=RED)
        d.text((cx + 8.5 - tw(d, num, f_num) / 2, cy + 3), num, font=f_num,
               fill=(255, 250, 240))
        hx = cx + 23
        hw = wdt - 23
        hl = wrap(d, head, f_head, hw)
        if len(hl) == 1 and tw(d, head, f_head) <= hw:
            d.text((hx, cy), head, font=f_head, fill=INK)
            by = cy + 15
        else:
            d.text((hx, cy), hl[0], font=f_head, fill=INK)
            if len(hl) > 1:
                d.text((hx, cy + 13), hl[1], font=f_head, fill=INK)
            by = cy + 28
        block(d, (hx, by), body, f_body, (58, 54, 48), hw, 10.5, 2)
        if i // cols < rows - 1:
            rule(d, cx, cx + wdt, cy + rh - 3, (216, 209, 192), 1)
    return y + rows * rh + 2


def draw_map(d, x, y, pitch=3.6, r=1.2):
    for ri, spans in enumerate(MAP_ROWS):
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                cx = x + c * pitch
                cy = y + ri * pitch
                d.ellipse([cx - r, cy - r, cx + r, cy + r],
                          fill=(150, 143, 126))
    for c, ri in PINS:
        cx = x + c * pitch
        cy = y + ri * pitch
        d.ellipse([cx - 3.4, cy - 3.4, cx + 3.4, cy + 3.4], fill=RED,
                  outline=(255, 250, 240), width=1)


def bottom_band(d, y):
    # ALSO ticker
    fa = fit(d, ALSO, SANS_CSB, CW, 12)
    d.text((M, y), ALSO, font=fa, fill=(44, 41, 36))
    y += 18
    rule(d, M, W - M, y, INK, 2)
    y += 8
    # map left
    d.text((M, y), "WHERE IT HAPPENED", font=F(SANS_CB, 11), fill=INK)
    draw_map(d, M + 2, y + 20)
    # date check box right
    bx = M + 420
    bw = W - M - bx
    d.rectangle([bx, y, bx + bw, y + 78], outline=RED, width=2)
    d.rectangle([bx, y, bx + bw, y + 20], fill=RED)
    fd_ = F(SANS_CB, 13)
    d.text((bx + 10, y + 3), "DATE CHECK", font=fd_, fill=(255, 250, 240))
    block(d, (bx + 10, y + 26), DATECHECK, F(SANS_C, 10.5), (44, 41, 36),
          bw - 20, 12.5, 4)
    # footer
    fy = y + 86
    ff = F(SANS_CM, 9)
    foot = ("Compiled Sunday 22 November 2026 \u2022 Sources: Reuters, AP, BBC, "
            "Schwab, Investopedia and wire reports \u2022 The Daily Orbit \u2014 "
            "the world in one day")
    d.text(((W - tw(d, foot, ff)) / 2, fy), foot, font=ff, fill=GRAY)
    return fy + 14


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = masthead(d)
    y = red_strip(d, y)
    y = world_strip(d, y)
    y = stats_strip(d, y)
    y = heroes(d, y)
    y = cards(d, y)
    bottom_band(d, y)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or (
        "/output" if os.path.isdir("/output") else HERE)
    out = os.path.join(out_dir, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
