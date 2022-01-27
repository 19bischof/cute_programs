from numpy import number
import pygame
import os.path
from pygame.constants import KEYDOWN
import storage_operation as so
import tkinter as tk #for screen size
import time
from tqdm import trange
from ball import ball
from settings import settings as st
from compile_video import entry_for_list_of_surface
from win32gui import SetWindowPos


collection_of_frames = []
root = tk.Tk()
root.withdraw()
screen_width, screen_height = root.winfo_screenwidth(),root.winfo_screenheight()
root.destroy()
del root
x_pos,y_pos = int((screen_width - st.width)/2),int((screen_height-st.height)/2)
x_pos += st.x_shift
y_pos += st.y_shift
def peek():
    pygame.init()
    is_running = True
    background = pygame.Surface((st.width, st.height))
    background.fill(pygame.Color(st.background_color))
    pygame.display.set_caption('Look!')
    pygame.display.set_icon(pygame.Surface(size=(800, 600)))
    window_surface = pygame.display.set_mode((st.width, st.height))
    window_surface.blit(background, (0, 0))
    ball.spawn_balls(st.width, st.height, st.max_number_of_balls)
    ball.draw_balls_on_Surface(window_surface)
    SetWindowPos(pygame.display.get_wm_info()[
                 'window'], -1, x_pos, y_pos, 0, 0, 1)
    x = 0
    y = 0
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_UP:
            #         y+= 1
            #     if event.key == pygame.K_LEFT:
            #         x+= 1
                # SetWindowPos(pygame.display.get_wm_info()[
                #  'window'], -1, x_pos-x, y_pos-y, 0, 0, 1)
                # print("x,y:",x_pos-x,y_pos-y)
        time.sleep(0.1)
        pygame.display.update()

    
def clean_render(frame_range = (0,st.fps*st.duration)):
    
    background = pygame.Surface((st.width, st.height))
    background.fill(pygame.Color(st.background_color))
    for m in range(*frame_range):
        new_surface = pygame.Surface((st.width, st.height))
        new_surface.blit(background, (0, 0))
        ball.move_balls()
        ball.draw_balls_on_Surface(new_surface)
        collection_of_frames.append(new_surface.copy())

def render(frame_range = (0,st.fps*st.duration)):
    
    background = pygame.Surface((st.width, st.height))
    background.fill(pygame.Color(st.background_color))
    print("rendering...")
    for m in trange(*frame_range):
        new_surface = pygame.Surface((st.width, st.height))
        new_surface.blit(background, (0, 0))
        ball.move_balls()
        ball.draw_balls_on_Surface(new_surface)
        collection_of_frames.append(new_surface.copy())

def display():
    pygame.init()
    is_running = True
    clock = pygame.time.Clock()
    pygame.display.set_caption('Look!')
    pygame.display.set_icon(pygame.Surface(size=(800, 600)))
    window_surface = pygame.display.set_mode((st.width, st.height))
    SetWindowPos(pygame.display.get_wm_info()[
                 'window'], -1, x_pos, y_pos, 0, 0, 1)
    i = 0
    while is_running and i < len(collection_of_frames):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        clock.tick(st.fps)
        window_surface.blit(collection_of_frames[i], (0, 0))
        pygame.display.update()
        i += 1
def big_frame_management():
    print("number of steps:",st.number_of_steps)
    print("number of bytes:", st.all_bytes)
    print(st.comp_file_path)
    if os.path.isfile(st.comp_file_path):
        big_frame_management_fetch()
    else:
        big_frame_management_render()

def big_frame_management_fetch():
    global collection_of_frames    
    collection_of_frames = []

    #usually you want to do each fetch iteration in a new thread while pygame is presenting the frames but cant be bothered (。_。)
    #actually now that i think about it it is a perfect usage of generators in python to compile video and render on pygame
    #so that is something to do for you!!
    while True:
        cur_frames, breaked = so.manage_big_files_entry()
        collection_of_frames += cur_frames
        if breaked:
            break
    display()
    
def big_frame_management_render():
    global collection_of_frames
    ball.spawn_balls(st.width, st.height, st.max_number_of_balls)
    for frame_index in trange(0,st.number_of_frames,st.step):
        collection_of_frames = []
        frame_range = (frame_index,frame_index + st.step)
        clean_render(frame_range)
        so.manage_big_files_entry(collection_of_frames,step = st.step,clean=True)

def small_frames():
    global collection_of_frames
    print(st.comp_file_path)
    if os.path.isfile(st.comp_file_path):
        print("fetching...")
        collection_of_frames = so.manage_big_files_entry()
    else:
        ball.spawn_balls(st.width, st.height, st.max_number_of_balls)
        render()
        print("storing...")
        so.manage_big_files_entry(collection_of_frames)
    print("number of frames:", len(collection_of_frames))
    if input("Do you want to store as Video?\n").lower().strip() in ("yes","y"):
        entry_for_list_of_surface(collection_of_frames)
    input("Upcoming is the pygame visual (Press Button to continue)")
    display()

if __name__ == "__main__":
    preview = False
    # preview = True
    if preview:
        peek()
        quit()
    # small_frames()
    big_frame_management()

