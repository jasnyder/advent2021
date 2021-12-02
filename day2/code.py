with open('input.txt','r') as fobj:
    raw = fobj.read()

inst = raw.split('\n')[:-1]

class Boat:
    def __init__(self):
        self.depth = 0
        self.pos = 0
    def apply(self, move):
        direction, length = move.split()
        if direction == 'forward':
            self.pos += int(length)
        elif direction == 'up':
            self.depth -= int(length)
        elif direction == 'down':
            self.depth += int(length)
        else:
            raise ValueError('move malformed')

boat = Boat()
for move in inst:
    boat.apply(move)

ans = boat.depth * boat.pos
with open('output.txt', 'w') as fobj:
    fobj.write(str(ans))

"""
Part2: now with aim!
"""

class Sub:
    def __init__(self):
        self.pos = 0
        self.depth = 0
        self.aim = 0
    def apply(self, move):
        direction, length = move.split()
        x = int(length)
        if direction == 'forward':
            self.pos += x
            self.depth += self.aim * x
        elif direction == 'up':
            self.aim -= x
        elif direction == 'down':
            self.aim += x
        else:
            raise ValueError('move malformed')

sub = Sub()
for move in inst:
    sub.apply(move)

ans = sub.depth * sub.pos
with open('output2.txt', 'w') as fobj:
    fobj.write(str(ans))
