#!/usr/bin/env python3
"""Generate app icons: a simple shopping basket on the Nudge-green brand."""
from PIL import Image, ImageDraw

GREEN = (29, 158, 117)      # --accent
DARK  = (15, 110, 86)       # --accent-d
WHITE = (255, 255, 255)

def basket(d, S, maskable=False):
    # padding bigger for maskable so the glyph stays inside the safe zone
    pad = S * (0.26 if maskable else 0.20)
    w = S - pad * 2
    top = pad + w * 0.18
    lw = max(2, int(S * 0.045))
    # handle
    hr = w * 0.22
    cx = S / 2
    d.arc([cx - hr, top - hr * 1.1, cx + hr, top + hr * 0.9], 180, 360, fill=WHITE, width=lw)
    # basket trapezoid
    bx0, bx1 = pad, S - pad
    by0, by1 = top, pad + w
    d.polygon([(bx0, by0), (bx1, by0), (bx1 - w*0.12, by1), (bx0 + w*0.12, by1)], fill=WHITE)
    # slats (cut-outs in green)
    for i in range(1, 4):
        x = bx0 + w * i / 4
        d.line([(x, by0 + lw), (x - w*0.03*(i-1.5)*2, by1 - lw)], fill=GREEN, width=max(2, int(lw*0.7)))

def make(size, name, maskable=False, radius_frac=0.0):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if maskable:
        d.rectangle([0, 0, size, size], fill=GREEN)
    else:
        r = int(size * 0.22)
        d.rounded_rectangle([0, 0, size, size], radius=r, fill=GREEN)
    basket(d, size, maskable)
    img.save(name)
    print("wrote", name)

make(1024, "icon-1024.png")
make(512, "icon-512.png")
make(192, "icon-192.png")
make(180, "icon-180.png")
make(512, "icon-maskable-512.png", maskable=True)
