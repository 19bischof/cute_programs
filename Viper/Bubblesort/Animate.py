from settings import Settings as st
import pygame 
from window import  Window
from list import List
class Animate:
    def render(vip,list = []):
        Window.screen.fill((0,0,0))
        width = int(st.screen_width / (len(list))) -1
        height = (st.screen_height / (st.range)) 
        if len(list)/st.screen_width > 0.50:
            print("list is too long, go for something like",int(st.screen_width*0.5))
            pygame.quit()
        for index,bar in enumerate(list):
            color = (204, 151, 6)
            if index == vip:
                color = (255,0,0)
            pygame.draw.rect(Window.screen,color,((1+width) * index,int(st.screen_height - bar * height)+1,width,int(bar*height)))
        Window.update()
    def start():        
        for l,i in List().sort_step_by_step():
            Window.check_events()
            Animate.render(i,l)
            pygame.time.delay(int(200/st.length))
Animate.start()
pygame.quit()
print("Done")