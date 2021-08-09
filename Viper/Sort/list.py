import random
from settings import Settings as st
from window import Window
class List:
    def __init__(self):
        self.generate()
        
    def generate(self):
        self.values = []
        for i in range(st.length):
            self.values.append(random.randint(0,st.range))
            
    def Bubblesort_step_by_step(self):
        l = self.values
        k = 0
        for k in range(len(l)):
            
            for i in range(len(l)-k-1):
                if l[i]>l[i+1]:
                    l[i],l[i+1] = l[i+1],l[i]
                    yield l,i+1
                    
        self.values = l
        for ii in List.check_sorted(l):
            yield l,ii        
    def Insertionsort_step_by_step(self):
        l = self.values
        for i in range (len(l)):
            for k in range(i):
                
                if l[k]>l[i]:
                    l.insert(k,l[i])
                    del l[i+1]
                    yield l,k
                    break
        for ii in List.check_sorted(l):
            yield l,ii
    def Shakersort_step_by_step(self):
        l = self.values
        iteration = 0
        while iteration <= len(l)/2:
            for i in range (iteration,len(l)-1):
                if l[i]>l[i+1]:
                    l[i],l[i+1] = l[i+1],l[i]
                    yield l,i+1
            iteration += 1
            for k in range (len(l)-iteration,0,-1):
                if l[k-1] > l[k]:
                    l[k-1],l[k] = l[k],l[k-1]
                    yield l,k-1
        for ii in List.check_sorted(l):
            yield l,ii
    def check_sorted(l):
        for i in range (len(l)-1):
            if l[i] > l[i+1] :
                print("The Algorithm is faulty and made a mistake!")
                Window.in_focus = False                 #Pauses the Animation
                Window.check_events()                 
                return False
            yield i+1
        return True                                     #Return doesn't do anything but ending the function early

