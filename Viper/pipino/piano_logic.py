import pygame
import random
from settings import settings as st


class pipino:
    @classmethod
    def get_start_surface(cls):
        s = pygame.Surface(st.size)
        s.fill(st.white)
        for i in range(5):
            pygame.draw.line(s, st.black, (0, st.height-(st.line_diff*(i+1)++st.y_offset)),
                             (st.width, st.height-(st.line_diff*(i+1)+st.y_offset)), st.line_width)
        cls.start_surface = s

    @classmethod
    def clef_update(cls):
        cls.clef_png = cls.clef_pngs[cls.clef]
        cls.notes = cls.all_notes[cls.clef]

    @classmethod
    def next_note(cls):
        if cls.init is False:
            cls.get_start_surface()
        while True:
            pos = random.randrange(len(cls.g_notes))
            cls.clef = cls.clefs[random.randrange(2)]
            if cls.cur_pos != pos:
                break
        cls.clef_update()
        cls.cur_pos = pos
        cls.cur_note = cls.notes[cls.cur_pos]
        cls.draw_note()
        cls.draw_clef()

    @classmethod
    def draw_note(cls):
        cls.cur_surface = cls.start_surface.copy()
        y_pos = st.height - \
            (int(cls.cur_pos*(st.line_diff/2)+st.y_offset))+1
        pygame.draw.circle(cls.cur_surface, st.black,
                           (st.width/2, y_pos), st.note_radius)
        pygame.draw.circle(cls.cur_surface, st.red,
                           (st.width/2, y_pos), st.note_radius-3)
        if cls.cur_pos in (0, 12):
            pygame.draw.line(cls.cur_surface, st.black, (st.width/2-int(st.note_radius*2),
                             y_pos), (st.width/2+int(st.note_radius*2), y_pos), st.line_width)

    @classmethod
    def draw_clef(cls):
        c_ratio = cls.clef_png.get_rect()[2] / cls.clef_png.get_rect()[3]
        if st.y_offset < 60:
            c_height = st.y_offset
        else:
            c_height = 60
        c_width = c_height * c_ratio        
        print(c_ratio)
        clef_s = pygame.transform.scale(cls.clef_png, (c_width, c_height))
        sub_s = pygame.Surface((clef_s.get_rect()[2],clef_s.get_rect()[3]))
        sub_s.fill(st.grey)
        sub_s.blit(clef_s,(0,0))
        cls.cur_surface.blit(sub_s,(0, (st.y_offset-c_height)/2))   #make sure opacity makes sense and not just white from the png


    g_clef_png = pygame.image.load('./images/g_clef.png')
    f_clef_png = pygame.image.load('./images/f_clef.png')
    init = False
    clefs = ('g', 'f')
    g_notes = ('c', 'd', 'e', 'f', 'g', 'a', 'h', 'c', 'd', 'e', 'f', 'g', 'a')
    f_notes = ('e', 'f', 'g', 'a', 'h', 'c', 'd', 'e', 'f', 'g', 'a', 'h', 'c')
    all_notes = {'g': g_notes, 'f': f_notes}
    clef_pngs = {'g': g_clef_png, 'f': f_clef_png}
    cur_surface = None
    cur_pos = None
    cur_note = None
    start_surface = None

    if st.number_of_pos != len(g_notes) or len(g_notes) != len(f_notes):
        print("number of notes don't match!")
        quit()
