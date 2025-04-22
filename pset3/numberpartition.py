# Karmarkar-Karp
# Repeated Random
import random
import heapq

def kk(A):
    heap = [-a for a in A]
    heapq.heapify(heap)

    while len(heap) > 1:
        heapq.heappush(heap, -abs(heapq.heappop(heap) - heapq.heappop(heap)))

    return -heap[0]

print(str(kk([1,2,3,4,4])))

# assume input is an array of non-negative integers, not necessarily sorted
def repeated_random(A, max_iter):
    # Start with a random solution S
    n = len(A)
    S = [random.choice([-1, 1]) for _ in range(n)]
    best_residue = calculate_residue(A, S)
    
    # For iter = 1 to max_iter
    for _ in range(max_iter):
        # S' = a random solution
        S_prime = [random.choice([-1, 1]) for _ in range(n)]
        residue_prime = calculate_residue(A, S_prime)
        
        # if residue(S') < residue(S) then S = S'
        if residue_prime < best_residue:
            S = S_prime
            best_residue = residue_prime
    
    # returns best assignment found out of all iterations
    return S

# Calculate the residue (difference) for a given solution (not written in prepartiti)
def calculate_residue(A, S):
    total = sum(A[i] * S[i] for i in range(len(A)))
    return abs(total)

# Hill Climbing
# Simulated Annealing
# Prepartitioned Repeated Random
# Prepartitioned Hill Climbing
# Prepartitioned Simulated Annealing
