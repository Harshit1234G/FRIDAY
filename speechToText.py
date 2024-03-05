import pyautogui as pg
import os
from time import sleep
import friday

fri = friday.Friday()

os.startfile(r"C:\Windows\System32\notepad")
# os.system("notepad")
sleep(1)
while True:
    text = fri.takeCommand() 
        
    if text == "stop" or text == "exit":
        break
    pg.typewrite(f"{text}\n", .07)

pg.hotkey('ctrl', 's')
sleep(1)
pg.typewrite("SpeechToText1")