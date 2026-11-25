#!/usr/bin/env python3
"""THE WORLD TODAY -- front page summing up Wednesday 25 November 2026.

Draws a 1024x1024 newspaper front page with Pillow (stdlib + Pillow only),
deterministically, with no network access and no timestamps in the output.
Writes entry.png next to this script and, when writable, to /output/entry.png.

Stories (see NEWS.md): Houthi drone strike hits Riyadh's tallest tower,
11 wounded; Huawei convicted on 10 counts in Brooklyn; Zelenskiy confirms
Ukraine hit the Russian cargo ship Sparta II; Trump awards Giuliani the
Medal of Freedom; CIA and ODNI breached; Gukesh-Sindarov chess Game 2
today; NATO early-warning aircraft for Poland; South Korea education
minister resigns; Nvidia shares fall 7%.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36

PAPER = (247, 241, 227)   # cream newsprint
INK = (25, 23, 19)
RED = (158, 27, 27)
NAVY = (30, 58, 95)
GREEN = (30, 107, 58)
GREY = (90, 84, 72)
LIGHT = (233, 224, 203)
GOLD = (201, 162, 39)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load a DejaVu font; fall back to Pillow's built-in bitmap font."""
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)             # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)         # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)               # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` px."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_para(draw, x, y, text, fnt, width, fill=INK, leading=1.28):
    """Draw wrapped text; return the y just below the last line."""
    size = fnt.size if hasattr(fnt, "size") else 16
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(size * leading)
    return y


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, color=RED, size=17):
    f = SANS_B(size)
    draw.text((x, y), text.upper(), font=f, fill=color)
    return y + size + 6


def story(draw, x, y, w, kick, head, body, head_size=27, body_size=16):
    """One grid story: red kicker, serif headline, sans body. Returns bottom y."""
    y = kicker(draw, x, y, kick)
    y = draw_para(draw, x, y, head, SERIF_B(head_size), w, leading=1.12)
    y += 2
    y = draw_para(draw, x, y, body, SANS(body_size), w, fill=(52, 48, 40),
                  leading=1.3)
    return y


