import os
import pygame
from pygame import surfarray
import storage_operation as so
import cv2
import tqdm
import numpy as np
from settings import settings as st

frameSize = (160, 90)

def compile_vid_from_zip_file():
    first = True
    for frames in so.zip_data_gen():
        
        if first:     
            ass = frames[0]
            frameSize = pygame.surfarray.array2d(ass).shape
            out = cv2.VideoWriter(st.video_file_name,cv2.VideoWriter_fourcc(*'mp4v'), 60, frameSize)
            first = False
        londa = []
        for s in (frames):
            londa.append(np.flip(pygame.surfarray.array3d(s).transpose(1,0,2),axis=(2,)))
        for nda in londa:
            out.write(nda)
    out.release()
    if not os.path.isdir(st.video_directory):
        os.mkdir(st.video_directory)
    if os.path.isfile(st.video_file_path):
        os.remove(st.video_file_path)
    os.rename(st.video_file_name, st.video_file_path)

def compile_vid(londa: list[np.ndarray]):
    print("compiling video...")
    out = cv2.VideoWriter(st.video_file_name,
                          cv2.VideoWriter_fourcc(*'mp4v'), 60, frameSize)
    for nda in londa:
        img = nda        
        out.write(img)

    out.release()
    if not os.path.isdir(st.video_directory):
        os.mkdir(st.video_directory)
    if os.path.isfile(st.video_file_path):
        os.remove(st.video_file_path)
    os.rename(st.video_file_name, st.video_file_path)


def entry_for_list_of_surface(los: list[pygame.Surface]):

    global frameSize
    ass = los[0]
    frameSize = pygame.surfarray.array2d(ass).shape
    londa = []
    print("converting to array...")
    for s in tqdm.tqdm(los):
        londa.append(np.flip(pygame.surfarray.array3d(s).transpose(1,0,2),axis=(2,)))
    compile_vid(londa)

def color_diashow():
    loc = []
    a, b, c = 0, 0, 0
    state = 0
    while True:
        aa = hex(a)[2:]
        if len(aa) == 1:
            aa = '0' + aa
        bb = hex(b)[2:]
        if len(bb) == 1:
            bb = '0' + bb
        cc = hex(c)[2:]
        if len(cc) == 1:
            cc = '0' + cc
        loc.append('#'+aa+bb+cc)
        if state == 0:
            a += 1
            if a == 255:
                state = 1
        elif state == 1:
            b += 1
            if b == 255:
                state = 2
        elif state == 2:
            a -= 1
            if a == 0:
                state = 3
        elif state == 3:
            c += 1
            if c == 255:
                state = 4
        elif state == 4:
            a += 1
            if a == 255:
                break
    surfaces = []
    for c in loc:
        s = pygame.Surface(frameSize)
        s.fill(c)
        surfaces.append(s)
    input("You are going to overwrite with color diashow (otherwise ctrl c)")
    entry_for_list_of_surface(surfaces)


if __name__ == "__main__":

    compile_vid_from_zip_file()