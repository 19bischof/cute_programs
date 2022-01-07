import shutil
import os
import pygame
import pickle
from settings import settings as st


def fetch_and_store_animation(los: list[pygame.Surface] = None):
    if los is None:
        #fetching
        if os.path.isfile(st.comp_file_path):
            print("unpacking...")
            shutil.unpack_archive(st.comp_file_path, st.dir_of_animations)
            with open(st.raw_file_path, "rb") as f:
                print("loading to variable...")
                bust = pickle.load(f)
            os.remove(st.raw_file_path)
            los = []
            print("converting to surface...")
            for b in bust:
                los.append(pygame.surfarray.make_surface(b))
            return los
    else:
        #storing
        ndas = []       #ndarrays
        print("converting to array...")
        for s in los:   #list of Surfaces
            ndas.append(pygame.surfarray.array2d(s))  
        del los  
        with open(st.raw_file_path, "wb") as f:
            print("dumping to file...")
            pickle.dump(ndas, f)
        del ndas
        print("compressing...")
        shutil.make_archive(st.raw_file_path, st.comp_protocol,st.dir_of_animations,st.raw_file_name)
        os.remove(st.raw_file_path)
if __name__ == "__main__":
    fetch_and_store_animation([pygame.Surface((0,0))])
    fetch_and_store_animation()