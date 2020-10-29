# import the pygame module, so you can use it
import pygame
import os

SCREEN_WIDTH = 128
SCREEN_HEIGHT  = 64
black = (0,0,0)
white = (255,255,255)
back = 'Back'

def init_screen():
    pygame.init()
    # create a surface on screen
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    screen.fill(black) 
    pygame.draw.rect(screen, white, (0,0,SCREEN_WIDTH,SCREEN_HEIGHT), 1) # screen border

    pygame.display.update()
    return screen

def get_menu_items(menu, mode):
    if menu == 'HOME':
        menu_items = ["LOAD SCHEDULE", "NEW SCHEDULE"]
    if menu == "LOAD SCHEDULE":
        menu_items = os.listdir('schedules')
        menu_items.append(back)
    if menu == 'DISPLAY SCHEDULE':
        menu_items = ["TEMP,RATE,TIME"]
    if menu == "NEW SCHEDULE":
        pass
    return (menu_items, mode)

def process_choice(menu, item):
    if menu == 'HOME' and item == 'LOAD SCHEDULE':
        new_menu = 'LOAD SCHEDULE'
    if menu == "HOME" and item == 'NEW SCHEDULE':
        new_menu = 'NEW SCHEDULE'
    if menu == 'LOAD SCHEDULE' and item == back:
        new_menu = 'HOME'
    if menu == 'LOAD SCHEDULE' and item != back:
        new_menu = 'DISPLAY SCHEDULE'
    return new_menu

def read_schedule(schedule_file):
    lines = []
    with open(schedule_file, "r") as f:
        for line in f:
            lines.append(line.rstrip())
    return lines

def display_selections(screen, selections, selected):
    init_screen()
    main_font = pygame.font.SysFont("menlo", 10)
    font_height = main_font.get_height()
    text_start = [2, 2]
    max_lines = (SCREEN_HEIGHT - text_start[1])//font_height
    print("max lines: " + str(max_lines))
    text = []
    for item in selections:
        if selected == selections.index(item):
            text.append(main_font.render(item, 1, black, white))
        else:
            text.append(main_font.render(item, 1, white, black))
    if (selected + 1) > max_lines:
        start_index = (selected + 1) - max_lines
        max_index = max_lines
    else:
        start_index = 0
        max_index = len(selections) - 1
    if max_index + 1 > max_lines:
        max_index = start_index + (max_lines - 1)
    for txt in range(start_index,max_index+1):
        screen.blit(text[txt], text_start)
        text_start = [text_start[0], text_start[1] + font_height]
    pygame.display.update()

def main():
    running = True
    screen = init_screen() 
    menu = "HOME"
    selected = 0
    # main loop
    while running:
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            #print(mode, event)
            (menu_items, mode) = get_menu_items(menu, mode)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if selected < len(menu_items) - 1:
                    selected = selected + 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if selected > 0 :
                    selected = selected - 1   
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                screen = init_screen()
                menu = process_choice(menu, menu_items[selected])
                selected = 0
            display_selections(screen, menu_items, selected)
            if (event.type == pygame.QUIT):
                # change the value to False, to exit the main loop
                running = False
     

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()