import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# How to represent graph
# Use adjacency lists, somehow encode the weight function as well?

# Binary Min Heap

class Heap:
    # TBD, I think just start empty
    def __init__(self):
        self.heap = []

    # Idea: We have a binary tree, and to keep it balanced, we insert at the last position, and trace down that branch
    def insert(self, elem):
        curr_elem = elem
        # list will grow to this insertion point
        insert_pos = len(self.heap)
        max_length = len(bin(insert_pos+1)[2:])

        for i in range(1,max_length):
            curr_ind = ((insert_pos+1)>>(max_length-i))-1
            if curr_elem < self.heap[curr_ind]:
                temp = self.heap[curr_ind]
                self.heap[curr_ind] = curr_elem
                curr_elem = temp

        self.heap.append(curr_elem)

    def print_heap(self):
        print(self.heap)
    # Update an elem (could be delete, tbd)
    # by usage, this will always be smaller, so we just bubble up
    def update(self, index, value):
        self.heap[index] = value
        curr_pos = index+1
        while not curr_pos == 1 and self.heap[curr_pos-1] < self.heap[(curr_pos>>1)-1]:
            temp = self.heap[curr_pos-1]
            self.heap[curr_pos-1] = self.heap[(curr_pos>>1)-1]
            self.heap[(curr_pos>>1)-1] = temp
            curr_pos = curr_pos >> 1
    # Return and Remove smallest
    def pop(self):
        if not self.heap:
            return
        if len(self.heap) == 1:
            return self.heap.pop()
        yoink = self.heap[0]
        self.heap[0] = self.heap.pop()
        curr_ind = 1

        while (curr_ind<<1) <= len(self.heap) and (self.heap[curr_ind-1] > self.heap[(curr_ind<<1)-1] or ((curr_ind<<1) < len(self.heap) and self.heap[curr_ind-1] > self.heap[(curr_ind<<1)])):
            if (curr_ind<<1) < len(self.heap) and self.heap[(curr_ind<<1)] < self.heap[(curr_ind<<1) - 1]:
                temp = self.heap[curr_ind-1]
                self.heap[curr_ind - 1] = self.heap[(curr_ind<<1)]
                self.heap[(curr_ind<<1)] = temp
                curr_ind = (curr_ind<<1) + 1
            else:
                temp = self.heap[curr_ind-1]
                self.heap[curr_ind-1] = self.heap[(curr_ind<<1) - 1]
                self.heap[(curr_ind<<1) - 1] = temp
                curr_ind = curr_ind<<1

        return yoink

# Gives type of random num, d is dimension
def rand_num(d):
    sum = 0
    for i in range(d):
        sum += (random.random()) **2
    return sum ** .5

# n is number of vertices, d is dim random
def complete_graph(n, d):
    mst_value = 0
    vertices = Heap()
    # WLOG vertex 1 is start, then 2-n
    # could drop min
    min = d
    for i in range(2,n+1):
        vertices.insert(rand_num(d))

    # Added 1 edge
    mst_value += vertices.pop()

    it=1
    while vertices.heap:
        for i in range(len(vertices.heap)):
            # Add new edge, only relevent if better than before
            new_edge = rand_num(d)
            if new_edge < vertices.heap[i]:
                vertices.update(i,new_edge)

        mst_value += vertices.pop()
        if it%100==0:
            print("Thing: ",it)
        it+=1

    return mst_value

class Heap2:
    # TBD, I think just start empty
    def __init__(self):
        self.heap = []

    # Idea: We have a binary tree, and to keep it balanced, we insert at the last position, and trace down that branch
    def insert(self, elem):
        curr_elem = elem
        # list will grow to this insertion point
        insert_pos = len(self.heap)
        max_length = len(bin(insert_pos+1)[2:])

        for i in range(1, max_length):
            curr_ind = ((insert_pos+1) >> (max_length-i)) - 1
            if curr_elem[0] < self.heap[curr_ind][0]:  # Compare by weight
                temp = self.heap[curr_ind]
                self.heap[curr_ind] = curr_elem
                curr_elem = temp

        self.heap.append(curr_elem)

    def print_heap(self):
        print(self.heap)

    # Update an elem (could be delete, tbd)
    # by usage, this will always be smaller, so we just bubble up
    def update(self, index, value):
        self.heap[index] = value
        curr_pos = index + 1
        while not curr_pos == 1 and self.heap[curr_pos - 1][0] < self.heap[(curr_pos >> 1) - 1][0]:  # Compare by weight
            temp = self.heap[curr_pos - 1]
            self.heap[curr_pos - 1] = self.heap[(curr_pos >> 1) - 1]
            self.heap[(curr_pos >> 1) - 1] = temp
            curr_pos = curr_pos >> 1

    # Return and Remove smallest
    def pop(self):
        if not self.heap:
            return
        if len(self.heap) == 1:
            return self.heap.pop()
        yoink = self.heap[0]
        self.heap[0] = self.heap.pop()
        curr_ind = 1

        while (curr_ind << 1) <= len(self.heap) and (self.heap[curr_ind - 1][0] > self.heap[(curr_ind << 1) - 1][0] or ((curr_ind << 1) < len(self.heap) and self.heap[curr_ind - 1][0] > self.heap[(curr_ind << 1)][0])):  # Compare by weight
            if (curr_ind << 1) < len(self.heap) and self.heap[(curr_ind << 1)][0] < self.heap[(curr_ind << 1) - 1][0]:
                temp = self.heap[curr_ind - 1]
                self.heap[curr_ind - 1] = self.heap[(curr_ind << 1)]
                self.heap[(curr_ind << 1)] = temp
                curr_ind = (curr_ind << 1) + 1
            else:
                temp = self.heap[curr_ind - 1]
                self.heap[curr_ind - 1] = self.heap[(curr_ind << 1) - 1]
                self.heap[(curr_ind << 1) - 1] = temp
                curr_ind = curr_ind << 1

        return yoink


