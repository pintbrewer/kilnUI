import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
# Create the SSD1306 OLED class.
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
#draw.rectangle((0, 0, width, height), outline=1, fill=1)
#draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)

# Load a font in 2 different sizes.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)

# Draw the text
#draw.text((0, 0), "Hello!", font=font, fill=255)
#draw.text((0, 30), "Hello!", font=font2, fill=255)
#draw.text((34, 46), "Hello!", font=font2, fill=255)
my_txt = draw.textsize('Hello', font=font2)

draw.text((0, 0), 'Hello', font=font2, outline=1, fill=1)
draw.text((0, (my_txt[1] )), 'World!', outline=1, font=font2, fill=1)
disp.image(image)
disp.show()
