import pygame
import os.path

from pygame.constants import KEYDOWN
import storage_operation as so
import tkinter as tk #for screen size
import time
from tqdm import trange
from ball import ball
from settings import settings as st
from win32gui import SetWindowPos
pygame.init()


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


def render():
    background = pygame.Surface((st.width, st.height))
    background.fill(pygame.Color(st.background_color))
    ball.spawn_balls(st.width, st.height, st.max_number_of_balls)

    max_count = st.fps * st.duration
    for m in trange(max_count):
        new_surface = pygame.Surface((st.width, st.height))
        new_surface.blit(background, (0, 0))
        ball.move_balls()
        ball.draw_balls_on_Surface(new_surface)
        collection_of_frames.append(new_surface.copy())


def display():
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


if __name__ == "__main__":
    preview = False
    # preview = True
    if preview:
        peek()
        quit()
    print(st.comp_file_path)
    if os.path.isfile(st.comp_file_path):
        print("fetching...")
        collection_of_frames = so.fetch_and_store_animation()
    else:
        print("rendering...")
        render()
        print("storing...")
        so.fetch_and_store_animation(collection_of_frames)
    print("number of frames:", len(collection_of_frames))
    input("ready?")
    display()
