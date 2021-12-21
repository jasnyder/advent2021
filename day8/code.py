with open('input.txt','r') as fobj:
    raw = fobj.read().split('\n')[:-1]

segment_num_to_digit = dict({
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: [8],
})

digit_to_segments = dict({
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg"
})

class Entry:
    def __init__(self, rawstring):
        a, b = rawstring.split('|')
        self.signal_pattern = a.split()
        self.output = b.split()
    
    def count_easy_digits(self):
        # returns the number of codewords in the output that are "easy" numbers: 1, 4, 7, or 8
        num = 0
        for word in self.output:
            if len(word) in [2, 3, 4, 7]:
                num += 1
        return num

entries = list()
for rawstring in raw:
    entries.append(Entry(rawstring))

ans = sum([entry.count_easy_digits() for entry in entries])
with open('output.txt','w') as fobj:
    fobj.write(str(ans))

"""
Part 2: I need to actually decode each entry. So what I need to do is to find which letter maps to which other letter

How to work with this?
As a start, the thing I want to find can be represented as a dict: map[a] = b

The information I have is a set of encoded numbers, and I know that each digit 0-9 is represented

For example I can locate the single length-2 code, and know that that represents the digit 1, and therefore the two symbols in the code correspond to c and f

What about hard-coding stuff?
    - segment a is the unique segment that's in 7 but not 1 (the 3-code and not the 2-code)
    - segments b and d are the segments in 4 but not 1
    - segments d and g are the overlap between 2 and 5

How about... disambiguating 2/3/5 and 0/6/9 based on pairwise overlap
    - overlap(2,3) = 4
    - overlap(2,5) = 3 ==> this identifies 3
    - overlap(3,5) = 4

    - KNOWN: 1, 3, 4, 7, 8
    
    - overlap(3,9) = 5 ==> this identifies 9
    - overlap(3,6) = 4
    - overlap(3,0) = 4
    
    - KNOWN: 1, 3, 4, 7, 8, 9
    
    - overlap(5,9) = 6
    - overlap(2,9) = 4 ==> this identifies 2 vs 5

    - KNOWN: 1, 2, 3, 4, 5, 7, 8, 9

    - overlap(1,0) = 2
    - overlap(1,6) = 1 ==> this identifies 0 vs 6
"""

def overlap(a, b):
    return len(set(a).intersection(set(b)))


class Entry:
    def __init__(self, rawstring):
        a, b = rawstring.split('|')
        self.signal_pattern = a.split()
        self.output = b.split()
        self.code = None
        self.out_value = None
    
    def count_easy_digits(self):
        # returns the number of codewords in the output that are "easy" numbers: 1, 4, 7, or 8
        num = 0
        for word in self.output:
            if len(word) in [2, 3, 4, 7]:
                num += 1
        return num

    def decode(self):
        if self.code is None:
            self.find_mapping()
        out_digits = [self.code[frozenset(o)] for o in self.output]
        self.out_value = sum([10**(3-i) * o for i, o in enumerate(out_digits)])
        return

    def get_out_value(self):
        if self.out_value is None:
            self.decode()
        return self.out_value

    def find_mapping(self):
        self.code = dict()
        # decode easy words
        for signal in self.signal_pattern:
            if len(signal) == 2:
                one = signal
                self.code[frozenset(one)] = 1
            elif len(signal) == 3:
                seven = signal
                self.code[frozenset(seven)] = 7
            elif len(signal) == 4:
                four = signal
                self.code[frozenset(four)] = 4
            elif len(signal) == 7:
                eight = signal
                self.code[frozenset(eight)] = 8
        # pick 3 out of 2/3/5
        ttf = [s for s in self.signal_pattern if len(s) == 5]
        if overlap(ttf[0], ttf[1]) == 3:
            three = ttf[2]
        elif overlap(ttf[0], ttf[2]) == 3:
            three = ttf[1]
        else:
            three = ttf[0]
        self.code[frozenset(three)] = 3
        # pick 9 out of 0/6/9. this requires knowledge of three
        osn = [s for s in self.signal_pattern if len(s) == 6]
        for signal in osn:
            if overlap(three, signal) == 5:
                nine = signal
                self.code[frozenset(nine)] = 9
        # disambiguate 2 vs 5 using 9
        ttf.remove(three)
        if overlap(ttf[0], nine) == 6:
            five = ttf[0]
            two = ttf[1]
        else:
            five = ttf[1]
            two = ttf[0]
        self.code[frozenset(two)] = 2
        self.code[frozenset(five)] = 5
        # finally disambiguate 0 vs 6 by comparing to 1
        osn.remove(nine)
        if overlap(osn[0], one) == 2:
            zero = osn[0]
            six = osn[1]
        else:
            zero = osn[1]
            six = osn[0]
        self.code[frozenset(six)] = 6
        self.code[frozenset(zero)] = 0
        return

entries = list()
for rawstring in raw:
    entries.append(Entry(rawstring))

def sanity_check(entry):
    # check that segment number of the output matches
    out_number_string = f'{entry.get_out_value():04}'
    output_lengths = [len(o) for o in entry.output]
    return [eval(s) in segment_num_to_digit[l] for l, s in zip(output_lengths, out_number_string)]

ans = sum([entry.get_out_value() for entry in entries])
with open('output2.txt','w') as fobj:
    fobj.write(str(ans))
