with open('input.txt', 'r') as fobj:
    raw = fobj.read()

pos = list(eval(raw))

def fuel(pos, mean):
    return sum([abs(p-mean) for p in pos])

scores = dict()

for mean in range(min(pos), max(pos)+1):
    scores[mean] = fuel(pos, mean)

with open('output.txt','w') as fobj:
    fobj.write(str(min(scores.values())))

# part 2: the score is different

def triangle(n):
    return int(n*(n+1)/2)

def fuel2(pos, mean):
    return sum([triangle(abs(p - mean)) for p in pos])

scores2 = dict()

for mean in range(min(pos), max(pos)+1):
    scores2[mean] = fuel2(pos, mean)

with open('output2.txt','w') as fobj:
    fobj.write(str(min(scores2.values())))