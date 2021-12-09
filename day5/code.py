with open('input.txt', 'r') as fobj:
    raw = fobj.read().split('\n')[:-1]

class Line:
    def __init__(self, start, end):
        self.x0, self.y0 = start
        self.x1, self.y1 = end
        if self.x0 == self.x1:
            self.orient = 'vertical'
        elif self.y0 == self.y1:
            self.orient = 'horizontal'
        else:
            self.orient = 'slant'

def goodrange(a, b):
    if a<b:
        return range(a, b+1)
    elif b<a:
        return range(b, a+1).__reversed__()
    else:
        return range(a, a+1)

lines = list()
for string in raw:
    start, end = string.split('->')
    lines.append(Line(eval(start), eval(end)))

def draw(grid, line):
    if line.orient == 'horizontal':
        for x in goodrange(line.x0, line.x1):
            point = (x, line.y0)
            if point in grid.keys():
                grid[point] += 1
            else:
                grid[point] = 1
    elif line.orient == 'vertical':
        for y in goodrange(line.y0, line.y1):
            point = (line.x0, y)
            if point in grid.keys():
                grid[point] += 1
            else:
                grid[point] = 1
    return

grid = dict()
for line in lines:
    draw(grid, line)

# find how many points there are where 2 or more lines overlap
def count_at_least_two(grid):
    return sum([v>=2 for v in grid.values()])

with open('output.txt', 'w') as fobj:
    fobj.write(str(count_at_least_two(grid)))

"""
Part 2: consider slant lines as well
"""

def draw(grid, line):
    if line.orient == 'horizontal':
        for x in goodrange(line.x0, line.x1):
            point = (x, line.y0)
            if point in grid.keys():
                grid[point] += 1
            else:
                grid[point] = 1
    elif line.orient == 'vertical':
        for y in goodrange(line.y0, line.y1):
            point = (line.x0, y)
            if point in grid.keys():
                grid[point] += 1
            else:
                grid[point] = 1
    elif line.orient == 'slant':
        for x, y in zip(goodrange(line.x0, line.x1), goodrange(line.y0, line.y1)):
            point = (x, y)
            if point in grid.keys():
                grid[point] += 1
            else:
                grid[point] = 1
    return


grid = dict()
for line in lines:
    draw(grid, line)

# find how many points there are where 2 or more lines overlap
def count_at_least_two(grid):
    return sum([v>=2 for v in grid.values()])

with open('output2.txt', 'w') as fobj:
    fobj.write(str(count_at_least_two(grid)))