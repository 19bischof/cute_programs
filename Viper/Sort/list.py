import random
from settings import Settings as st
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
    def Insertion_sort_step_by_step(self):
        l = self.values
        for i in range (len(l)):
            for k in range(i):
                
                if l[k]>l[i]:
                    l.insert(k,l[i])
                    del l[i+1]
                    yield l,k,i
                    break
        


