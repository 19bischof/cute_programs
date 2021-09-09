#When instance created sort-algorithm can be performed on it
#stores step by step changes in progress-variable
#check_sorted() progress is stored seperately to have the same speed on it in the animation later
import random
from settings import Settings as st
from window import Window
class List:
    def __init__(self):
        self.values = []
        self.generate()
        self.progress = []
        self.check_progress = []
        
    def generate(self):
        for i in range(st.length):
            self.values.append(random.randint(0,st.range))

    def Bubblesort_step_by_step(self):
        l = self.values
        for k in range(len(l)):            
            for i in range(len(l)-k-1):
                if l[i]>l[i+1]:
                    l[i],l[i+1] = l[i+1],l[i]
                    self.progress.append((l[:],[i+1],[len(l)-k-1]))
        self.values = l
        self.check_sorted()

    def Insertionsort_step_by_step(self):
        l = self.values
        for i in range (len(l)):
            for k in range(i):                
                if l[k]>l[i]:
                    l.insert(k,l[i])
                    del l[i+1]
                    self.progress.append((l[:],[k],[i+1]))
                    break
        self.values = l
        self.check_sorted()

    def Shakersort_step_by_step(self):
        l = self.values
        iteration = 0
        while iteration <= len(l)/2:
            for i in range (iteration,len(l)-1-iteration):
                if l[i]>l[i+1]:
                    l[i],l[i+1] = l[i+1],l[i]
                    self.progress.append((l[:],[i+1],[len(l)-1-iteration,iteration]))
            for k in range (len(l)-iteration-1,iteration,-1):
                if l[k-1] > l[k]:
                    l[k-1],l[k] = l[k],l[k-1]
                    self.progress.append((l[:],[k-1],[len(l)-1-iteration,iteration]))
            iteration += 1
        self.values = l
        self.check_sorted()

    def Quicksort_step_by_step(self):
        l = self.values
        self.recursive_quicksort(0,len(l)-1)
        self.check_sorted()

    def recursive_quicksort(self,lower_bound = 0,upper_bound = 0):
        l = self.values
        low = lower_bound
        up = upper_bound
        if low >= up:
            return 
        pivot = l[random.randint(low, up)]
        while low < up:
            while l[low] < pivot:
                low += 1
            while l[up] > pivot:
                up -= 1
            if low <= up:
                l[low],l[up] = l[up],l[low]
                low += 1;up -= 1
                self.progress.append((l[:],[up,low],[lower_bound,upper_bound]))
        self.recursive_quicksort(lower_bound,up)
        self.recursive_quicksort(low,upper_bound)
            

    def Selectionsort_step_by_step(self):
        l = self.values
        for k in range(len(l)-1):
            smallest_i = k
            for i in range(k,len(l)):
                if l[smallest_i] > l[i]:
                    smallest_i = i
            l[smallest_i],l[k] = l[k],l[smallest_i]
            self.progress.append((l[:],[smallest_i,k],[k-1,len(l)-1]))
        # self.check_sorted()


    def check_sorted(self):
        l = self.values
        for i in range (len(l)-1):
            if l[i] > l[i+1] :
                print("The Algorithm is faulty and made a mistake!")
                Window.in_focus = False                 #Pauses the Animation
                Window.check_events()                 
                return False
            self.check_progress.append((l,[i]))
        self.check_progress.append((l,[len(l)-1]))        #last index otherwise not highlighted
        return True                                     #Return doesn't do anything but ending the function early


