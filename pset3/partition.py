# Karmarkar-Karp
# Repeated Random
import random
import heapq
import math
import sys
import matplotlib.pyplot as plt
import numpy as np

def kk(A):
    heap = [-a for a in A]
    heapq.heapify(heap)

    while len(heap) > 1:
        heapq.heappush(heap, -abs(heapq.heappop(heap) - heapq.heappop(heap)))

    return -heap[0]

def repeated_random(A, max_iter=25000):
    n = len(A)
    S = [random.choice([-1, 1]) for _ in range(n)]
    best_residue = calculate_residue(A, S)
    
    for _ in range(max_iter):
        S_prime = [random.choice([-1, 1]) for _ in range(n)]
        residue_prime = calculate_residue(A, S_prime)
        
        if residue_prime < best_residue:
            S = S_prime
            best_residue = residue_prime
    
    return best_residue

def calculate_residue(A, S):
    total = sum(A[i] * S[i] for i in range(len(A)))
    return abs(total)

# Prepartitioned Repeated Random
def prepartitioned_repeated_random(A, max_iter=25000):
    n = len(A)
    P = [random.randint(1, n) for _ in range(n)]
    best_residue = calculate_prepartition_residue(A, P)
    
    for _ in range(max_iter):
        P_prime = [random.randint(1, n) for _ in range(n)]
        residue_prime = calculate_prepartition_residue(A, P_prime)
        
        if residue_prime < best_residue:
            P = P_prime
            best_residue = residue_prime
    
    return best_residue

def calculate_prepartition_residue(A, P):
    partition_sums = {}
    
    for i in range(len(A)):
        partition = P[i]
        if partition in partition_sums:
            partition_sums[partition] += A[i]
        else:
            partition_sums[partition] = A[i]
    
    partition_array = list(partition_sums.values())
    
    return kk(partition_array)

def hill_climb(A, max_iter=25000):
    n = len(A)
    S = [random.choice([-1, 1]) for _ in A]
    best = calculate_residue(A, S)
    best_S = S

    for _ in range(max_iter):
        new = S.copy()
        inds = random.sample(range(n), 2)
        new[inds[0]] *= -1
        if random.random() < 0.5:
            new[inds[1]] *= -1

        new_r = calculate_residue(A, new)

        if new_r < best:
            S = new
            best = new_r
            best_S = S

    return best

def hill_climb_prepartitioned(A, max_iter=25000):
    n = len(A)
    P = [random.randint(1, n) for _ in range(n)]
    best_residue = calculate_prepartition_residue(A, P)
    
    for _ in range(max_iter):
        P_prime = P.copy()
        
        i = random.randint(0, n - 1)
        current_partition = P_prime[i]
        
        possible_partitions = list(range(1, n+1))
        possible_partitions.remove(current_partition)
        
        if possible_partitions:
            j = random.choice(possible_partitions)
            P_prime[i] = j
            
            residue_prime = calculate_prepartition_residue(A, P_prime)
            
            if residue_prime < best_residue:
                P = P_prime
                best_residue = residue_prime

    return best_residue

def simulated_annealing(A, max_iter=25000):
    n = len(A)
    S = [random.choice([-1, 1]) for _ in A]
    best = calculate_residue(A, S)
    best_S = S

    for i in range(max_iter):
        new = S.copy()
        inds = random.sample(range(n), 2)
        new[inds[0]] *= -1
        if random.random() < 0.5:
            new[inds[1]] *= -1

        S_r = calculate_residue(A, S)
        new_r = calculate_residue(A, new)

        T = 1e10 * (0.8 ** (i / 300))

        if new_r < S_r or random.random() < math.exp(-(new_r - S_r) / T):
            S = new
            S_r = new_r

        if S_r < best:
            best = S_r
            best_S = S

    return best

def simulated_annealing_prepartitioned(A, max_iter=25000):
    n = len(A)
    P = [random.randint(1, n) for _ in range(n)]
    P_r = calculate_prepartition_residue(A, P)
    best_residue = P_r
    best_P = P.copy()
    
    for i in range(max_iter):
        P_prime = P.copy()
        
        # Choose two random indices i and j with pi ≠ j
        i = random.randint(0, n-1)  # Random element to change
        current_partition = P_prime[i]
        
        # Find a different partition number for this element
        possible_partitions = list(range(1, n+1))
        possible_partitions.remove(current_partition)
        
        if possible_partitions:  # Make sure there's at least one other partition option
            # Set pi to j (move element i to a different partition)
            j = random.choice(possible_partitions)
            P_prime[i] = j
            
            # Calculate residue of the neighbor
            P_prime_r = calculate_prepartition_residue(A, P_prime)
            
            # Calculate temperature (cooling schedule)
            T = 1e10 * (0.8 ** (i / 300))
            
            # Accept new solution if it's better or with probability based on temperature
            if P_prime_r < P_r or random.random() < math.exp(-(P_prime_r - P_r) / T):
                P = P_prime
                P_r = P_prime_r
            
            # Keep track of the best solution found
            if P_r < best_residue:
                best_residue = P_r
                best_P = P.copy()
    
    # Return the best assignment found
    return best_residue

# Generate 50 random instances
num_instances = 50
n = 100
instances = [[random.randint(1, 10**12) for _ in range(n)] for _ in range(num_instances)]

# Storage for results
results = {
    "KK": [],
    "RR": [],
    "RR-PP": [],
    "HC": [],
    "HC-PP": [],
    "SA": [],
    "SA-PP": []
}

# Run all algorithms on all instances
i = 1
for A in instances:
    results["KK"].append(kk(A))
    results["RR"].append(repeated_random(A))
    results["RR-PP"].append(prepartitioned_repeated_random(A))
    results["HC"].append(hill_climb(A))
    results["HC-PP"].append(hill_climb_prepartitioned(A))
    results["SA"].append(simulated_annealing(A))
    results["SA-PP"].append(simulated_annealing_prepartitioned(A))
    print("Done with "+str(i)+"!\n")
    i+=1

# Create a boxplot for visual comparison
fig, ax = plt.subplots(figsize=(12, 6))
labels = list(results.keys())
data = [results[key] for key in labels]
ax.boxplot(data, labels=labels, showmeans=True)
ax.set_title("Residue Comparison of Partition Algorithms (50 Random Instances)")
ax.set_ylabel("Residue")
ax.set_yscale('log')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True, which="both", ls="--")
plt.show()



# code = int(sys.argv[2])
# input_file = sys.argv[3]

# with open(input_file, 'r') as f:
#     A = [int(line.strip()) for line in f]

# if code == 0:
#     result = kk(A)
# elif code == 1:
#     result = repeated_random(A)
# elif code == 2:
#     result = hill_climb(A)
# elif code == 3:
#     result = simulated_annealing(A)
# elif code == 11:
#     result = prepartitioned_repeated_random(A)
# elif code == 12:
#     result = hill_climb_prepartitioned(A)
# elif code == 13:
#     result = simulated_annealing_prepartitioned(A)

# print(result)