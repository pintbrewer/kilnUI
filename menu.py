import os
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306



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
        self.screen_end = 1
        self.canvas = Image.new('1', (self.width, 
                                     self.height))
        self.drawing = ImageDraw.Draw(self.canvas)
        self.wipe_canvas()
        self.draw_text()
        

    def draw_text(self):
        """
        Draw the text, skipping anything that is our of range of the available
        lines on the screen
        Draw a triangle next to the selected item
        """
        start = 0
        space = 4
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        txt_ht = (self.drawing.textsize('A', font=font))[1]
        max_lines = self.height//(txt_ht + space)
        self.screen_end = max_lines - 1 + self.screen_start
        
        for index, line in enumerate(self.txt_lst):
            if self.screen_start > index:
                continue
            if index > self.screen_end:
                break
            self.drawing.text((10,start), line, font=font, fill=1)
            if index == self.selected:
                self.drawing.polygon([(0,start),
                                      (6,start + (txt_ht//2)),
                                      (0,start + txt_ht)],fill=1, outline=1)
            start = start + txt_ht + space

    def wipe_canvas(self):
        '''
        just draw a black square to clear the screen
        '''
        self.drawing.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

    def inc_selected(self):
        '''
        Increment the selected item by one until max items
        adjust the list start and end attributes if scrolling
        '''
        if self.selected < len(self.txt_lst) - 1:
            self.selected += 1
            if self.selected > self.screen_end:
                self.screen_start += 1
                self.screen_end += 1
        self.wipe_canvas()
        self.draw_text()

    def dec_selected(self):
        """
        Decrement the selected item by one until max items
        adjust the list start and end attributes if scrolling
        """
        if self.selected > 0:
            self.selected -= 1
            if self.selected < self.screen_start:
                self.screen_start -= 1
                self.screen_end -= 1
        self.wipe_canvas()
        self.draw_text()

class Mode(object):
    """
    docstring
    """
    def __init__(self):
        self.mode = 'home'
        self.HOME = ['LOAD_SCHEDULE', 'NEW_SCHEDULE']
        self.menu = self.HOME

    def change(self, select):
        print(self.mode + ' : ' + select)
        if self.mode == 'home' and select == 'LOAD_SCHEDULE':
            self.menu = self._get_files()
            self.menu.append('Back')
            self.mode = 'disp_files'
        elif self.mode == 'disp_files' and select == 'Back':
            self.mode = 'home'
            self.menu = self.HOME
        elif self.mode == 'disp_files' and select != 'Back':
            self.mode = 'disp_schedule'
            self.menu = self._read_schedule(select)
            self.menu.extend(['START_SCHEDULE', 'Back'])
        elif self.mode == 'disp_schedule' and select == 'Back':
            self.mode = 'home'
            self.menu = self.HOME
        elif self.mode == 'disp_schedule' and select == 'START_SCHEDULE':
            print('starting schedule')
            self.mode = 'home'
            self.menu = self.HOME
    
    @staticmethod
    def _get_files():
        schedules = os.listdir('schedules')
        return schedules
    
    @staticmethod
    def _read_schedule(schedule_file):
        lines = []
        with open('schedules/' + schedule_file, "r") as f:
            for line in f:
                lines.append(line.rstrip())
        return lines


def main():
    # Create the I2C interface.
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create the SSD1306 OLED class.
    disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

    # Clear display.
    disp.fill(0)
    disp.show()

    # Input pins:
    # button_A = DigitalInOut(board.D5)
    # button_A.direction = Direction.INPUT
    # button_A.pull = Pull.UP

    # button_B = DigitalInOut(board.D6)
    # button_B.direction = Direction.INPUT
    # button_B.pull = Pull.UP

    # button_L = DigitalInOut(board.D27)
    # button_L.direction = Direction.INPUT
    # button_L.pull = Pull.UP

    # button_R = DigitalInOut(board.D23)
    # button_R.direction = Direction.INPUT
    # button_R.pull = Pull.UP

    button_U = DigitalInOut(board.D17)
    button_U.direction = Direction.INPUT
    button_U.pull = Pull.UP
    U_pressed = False

    button_D = DigitalInOut(board.D22)
    button_D.direction = Direction.INPUT
    button_D.pull = Pull.UP
    D_pressed = False

    button_C = DigitalInOut(board.D4)
    button_C.direction = Direction.INPUT
    button_C.pull = Pull.UP
    C_pressed = False
    
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height


    mode = Mode()
    menu = Menu(mode.menu, screen_sz=(width, height))

    while True:
        if button_U.value:  # button is released
            if U_pressed:
                menu.dec_selected()
                U_pressed = False
        else: # button pressed
            U_pressed = True
        
        if button_D.value:
            if D_pressed:
                menu.inc_selected()
                D_pressed = False
        else:
            D_pressed = True
        
        if button_C.value:
            if C_pressed:
                mode.change(menu.txt_lst[menu.selected])
                menu = Menu(mode.menu)
                C_pressed = False
        else:
            C_pressed = True

        
        disp.image(menu.canvas)
        disp.show()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()