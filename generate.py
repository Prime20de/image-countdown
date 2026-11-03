from datetime import date, datetime
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont

# ---- Einstellungen ----
STICHTAG = date(2028, 9, 1)
TEXT_FARBE = (58, 170, 53)       # Grün
ZAHL_FARBE = (58, 170, 53)       # Grün
HINTERGRUND = (255, 255, 255, 0) # transparent; für Weiß: (255, 255, 255, 255)
AUSGABE = "docs/countdown.png"
SCALE = 2                        # 2x für scharfe Darstellung (Retina)
# -----------------------

FONT_PFADE = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

def font(size, bold=False):
    pfad = FONT_PFADE[1] if bold else FONT_PFADE[0]
    return ImageFont.truetype(pfad, size * SCALE)

heute = datetime.now(ZoneInfo("Europe/Berlin")).date()
tage = (STICHTAG - heute).days

if tage > 1:
    teile = [(str(tage), True), (" Tage noch", False)]
elif tage == 1:
    teile = [("1", True), (" Tag noch!", False)]
elif tage == 0:
    teile = [("Es ist soweit!", True)]
else:
    vergangen = abs(tage)
    einheit = "Tag" if vergangen == 1 else "Tagen"
    teile = [("Seit ", False), (str(vergangen), True), (f" {einheit} ist es soweit", False)]

W, H = 360 * SCALE, 30 * SCALE
img = Image.new("RGBA", (W, H), HINTERGRUND)
d = ImageDraw.Draw(img)

x = 0
for text, fett in teile:
    f = font(15, bold=fett)
    farbe = ZAHL_FARBE if fett else TEXT_FARBE
    d.text((x, H // 2), text, font=f, fill=farbe, anchor="lm")
    x += d.textlength(text, font=f)

img = img.crop((0, 0, int(x) + 2, H))
img.save(AUSGABE)
print(f"{heute}: {tage} Tage -> {AUSGABE} ({img.size[0] // SCALE}x{img.size[1] // SCALE} px)")