def draw_hero_art(draw, x, y, w, h):
    """Vector illustration: the PIF Tower in Riyadh, struck midway up,
    with a small drone approaching from the right."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    # PIF Tower: tall slab, slightly tapered
    tx0, tx1 = x + 118, x + 218
    ty0, ty1 = y + 14, y + h - 62
    draw.polygon([(tx0, ty1), (tx0 + 8, ty0), (tx1 - 8, ty0), (tx1, ty1)],
                 fill=(52, 84, 128))
    # lit windows
    for wy in range(ty0 + 16, ty1 - 12, 18):
        for wx in (tx0 + 18, tx0 + 46, tx0 + 74):
            draw.rectangle([wx, wy, wx + 8, wy + 8],
                           fill=(201, 162, 39))
    # impact burst midway up the tower
    ix, iy = (tx0 + tx1) // 2, y + 108
    for ang in range(0, 360, 30):
        import math
        r = 26
        ex = ix + int(r * math.cos(math.radians(ang)))
        ey = iy + int(r * math.sin(math.radians(ang)))
        draw.line([(ix, iy), (ex, ey)], fill=(255, 190, 60), width=4)
    draw.ellipse([ix - 14, iy - 14, ix + 14, iy + 14], fill=(255, 120, 40),
                 outline=(255, 220, 120), width=2)
    # small drone, top right
    dx, dy = x + w - 78, y + 34
    draw.ellipse([dx - 16, dy - 6, dx + 16, dy + 6], fill=(220, 225, 235))
    draw.line([(dx - 24, dy - 10), (dx - 8, dy - 2)], fill=(220, 225, 235),
              width=3)
    draw.line([(dx + 8, dy - 2), (dx + 24, dy - 10)], fill=(220, 225, 235),
              width=3)
    draw.line([(dx - 24, dy + 10), (dx - 8, dy + 2)], fill=(220, 225, 235),
              width=3)
    draw.line([(dx + 8, dy + 2), (dx + 24, dy + 10)], fill=(220, 225, 235),
              width=3)
    draw.text((x + 16, y + h - 30), "PIF TOWER, RIYADH  •  2ND STRIKE IN A WEEK",
              font=SANS_B(13), fill=(255, 255, 255))
    draw.text((x + 16, y + h - 52), "11 WOUNDED",
              font=SANS_B(16), fill=(255, 190, 60))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # ---- Masthead -------------------------------------------------------
    d.text((W // 2, 18), "THE WORLD TODAY", font=SERIF_B(84), fill=INK,
           anchor="ma")
    rule(d, x0, x1, 118, width=3)
    d.text((x0, 128), "WEDNESDAY, 25 NOVEMBER 2026", font=SANS_B(19), fill=INK)
    d.text((x1, 128), "ONE DAY  •  ONE PAGE  •  THE WORLD",
           font=SANS_B(19), fill=INK, anchor="ra")
    rule(d, x0, x1, 158, width=1)

    # ---- Hero -----------------------------------------------------------
    hy = 172
    hy = kicker(d, x0, hy, "Conflict  •  Middle East", size=18)
    hero_head = "DRONE HITS RIYADH\nTALLEST TOWER"
    y = hy
    for line in hero_head.split("\n"):
        d.text((x0, y), line, font=SERIF_B(46), fill=INK)
        y += 50
    y += 4
    y = draw_para(d, x0, y,
                  "Houthi fighters struck the PIF Tower in Riyadh "
                  "for the second time in less than a week. "
                  "Eleven people were wounded; the Saudi-led "
                  "coalition vowed a decisive response.",
                  SANS(18), 560, leading=1.35)

    # hero art, right column
    draw_hero_art(d, 612, 172, x1 - 612, 236)
    rule(d, x0, x1, 428, width=2)

    # ---- Grid: 2 columns x 3 rows ---------------------------------------
    col_w = (x1 - x0 - 28) // 2
    col_x = [x0, x0 + col_w + 28]
    row_y = [446, 606, 766]
    stories = [
        ("Law  •  United States",
         "Huawei guilty on 10 counts",
         "A Brooklyn jury convicted Huawei of bank fraud, sanctions "
         "violations and stealing trade secrets. It was acquitted of "
         "racketeering; the case dates to 2018."),
        ("War  •  Ukraine",
         "Zelenskiy owns ship strike",
         "Kyiv confirms its drone hit the Russian cargo ship Sparta II "
         "in the Gulf of Finland. Norway, a staunch ally, urges caution."),
        ("Politics  •  United States",
         "Trump honours Giuliani",
         "The Medal of Freedom goes to ex-New York mayor Rudy Giuliani "
         "in a private Oval Office ceremony — the third of Trump's "
         "second term."),
        ("Security  •  Washington",
         "CIA and spy chief's office breached",
         "America's CIA and the director of national intelligence "
         "suffered a cyber breach involving some unclassified "
         "information, a source says."),
        ("Sport  •  Chess",
         "Game 2 today in Geneva",
         "Gukesh and Sindarov drew their world title opener in 38 "
         "moves. Game 2 today, 15:00 CET — Gukesh has White, "
         "scores level."),
        ("Defence  •  Europe",
         "NATO watches Poland's skies",
         "NATO plans early-warning aircraft in Poland after missiles "
         "landed there during an attack on Ukraine."),
    ]
    for i, (kick, head, body) in enumerate(stories):
        story(d, col_x[i % 2], row_y[i // 2], col_w, kick, head, body)
    rule(d, x0, x1, 926, width=1)

    # ---- Footer briefs --------------------------------------------------
    fy = 940
    d.text((x0, fy), "ALSO TODAY", font=SANS_B(16), fill=RED)
    d.text((x0 + 130, fy),
           "South Korea's education minister resigns over an exam-cheating scandal.",
           font=SANS(16), fill=INK)
    d.text((x0, fy + 26),
           "MARKETS",
           font=SANS_B(16), fill=RED)
    d.text((x0 + 130, fy + 26),
           "Nvidia falls 7% as lawmakers demand answers on Huang; Dell lifts forecasts.",
           font=SANS(16), fill=INK)
    d.text((x1, fy + 52), "Sources: Reuters  •  AP  •  Bloomberg  •  DOJ  •  FIDE",
           font=SANS(13), fill=GREY, anchor="ra")

    out_here = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "entry.png")
    img.save(out_here, "PNG")
    try:
        os.makedirs("/output", exist_ok=True)
        img.save("/output/entry.png", "PNG")
    except OSError:
        pass
    print("wrote", out_here)


if __name__ == "__main__":
    main()
