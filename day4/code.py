with open('input.txt','r') as fobj:
    raw = fobj.read().split('\n')

drawn = [int(n) for n in raw[0].split(',')]

boardsize = 5

class Board:
    def __init__(self, data, size = None):
        if size is None:
            self.size = len(data)
        else:
            assert isinstance(size, int)
            self.size = size
        assert len(data[0])==self.size==len(data)
        self.data = data
        self.mask = [[False for j in range(self.size)] for i in range(self.size)]
        self.done = False

    def call(self, num):
        # check off the number num from your board by switching the right element of the mask to True
        for i in range(self.size):
            for j in range(self.size):
                if self.data[i][j] == num:
                    self.mask[i][j] = True

    def call_batch(self, nums):
        for num in nums:
            self.call(num)

    def check_for_bingo(self):
        # check rows and columns
        for i in range(self.size):
            if all(self.mask[i]):
                self.done = True
            if all([self.mask[j][i] for j in range(self.size)]):
                self.done = True
        # check diagonals
        if all([self.mask[i][i] for i in range(self.size)]):
            self.done = True
        if all([self.mask[i][self.size-i-1] for i in range(self.size)]):
            self.done = True
        return self.done
    
    def sum_of_unmarked(self):
        sum = 0
        for i in range(self.size):
            for j in range(self.size):
                if not self.mask[i][j]:
                    sum += self.data[i][j]
        return sum

                

boards = list()
for i in range(100):
    rawdata = raw[2+6*i : 7+6*i]
    data = [[int(n) for n in row.split()] for row in rawdata]
    boards.append(Board(data))

# now play the game!
def play(boards, drawn):
    for i, n in enumerate(drawn):
        for board in boards:
            board.call(n)
            if board.check_for_bingo():
                return board, (i, n)

winner, (i, n) = play(boards, drawn)

ans = winner.sum_of_unmarked() * n
with open('output.txt', 'w') as fobj:
    fobj.write(str(ans))


# part 2
boards = list()
for i in range(100):
    rawdata = raw[2+6*i : 7+6*i]
    data = [[int(n) for n in row.split()] for row in rawdata]
    boards.append(Board(data))

def find_the_loser(boards):
    bb = boards.copy()
    for n in drawn:
        for board in bb:
            board.call(n)
            if len(bb) > 1 and board.check_for_bingo():
                bb.remove(board)
            if len(bb) == 1 and board.check_for_bingo():
                return bb[0], n

loser, n = find_the_loser(boards)
ans = loser.sum_of_unmarked() * n
with open('output2.txt','w') as fobj:
    fobj.write(str(ans))