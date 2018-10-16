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
    main_font = pygame.font.SysFont("menlo", 10)
    font_height = main_font.get_height()
    text_start = [2, 2]
    text = []
    for item in selections:
        if selected == selections.index(item):
            text.append(main_font.render(item, 1, black, white))
        else:
            text.append(main_font.render(item, 1, white, black))
    for txt in text:
        screen.blit(txt, text_start)
        text_start = [text_start[0], text_start[1] + font_height]
    pygame.display.update()

def get_new_list(selected):
    if selected == "LOAD SCHEDULE":
        new_list = load_schedule()
    elif selected =="HOME":
        new_list = HOME
    elif selected == "NEW SCHEDULE":
        new_list = display_schedule()
    return new_list

def load_schedule():
    schedules = os.listdir('schedules')
    return schedules

def main():
    running = True
    screen = init_screen() 
    selected = 0
    item_list = HOME
    select_mode(screen, item_list, selected)
    # main loop
    while running:
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            print(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if selected < len(item_list) - 1:
                    selected = selected + 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if selected > 0 :
                    selected = selected - 1   
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                screen = init_screen()
                item_list = get_new_list(item_list[selected])
            select_mode(screen, item_list, selected)
            if (event.type == pygame.QUIT):
                # change the value to False, to exit the main loop
                running = False
     

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()