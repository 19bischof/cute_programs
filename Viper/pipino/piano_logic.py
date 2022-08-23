import pygame
import random
from settings import settings as st
import pathlib
project_path = pathlib.Path(__file__).absolute().parent.as_posix()

class pipino:
    @classmethod
    def get_start_surface(cls):
        s = pygame.Surface(st.size)
        s.fill(st.white)
        font = pygame.font.SysFont('Courier',st.font_size,bold=True)
        for i in range(5):
            h = st.height-(st.line_diff*(i+1)+st.y_offset)
            if i == 0 and cls.help_letter:
                letter = font.render(cls.notes[i*2+1],True,st.red)
                s.blit(letter,(0,h+st.font_size*0.5))
            pygame.draw.line(s,st.black,(0,h),(st.width,h), st.line_width)
            if cls.help_letter:
                letter = font.render(cls.notes[i*2+3],True,st.red)
                s.blit(letter,(0,h-st.font_size*1.5))
        cls.start_surface = s

    @classmethod
    def clef_update(cls):
        cls.clef_png = cls.clef_pngs[cls.clef]
        cls.notes = cls.all_notes[cls.clef]

    @classmethod
    def next_note(cls):
        if cls.init:
            cls.do_init()
            cls.init = False
        while True:
            pos = random.randrange(len(cls.g_notes))
            cls.clef = cls.clefs[random.randrange(len(cls.clefs))]
            # cls.clef = 'g'  #to just train g-clef
            if cls.cur_pos != pos:
                break
        
        cls.cur_pos = pos
        cls.clef_update()
        cls.cur_note = cls.notes[cls.cur_pos]
        cls.get_start_surface()
        cls.draw_note()
        cls.draw_clef()

    @classmethod
    def draw_note(cls):
        cls.cur_surface = cls.start_surface.copy()
        y_pos = st.height - (int(cls.cur_pos*(st.line_diff/2)+st.y_offset))+1
        pygame.draw.circle(cls.cur_surface, st.black,(st.width/2, y_pos), st.note_radius)
        pygame.draw.circle(cls.cur_surface, st.red,(st.width/2, y_pos), st.note_radius-3)
        if cls.cur_pos in (0, 12):
            pygame.draw.line(cls.cur_surface, st.black, (st.width/2-int(st.note_radius*2),
                             y_pos), (st.width/2+int(st.note_radius*2), y_pos), st.line_width)

    @classmethod
    def draw_clef(cls):
        c_ratio = cls.clef_png.get_width() / cls.clef_png.get_height()
        if st.y_offset < 60:
            c_height = st.y_offset
        else:
            c_height = 60
        if cls.clef == 'g':
            c_height = int(c_height * 1.5)
        c_width = c_height * c_ratio
        clef_s = pygame.transform.scale(cls.clef_png, (c_width, c_height))
        sub_s = pygame.Surface((clef_s.get_width(), clef_s.get_height()))
        sub_s.fill(st.red)
        # clef_s.set_alpha(160) #if you want to set background color to emphasize the clef
        sub_s.blit(clef_s, (0, 0))
        cls.cur_surface.blit(sub_s, (0, (st.y_offset-c_height)/2))
    
    @classmethod
    def do_init(cls):
        cls.clefs = st.what_clefs
    
    g_clef_png = pygame.image.load(project_path+'/images/g_clef.png')
    f_clef_png = pygame.image.load(project_path+'/images/f_clef.png')
    init = True
    help_letter = st.easy_mode
    
    g_notes = ('c', 'd', 'e', 'f', 'g', 'a', 'h', 'c', 'd', 'e', 'f', 'g', 'a')
    f_notes = ('e', 'f', 'g', 'a', 'h', 'c', 'd', 'e', 'f', 'g', 'a', 'h', 'c')
    all_notes = {'g': g_notes, 'f': f_notes}
    clef_pngs = {'g': g_clef_png, 'f': f_clef_png}
    cur_surface = None
    cur_pos = None
    cur_note = None
    start_surface = None

    assert not (st.number_of_pos != len(g_notes) or len(g_notes) != len(f_notes))
