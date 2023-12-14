from PIL import ImageDraw, Image, ImageFont
from os import path

def split_text(text, font, draw):
    text_words = text.split()
    temp = ""
    lines = []
    for i in range(0, len(text_words)):
        pixels = draw.textlength(temp, font)
        if pixels > (1024 - 200 - 200):
            lines.append(temp)
            temp = ""
        temp = temp + text_words[i] + " "
    temp = ""
    for line in lines:
        line = line.rstrip()
        temp = temp + line + "\n"
    return temp

def add_punchline(draw, text, color):
    font = ImageFont.truetype(font="./banner/fonts/Lato/Lato-Bold.ttf", size=44)
    text = split_text(text, font, draw)
    draw.multiline_text(xy=(100, 700), text=text, fill=color, font=font, align='center')

def draw_button(d, text, canvas_width, canvas_height, color):
    font = ImageFont.truetype("./banner/fonts/Lato/Lato-Regular.ttf", size=24)
    text_width = d.textlength(text, font)
    padding_y = 20
    padding_x = padding_y * 2
    button_size = (padding_x + text_width + padding_x, padding_y + font.size + padding_y)

    margin_bottom = 40
    margin_left = (int)((canvas_width - button_size[0]) / 2)
    d.rounded_rectangle(xy=(margin_left,
                            canvas_height - (7 + margin_bottom + button_size[1]),
                            margin_left + button_size[0],
                            canvas_height - (7 + margin_bottom)),
                        fill=(41,88,63),
                        corners=(True, True, True, True),
                        radius=7)
    x0 = margin_left + padding_x
    y0 = canvas_height - (7 + margin_bottom + padding_y + font.size)
    d.text(xy=(x0, y0), text=text, font=font, align='center')

def create(sd, logo, color, punchline, button_text):
    canvas_size = (1024, 1024)
    logo_size = (128, 128)
    sd_image_size = (512, 512)
    im = Image.new(mode="RGB", size=canvas_size, color=(255, 255, 255))
    logo_image = Image.open(logo).convert('RGB').resize(logo_size)
    sd_image = Image.open(sd).convert('RGB').resize(sd_image_size)
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle(xy=(30, 0, 996, 7), fill=color, corners=(False, False, True, True), radius=6)
    draw.rounded_rectangle(xy=(30, 1017, 996, 1024), fill=color, corners=(True, True, False, False), radius=6)
    im.paste(logo_image, ((int)((canvas_size[0] - logo_size[0]) / 2), 20))
    im.paste(sd_image, ((int)((canvas_size[0] - sd_image_size[0]) / 2), (20 + logo_size[1] + 20)))
    add_punchline(draw, punchline, color)
    draw_button(draw, button_text, canvas_size[0], canvas_size[1], color)
#   im.save("./banner/ad.png")
    return im