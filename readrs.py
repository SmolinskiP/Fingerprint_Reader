from datetime import datetime
import sys
from lib.init_envs import *
from lib.drawing import Draw_Text, Draw_Img
from sql.functions import Get_EmployeeData, Update_EmployeeData, Get_Actual_Breaks
from lib.checkentry import Check_Entry

def Draw_MainScreen(db_counter, breaks_dict):
    screen.fill((42, 42, 42))
    Draw_Text(datetime.now().strftime("%H:%M:%S"), screen, main_font, x // 2, y * 6/8)
    Draw_Text("Przyłóż kartę do czytnika", screen, main_font, x // 2, y * 5/8)
    Draw_Img(img_logo, screen, x //2, y * 3/10)
    if krzychu_jest == "krzychu":
        Draw_Img(img_krzychu_dir[img_rotation], screen, x * 17/20, y * 17/20)
    if db_counter == 0:
        breaks_dict = Get_Actual_Breaks()
    y_offset = 20
    for key, item in breaks_dict.items():
        y_offset+=22
        Draw_Text(item, screen, list_font, x-200, y-y_offset, color=(0, 153, 76))
    if len(breaks_dict) > 0:
        y_offset+=25
        Draw_Text("Na przerwie:", screen, list_font, x-200, y-y_offset)
    return breaks_dict
            
        
def Draw_ChoiceScreen(name):
    screen.fill((42, 42, 42))
    Draw_Text("Witaj", screen, name_font, x // 2, y * 2/20)
    Draw_Text(name, screen, name_font, x // 2, y * 3/20)
    area_enter = pygame.Rect(5, y * 5/20, x/2-10, y * 13/40)
    area_exit = pygame.Rect(x/2+5, y * 5/20, x/2-10, y * 13/40)
    area_break = pygame.Rect(5, y * 12/20+5, x/2-10, y * 13/40)
    area_breakend = pygame.Rect(x/2+5, y * 12/20+5, x/2-10, y * 13/40)
    entry_enter = pygame.draw.rect(screen, (0, 158, 96), area_enter, border_radius = 30)
    entry_break = pygame.draw.rect(screen, (119,136,153), area_break, border_radius = 30)
    entry_exit = pygame.draw.rect(screen, (165, 42, 42), area_exit, border_radius = 30)
    entry_breakend = pygame.draw.rect(screen, (47,79,79), area_breakend, border_radius = 30)
    text_color = (20, 20, 20)
    Draw_Text("Wejście", screen, button_font, area_enter.center[0], area_enter.center[1], color=text_color)
    Draw_Text("Wyjście", screen, button_font, area_exit.center[0], area_exit.center[1], color=text_color)
    Draw_Text("Przerwa", screen, button_font, area_break.center[0], area_break.center[1], color=text_color)
    Draw_Text("Po przerwie", screen, button_font, area_breakend.center[0], area_breakend.center[1], color=text_color)
    if screen_timeout < 290:
        Draw_Text(str(int(screen_timeout/60)), screen, main_font, x/4, y/9, color=text_color)
        Draw_Img(img_wheel_dir[img_rotation], screen, x/4, y/9)
        Draw_Text(str(int(screen_timeout/60)), screen, main_font, x*3/4, y/9, color=text_color)
        Draw_Img(img_wheel_dir[img_rotation_2], screen, x*3/4, y/9)
    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
        if event.type == pygame.FINGERDOWN:
            fingerx = event.x * screen.get_width()
            fingery = event.y * screen.get_height()
            event.pos = fingerx, fingery
        print(event.pos)
#        if event.button == 1:
        if area_enter.collidepoint(event.pos):
            print("Wejście")
            action = 1
        elif area_exit.collidepoint(event.pos):
            print("Wyjście")
            action = 2
        elif area_break.collidepoint(event.pos):
            print("Przerwa")
            action = 3
        elif area_breakend.collidepoint(event.pos):
            action = 4
            print("Koniec przerwy")
        else:
            action = 5
    if 'action' not in locals():
        action = 5
    return action
            
def Draw_SuccessErrorScreen(text1, text2, text_color):
    screen.fill((42, 42, 42))
    if screen_timeout < 180:
        Draw_Text(text1, screen, main_font, x/2, y*5/8, color=text_color)
        Draw_Text(text2, screen, main_font, x/2, y*6/8, color=text_color)
        Draw_Img(img_icon, screen, x/2, y*5/16)
        Draw_Img(img_wheel2_dir[img_rotation], screen, x/2, y*5/16)

    

        
        
pygame.quit()