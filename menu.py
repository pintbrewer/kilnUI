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
        self.width = screen_sz[0]
        self.height = screen_sz[1]
        self.selected = selected or 0
        self.screen_start = 0
        self.canvas = Image.new('1', (self.width, 
                                     self.height))
        self.drawing = ImageDraw.Draw(self.canvas)
        self.wipe_canvas()
        self.draw_text()
        

    def draw_text(self):
        """
        docstring
        """
        start = 0
        space = 4
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        txt_ht = (self.drawing.textsize('A', font=font))[1]
        max_lines = self.height//(txt_ht + space)
        screen_end = max_lines - 1 + self.screen_start
        
        for index, line in enumerate(self.txt_lst):
            if self.screen_start > index:
                continue
            if index > screen_end:
                break
            self.drawing.text((10,start), line, font=font, fill=1)
            if index == self.selected:
                self.drawing.polygon([(0,start),
                                      (6,start + (txt_ht//2)),
                                      (0,start + txt_ht)],fill=1, outline=1)
            start = start + txt_ht + space



        #max_lines = (display.height - text_start[1])//font_ht

    def wipe_canvas(self):
        self.drawing.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

    def inc_selected(self):
        self.selected == (len(self.txt_lst)-1) or self.selected = self.selected + 1
        self.wipe_canvas()
        self.draw_text()

    def dec_selected(self):
        """
        docstring
        """
        self.selected == 0 or = self.selected - 1
        self.wipe_canvas()
        self.draw_text()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height

home_menu = Menu(['LOAD_SCHEDULE', 'NEW_SCHEDULE'], screen_sz=(width, height))
disp.image(home_menu.canvas)
disp.show() 
