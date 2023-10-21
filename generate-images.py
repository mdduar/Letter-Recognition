import argparse
from PIL import Image, ImageDraw, ImageFont
import string

## BLUE 55 182 246

## ORANGE 249 157 7

## YELLOW 249 225 4

## GREEN 53 212 97

def main():
  parser = argparse.ArgumentParser(
    description='Generate Images',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  
  parser.add_argument('--dimensions','-d', type=int, nargs=2,
                        default=[1920, 1080],
                        metavar="N N",
                        help="Dimensions for the images")
  
  parser.add_argument('--bgcolor','-bg', type=int, nargs=3,
                        default=[255, 255, 255],
                        metavar="N N N",
                        help="Background Color")
  
  parser.add_argument('--fgcolor','-fg', type=int, nargs=3,
                        default=[0, 0, 0],
                        metavar="N N N",
                        help="Foreground Color")

  parser.add_argument('--uppercase', '-u',action='store_true', 
                      help='include the uppercase letter')
  
  parser.add_argument('--lowercase', '-l',action='store_true', 
                      help='include the lowercase letter')
  
  parser.add_argument('--numbers', '-n',action='store_true', 
                      help='include the numbers 0-9')
  
  parser.add_argument('--font-size', '-fs', type=int, default=900,
                      help='font-size for each character')
  
  args = parser.parse_args()
  characters = []
  
  if args.uppercase:
    characters.extend(string.ascii_uppercase)

  if args.lowercase:
    characters.extend(string.ascii_lowercase)

  if args.numbers:
    characters.extend([str(x) for x in range(10)])

  for x in characters:
    generate_image(x, args.dimensions, f'output/{x}.png', args.font_size, tuple(args.bgcolor), tuple(args.fgcolor))


def generate_image(character, dimensions, file_name, font_size, bgcolor, fgcolor):
  image = Image.new('RGB', dimensions, bgcolor)

  font = ImageFont.truetype("/home/mdduar/.local/share/fonts/Monotype/OpenType/Sassoon Infant Std/Sassoon_Infant_Std_Bold.otf", font_size)

  draw = ImageDraw.Draw(image)

  text_dimensions = draw.textbbox((0,0), character, font, anchor="lt")

  coord = tuple((dimensions[x] - text_dimensions[x+2]) // 2 for x in range(2))
  print(coord)

  draw.text(coord, character, fill=fgcolor, font=font, anchor="lt")

  image.save(file_name)

if __name__ == '__main__':
  main()