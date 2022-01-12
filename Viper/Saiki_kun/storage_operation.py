from io import BytesIO
import shutil
import os
import pygame
import numpy
import pickle
import zipfile
from tqdm import tqdm
from settings import settings as st


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

def manage_big_files_entry(los: list[pygame.Surface] = None):
    
    pixels_in_frame = st.width*st.height
    size_of_part = int(10000000 / pixels_in_frame)
    print("size:",size_of_part)

    
    if los is None:
        #fetching
        with zipfile.ZipFile(st.comp_file_path,"r") as zip_file:
            busty = []
            for file in zip_file.filelist:
                name = file.filename
                bite = ((zip_file.read(name)))
                print("read:",name)
                busty += (pickle.loads(bite))
        cur_los = []
        bust = busty
        print("converting to surface...")
        for b in tqdm(bust):
            cur_los.append(pygame.surfarray.make_surface(b))
        return cur_los
    else:
        #storing
        index_start = 0
        index_end = size_of_part
        iteration = 0
        if os.path.isfile(st.comp_file_path):
            os.remove(st.comp_file_path)
        print("converting to array...")
        ndas = []
        for s in tqdm(los):   
            ndas.append(pygame.surfarray.array3d(s))   
        print("compressing...")
        while len(ndas)>0:
            if index_end >= len(los):
                index_end = len(los)
            cur_ndas = ndas[index_start:index_end]
            if not os.path.isdir(st.dir_of_animations):
                os.mkdir(st.dir_of_animations)
            #in memory only:
            print("write:",st.raw_file_name+"__"+str(iteration))
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