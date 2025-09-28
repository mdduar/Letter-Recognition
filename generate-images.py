import argparse
from PIL import Image, ImageDraw, ImageFont
import string
import os
import math

IMAGELOOKUP = {
  "a" : "assets/images/apple.png",
  "b" : "assets/images/ball.png",
  "c" : "assets/images/cat.png",
  "d" : "assets/images/dog.png",
  "e" : "assets/images/elephant.png",
  "f" : "assets/images/fish.png",
  "g" : "assets/images/goat.png",
  "h" : "assets/images/house.png",
}

def main():
  parser = argparse.ArgumentParser(
    description='Generate Images',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--dimensions','-d', type=int, nargs=2,
                        default=[1920, 1080],
                        metavar="N N",
                        help="Dimensions for the images")
  
  parser.add_argument('--font-path','-fp', type=str,
                        default=None,
                        help="Path to font")
  
  parser.add_argument('--bgcolor','-bg', type=int, nargs=3,
                        default=[255, 255, 255],
                        metavar="N N N",
                        help="Background Color")
  
  parser.add_argument('--fgcolor','-fg', type=int, nargs=3,
                        default=[0, 0, 0],
                        metavar="N N N",
                        help="Foreground Color")
  

  parser.add_argument('--image-width','-iw', type=int,
                        default=None,
                        help="Image width, if blank no image")

  parser.add_argument('--uppercase', '-u',action='store_true', 
                      help='include the uppercase letter')
  
  parser.add_argument('--lowercase', '-l',action='store_true', 
                      help='include the lowercase letter')
  
  parser.add_argument('--bothcases', '-bc',action='store_true', 
                      help='include the uppercase and lower case letters paired')
  
  parser.add_argument('--numbers', '-n',action='store_true', 
                      help='include the numbers 0-9')
  
  parser.add_argument('--font-size', '-fs', type=int, default=900,
                      help='font-size for each character')
  
  parser.add_argument('--character-set', '-cs', type=str, default=None,
                      help='custom character set')
  
  args = parser.parse_args()
  characters = []

  if args.character_set:
    characters.extend(args.character_set)
  
  if args.uppercase:
    characters.extend(string.ascii_uppercase)

  if args.lowercase:
    characters.extend(string.ascii_lowercase)

  if args.bothcases:
    characters.extend(["".join(pair) for pair in zip(string.ascii_uppercase, string.ascii_lowercase)])



  if args.numbers:
    characters.extend([str(x) for x in range(10)])

  for x in characters:
    generate_image(x, args.dimensions, f'output/{x}.png', args.font_path, args.font_size, tuple(args.bgcolor), tuple(args.fgcolor), args.image_width)

def get_font_path(path):
  if path:
    return path
  
  fonts = [f for f in os.listdir('assets/fonts/') if os.path.isfile(os.path.join('fonts',f)) and f != '.gitkeep']
  if len(fonts):
    return os.path.join('fonts',fonts[0])
  
  return None

def generate_image(character, dimensions, file_name, font_path, font_size, bgcolor, fgcolor, addon_width):
  image = Image.new('RGB', dimensions, bgcolor)

  font_path = get_font_path(font_path)
  if font_path == None:
    font = ImageFont.load_default(font_size)

  else:
    font = ImageFont.truetype(font_path, font_size)

  draw = ImageDraw.Draw(image)

  text_dimensions = draw.textbbox((0,0), character, font, anchor="lt")

  # coord = list((dimensions[x] - text_dimensions[x+2]) // 2 for x in range(2))
  coord = list(dimensions[x] // 2 for x in range(2))
  if addon_width:
    try:
      addon_image = Image.open(IMAGELOOKUP[character[0].lower()])
    except:
      addon_image = None
  else:
    addon_image = None

  if addon_image:
    # resize image
    original_size = addon_image.size
    resize = float(addon_width) / float( original_size[0])
    addon_height = int(float(original_size[1]) * resize)
    addon_image = addon_image.resize((addon_width, addon_height))
    total_foreground_width = addon_width + text_dimensions[2]
    total_horizontal_margin = dimensions[0] - total_foreground_width
    x = int(total_horizontal_margin // 1.5)
    addon_coord = list((dimensions[x] - addon_image.size[x]) // 2 for x in range(2))
    coord[0]  = text_dimensions[2] // 2 + x
    addon_coord[0] = dimensions[1]  - x

    image.paste(addon_image, addon_coord, addon_image)
  draw.text(coord, character, fill=fgcolor, font=font, anchor="mm")

  image.save(file_name)

if __name__ == '__main__':
  main()