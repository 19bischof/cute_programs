from settings import Settings as st
import pygame 
from window import  Window
from list import List
class Animate:
    def render(list,vip=[]):
        Window.instance.screen.fill((0,0,0))
        width = int(st.screen_width / (len(list))) -1
        height = (st.screen_height / (st.range)) 
        if len(list)/st.screen_width > 0.50:
            print("list is too long, go for something like",int(st.screen_width*0.5))
            pygame.quit()
        for index,bar in enumerate(list):
            color = (204, 151, 6)
            if index in vip:
                color = (255,0,0)
            pygame.draw.rect(Window.instance.screen,color,((1+width) * index,int(st.screen_height - bar * height)+1,width,int(bar*height)))
        Window.update()
    def start():    
        selection = ""    
        while selection not in ["1","1)","Bubblesort","Bubble-sort","Bubble_sort","2","2)","Insertion-sort","Insertionsort","Insertion_sort","3","3)","Shakersort","Shaker_sort","Shaker-sort"]:
            print("What sorting algorithm do you want to see?")
            print("1) Bubblesort")
            print("2) Insertionsort")
            print("3) Shakersort")
            selection = input()
        print("Press Space to start and to pause!")
        if selection in ["1","1)","Bubblesort","Bubble-sort","Bubble_sort"]:
            Animate.Bubblesort()
        if selection in ["2","2)","Insertion-sort","Insertionsort","Insertion_sort"]:
            Animate.Insertionsort()
        if selection in ["3","3)","Shakersort","Shaker_sort","Shaker-sort"]:
            Animate.Shakersort()
    def Bubblesort():
        Window("Bubblesort")
        for l,i in List().Bubblesort_step_by_step():
            Window.check_events()
            Animate.render(l,vip=[i])
            pygame.time.delay(int(200/st.length))
    def Insertionsort():
        Window("Insertionsort")
        for l,i in List().Insertionsort_step_by_step():
            Window.check_events()
            Animate.render(l,vip=[i])
            pygame.time.delay(int(5000/st.length))
    def Shakersort():
        Window("Shakersort")
        for l,i in List().Shakersort_step_by_step():
            Window.check_events()
            Animate.render(l,vip=[i])
            pygame.time.delay(int(100*2/st.length))
Animate.start()
pygame.quit()
print("Done")