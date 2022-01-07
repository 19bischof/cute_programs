import pygame
from storage_operation import fetch_and_store_animation
import cv2
import numpy as np
from settings import settings as st

frameSize = (100,30)

def compile_vid(londa:list[np.ndarray]):

    out = cv2.VideoWriter('one_output_video.mp4',
                        cv2.VideoWriter_fourcc(*'MP4V'), 60,frameSize)
    for nda in londa:
        img = nda
        out.write(img)

    out.release()

def entry_for_list_of_surface(los:list[pygame.Surface]):
    for s in los:
        nda = pygame.surfarray.array2d(s)
    new_nda = np.ones(frameSize[::-1]+(3,),dtype=np.uint8)
    for index,col in enumerate(nda):
        for iindex,e in enumerate(col):
            h = hex(e)
            h = h[2:]
            loh = []
            for i in range(0,6,2):
                loh.append(h[i:i+2])
            for i in range(len(loh)):
                loh[i] = int(loh[i],16)
            # print(type(loh))
            # print(type(new_nda[0][0]))
            new_nda[index][iindex] = loh[::-1]
            
    with open("at_i_is_100.txt","w") as f:
        f.write(str(len(new_nda))+repr(new_nda))
    londa = []
    for i in range(360):        
        londa.append(new_nda)
    compile_vid(londa)
if __name__ == "__main__":
    s = pygame.Surface(frameSize[::-1])
    s.fill('#FF0FF0')
