import numpy as np
import matplotlib.pyplot as plt
import sys

threshold = 3

def bad(X, Y):
    n = X.shape[0]
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i, j]+=X[i, k]*Y[k, j]
    return C


def mult(X, Y, ni=16):
    n = X.shape[0]
    
    if n<=ni:
        return bad(X, Y)

    #I am actually such a moron for missing this
    changed = n%2
    if changed:
        X = np.pad(X, ((0, 1), (0, 1)), mode='constant')
        Y = np.pad(Y, ((0, 1), (0, 1)), mode='constant')
        n += 1

    mid = n//2
    A = X[:mid, :mid]
    B = X[:mid, mid:]
    C = X[mid:, :mid]
    D = X[mid:, mid:]

    E = Y[:mid, :mid]
    F = Y[:mid, mid:]
    G = Y[mid:, :mid]
    H = Y[mid:, mid:]

    P1 = mult(A + D, E + H, ni)
    P2 = mult(C + D, E, ni)
    P3 = mult(A, F - H, ni)
    P4 = mult(D, G - E, ni)
    P5 = mult(A + B, H, ni)
    P6 = mult(C - A, E + F, ni)
    P7 = mult(B - D, G + H, ni)

    C11 = P1 + P4 - P5 + P7
    C12 = P3 + P5
    C21 = P2 + P4
    C22 = P1 - P2 + P3 + P6

    
    top = np.hstack((C11, C12))
    bottom = np.hstack((C21, C22))
    C = np.vstack((top, bottom))

    if changed:
        C = C[:n - 1, :n - 1]

    return C

def generate_random_graph(n, p):
    """
    Generate a random graph with n vertices where each edge is included with probability p.
    
    Args:
        n: Number of vertices
        p: Probability of including an edge
        
    Returns:
        A: Adjacency matrix of the graph
    """
    # Generate a random matrix with values between 0 and 1
    R = np.random.random((n, n))
    
    # Create adjacency matrix where an edge exists if random value < p
    A = np.zeros((n, n))
    A[R < p] = 1
    
    # Make the matrix symmetric (undirected graph) and remove self-loops
    # We take upper triangular portion of matrix A
    A = np.triu(A, 1) + np.triu(A, 1).T
    
    return A

def count_triangles(A):
    """
    Count the number of triangles in a graph with adjacency matrix A using Strassen's algorithm.
    
    Args:
        A: Adjacency matrix of the graph
        
    Returns:
        Number of triangles in the graph
    """
    # Compute A^2 using Strassen's algorithm
    A_squared = mult(A, A)
    
    # Compute A^3 using Strassen's algorithm
    A_cubed = mult(A_squared, A)
    
    # The number of triangles is the sum of diagonal elements of A^3 divided by 6
    return np.trace(A_cubed) / 6

def main():
    n = 1024  # Number of vertices
    probabilities = [0.01, 0.02, 0.03, 0.04, 0.05]
    
    observed_triangles = []
    expected_triangles = []
    
    print(f"Generating random graphs and counting triangles for n = {n} vertices")
    
    for p in probabilities:
        print(f"\nProcessing graph with p = {p}")
        
        # Expected number of triangles: (n choose 3) * p^3 = n^3 * p^3 / 6
        expected = (n**3) * (p**3) / 6
        expected_triangles.append(expected)
        
        # Generate random graph and count triangles
        A = generate_random_graph(n, p)
        num_triangles = count_triangles(A)
        observed_triangles.append(num_triangles)
        
        print(f"  Observed triangles: {num_triangles:.2f}")
        print(f"  Expected triangles: {expected:.2f}")
        
        # Calculate percentage difference
        diff_percent = (num_triangles - expected) / expected * 100
        print(f"  Percentage difference: {diff_percent:.2f}%")
    
    # Create a chart showing the results
    plt.figure(figsize=(12, 8))
    
    # Plot observed vs expected triangles
    plt.subplot(2, 1, 1)
    plt.plot(probabilities, observed_triangles, 'o-', label='Observed')
    plt.plot(probabilities, expected_triangles, 's-', label='Expected')
    plt.xlabel('Edge Probability (p)')
    plt.ylabel('Number of Triangles')
    plt.title(f'Number of Triangles in Random Graphs (n={n})')
    plt.legend()
    plt.grid(True)
    
    # Plot percentage difference
    plt.subplot(2, 1, 2)
    percentage_diff = [(obs - exp) / exp * 100 for obs, exp in zip(observed_triangles, expected_triangles)]
    plt.bar(probabilities, percentage_diff)
    plt.xlabel('Edge Probability (p)')
    plt.ylabel('Percentage Difference (%)')
    plt.title('Percentage Difference Between Observed and Expected')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('triangle_counting_results.png')
    plt.show()
    
    # Print the results in a table
    print("\nResults Summary:")
    print("-----------------------------------------------------------------------")
    print("| Probability | Observed Triangles | Expected Triangles | Difference % |")
    print("-----------------------------------------------------------------------")
    for i, p in enumerate(probabilities):
        diff_percent = (observed_triangles[i] - expected_triangles[i]) / expected_triangles[i] * 100
        print(f"| {p:^11.2f} | {observed_triangles[i]:^18.2f} | {expected_triangles[i]:^18.2f} | {diff_percent:^12.2f} |")
    print("-----------------------------------------------------------------------")

main()