import qrcode
from qrcode.constants import ERROR_CORRECT_H
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw, ImageFont
import os

URL = "https://jaydencheng.github.io/senhe-kitchen-menu/"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

BRAND_ORANGE = (232, 114, 30)
INK = (90, 52, 22)
PAPER = (251, 238, 218)

qr = qrcode.QRCode(
    version=None,
    error_correction=ERROR_CORRECT_H,
    box_size=24,
    border=2,
)
qr.add_data(URL)
qr.make(fit=True)

img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=SolidFillColorMask(back_color=PAPER, front_color=INK),
).convert("RGB")

# Add brand-color frame and caption
W, H = img.size
PAD_TOP = 180
PAD_BOTTOM = 160
PAD_SIDE = 80
canvas = Image.new("RGB", (W + PAD_SIDE * 2, H + PAD_TOP + PAD_BOTTOM), PAPER)
canvas.paste(img, (PAD_SIDE, PAD_TOP))

draw = ImageDraw.Draw(canvas)

# Orange header bar with brand title inside
header_h = 130
draw.rectangle([(0, 0), (canvas.size[0], header_h)], fill=BRAND_ORANGE)

def try_font(names, size):
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            pass
    return ImageFont.load_default()

title_font = try_font([
    "/System/Library/Fonts/PingFang.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
], 72)
sub_label_font = try_font([
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
], 24)
sub_font = try_font([
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
], 38)
small_font = try_font([
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
], 28)

# Title 森禾樂廚 centered in header
title = "森禾樂廚"
bbox = draw.textbbox((0, 0), title, font=title_font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
draw.text(((canvas.size[0] - tw) / 2, (header_h - th) / 2 - 4), title, fill=PAPER, font=title_font)

# Bilingual menu caption
caption = "SCAN FOR BILINGUAL MENU"
cw = draw.textlength(caption, font=sub_font)
draw.text(((canvas.size[0] - cw) / 2, PAD_TOP + H + 40), caption, fill=INK, font=sub_font)

# URL footer
url_short = "jaydencheng.github.io/senhe-kitchen-menu"
uw = draw.textlength(url_short, font=small_font)
draw.text(((canvas.size[0] - uw) / 2, PAD_TOP + H + 95), url_short, fill=(138, 90, 48), font=small_font)

out = os.path.join(OUT_DIR, "qr-code.png")
canvas.save(out, "PNG", optimize=True)
print(f"Saved: {out}")
print(f"Size: {canvas.size}")

# Also save a plain version for prints/stickers
img_plain = qrcode.make(URL, error_correction=ERROR_CORRECT_H, box_size=20, border=4).convert("RGB")
plain_out = os.path.join(OUT_DIR, "qr-code-plain.png")
img_plain.save(plain_out, "PNG", optimize=True)
print(f"Saved plain: {plain_out} ({img_plain.size})")