def generate_hypercube_graph(n):
    # represent the graph using adjacency lists
    graph = {i: [] for i in range(n)}

    # add edges with weights given condition
    for i in range(n):
        for j in range(i+1, n):
            # check if j-i > 0 is a power of 2, avoid adding inconsistent weights
            if (j-i & (j-i - 1)) == 0:
                weight = random.uniform(0, 1)
                graph[i].append((j, weight))
                graph[j].append((i, weight))

    return graph

def prim_algo(graph):
    start_node = 0 # assume WLOG
    mst_edges = []  # store mst edges
    visited = set([start_node]) # the X set
    min_heap = Heap2()
    mst_val = 0

    # add edges of the starting node to the heap
    for neighbor, weight in graph[start_node]:
        min_heap.insert((weight, start_node, neighbor))

    while min_heap and len(visited) < len(graph):
        weight, u, v = min_heap.pop()
        if v not in visited:
            visited.add(v)
            mst_val += weight
            mst_edges.append((u, v, weight))

            for neighbor, weight in graph[v]:
                if neighbor not in visited:
                    min_heap.insert((weight, v, neighbor))

    return mst_val
                
                

# Testing for hypercube
n_values_hyper = [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144]

num_trials_hyper = 5
data_hyper = []
for n in n_values_hyper:
        print("STARTING N=",n)
        for trial in range(1, num_trials_hyper + 1):
            mst_weight = prim_algo(generate_hypercube_graph(n))
            data_hyper.append({'n': n,  'trial': trial, 'MST': mst_weight})

# Create DataFrame
df_hyper = pd.DataFrame(data_hyper)

# Print DataFrame
print(df_hyper)

# Plot results
plt.figure(figsize=(10, 6))

# Plot each trial
for trial in range(1, num_trials_hyper + 1):
    trial_data_hyper = df_hyper[df_hyper['trial'] == trial]
    plt.plot(trial_data_hyper['n'], trial_data_hyper['MST'], linestyle='-', color='gray', alpha=0.3)

# Plot the average
avg_mst = df_hyper.groupby('n')['MST'].mean()
plt.plot(n_values_hyper, avg_mst, linestyle='-', color='black', label=f'(avg)')

# Labels and title
plt.xscale('log', base=2)
plt.xlabel('number of vertices')
plt.ylabel('Minimum Spanning Tree (MST) Weight')
plt.title('MST Weight vs. n Vertices Hypercube Graph')
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)


# Show plot
plt.show()

# Implement testing area
n_values = [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]
d_values = [1, 2, 3]
num_trials = 5

# Collect data
data = []
for d in d_values:
    print("STARTING D=",d)
    for n in n_values:
        print("STARTING N=",n)
        for trial in range(1, num_trials + 1):
            mst_weight = complete_graph(n, d)
            data.append({'n': n, 'd': d, 'trial': trial, 'MST': mst_weight})

# Create DataFrame
df = pd.DataFrame(data)

# Print DataFrame
print(df)

# Plot results
plt.figure(figsize=(10, 6))

for d in d_values:
    subset = df[df['d'] == d]
    
    # Plot each trial
    for trial in range(1, num_trials + 1):
        trial_data = subset[subset['trial'] == trial]
        plt.plot(trial_data['n'], trial_data['MST'], linestyle='-', color='gray', alpha=0.3)
    
    # Plot the average
    avg_mst = subset.groupby('n')['MST'].mean()
    plt.plot(n_values, avg_mst, linestyle='-', color='black', label=f'd={d} (avg)')

# Add the convergence line
plt.axhline(y=1.2, color='black', linestyle='dotted', label="y = 1.2")

# Labels and title
plt.xscale('log', base=2)
plt.xlabel('number of vertices')
plt.ylabel('Minimum Spanning Tree (MST) Weight')
plt.title('MST Weight vs. n-Complete Graphs for Different d Values')
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Show plot
plt.show()
