# import the pygame module, so you can use it
import pygame
import os

SCREEN_WIDTH = 128
SCREEN_HEIGHT  = 64
black = (0,0,0)
white = (255,255,255)
HOME = ["LOAD SCHEDULE", "NEW SCHEDULE"]

def init_screen():
    pygame.init()
    # create a surface on screen
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    screen.fill(black) 
    pygame.draw.rect(screen, white, (0,0,SCREEN_WIDTH,SCREEN_HEIGHT), 1) # screen border

    pygame.display.update()
    return screen

def select_mode(screen, selections, selected):
    #selections = ["LOAD SCHEDULE", "NEW SCHEDULE"]
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

def get_new_list(mode, selected):
    if mode == "list_strings":
        if selected == "LOAD SCHEDULE":
            new_list = dir_schedules()
            new_mode = "list_files"
    elif mode == "list_files":
        new_list = read_schedule("schedules/" + selected)
        new_mode = "list_display"
    return (new_mode, new_list)

def dir_schedules():
    schedules = os.listdir('schedules')
    return schedules

def read_schedule(schedule_file):
    lines = []
    with open(schedule_file, "r") as f:
        for line in f:
            lines.append(line.rstrip())
    return lines

def main():
    running = True
    screen = init_screen() 
    mode = "list_strings"
    selected = 0
    item_list = HOME
    select_mode(screen, item_list, selected)
    # main loop
    while running:
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            print(mode, event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if selected < len(item_list) - 1:
                    selected = selected + 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if selected > 0 :
                    selected = selected - 1   
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                screen = init_screen()
                (mode, item_list) = get_new_list(mode, item_list[selected])
            select_mode(screen, item_list, selected)
            if (event.type == pygame.QUIT):
                # change the value to False, to exit the main loop
                running = False
     

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()