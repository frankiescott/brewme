import itertools

graph = [[0,2,2,3,3,2,4],
         [2,0,3,3,5,3,6],
         [2,3,0,2,3,6,8],
         [3,3,2,0,3,8,5],
         [2,5,3,3,0,3,6],
         [2,3,4,2,3,0,8],
         [3,3,2,3,3,8,0]]


#https://github.com/CarlEkerot/held-karp/blob/master/held-karp.py
def hamiltonian_beer_cycle(dists):
    n = len(dists)
    memo = {}

    # Set transition cost from initial state
    for k in range(1, n):
        memo[(1 << k, k)] = (dists[0][k], 0)

        # Iterate subsets of increasing length and store intermediate results
        # in classic dynamic programming manner
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            for k in subset:
                prev = bits ^ (1 << k)

                res = []
                for m in subset:
                    if m == k:
                        continue
                    res.append((memo[(prev, m)][0] + dists[m][k], m))
                memo[(bits, k)] = min(res)

        # We're interested in all bits but the least significant (the start state)
    bits = (2 ** n - 1) - 1
    # Calculate optimal cost
    end = []
    for k in range(1, n):
        end.append((memo[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(end)

    # Backtrack to find full path
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits ^ (1 << parent)
        _, parent = memo[(bits, parent)]
        bits = new_bits

    # Add implicit start state
    path.append(0)

    return opt, list(reversed(path))