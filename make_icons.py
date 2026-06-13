#!/usr/bin/env python3
"""App icon for 'Aisle Be There' — a bright shopping basket with colourful
groceries poking out, on the brand green."""
from PIL import Image, ImageDraw

GREEN = (29, 158, 117)
DARK  = (15, 110, 86)
WHITE = (255, 255, 255)
# little grocery colours peeking out of the basket
VEGGIES = [(99, 153, 34), (216, 90, 48), (224, 169, 59), (55, 138, 221), (214, 96, 138)]

def draw(d, S, maskable=False):
    pad = S * (0.27 if maskable else 0.21)
    w = S - pad * 2
    lw = max(2, int(S * 0.045))
    cx = S / 2
    rim_y = pad + w * 0.34          # top rim of basket
    base_y = pad + w                # bottom

    # groceries peeking above the rim (drawn first, behind the basket front)
    n = len(VEGGIES)
    for i, col in enumerate(VEGGIES):
        gx = pad + w * (i + 0.5) / n
        gr = w * 0.12
        d.ellipse([gx - gr, rim_y - gr * 1.7, gx + gr, rim_y + gr * 0.3], fill=col)

    # handle
    hr = w * 0.30
    d.arc([cx - hr, rim_y - hr * 1.5, cx + hr, rim_y + hr * 0.5],
          200, 340, fill=WHITE, width=lw)

    # basket body (trapezoid) as a filled white shape
    bx0, bx1 = pad + w * 0.04, S - pad - w * 0.04
    d.polygon([(bx0, rim_y), (bx1, rim_y),
               (bx1 - w * 0.14, base_y), (bx0 + w * 0.14, base_y)], fill=WHITE)
    # rim bar
    d.rounded_rectangle([pad, rim_y - lw, S - pad, rim_y + lw],
                        radius=lw, fill=WHITE)
    # basket weave slats (green cut-outs)
    for i in range(1, 4):
        x = bx0 + (bx1 - bx0) * i / 4
        d.line([(x, rim_y + lw * 1.5), (x - w * 0.04 * (i - 1.5) * 2, base_y - lw)],
               fill=GREEN, width=max(2, int(lw * 0.7)))

def make(size, name, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if maskable:
        d.rectangle([0, 0, size, size], fill=GREEN)
    else:
        d.rounded_rectangle([0, 0, size, size], radius=int(size * 0.22), fill=GREEN)
    draw(d, size, maskable)
    img.save(name)
    print("wrote", name)

make(1024, "icon-1024.png")
make(512,  "icon-512.png")
make(192,  "icon-192.png")
make(180,  "icon-180.png")
make(512,  "icon-maskable-512.png", maskable=True)
