import shutil
import os
import pygame
import pickle
from settings import settings as st


def fetch_and_store_animation(S: pygame.Surface = None):
    comp_file = st.file_name + ".tar.gz"
    raw_file = st.file_name
    if S is None:
        if os.path.isfile(comp_file):
            shutil.unpack_archive(comp_file, "./")
            with open(raw_file, "rb") as f:
                bust = pickle.load(f)
            os.remove(raw_file)
            return pygame.surfarray.make_surface(bust)
    else:
        nda = pygame.surfarray.array2d(S)
        with open(raw_file, "wb") as f:
            pickle.dump(nda, f)
        shutil.make_archive(raw_file, "gztar", "./", raw_file)
        os.remove(raw_file)
