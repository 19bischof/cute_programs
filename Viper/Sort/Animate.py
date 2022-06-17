# Controller of UI of Window-Class,List-Class and Animates progress
from settings import Settings as st
import pygame
from window import Window
from list import List


class Animate:
    def render(list, vip=[], vvip=[]):
        Window.instance.screen.fill((0, 0, 0))
        width = int(st.screen_width / (len(list))) - 1
        height = st.screen_height / (st.range)

        if len(list) / st.screen_width > 0.50:
            print("list is too long, go for something like", int(st.screen_width * 0.5))
            pygame.quit()
        for index, bar in enumerate(list):
            color = (204, 151, 6)
            if index in vip:
                color = (255, 0, 0)
            if index in vvip:
                color = (39, 26, 232)
            pygame.draw.rect(Window.instance.screen, color,
                             ((1 + width) * index, int(st.screen_height - bar * height) + 1, width, int(bar * height)))
        Window.update()

    def start():
        print(chr(27) + "[2J")
        selection = ""
        Bubblesort_set = ["1", "1)", "bubblesort", "bubble-sort", "bubble_sort"]
        Insertionsort_set = ["2", "2)", "insertion-sort", "insertionsort", "insertion_sort"]
        Shakersort_set = ["3", "3)", "shakersort", "shaker_sort", "shaker-sort"]
        Quicksort_set = ["4", "4)", "quicksort", "quick_sort", "quick-sort"]
        Selectionsort_set = ["5", "5)", "selectionsort", "selection_sort", "selection-sort"]
        while selection not in Bubblesort_set + Insertionsort_set + Shakersort_set + Quicksort_set + Selectionsort_set:
            print("What Sorting-Algorithm do you want to see?")
            print("1) Bubblesort")
            print("2) Insertionsort")
            print("3) Shakersort")
            print("4) Quicksort")
            print("5) Selectionsort")
            selection = input().lower()
        print("Press Space to start and to pause!")
        if selection in Bubblesort_set:
            Animate.Bubblesort()
        elif selection in Insertionsort_set:
            Animate.Insertionsort()
        elif selection in Shakersort_set:
            Animate.Shakersort()
        elif selection in Quicksort_set:
            Animate.Quicksort()
        elif selection in Selectionsort_set:
            Animate.Selectionsort()
        pygame.display.quit()
        pygame.quit()

    def Bubblesort():
        Window("Bubblesort")
        _list = List()
        _list.Bubblesort_step_by_step()
        delay = int(1000 / len(_list.progress) + 7)
        for p in _list.progress:
            Window.check_events()
            Animate.render(p[0], vip=p[1], vvip=p[2])
            pygame.time.delay(delay)
        already_checked = []
        for p in _list.check_progress:
            Animate.check_loop(p, already_checked)

    def Insertionsort():
        Window("Insertionsort")
        _list = List()
        _list.Insertionsort_step_by_step()
        delay = int(5000 / len(_list.progress) + 5)
        for p in _list.progress:
            Window.check_events()
            Animate.render(p[0], vip=p[1], vvip=p[2])
            pygame.time.delay(delay)
        already_checked = []
        for p in _list.check_progress:
            Animate.check_loop(p, already_checked)

    def Shakersort():
        Window("Shakersort")
        _list = List()
        _list.Shakersort_step_by_step()
        delay = int(1000 / len(_list.progress) + 7)
        for p in _list.progress:
            Window.check_events()
            Animate.render(p[0], vip=p[1], vvip=p[2])
            pygame.time.delay(delay)
        already_checked = []
        for p in _list.check_progress:
            Animate.check_loop(p, already_checked)

    def Quicksort():
        Window("Quicksort")
        _list = List()
        _list.Quicksort_step_by_step()
        delay = int(8000 / len(_list.progress) + 10)
        for p in _list.progress:
            Window.check_events()
            Animate.render(p[0], vip=p[1], vvip=p[2])
            pygame.time.delay(delay)
        already_checked = []
        for p in _list.check_progress:
            Animate.check_loop(p, already_checked)

    def Selectionsort():
        Window("Selectionsort")
        _list = List()
        _list.Selectionsort_step_by_step()
        delay = int(4000 / len(_list.progress) + 7)
        for p in _list.progress:
            Window.check_events()
            Animate.render(p[0], vip=p[1], vvip=p[2])
            pygame.time.delay(delay)
        already_checked = []
        for p in _list.check_progress:
            Animate.check_loop(p, already_checked)

    def check_loop(p, already_checked):
        already_checked += p[1]  # inplace change
        Window.check_events()
        Animate.render(p[0], vvip=already_checked)
        pygame.time.delay(int(100 / len(p[0])))


while input("quit?").lower().strip() not in ("yes", "y"):
    Animate.start()
pygame.quit()
print("Done")
