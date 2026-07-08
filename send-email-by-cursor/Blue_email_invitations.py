import ctypes
import time

# Windows API func
user32 = ctypes.windll.user32

# Constants for keypresses
Press_key = 0x0000
LetGo_key = 0x0002
ENTER = 0x0D    #enter
SPACE = 0x20     #space



Left_Window = 0x5B      # Left Windows key
Up_arrow = 0x26        # Up
Down_arrow = 0x28
backspace = 0x08


# Move cursor
def move_cursor(x, y):
    user32.SetCursorPos(x, y)

# keyboard of user
def press_key(key_code):
    user32.keybd_event(key_code, 0, Press_key, 0)
    user32.keybd_event(key_code, 0, LetGo_key, 0)

# Type something
def type_text(text):
    for char in text:
        if char == ' ':
            press_key(SPACE)
        else:
            press_key(ord(char))  # ASCII 
        time.sleep(0.1)
# mouse click
def Click(x, y):
    move_cursor(x, y)
    user32.mouse_event(0x02, 0, 0, 0, 0) 
    user32.mouse_event(0x04, 0, 0, 0, 0)  

#press enter
def press_enter():
    user32.keybd_event(ENTER, 0, Press_key, 0)  
    user32.keybd_event(ENTER, 0, LetGo_key, 0)
def press_backspace():
    user32.keybd_event(backspace, 0, Press_key, 0)
    user32.keybd_event(backspace, 0, LetGo_key, 0)
def press_down():
    user32.keybd_event(Down_arrow, 0, Press_key, 0)
    user32.keybd_event(Down_arrow, 0, LetGo_key, 0)


move_cursor(850,300)
Click(850,300)
time.sleep(1)


with open('list.txt', 'r') as file: 
    # Iterate through each line
    for line in file:
        # Now current_string holds the string from that lin
        current_string = line.strip().upper()
        text = current_string

        #types the text and waits for it to load
        type_text(text)
        print(text)
        time.sleep(4)
        press_enter()
       
    