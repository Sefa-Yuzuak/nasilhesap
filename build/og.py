# -*- coding: utf-8 -*-
"""static/og.png (1200x630) sosyal paylaşım görseli."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

KOK = Path(__file__).resolve().parent.parent
W, H = 1200, 630


def font(px, bold=True):
    for p in (["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold
              else ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]):
        try:
            return ImageFont.truetype(p, px)
        except OSError:
            continue
    return ImageFont.load_default()


im = Image.new("RGB", (W, H), (79, 70, 229))
d = ImageDraw.Draw(im)
for y in range(H):
    f = y / H
    d.line([(0, y), (W, y)], fill=(int(79 - 25 * f), int(70 - 25 * f), int(229 - 40 * f)))
d.rounded_rectangle([80, 120, 200, 240], radius=28, fill=(255, 255, 255))
d.rounded_rectangle([104, 158, 176, 172], radius=7, fill=(79, 70, 229))
d.rounded_rectangle([104, 188, 176, 202], radius=7, fill=(79, 70, 229))
d.ellipse([178, 108, 206, 136], fill=(251, 191, 36))
d.text((80, 290), "Nasıl Hesap", font=font(88), fill=(255, 255, 255))
d.text((84, 400), "Nasıl hesaplanır? Anında hesapla.", font=font(40, False), fill=(224, 231, 255))
d.text((84, 470), "KDV · maaş · kıdem · kredi · kira artışı · vergi · emlak · sağlık", font=font(30, False), fill=(199, 210, 254))
d.text((84, 560), "nasilhesap.com  ·  2026 resmî oranlar  ·  ücretsiz", font=font(28), fill=(255, 255, 255))
(KOK / "static").mkdir(exist_ok=True)
im.save(KOK / "static" / "og.png", optimize=True)
print("og.png OK")
