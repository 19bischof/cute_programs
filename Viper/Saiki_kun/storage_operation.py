from io import BytesIO
import shutil
import os
import pygame
import numpy
import pickle
import zipfile
import time
from tqdm import tqdm
from settings import settings as st
import threading

last_file_name = ""

def fetch_and_store_animation(los: list[pygame.Surface] = None):
    in_memory = False
    if los is None:
        #fetching
        if in_memory is True:
            with zipfile.ZipFile(st.comp_file_path,"r") as zip_file:
                bust = pickle.loads(zip_file.read(st.raw_file_name))
        else:
            if os.path.isfile(st.comp_file_path):
                print("unpacking...")
                shutil.unpack_archive(st.comp_file_path, st.dir_of_animations)
                with open(st.raw_file_path, "rb") as f:
                    print("loading to variable...")
                    bust = pickle.load(f)
                os.remove(st.raw_file_path)
        los = []
        print("converting to surface...")
        for b in tqdm(bust):
            los.append(pygame.surfarray.make_surface(b))
        return los
    else:
        #storing
        ndas = []       #ndarrays
        print("converting to array...")
        for s in tqdm(los):   #list of Surfaces
            ndas.append(pygame.surfarray.array2d(s))  
        del los  
        if not os.path.isdir(st.dir_of_animations):
            os.mkdir(st.dir_of_animations)


        if in_memory is True:
            print("compressing...")
            with zipfile.ZipFile(st.comp_file_path,"w") as zip_file:
                zip_file.writestr(st.raw_file_name,pickle.dumps(ndas))
            
        else:
            with open(st.raw_file_path, "wb") as f:
                print("dumping to file...")
                pickle.dump(ndas, f)
            del ndas                
            print("compressing...")
            shutil.make_archive(st.raw_file_path, st.comp_protocol,st.dir_of_animations,st.raw_file_name)
            os.remove(st.raw_file_path)

def zip_data_gen(step = st.step):
    
    global stash,already_fetched
    print("step:",step)
    stash = None
    already_fetched = []
    my_frames = []
    prep_zip_data_for_yield()
    while True:
        if stash == my_frames:
            print(len(already_fetched),number_of_files)
            time.sleep(0.5)
            continue
        my_frames = stash.copy()
        threading.Thread(target=prep_zip_data_for_yield,args=(step,already_fetched)).start()
        print("yielding")
        yield my_frames
        if len(already_fetched) >= number_of_files:
            break

def prep_zip_data_for_yield(step = st.step,already_fetched_2 = None):
    global stash,already_fetched,number_of_files
    if already_fetched_2 is not None:
        already_fetched = already_fetched_2
    print("shere",step)
    length_before = len(already_fetched)
    with zipfile.ZipFile(st.comp_file_path,"r") as zip_file:
        busty = []
        number_of_files = len(zip_file.filelist)

        for index,file in enumerate(zip_file.filelist):
            if index in already_fetched:
                continue
            name = file.filename
            bite = ((zip_file.read(name)))
            print("read:",name)
            busty += (pickle.loads(bite))
            already_fetched += [index]
            print("indexlsdflks",index,step+length_before)
            if index == step+length_before:    #minus one because it is increased in the line before
                break
    cur_los = []
    bust = busty
    for b in (bust):
        cur_los.append(pygame.surfarray.make_surface(b))
    stash =  cur_los
    

def manage_big_files_entry(los: list[pygame.Surface] = None,step = st.step,clean = False):
    global last_file_name
    breaked = False
    if los is None:
        #fetching
        with zipfile.ZipFile(st.comp_file_path,"r") as zip_file:
            busty = []
            for index,file in enumerate(zip_file.filelist):
                name = file.filename
                bite = ((zip_file.read(name)))
                print("read:",name)
                busty += (pickle.loads(bite))
                if index == step:
                    breaked = True
                    break
        cur_los = []
        bust = busty
        print("converting to surface...")
        for b in tqdm(bust):
            cur_los.append(pygame.surfarray.make_surface(b))
        return cur_los,breaked
    else:
        #storing
        index_start = 0
        index_end = step
        iteration = 0
        if os.path.isfile(st.comp_file_path) and last_file_name == "":
            os.remove(st.comp_file_path)
        if last_file_name != "":
            iteration = int(last_file_name[len(st.raw_file_name+"__"):]) +1
        if not clean:
            print("converting to array...")
        ndas = []
        if not clean:
            for s in tqdm(los):   
                ndas.append(pygame.surfarray.array3d(s))   
        else:
            for s in los:
                ndas.append(pygame.surfarray.array3d(s))
        if not clean:
            print("compressing...")
        while len(ndas)>0:
            if index_end >= len(los):
                index_end = len(los)
            cur_ndas = ndas[index_start:index_end]
            if not os.path.isdir(st.dir_of_animations):
                os.mkdir(st.dir_of_animations)
            #in memory only:
            if not clean:
                print("write:",st.raw_file_name+"__"+str(iteration))
            last_file_name = st.raw_file_name+"__"+str(iteration)
            with zipfile.ZipFile(st.comp_file_path,"a",zipfile.ZIP_LZMA) as zip_file:
                zip_file.writestr(st.raw_file_name+"__"+str(iteration),pickle.dumps(cur_ndas))
                
            if index_end == len(los):
                break
            iteration += 1
            ndas = ndas[index_end:]
if __name__ == "__main__":
    # fetch_and_store_animation([pygame.Surface((10,0))]*10000)
    s = pygame.Surface((10,200))
    s.fill('#0000f0')
    my_los = [s for x in range(10000)]
    manage_big_files_entry(my_los)
    print(len(manage_big_files_entry()))