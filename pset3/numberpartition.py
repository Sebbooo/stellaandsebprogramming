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

# Prepartitioned Repeated Random
def prepartitioned_repeated_random(A, max_iter):
    # Start with a random solution P (prepar)
    n = len(A)
    P = [random.randint(1, n) for _ in range(n)]
    best_residue = calculate_prepartition_residue(A, P)
    
    # For iter = 1 to max_iter
    for _ in range(max_iter):
        # P' = a random solution
        P_prime = [random.randint(1, n) for _ in range(n)]
        residue_prime = calculate_prepartition_residue(A, P_prime)
        
        # if residue(P') < residue(P) then P = P'
        if residue_prime < best_residue:
            P = P_prime
            best_residue = residue_prime
    
    # returns best assignment found out of all iterations
    return P

# Calculate the residue for a prepartitioned solution
def calculate_prepartition_residue(A, P):
    # create a dictionary to track the sum of each partition
    partition_sums = {}
    
    # calculate the sum for each number
    for i in range(len(A)):
        partition = P[i]
        if partition in partition_sums:
            partition_sums[partition] += A[i]
        else:
            partition_sums[partition] = A[i]
    
    # dictionary values to an array
    partition_array = list(partition_sums.values())
    
    # use kk to calculate residue
    return kk(partition_array)

# Hill Climbing
# Simulated Annealing
# Prepartitioned Hill Climbing
# Prepartitioned Simulated Annealing
