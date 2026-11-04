from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
canvas = Image.new('RGB', (1800, 560), '#071c22')
draw = ImageDraw.Draw(canvas)
title = ImageFont.truetype('C:/Windows/Fonts/georgia.ttf', 42)
body = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 20)
small = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 15)
draw.text((40, 25), 'Life in Mumbai', font=title, fill='#f4ead4')
draw.text((42, 83), 'Landscape depth study / three moments from the scroll journey', font=body, fill='#a9bcba')
frames = [
    ('mumbai-city.jpg', '01 / ARRIVE', 'Mumbai never slows down.'),
    ('mumbai-curiosity.jpg', '02 / GO DEEPER', 'Neither does my curiosity.'),
    ('mumbai-journey.jpg', '03 / FURTHER IN', 'Look where it took me.'),
]
for i, (name, label, phrase) in enumerate(frames):
    x = 40 + i * 580
    image = Image.open(ROOT / name).convert('RGB').resize((560, 350), Image.Resampling.LANCZOS)
    canvas.paste(image, (x, 130))
    draw.text((x, 497), label, font=small, fill='#a9bcba')
    draw.text((x, 524), phrase, font=body, fill='#f4ead4')
canvas.save(ROOT / 'mumbai-depth-mockup.png')
print('Saved review/mumbai-depth-mockup.png')
