from os.path import join

import PIL.Image
import PIL.ImageFont
import PIL.ImageDraw


weights = {
    'regular': 'FiraSans-Regular.ttf',
    'bold':  'FiraSans-Bold.ttf'
}

font_cache = {}

def load_font(weight, size):
    """
    Load font given weight and size into the font cache and return
    a PIL.ImageFont representing it
    """
    if (weight, size) in font_cache:
        return font_cache[(weight, size)]

    else:
        font = PIL.ImageFont.truetype(join('fonts', weights[weight]), size)
        font_cache[(weight, size)] = font

        return font

def stamp(img, xy, text, weight='regular', size=10, fill=(255,255,255,255)):
    """
    Draw text on PIL image in place
    """
    font = load_font(weight, size)
    draw = PIL.ImageDraw.Draw(img)
    draw.text(xy, text, fill=fill, font=font)
