from PIL import Image, ImageDraw

# Bilder laden
img1 = Image.open("../figures/Fig 2a de üs 2020 baseline 13-19 plus C19.tif")
img2 = Image.open("../figures/Fig 2b de üs 2021 baseline 13-19.tif")
img3 = Image.open("../figures/Fig 2c de üs 2022 baseline 13-19.tif")
img4 = Image.open("../figures/Fig 2d de üs 2023 baseline 13-19.tif")

# gleiche Größe annehmen
w, h = img1.size

# neue Leinwand
canvas = Image.new("RGB", (2*w, 2*h), "white")

# einfügen
canvas.paste(img1, (0, 0))
canvas.paste(img2, (w, 0))
canvas.paste(img3, (0, h))
canvas.paste(img4, (w, h))

# optional Labels
draw = ImageDraw.Draw(canvas)
draw.text((20, 20), "(a)", fill="black")
draw.text((w+20, 20), "(b)", fill="black")
draw.text((20, h+20), "(c)", fill="black")
draw.text((w+20, h+20), "(d)", fill="black")

canvas.save("../figures/Fig 2 abcd_combined.tif", dpi=(600,600),
            compression="tiff_lzw")