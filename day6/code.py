with open('input.txt','r') as fobj:
    raw = fobj.read()

def evolve(timers, T = 6):
    new_timers = list()
    new_fish_count = 0
    for timer in timers:
        if timer > 0:
            new_timers.append(timer - 1)
        elif timer == 0:
            new_timers.append(T)
            new_fish_count += 1
    for fish in range(new_fish_count):
        new_timers.append(T+2)
    return new_timers


timers = list(eval(raw))

for day in range(80):
    timers = evolve(timers)

ans = len(timers)
with open('output.txt','w') as fobj:
    fobj.write(str(ans))

# part 2.... can I do 256??
# it would be great if I could explicitly compute number of progeny of each fish...

# another approach: keep track of # fish at each age    

timers = list(eval(raw))
timer_counts = dict()

for timer in timers:
    if timer in timer_counts.keys():
        timer_counts[timer] += 1
    else:
        timer_counts[timer] = 1

def evolve_counts(old_counts):
    new_counts = dict()
    for t in range(9):
        new_counts[t] = 0
    for timer in old_counts.keys():
        if timer > 0:
            new_counts[timer-1] = old_counts[timer]
    new_counts[8] += old_counts.get(0, 0)
    new_counts[6] += old_counts.get(0, 0)
    return new_counts
    

for day in range(256):
    timer_counts = evolve_counts(timer_counts)

ans = sum(timer_counts.values())
with open('output2.txt','w') as fobj:
    fobj.write(str(ans))
