def Draw_Text(text, screen, font, x, y, color=(190, 190, 190)):
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)
    
def Draw_Img(img, screen, x, y):
    imgRect = img.get_rect()
    imgRect.center = (x, y)
    screen.blit(img, imgRect)
