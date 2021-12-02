with open('input.txt', 'r') as fobj:
    nums = list(map(int, fobj.read().split()))

ans = 0
for a, b in zip(nums[:-1], nums[1:]):
    if b > a:
        ans += 1

with open('output.txt', 'w') as fobj:
    fobj.write(str(ans))


"""
Part 2

Now I need to take the input numbers and sum them three-at-a-time, then find how many times this running average increases

There should be some math to do to make this simpler - the running average only increases if the newest number is larger than the oldest number, since the other two stay the same.
I should then be able to use exactly the same code, just with different slices of nums
"""



ans = 0
for a, b in zip(nums[:-3], nums[3:]):
    if b > a:
        ans += 1

with open('output2.txt', 'w') as fobj:
    fobj.write(str(ans))