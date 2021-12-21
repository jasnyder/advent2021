import functools


with open('input.txt', 'r') as fobj:
    raw = fobj.read().split('\n')[:-1]

cave = [list(map(int, r)) for r in raw]

@functools.lru_cache(maxsize=None)
def neighbors(i, j, I, J):
    possible_neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
    true_neighbors = list()
    for x, y in possible_neighbors:
        if (0<=x<I) and (0<=y<J):
            true_neighbors.append((x,y))
    return true_neighbors

def find_minima(cave):
    minima = list()
    shape = (len(cave), len(cave[0]))
    for i in range(shape[0]):
        for j in range(shape[1]):
            nbrs = neighbors(i, j, *shape)
            if all([cave[i][j] < cave[x][y] for x,y in nbrs]):
                minima.append((i,j))
    return minima

minima = find_minima(cave)

answer = 0
for i, j in minima:
    answer += 1 + cave[i][j]

with open('output.txt', 'w') as fobj:
    fobj.write(str(answer))

"""
Now I need to find the basins of each minimum... That's a bit tricky tbh. How to decide which site flows to which other?
I think a reasonable rule is: smoke flows to the lowest adjacent cell.

I've been background thinking about this for a bit... I feel like there are two approaches: start from minima and expand out, or consider each cell in turn and flow down from it until you find a minimum.
(I think this is a slightly more complicated version of the "count the islands" problem)

I think what I want to do is: create a dictionary whose keys are grid sites and values are basin IDs (i.e. the location of the minimum of the basin).
First, the basin of each minimum is itself
Next, take each non-minimum site, and start flowing downhill, keeping track of the path you take. When you reach a site with a defined basin value, add all the sites you visited to that basin.

Now comes the flow rule... I think that smoke should flow to all sites that are at the minimum height of all neighbor sites. That's encoded in the flow function.
A downside of this is that the "path" branches... so how do I keep track of that branching?
Looking at the data... it seems like it's relatively well-behaved, and I can keep track of just one path
"""
@functools.lru_cache(maxsize=None)
def flow(i, j, I, J):
    nbrs = neighbors(i, j, I, J)
    vals = {(k,l): cave[k][l] for (k, l) in nbrs}
    min_height = min(vals, key = vals.get)
    return [site for site in nbrs if vals[site]==min_height]

@functools.lru_cache(maxsize=None)
def flow_single(i, j, I, J):
    nbrs = neighbors(i, j, I, J)
    vals = {(k,l): cave[k][l] for (k, l) in nbrs}
    return min(vals, key = vals.get)


def find_basins(cave):
    shape = (len(cave), len(cave[0]))
    minima = find_minima(cave)
    basin = dict()
    for site in minima:
        basin[site] = site

    for i in range(shape[0]):
        for j in range(shape[1]):
            if cave[i][j] == 9:
                # the basin value of any site at height 9 is undefined.
                basin[(i,j)] = None
            elif (i,j) in basin.keys():
                # we've already figured out what basin this site is in, either because it's a minimum or because it was on the path we followed while figuring out a different site's basin value
                pass
            else:
                # we need to figure out what basin the site is in. To do this, we flow downhill until we find a site whose basin ID is known
                visited_sites = list()
                k, l = i, j
                visited_sites.append((k, l))
                while (k, l) not in basin.keys():
                    k, l = flow_single(k, l, *shape)
                    visited_sites.append((k, l))
                new_basin = basin[(k,l)]
                # up on exiting the while loop, we've reached a site whose basin value we know already. We can now update the basin value of every site that we visited on the way to be equal to the site we just arrived at
                for site in visited_sites:
                    basin[site] = new_basin
            if (i, j) not in basin.keys():
                print(f'victoria is literaly the best and noone evr crys {i, j}')
    return basin

def sizes(basin):
    return [len([key for key, val in basin.items() if val == minimum]) for minimum in set(basin.values())]

s = sorted(sizes(find_basins(cave)))

ans = s[-4] * s[-3] * s[-2]

with open('output2.txt','w') as fobj:
    fobj.write(str(ans))