import pygame

running = True
pygame.init()
pygame.display.set_caption('RCP_v2.0') #Tytuł
pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #FULLSCREEN
#screen = pygame.display.set_mode([600, 600])

clock = pygame.time.Clock() #Initiate clock to set max fps to 60

x = screen.get_width() #scren width
y = screen.get_height() #same but height

#Initialize fonts
main_font = pygame.font.SysFont("Verdana", int(x/22), bold=True)
list_font = pygame.font.SysFont("Verdana", int(x/110), bold=True)
name_font = pygame.font.SysFont("Verdana", int(x/30), bold=True)
button_font = pygame.font.SysFont("Verdana", int(x/15), bold=True)

#Load logo image (main screen)
img_logo = pygame.image.load('img\\logo.png') #load image from directory
img_logo_x = img_logo.get_width() #get width of image
img_logo_y = img_logo.get_height() #get height of image
new_img_logo_size = (int(x * 7/10), int(img_logo_y * (x * 7/10 / img_logo_x))) #set new image size based of values you get and some high university math (output - tuple i think)
img_logo = pygame.transform.scale(img_logo, new_img_logo_size) #finally transform image (img_logo) to new size from previous step (new_img_logo_size)

#Load krzychu image, create dictionary with 360 krzychu images every rotated 1 degree more realational to previous
img_krzychu = pygame.image.load('img\\krzychu.jpg') #same as before but...
img_krzychu_x = img_krzychu.get_width()
img_krzychu_y = img_krzychu.get_height()
new_img_krzychu_size = (int(x * 1/10), int(img_krzychu_y * (x * 1/10 / img_krzychu_x)))
img_krzychu = pygame.transform.scale(img_krzychu, new_img_krzychu_size)
i = 0 #... here initialize 0 for loop below
img_krzychu_dir = {} #initialize empty dictionary
while i <= 360: #for every number from 0 to 360
    img_krzychu_dir[i] = pygame.transform.rotate(img_krzychu, i) #assign to that number in dictionary image of rotated krzychu
    i+=1 #and finally, add 1 to i to avoid neverending loop
    
#Same with wheel 1 - needs rotation
img_wheel = pygame.image.load('img\\wheel.png')
img_wheel_x = img_wheel.get_width()
img_wheel_y = img_wheel.get_height()
new_img_wheel_size = (int(x * 1/9), int(img_wheel_y * (x * 1/9 / img_wheel_x)))
img_wheel = pygame.transform.scale(img_wheel, new_img_wheel_size)
i = 0
img_wheel_dir = {}
while i <= 360:
    img_wheel_dir[i] = pygame.transform.rotate(img_wheel, i)
    i+=1
    
#Load icon image (success / error screen)
img_icon = pygame.image.load('img\\icon.png')
img_icon_x = img_icon.get_width()
img_icon_y = img_icon.get_height()
new_img_icon_size = (int(x * 3/20), int(img_icon_y * (x * 3/20 / img_icon_x)))
img_icon = pygame.transform.scale(img_icon, new_img_icon_size)

#Same as wheel 2
img_wheel2 = pygame.image.load('img\\wheel2.png')
img_wheel2_x = img_wheel2.get_width()
img_wheel2_y = img_wheel2.get_height()
new_img_wheel2_size = (int(x * 3/9), int(img_wheel2_y * (x * 3/9 / img_wheel2_x)))
img_wheel2 = pygame.transform.scale(img_wheel2, new_img_wheel2_size)
i = 0
img_wheel2_dir = {}
while i <= 360:
    img_wheel2_dir[i] = pygame.transform.rotate(img_wheel2, i)
    i+=1
    
#Declare some initial setup for main program
img_rotation = 0 #Incrementing rotation (right) - every step +X
img_rotation_2 = 360 #Decrementing rotation (left) - every step -X
screen_state = 0 #screen state (0 - main, 1 - buttons, 2 - success/error)
screen_timeout = 290 #after that amount of frames close screen (screen state 1 and 2)
data_crawled = False #check if have user info, 0 - dont have, 1 - have. Should be True/False but whatever
action = 5 #initial action, 5 means no action. 1 - entry, 2 - exit, 3 - break, 4 - breakend
db_counter = 0
breaks_dict = {}