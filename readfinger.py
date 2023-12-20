from datetime import datetime
import sys, os, time, threading, serial
from lib.init_envs import *
from lib.drawing import Draw_Text, Draw_Img
from sql.functions import Get_EmployeeData, Update_EmployeeData, Get_Actual_Breaks
from lib.checkentry import Check_Entry

global screen_state
global text1
global text2
global text_color
global screen_timeout

def Draw_MainScreen(db_counter, breaks_dict):
    screen.fill((42, 42, 42))
    Draw_Text(datetime.now().strftime("%H:%M:%S"), screen, main_font, x // 2, y * 6/8)
    Draw_Text("Przyłóż palec do czytnika", screen, main_font, x // 2, y * 5/8)
    Draw_Img(img_logo, screen, x //2, y * 3/10)
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

def Draw_AdminScreen():
    screen.fill((42, 42, 42)) 
    text_color = (20, 20, 20)
    Draw_Text("Wybierz akcje", screen, name_font, x // 2, y * 2/20)
    
    area_add_finger = pygame.Rect(5, y * 5/20, x-5, y * 13/40)
    entry_add_finger = pygame.draw.rect(screen, (0, 158, 96), area_add_finger, border_radius = 30)
    Draw_Text("Dodaj odcisk", screen, button_font, area_add_finger.center[0], area_add_finger.center[1], color=text_color)
    area_remove_finger = pygame.Rect(5, y * 12/20+5, x-5, y * 13/40)
    entry_remove_finger = pygame.draw.rect(screen, (165, 42, 42), area_remove_finger, border_radius = 30)
    Draw_Text("Usuń odcisk", screen, button_font, area_remove_finger.center[0], area_remove_finger.center[1], color=text_color)
    
    if screen_timeout < 600:
        Draw_Text(str(int(screen_timeout/60)), screen, main_font, x/4, y/9, color=text_color)
        Draw_Img(img_wheel_dir[img_rotation], screen, x/4, y/9)
        Draw_Text(str(int(screen_timeout/60)), screen, main_font, x*3/4, y/9, color=text_color)
        Draw_Img(img_wheel_dir[img_rotation_2], screen, x*3/4, y/9)
        
    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
         if event.type == pygame.FINGERDOWN:
            fingerx = event.x * screen.get_width()
            fingery = event.y * screen.get_height()
            event.pos = fingerx, fingery
         if area_add_finger.collidepoint(event.pos):
             Tx_Data_Process("CMD2")
         if area_remove_finger.collidepoint(event.pos):
             print("USUWAM ODCISK") 
            
def Draw_SuccessErrorScreen(text1, text2, text_color):
    screen.fill((42, 42, 42))
    if screen_timeout < 180:
        Draw_Text(text1, screen, main_font, x/2, y*5/8, color=text_color)
        Draw_Text(text2, screen, main_font, x/2, y*6/8, color=text_color)
        Draw_Img(img_icon, screen, x/2, y*5/16)
        Draw_Img(img_wheel2_dir[img_rotation], screen, x/2, y*5/16)

def Draw_InfoScreen(text1, text2, text_color):
    screen.fill((42, 42, 42))
    Draw_Text(text1, screen, main_font, x // 2, y * 5/8)
    Draw_Text(text2, screen, main_font, x // 2, y * 6/8)
    Draw_Img(img_logo, screen, x //2, y * 3/10)
        

# Packet Identify code
Command                 = 0xAA55
Response                = 0x55AA
Command_Data            = 0xA55A
Response_Data           = 0x5AA5

# Soruce Device ID
Command_SID             = 0x00
Response_SID            = 0x01

# Destination Device ID 
Command_DID             = 0x00
Response_DID            = 0x00

# Command Code and Response Code
CMD_TEST_CONNECTION     = 0x01
CMD_FINGER_DETECT       = 0x21
CMD_GET_IMAGE           = 0x20
CMD_GENERATE            = 0x60
CMD_MERGE               = 0x61
CMD_DEL_CHAR            = 0x44
CMD_STORE_CHAR          = 0x40
CMD_SEARCH              = 0x63
CMD_VERIFY 				= 0x64
CMD_GET_EMPTY_ID 		= 0x45
CMD_GET_ENROLL_COUNT 	= 0x48
CMD_DOWN_IMAGE 			= 0x23
CMD_UP_IMAGE_CODE 		= 0x22

# Result Code  		
ERR_SUCCESS				= 0x00
ERR_FAIL				= 0x01
ERR_TIME_OUT			= 0x23
ERR_FP_NOT_DETECTED		= 0x28
ERR_FP_CANCEL			= 0x41
ERR_INVALID_BUFFER_ID	= 0x26
ERR_BAD_QUALITY			= 0x19
ERR_GEN_COUNT			= 0x25
ERR_INVALID_TMPL_NO		= 0x1D
ERR_DUPLICATION_ID		= 0x18
ERR_INVALID_PARAM		= 0x22
ERR_TMPL_EMPTY			= 0x12
ERR_VERIFY				= 0x10
ERR_IDENTIFY			= 0x11

# Length of DATA
DATA_0					= 0x0000		
DATA_1					= 0x0001		
DATA_2					= 0x0002		
DATA_3					= 0x0003		
DATA_4					= 0x0004		
DATA_5					= 0x0005		
DATA_6					= 0x0006		
DATA_38					= 0x0026		
DATA_498				= 0x01F2
DATA_390				= 0x0186

# Command structure
CMD_Len  				= 16
RPS_Len 				= 14
CMD_Packet_Len  		= 498
RPS_Packet_Len  		= 498

Finger_RST_Pin    		= 24
TRUE       				= 1
FALSE        			= 0
Tx_flag        			= 0

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')

ser = serial.Serial("COM8", 115200)
cmd = [0x55, 0xAA ,0x00 ,0x00 ,0x01 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00, 0x00 ,0x01]
rps = [0x00] * 26
cmd_data = [0xff] * 508
cmd_data1 = [0xff] * 400


class Cmd_Packet:
    def __init__(self):
        self.PREFIX = 0x0000
        self.SID 	= 0x00
        self.DID 	= 0x00
        self.CMD 	= 0x00
        self.LEN 	= 0x0000
        self.DATA 	= [0x00] * 16
        self.CKS 	= 0x0000

class Rps_Packet:
    def __init__(self):
        self.PREFIX = 0x0000
        self.SID 	= 0x00
        self.DID 	= 0x00
        self.CMD 	= 0x00
        self.LEN 	= 0x0000
        self.RET 	= 0x0000
        self.DATA 	= [0x00] * 14
        self.CKS 	= 0x0000	

class Command_Packet:
    def __init__(self):
        self.PREFIX = 0x0000
        self.SID 	= 0x00
        self.DID 	= 0x00
        self.CMD 	= 0x00
        self.LEN 	= 0x0000
        self.DATA 	= [0x00] * 498
        self.CKS 	= 0x0000

class Response_Packet:
    def __init__(self):
        self.PREFIX = 0x0000
        self.SID 	= 0x00
        self.DID 	= 0x00
        self.CMD 	= 0x00
        self.RCM    = 0X0000
        self.LEN 	= 0x0000
        self.RET 	= 0x0000
        self.DATA 	= [0x00] * 498
        self.CKS 	= 0x0000	

CMD = Cmd_Packet()
RPS = Rps_Packet()
CMD_DATA = Command_Packet()
RPS_DATA = Response_Packet()

def Tx_cmd():
    CKS = 0
    cmd[0] = CMD.PREFIX & 0xff
    cmd[1] = (CMD.PREFIX & 0xff00) >> 8
    cmd[2] = CMD.SID
    cmd[3] = CMD.DID
    cmd[4] = CMD.CMD
    cmd[5] = 0x00
    cmd[6] = CMD.LEN & 0xff
    cmd[7] = (CMD.LEN & 0xff00) >> 8
    for i in range(CMD.LEN):
        cmd[8+i] = CMD.DATA[i]
    for i in range(24):
        CKS = CKS + cmd[i]
    cmd[24] = CKS & 0xff
    cmd[25] = (CKS & 0xff00) >> 8
    ser.write(cmd)   

def Tx_cmd_data(SN):
    CKS = 0
    cmd_data[0] = CMD_DATA.PREFIX & 0xff
    cmd_data[1] = (CMD_DATA.PREFIX & 0xff00) >> 8
    cmd_data[2] = CMD_DATA.SID
    cmd_data[3] = CMD_DATA.DID
    cmd_data[4] = CMD_DATA.CMD
    cmd_data[5] = 0x00
    cmd_data[6] = CMD_DATA.LEN & 0xff
    cmd_data[7] = (CMD_DATA.LEN & 0xff00) >> 8
    if SN<129:
        for i in range(CMD_DATA.LEN):
            cmd_data[8+i] = CMD_DATA.DATA[i]
        for i in range(506):
            CKS = CKS + cmd_data[i]
            cmd_data[506] = CKS & 0xff
            cmd_data[507] = (CKS & 0xff00) >> 8

        ser.write(cmd_data)
    else :
        for i in range(CMD_DATA.LEN):
            cmd_data[8+i] = CMD_DATA.DATA[i]
        for i in range(398):
            CKS = CKS + cmd_data[i]
            cmd_data[398] = CKS & 0xff
            cmd_data[399] = (CKS & 0xff00) >> 8
        ser.write(cmd)

def Tx_Data_Process(command):
    str = command
    if((str[0] == 'C') & (str[1] == 'M') & (str[2] == 'D')):
        if str[3] == '0':
            CmdTestConnection( 0 )
        elif str[3] == '1':
            status = CmdFingerDetect( 0 )
            return status
        elif str[3] == '2':
            AddUser()
            return 1
        elif str[3] == '3':
            ClearUser( 0 )
        elif str[3] == '4':
            VerifyUser()
        elif str[3] == '5':
            status = ScopeVerifyUser()
            return status
        elif str[3] == '6':
            CmdGetEmptyID( 0 )
        elif str[3] == '7':
            GetUserCount( 1 )
        elif str[3] == '8':
            CmdUpImageCode( 1 )
        elif str[3] == '9':
            CmdDownImage()
        else:
            time.sleep(0.01)
            return 0

def CmdTestConnection( back ):
    CMD.CMD = CMD_TEST_CONNECTION
    CMD.LEN = DATA_0
    Tx_cmd()
    return Rx_cmd(back)

def CmdFingerDetect( back ):
    CMD.CMD = CMD_FINGER_DETECT
    CMD.LEN = DATA_0
    Tx_cmd()
    return Rx_cmd(back)

def CmdGetImage( back ):
	CMD.CMD = CMD_GET_IMAGE
	CMD.LEN = DATA_0
	Tx_cmd()
	return Rx_cmd(back)

def CmdGenerate( k , back ):
	CMD.CMD = CMD_GENERATE
	CMD.LEN = DATA_2
	CMD.DATA[0] = k 
	CMD.DATA[1] = 0x00 
	Tx_cmd()
	return Rx_cmd(back)

def CmdMerge( k , n , back ):
	CMD.CMD = CMD_MERGE
	CMD.LEN = DATA_3
	CMD.DATA[0] = k 
	CMD.DATA[1] = 0x00 
	CMD.DATA[2] = n 
	Tx_cmd()
	return Rx_cmd(back)

def CmdStoreChar( k , n , back ):
	CMD.CMD = CMD_STORE_CHAR
	CMD.LEN = DATA_4
	CMD.DATA[0] = k 
	CMD.DATA[1] = 0x00 
	CMD.DATA[2] = n 
	CMD.DATA[3] = 0x00 
	Tx_cmd()
	return Rx_cmd(back)

def AddUser():
    CMD.CMD = CMD_GET_EMPTY_ID
    CMD.LEN = DATA_4
    CMD.DATA[0] = 0x01
    CMD.DATA[1] = 0x00
    CMD.DATA[2] = 0xB8
    CMD.DATA[3] = 0x0B
    Tx_cmd()
    Rx_cmd(1)
    data = RPS.DATA[0] + RPS.DATA[1] * 0x0100

    print("The recommended registration number is : %d"%data)
    Data = TX_DATA(1, fingerprint_id=str(data))
    k = (Data & 0xffff0000) >> 16

    for a in range(3):
        for i in range(3):
            if not CmdFingerDetect(1):
                print("Please move your finger away")
                Draw_InfoScreen("Zabierz palec", "z czytnika", "white")
                pygame.display.flip()
                clock.tick(60)
            while not CmdFingerDetect(1):
                time.sleep(0.01)
            print("Please press your finger")
            Draw_InfoScreen("Przylóż palec", "do czytnika - %s / 3" % (a+1), "white")
            pygame.display.flip()
            clock.tick(60)
            while CmdFingerDetect( 1 ):
                time.sleep(0.01)
            if not CmdFingerDetect( 1 ):
                if not CmdGetImage( 1 ):
                    if not CmdGenerate(a, 1):
                        break

    if i == 2:
        print("Fingerprint entry failure\r\n")
        return 1
    if not CmdMerge(0,3,1):
        if not CmdStoreChar(k,0,0):
            print("The fingerprint is saved successfully, and the id is : %d\r\n"%k)
            screen_state = 2
            text1 = "Pomyślnie dodano odcisk do bazy danych"
            text2 = "ID w bazie: %d"%k
            screen_timeout = 180
    else :
        print("Fingerprint entry failure\r\n")


    return 0

def ClearUser( back ):
    data = TX_DATA(0)
    k = (data & 0xffff0000) >> 16
    n = data & 0xffff

    CMD.CMD = CMD_DEL_CHAR
    CMD.LEN = DATA_4
    CMD.DATA[0] = k & 0xff
    CMD.DATA[1] = (k & 0xff00) >> 8
    CMD.DATA[2] = n & 0xff
    CMD.DATA[3] = (n & 0xff00) >> 8
    Tx_cmd()
    return Rx_cmd(back)

def VerifyUser():
    data = TX_DATA(1)
    Data = (data & 0xffff0000) >> 16

    for i in range(3):
        if not CmdFingerDetect(1):
            print("Please move your finger away")
        while not CmdFingerDetect(1):
            time.sleep(0.01)
        print("Please press your finger")
        while CmdFingerDetect( 1 ):
            time.sleep(0.01)
        if not CmdFingerDetect( 1 ):
            if not CmdGetImage( 1 ):
                if not CmdGenerate(0, 1):
                    break
    if i == 2:
        print("Fingerprint entry failure\r\n")
        return 1

    CMD.CMD = CMD_VERIFY
    CMD.LEN = DATA_4
    CMD.DATA[0] = Data & 0xff
    CMD.DATA[1] = (Data & 0xff00) >> 8
    CMD.DATA[2] = 0x00
    CMD.DATA[3] = 0x00
    Tx_cmd()
    return Rx_cmd(0)

def ScopeVerifyUser():
    data = TX_DATA(0)
    k = (data & 0xffff0000) >> 16
    n = data & 0xffff

    for i in range(3):
        if not CmdFingerDetect(1):
            print("Please move your finger away")
            Draw_InfoScreen("Zabierz palec", "z czytnika", "white")
            pygame.display.flip()
            clock.tick(60)
            print("Zabierz palec z czytnika")
        while not CmdFingerDetect(1):
            time.sleep(0.01)
        print("Please press your finger")
        Draw_InfoScreen("Przyloz palec", "do czytnika", "white")
        pygame.display.flip()
        clock.tick(60)
        while CmdFingerDetect( 1 ):
            time.sleep(0.01)
        if not CmdFingerDetect( 1 ):
            if not CmdGetImage( 1 ):
                if not CmdGenerate(0, 1):
                    break

    if i==2:
        print("Fingerprint entry failure\r\n")
        return 1

    CMD.CMD = CMD_SEARCH
    CMD.LEN = DATA_6
    CMD.DATA[0] = 0x00
    CMD.DATA[1] = 0x00
    CMD.DATA[2] = k & 0xff 
    CMD.DATA[3] = (k & 0xff00) >> 8
    CMD.DATA[4] = n & 0xff
    CMD.DATA[5] = (n & 0xff00) >> 8
    Tx_cmd()
    result = Rx_cmd(0)
    return result

def CmdGetEmptyID(back):
	data = TX_DATA(0)
	k = (data & 0xffff0000) >> 16
	n = data & 0xffff
	
	CMD.CMD = CMD_GET_EMPTY_ID
	CMD.LEN = DATA_4
	CMD.DATA[0] = k & 0xff
	CMD.DATA[1] = (k & 0xff00) >> 8
	CMD.DATA[2] = n & 0xff
	CMD.DATA[3] = (n & 0xff00) >> 8 
	Tx_cmd()
	return Rx_cmd(back)

def GetUserCount(back):
	data = TX_DATA(0)
	k = (data & 0xffff0000) >> 16
	n = data & 0xffff
	
	CMD.CMD = CMD_GET_ENROLL_COUNT
	CMD.LEN = DATA_4
	CMD.DATA[0] = k & 0xff
	CMD.DATA[1] = (k & 0xff00) >> 8
	CMD.DATA[2] = n & 0xff
	CMD.DATA[3] = (n & 0xff00) >> 8 
	Tx_cmd()
	return Rx_cmd(not back)

def CmdUpImageCode(back):
    Rx_data = []
    if not CmdFingerDetect(back):
        print("Please move your finger away")
    while not CmdFingerDetect(back):
        time.sleep(0.01)
    print("Please press your finger")
    while CmdFingerDetect( back ):
        time.sleep(0.01)
    if not CmdFingerDetect( back ):
        if not CmdGetImage( back ):
            print("Please wait while data is being received")
            CMD.CMD = CMD_UP_IMAGE_CODE
            CMD.LEN = DATA_1
            CMD.DATA[0] = 0x00 
            Tx_cmd()
            time.sleep(0.1)
            while ser.inWaiting()>0:
                for i in range(66218):
                    Rx_data.append(ord(ser.read()))
            Data_Txt(Rx_data)
    return 0

def Data_Txt(Rx_data):
    output = open('data.txt','w',encoding='gbk')
    i = 38
    for j in range(129):
        for o in range(8):
            for p in range(62):
                output.write("0x%x,"%Rx_data[i])
                i = i + 1
            output.write('\n')
        i = i + 14
    for j in range(6):
        for p in range(62):
            output.write("0x%x,"%Rx_data[i])
            i = i + 1
        output.write('\n')
    for p in range(8):
        output.write("0x%x,"%Rx_data[i])
        i = i + 1
    print("To write to the data.txt document")

def CmdDownImage():
    print("Please wait while writing fingerprint image")
    CMD.CMD = CMD_DOWN_IMAGE
    CMD.LEN = DATA_4
    CMD.DATA[0] = 242 & 0xff
    CMD.DATA[1] = (242 & 0xff00) >> 8
    CMD.DATA[2] = 266 & 0xff
    CMD.DATA[3] = (266 & 0xff00) >> 8
    Tx_cmd()
    Rx_cmd(0)

    Himage = Image.open(os.path.join(picdir, '2.bmp'))
    image_monocolor = Himage.convert('L')
    imwidth, imheight = image_monocolor.size
    pixels = image_monocolor.load()

    CMD_DATA.PREFIX = Command_Data
    CMD_DATA.SID = Command_SID
    CMD_DATA.DID = Command_DID
    CMD_DATA.CMD = CMD_DOWN_IMAGE
    CMD_DATA.LEN = DATA_498
    length = 0
    width = 0
    for SN in range(129):
        CMD_DATA.DATA[0] = SN & 0xff 
        CMD_DATA.DATA[1] = (SN & 0xff00) >> 8
        for i in range(496):
            CMD_DATA.DATA[i+2] = pixels[width,length]
            width = width + 1
            if width > 241 :
                width = 0
                length = length + 1
        Tx_cmd_data(SN)
        fun = Rx_cmd_ten(0)
        if fun:
            print("Write Error")
            return 1
    CMD_DATA.LEN = DATA_390
    CMD_DATA.DATA[0] = SN & 0xff 
    CMD_DATA.DATA[1] = (SN & 0xff00) >> 8
    for i in range(388):
        CMD_DATA.DATA[i+2] = pixels[width,length]
        width = width + 1
        if width > 241 :
            width = 0
            length = length + 1
    Tx_cmd_data( SN+1 )
    fun = Rx_cmd(0)
    if fun:
        print("Write Error")
        return 1

    CmdGenerate(0, 1) 
    CMD.CMD = CMD_GET_EMPTY_ID
    CMD.LEN = DATA_4
    CMD.DATA[0] = 0x01
    CMD.DATA[1] = 0x00
    CMD.DATA[2] = 0xB8 
    CMD.DATA[3] = 0x0B 
    Tx_cmd()
    Rx_cmd(1)
    data = RPS.DATA[0] + RPS.DATA[1] * 0x0100
    if( not CmdStoreChar(data,0,0) ):
        print("The fingerprint is saved successfully, and the id is : %d\r\n"%data)
    return 0

def TX_DATA(Tx_flag, fingerprint_id=None):
    a = 0
    while(1):
        data_start = 0
        data_end = 0
        if(Tx_flag):
            if fingerprint_id != None:
                str = fingerprint_id
            else:
                str = input("Enter an address from 1 to 3000 : ")
            a = len(str)
            if(a > 4):
                print("please input again")
                continue
            else:
                for i in range(a):
                    data_start = data_start * 10 + ord(str[i]) - 0x30
                if((data_start > 3000) | (data_start < 1)):
                    print("please input again")
                    continue
                break
        else:
            str = "1,3000"
            a = len(str)
            if ((a > 9) | (a<3)):
                print("please input again")
                continue
            else:
                i = 0
                while str[i] != ',':
                    data_start = data_start * 10 + ord(str[i]) - 0x30
                    i = i+1
                    if((i>3) | (i==a)):
                        break
                if((data_start > 3000) | (data_start < 1) | (i>3)):
                    print("please input again")
                    continue
                i = i + 1
                while i<a:
                    data_end = data_end * 10 + ord(str[i]) - 0x30
                    i = i+1
                if((data_end > 3000) | (data_end < 1)):
                    print("please input again")
                    continue
                break
    Data = data_start * 0x10000 + data_end
    return Data

def Rx_cmd(back):
    a=1
    CKS = 0
    while a:
        while ser.inWaiting()>0:
            for i in range(26):
                rps[i] =ord(ser.read())
            a = 0
            if rps[4] == 0xff:
                return 1
            Rx_CMD_Process(1)
            for i in range(24):
                CKS = (CKS + rps[i])&0xffff
            if CKS == RPS.CKS:
                return Rx_Data_Process(back)
    return 1

def Rx_cmd_ten(back):
    a=1
    CKS = 0
    while a:
        while ser.inWaiting()>0:
            for i in range(12):
                rps[i] =ord(ser.read())
            a = 0
            if rps[4] == 0xff:
                return 1
            Rx_CMD_Process(0)
            for i in range(10):
                CKS = (CKS + rps[i])&0xffff
            if CKS == RPS.CKS:
                return Rx_Data_Process(back)
    return 1

def Rx_cmd_data(back):
     while a:
        while ser.inWaiting()>0:
            print(hex(ord(ser.read())))

def Rx_CMD_Process(flag):
    RPS.PREFIX = rps[0] + rps[1] * 0x100
    RPS.SID = rps[2]
    RPS.DID = rps[3]
    RPS.CMD = rps[4] + rps[5] * 0x100
    RPS.LEN = rps[6] + rps[7] * 0x100
    RPS.RET = rps[8] + rps[9] * 0x100
    if flag:
        for i in range(RPS_Len):
            RPS.DATA[i] = rps[10 +i]
        RPS.CKS = rps[24] + rps[25] * 0x100
    else:
        RPS.CKS = rps[10] + rps[11] * 0x100;

def Rx_Data_Process( back ):
    a = 1
    if RPS.CMD==CMD_TEST_CONNECTION:
        a = RpsTestConnection(back)
    elif RPS.CMD==CMD_FINGER_DETECT:
        a = RpsFingerDetect(back)
    elif RPS.CMD==CMD_GET_IMAGE:
        a = RpsGetImage(back)
    elif RPS.CMD==CMD_GENERATE:
        a = RpsGenerate(back)
    elif RPS.CMD==CMD_MERGE:
        a = RpsMerge(back)
    elif RPS.CMD==CMD_DEL_CHAR:
        a = RpsDelChar(back)
    elif RPS.CMD==CMD_STORE_CHAR:
        a = RpsStoreCher(back)
    elif RPS.CMD==CMD_SEARCH:
        a = RpsSearch(back)
    elif RPS.CMD==CMD_VERIFY:
        a = RpsVerify(back)
    elif RPS.CMD==CMD_GET_EMPTY_ID:
        a = RpsGetEmptyID(back)
    elif RPS.CMD==CMD_GET_ENROLL_COUNT:
        a = RpsGetEnrollCount(back)
    elif RPS.CMD==CMD_DOWN_IMAGE:
        a = RpsDownImage(back)
    else :
        time.sleep(0.01)
    return a

def RPS_RET():
    if RPS.RET == ERR_SUCCESS:
        print("Instruction processing succeeded\r\n")
    elif RPS.RET == ERR_FAIL:
        print("Instruction processing failure\r\n")
    elif RPS.RET == ERR_TIME_OUT:
        print("No prints were entered within the time limit\r\n")
    elif RPS.RET == ERR_FP_NOT_DETECTED:
        print("There is no fingerprint input on the collector\r\n")
    elif RPS.RET == ERR_FP_CANCEL:
        print("Instruction cancelled\r\n")
    elif RPS.RET == ERR_INVALID_BUFFER_ID:
        print("The Ram Buffer number is invalid\r\n")
    elif RPS.RET == ERR_BAD_QUALITY:
        print("Poor fingerprint image quality\r\n")
    elif RPS.RET == ERR_GEN_COUNT:
        print("Invalid number of combinations\r\n")
    elif RPS.RET == ERR_INVALID_TMPL_NO:
        print("The specified Template number is invalid\r\n")
    elif RPS.RET == ERR_DUPLICATION_ID:
        global screen_state
        global text1
        global text2
        global text_color
        global screen_timeout
        a = RPS.DATA[0]+RPS.DATA[1]*0x100
        print("The fingerprint has been registered, and the id is : %d\r\n"%a )
        screen_state = 2
        text1 = "Taki odcisk już istnieje"
        text2 = "w bazie danych, ID: %d"%a
        text_color = (0, 158, 96)
        screen_timeout = 180
    elif RPS.RET == ERR_INVALID_PARAM:
        print("Specified range invalid\r\n")
    elif RPS.RET == ERR_TMPL_EMPTY:
        print("Template is not registered in the specified range\r\n")
    elif RPS.RET == ERR_VERIFY:
        print("Description Failed to specify fingerprint comparison\r\n")
    elif RPS.RET == ERR_IDENTIFY:
        print("Fingerprint comparison failed for the specified range\r\n")
    else :
        time.sleep(0.01)
    return RPS.RET

def RpsTestConnection( back ):
    if back :
        return RPS.RET
    else :
        if RPS.RET :
            return RPS_RET()
        else :
            print("Connection successful\r\n")

            return RPS.RET

def RpsFingerDetect( back ):
    if back:
        if not RPS.RET :
            return not RPS.DATA[0]
    else :
        if RPS.RET :
            return RPS_RET()
        else :
            if RPS.DATA[0]:
                print("We got a print on it\r\n")
            #else :
                #print("No prints were detected\r\n")
            return not RPS.DATA[0]
    return 2

def RpsGetImage( back ):
	if back:
		return RPS.RET
	else :
		return RPS_RET()

def RpsGenerate( back ):
	if back:
		return RPS.RET
	else :
		return RPS_RET()

def RpsMerge( back ):
	if back:
		return RPS.RET
	else :
		return RPS_RET()

def RpsStoreCher( back ):
	if back:
		return RPS.RET
	else :
		if RPS.RET:
			return RPS_RET()
		else :
			return RPS.RET

def RpsDelChar( back ):
	if back:
		return RPS.RET
	else :
		return RPS_RET()

def RpsVerify( back ):
	if back:
		return RPS.RET
	else :
		if RPS.RET :
			return RPS_RET()
		else :
			print("Successful fingerprint comparison\r\n")
			return RPS.RET

def RpsSearch( back ):
	if back:
		return RPS.RET
	else :
		if RPS.RET:
			return RPS_RET()
		else :
			data = RPS.DATA[0] + RPS.DATA[1] * 0x0100
			print("Successful fingerprint comparison")
			print("The number of the first successful match is : %d \r\n"%data)
			return data

def RpsGetEmptyID( back ):
	if back:
		return RPS.RET
	else :
		if RPS.RET:
			return RPS_RET()
		else :
			data = RPS.DATA[0] + RPS.DATA[1] * 0x0100
			print("The first number that can be registered within the specified range is : %d \r\n"%data)
			return RPS.RET

def RpsGetEnrollCount(back):
	if back:
		return RPS.RET
	else :
		if RPS.RET:
			return RPS_RET()
		else :
			data = RPS.DATA[0] + RPS.DATA[1] * 0x0100;
			print("The total number of registered fingerprints in the specified range is : %d \r\n"%data);
			return RPS.RET

def RpsDownImage(back):
	return RPS.RET

def Cmd_Packet_Init():
    CMD.PREFIX = Command
    CMD.SID = Command_SID
    CMD.DID = Command_DID
    CMD.CMD = CMD_TEST_CONNECTION
    CMD.LEN = DATA_0
    for i in range(CMD_Len):
        CMD.DATA[i] = 0x00


try:
    time.sleep(0.5)    # Wait for module to start
    Cmd_Packet_Init()
    while 1:
        Tx_cmd()
        if Rx_cmd(1):
            print("Connection closed by server")
            print("Try to reconnect")
            i = i+1
            if(i > 3):
                print("Power on the device again")
            while 1:
                time.sleep(1000)
        else :
            break
        time.sleep(1)
        
    i = 0
    while running:
        #print("STAN EKRANU - %s" % screen_state)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        if screen_state == 0:
            read_state = Tx_Data_Process("CMD1")
            breaks_dict = Draw_MainScreen(db_counter, breaks_dict)
            db_counter+=1
            if db_counter >= 600:
                db_counter = 0
                
            if read_state == False:
                read_state = Tx_Data_Process("CMD5")
                if read_state > 0:
                    card_id = str(read_state)
                    print("Wykryty odcisk - %s" % card_id)
                    screen_state = 1
                    screen_timeout = 290
                    
        elif screen_state == 1:
            if data_crawled == False:
                employee_data = Get_EmployeeData(card_id, datetime.today().strftime('%Y-%m-%d'))
                data_crawled = True
                screen_timeout-=1

            if screen_timeout <= 0:
                screen_timeout = 290
                db_counter = 0
                screen_state = 0
                data_crawled = False
              
            if employee_data['admin'] == 1:
                screen_state = 3
                screen_timeout = 600
            elif employee_data['id'] != None:
                action = Draw_ChoiceScreen(employee_data['fname'] + " " + employee_data['lname'])
                screen_timeout-=1
            else:
                print(employee_data['id'])
                screen_state = 2
                screen_timeout = 180
                text1 = "Nie znaleziono odcisku"
                text2 = "w bazie danych"
                text_color = (165, 42, 42)
                
            if action < 5:            
                screen_timeout = 0
                screen_state = 2
                data_crawled = False
                action_result = Check_Entry(action, employee_data['entry_list'], employee_data['fname'])
                if action_result == "OK":
                    entry_result = Update_EmployeeData(employee_data['id'], action, datetime.today().strftime('%Y-%m-%d'), employee_data['fname'])
                    text1 = entry_result[0]
                    text2 = entry_result[1]
                    text_color = entry_result[2]
                else:
                    text1 = action_result[0]
                    text2 = action_result[1]
                    text_color = (165, 42, 42)
                screen_timeout = 180
                
        elif screen_state == 2:
            Draw_SuccessErrorScreen(text1, text2, text_color)
            screen_timeout-=1
            if screen_timeout <= 0:
                screen_timeout = 290
                db_counter = 0
                screen_state = 0
                data_crawled = False
                
        elif screen_state == 3:
             Draw_AdminScreen()
             screen_timeout-=1
             if screen_timeout <= 0:
                screen_timeout = 290
                db_counter = 0
                screen_state = 0
                data_crawled = False
            
    
        pygame.display.flip()
        clock.tick(60)
    
        if img_rotation < 360:
            img_rotation += 1
        else:
            img_rotation = 0
        
        if img_rotation_2 > 0:
            img_rotation_2 -= 1
        else:
            img_rotation_2 = 360
        
        
    pygame.quit()
    

    #while True:     
        #Tx_Data_Process()        
        
except KeyboardInterrupt:
    if ser != None:
        ser.close()               
    print("\n\n Test finished ! \n") 
    sys.exit()