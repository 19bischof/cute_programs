import random

width, height = 10,10    


class snack:
    """snake class for snake game"""

    def __init__(self):
        self.head = int(height / 2), int(width / 2)
        self.body = [self.head for x in range(3)]
        self.spawn_apple()
        self.direction = 1  # 0-3, 0 = north, 1 = west
        self.digestion = 0  # if apple in stomach and not part of body
        self.state = 1      #0:lost, 1:alive, 2: won
        self.score = 0
        self.turns = [] #if snack too slow to respond it buffers input

    def move(self):
        if self.turns:
            self.direction = self.turns.pop(0)
        dick = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
        r, c = dick[self.direction]
        self.body.append(self.head)      
        self.head = self.head[0] + r, self.head[1] + c
        # out of bounds:
        if self.head[0] >= height:
            self.head = 0,self.head[1]
        if self.head[0] < 0:
            self.head = height - 1,self.head[1]
        if self.head[1] >= width:
            self.head = self.head[0],0
        if self.head[1] < 0:
            self.head = self.head[0],width - 1

        if self.digestion == 0:
            self.body.pop(0)
        else:
            self.digestion -= 1
        self.collision_check()
        self.turn_signal = False

    def collision_check(self):
        if self.head in self.body:
            self.state = 0
        if self.head == self.apple:
            self.digestion += 1
            self.spawn_apple()
            self.score += 1
            if len(self.body)+1+self.digestion == width*height:
                self.state = 2  #won the game

    def spawn_apple(self):
        empty_spaces = []
        for x in range(width):
            for y in range(height):
                if (y,x) not in self.body and (y,x) != self.head:
                    empty_spaces.append((y,x))
        if len(empty_spaces) == 0:
            print("something went wrong no more space left for apple")
            raise RuntimeError
        self.apple = random.choice(empty_spaces)

    def change_dir(self, dir):
        # or use is_instance if you know the correct syntax for it since i currently don't and have no internet!
        if dir == type(str):
            dick = {"north": 0, "east": 1, "south": 2, "west": 3}
            dir = dick[dir]
        if not self.turns:
            if abs(self.direction - dir) == 2:
                return
        else:
            if abs(self.turns[-1] - dir) == 2:
                return
        if 0 <= dir <= 3:
            self.turns.append(dir)
