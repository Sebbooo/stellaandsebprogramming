import numpy as np

threshold = 3

def bad_mult(A, B):
    n = A.shape[0]
    C = np.zeros((n, n), dtype=A.dtype)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i, j] += A[i, k] * B[k, j]
    return C


def mult(A, B, ni=64):
    n = A.shape[0]
    
    if n <= ni:
        return A @ B

    pad = n % 2
    if pad:
        A = np.pad(A, ((0, 1), (0, 1)), mode='constant')
        B = np.pad(B, ((0, 1), (0, 1)), mode='constant')
        n += 1

    mid = n / 2
    A11, A12 = A[:mid, :mid], A[:mid, mid:]
    A21, A22 = A[mid:, :mid], A[mid:, mid:]
    B11, B12 = B[:mid, :mid], B[:mid, mid:]
    B21, B22 = B[mid:, :mid], B[mid:, mid:]

    M1 = mult(A11 + A22, B11 + B22, ni)
    M2 = mult(A21 + A22, B11, ni)
    M3 = mult(A11, B12 - B22, ni)
    M4 = mult(A22, B21 - B11, ni)
    M5 = mult(A11 + A12, B22, ni)
    M6 = mult(A21 - A11, B11 + B12, ni)
    M7 = mult(A12 - A22, B21 + B22, ni)

    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    top = np.hstack((C11, C12))
    bottom = np.hstack((C21, C22))
    C = np.vstack((top, bottom))

    if pad:
        C = C[:n - 1, :n - 1]

    return C


A = np.random.randint(0, 10, (9, 9))
B = np.random.randint(0, 10, (9, 9))

C = mult(A, B)
print("A @ B using Strassen:\n", C)

print("A @ B using numpy:\n", A @ B)
