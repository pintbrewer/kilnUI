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

class Menu(object):
    """
    docstring
    """
    def __init__(self, txt_lst, screen_sz=(128, 64), selected=None):
        self.txt_lst = txt_lst
        self.screen_sz = screen_sz
        self.selected = selected or 0
        self.canvas = Image.new('1', (self.screen_sz[0], 
                                     self.screen_sz[1]))
        self.drawing = ImageDraw.Draw(self.canvas)
        self.draw_text()

    def draw_text(self):
        """
        docstring
        """
        start = 0
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        txt_ht = (self.drawing.textsize('A', font=font))[1]
        for line in self.txt_lst:
            self.drawing.text((0,start), line, font=font, fill=1)
            start = start + txt_ht
        #max_lines = (display.height - text_start[1])//font_ht


# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height

home_menu = Menu(['LOAD_SCHEDULE', 'NEW_SCHEDULE'], screen_sz=(width, height))
disp.image(home_menu.canvas)
disp.show() 
