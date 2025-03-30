import numpy as np
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

#TESTING
# np.set_printoptions(threshold=np.inf, linewidth=np.inf)
# X = np.random.randint(0, 11, (17, 17))
# Y = np.random.randint(0, 11, (17, 17))

# print(mult(X, Y, ni=8))




d = int(sys.argv[2])

with open(sys.argv[3], 'r') as f:
    numbers = []
    for line in f:
        numbers.append(int(float(line.strip())))

A = np.array(numbers[:d*d]).reshape((d, d))
B = np.array(numbers[d*d:]).reshape((d, d))

C = mult(A, B)

for i in range(d):
    print(int(C[i, i]))
