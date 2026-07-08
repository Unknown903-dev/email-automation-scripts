#dont move mouse till you see the word done

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

time.sleep(3)
move_cursor(850,300)
Click(850,300)
time.sleep(1)



#Load existing names
with open('previous_classes.txt', 'r') as f:
    existing_names = set(line.strip().upper() for line in f)
    old_names = existing_names.copy()


# Append only new names
with open('current_class.txt', 'r') as file:
    for line in file:
        name = line.strip().upper()
        if not name:
            continue

        if name not in existing_names:
            #adds the name to the set
            existing_names.add(name)

            Click(850, 300)
            time.sleep(4)
                
            type_text(name)
            #if for some reason program stops suddenly copy past names that prints into your previous_classes.txt
            print(name)
            time.sleep(2)
            press_enter()


# append the names to the file that didnt exist before
with open('previous_classes.txt', 'a') as same_file:
    for i in existing_names:
        if i not in old_names:
            same_file.write(i + "\n")
            
type_text("DONE")


#note to future reader: i tried having it append at the same time as sending the email
#                        an unknown anomly happened and decided to seperate it