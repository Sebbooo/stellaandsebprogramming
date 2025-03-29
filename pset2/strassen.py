import numpy as np
import sys

threshold = 3

def bad(A, B):
    n = A.shape[0]
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i, j]+=A[i, k]*B[k, j]
    return C


def mult(A, B, ni=64):
    n = A.shape[0]
    
    if n<=ni:
        return bad(A, B)

    if n%2:
        A = np.pad(A, ((0, 1), (0, 1)), mode='constant')
        B = np.pad(B, ((0, 1), (0, 1)), mode='constant')
        n += 1

    # Copy paste laecture
    mid = n/2
    A = A[:mid, :mid]
    B = A[:mid, mid:]
    C = A[mid:, :mid]
    D = A[mid:, mid:]

    E = B[:mid, :mid]
    F = B[:mid, mid:]
    G = B[mid:, :mid]
    H = B[mid:, mid:]

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

    if n % 2:
        C = C[:n - 1, :n - 1]

    return C

d = int(sys.argv[2])

with open(sys.argv[3], 'r') as f:
    numbers = [int(line.strip()) for line in f]

A = np.array(numbers[:d*d]).reshape((d, d))
B = np.array(numbers[d*d:]).reshape((d, d))

C = mult(A, B)

for i in range(d):
    print(C[i, i])
