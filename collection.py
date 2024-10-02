from PIL import Image
from mss import mss
import keyboard
import numpy as np

import os.path
import time
import pandas as pd
import sys
import keyboard
from ahk import AHK
import os

ah=AHK(executable_path = "C://Program Files//AutoHotkey//UX//AutoHotkeyUX.exe")
n_window= ah.find_window(title='NSUNS4')

global images, events, save ,fnum

N_FRAMES = 3
RES_=(64, 64)
images = np.zeros( (1 , N_FRAMES , RES_[0] , RES_[1]) )
events = np.array(keyboard.KeyboardEvent(   "down" , 4)).reshape(1, -1)
if os.path.exists("data"):

    if os.path.exists("data/episode_count.txt"):
        f=open('data/episode_count.txt','r')
        fnum=f.readline() 
        f.close()

    else:
        
        fnum="1"

        with open("data/episode_count.txt" ,"w") as f:
            f.write("1")

else:
    os.makedirs("data") 
    fnum="1"

    with open("data/episode_count.txt" ,"w") as f:
            f.write("1")
  


def capture_screenshot(n_frames =3 , res = (768, 768) ):
    images_stack = np.zeros((1 , res[0] , res[1]))
    with mss() as sct:

        event=keyboard.read_event()
      
        monitor = sct.monitors[1]

        for i in range(n_frames):

            sct_img = sct.grab(monitor)
            images_stack = np.concatenate( [ images_stack , np.array(    Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX').resize(res).convert("L")     ).reshape(1 , res[0] , res[1]) ]  ) 
            if i == 0 :
                images_stack = images_stack[1: , :]


    images_stack = images_stack / 255
    images_stack = images_stack.reshape(1 , n_frames ,res[0] , res[1])
    if event.name=='esc':
            return None,None
    else :
        
        return images_stack , event


if __name__=='__main__':
   
   print("Press ` to start recoarding")
   keyboard.wait('`')
   
   while True:
       
      #try:
        img_stack , event =capture_screenshot(N_FRAMES , RES_)
        if event ==None:
            events = events[1: ]
            images = images[1: , : , : , :]

            np.save("data/"+"episode"+fnum , images)
            np.save("data/"+"episode_events"+fnum , events)
            fnum = str( int(fnum)+1  )
            with open("data/episode_count.txt" ,"w") as f:
                f.write(fnum)

            del images
            del events

            images = np.zeros( (1 , N_FRAMES , RES_[0] , RES_[1]) )
            events = np.array(keyboard.KeyboardEvent(   "down" , 4)).reshape(1, -1)

  
            print('Capturing paused , press (`) to continue ... ')
            keyboard.wait('`')

        else:
            images = np.concatenate(  [images , img_stack] , axis=0  )
            events = np.append(events , np.array(event).reshape(1, -1) )

            if n_window !=None:
               n_window.restore()
     #except Exception :
         #print ('invalid keys entered ... cancelling iteration...')
         #continue
