with open('input.txt', 'r') as fobj:
    code_strings = fobj.read().split('\n')[:-1]
    codes = [[int(ci) for ci in c] for c in code_strings]
N = len(codes)      # number of input strings
L = len(codes[0])   # length of each input string (and target string)
"""
I need to find the most common and least common bits in each position
"""

S = [sum(z) for z in zip(*codes)]

gamma_bits = [0 if s > 500 else 1 for s in S]
eps_bits = [0 if g==1 else 1 for g in gamma_bits]

def binary_to_decimal(bitstring):
    L = len(bitstring)
    return sum([2**(L-i-1)*bi for i, bi in enumerate(bitstring)])

gamma = binary_to_decimal(gamma_bits)
eps = binary_to_decimal(eps_bits)

ans = gamma*eps

with open('output.txt', 'w') as fobj:
    fobj.write(str(ans))


"""
Part 2: some different shit

This will require repeated application of a subroutine for: find most/least common bit in X position
"""

def most_common_bits(codes):
    N = len(codes)
    S = [sum(z) for z in zip(*codes)]
    return [1 if s>=N/2 else 0 for s in S]

def filter(codes, pos, bit):
    # removes any code that does not satisfy code[pos] == bit
    good = list()
    for code in codes:
        if code[pos] == bit:
            good.append(code)
    return good

# find oxygen generator rating: filter by 
oxy = codes.copy()
pos = 0
while len(oxy) > 1:
    mcb = most_common_bits(oxy)
    oxy = filter(oxy, pos, mcb[pos])
    pos += 1
    pos = pos%L

co2 = codes.copy()
pos = 0
while len(co2) > 1:
    mcb = most_common_bits(co2)
    co2 = filter(co2, pos, 1-mcb[pos])
    pos += 1
    pos = pos%L
ans = binary_to_decimal(oxy[0]) * binary_to_decimal(co2[0])
with open('output2.txt', 'w') as fobj:
    fobj.write(str(ans))