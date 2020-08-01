import numpy as np
import math

n = 2
m = 3

z = 0

A = np.array([[2, 3, -1], [4, 9, -5]])

T = np.zeros((m, m))

S = np.zeros((n, n))

for i in range(n):
    S[i][i] = 1
for j in range(m):
    T[j][j] = 1

B = np.zeros((n, m))

def read_A():
    global A, T, S
    n = int(input("Enter matrix dimension (n):"))
    m = int(input("Enter matrix dimension (m):"))

    A = np.zeros((n, m))

    T = np.zeros((m, m))

    S = np.zeros((n, n))
    
    for i in range(n):
        S[i][i] = 1
        for j in range(m):
            if i == 0:
                T[j][j] = 1
            A[i][j] = input("Enter entry (" + str(i) + ", " + str(j) + "):")
    return

def smith_nf(A):
    global B, n, m, z
    B = A.copy()
    if np.array_equal(B, np.zeros((n, m))):
        return

    print_full(B, S, T)
    while (z < n) and (z < m):
        min_to_first()
        
        divide_and_rest()
        for i in range(z, n):
            for j in range(z, m):
                if not (B[i][j] % B[z][z] == 0):
                    B[z] += B[i]
                    S[z] += S[i]
                    divide_and_rest()
                    break
        z += 1
    if check_validity():
        print("Smith-NF was calculated correctly.")
    else:
        print("Smith-NF could not be calculated.")

def divide_and_rest():
    global S, T, B, m, n, z
    for j in range(z + 1, m):
        q = math.floor(B[z][j] / B[z][z])
        B[:, [j]] -= q * B[:, [z]]
        T[:, [j]] -= q * T[:, [z]]

        if q > 0:
            print("Subtracted column "
                  + str(z + 1)
                  + " from column "
                  + str(j + 1) + " a total of "
                  + str(q) + " times")
        else:
            print("Added column "
                  + str(z + 1)
                  + " to column "
                  + str(j + 1) + " a total of "
                  + str(-q) + " times")
            
        print_full(B, S, T)
        
        if not B[z][j] == 0:
            j = 1
            min_to_first()

    for j in range(z + 1, n):
        q = math.floor(B[j][z] / B[z][z])
        B[[j]] -= q * B[[z]]
        S[[j]] -= q * S[[z]]

        if q > 0:
            print("Subtracted row "
                  + str(z + 1)
                  + " from row "
                  + str(j + 1) + " a total of "
                  + str(q) + " times")
        else:
            print("Added row "
                  + str(z + 1)
                  + " to row "
                  + str(j + 1) + " a total of "
                  + str(-q) + " times")
        
        print_full(B, S, T)
        
        if not B[j][z] == 0:
            j = 1
            min_to_first()
        
def min_to_first():
    global S, T, B, n, m, z
    #find min:
    mm = abs(B[z][z])
    i_sel = z
    j_sel = z
    for i in range(z, n):
        for j in range(z, m):
            if abs(B[i][j]) < mm:
                i_sel = i
                j_sel = j
                mm = abs(B[i][j])
    #swap first row with i-th row:
    B[[z, i_sel]] = B[[i_sel, z]]
    S[[z, i_sel]] = S[[i_sel, z]]
    if not z == i_sel:
        print("Swapped rows: " + str(z) + " and " + str(i_sel))
    #swap first column with j-th column:
    B[:, [z, j_sel]] = B[:, [j_sel, z]]
    T[:, [z, j_sel]] = T[:, [j_sel, z]]
    if not z == j_sel:
        print("Swapped columns: " + str(z + 1) + " and " + str(j_sel + 1))
    print_full(B, S, T)

    #normalize if < 0
    if B[z][z] < 0:
        B[z] *= -1
        S[z] *= -1
        print("Multiplied row " + str(z + 1) + " by -1")
        print_full(B, S, T)

def check_validity():
    if(np.array_equal(S.dot(A).dot(T), B)):
        return True

def print_full(B, S, T):
    print("--------------")
    for i in range(n):
        print("[", end = " ")
        for j in range(m):
            print(str(int(B[i][j])), end = " ")
        print("][", end = " ")
        for j in range(n):
            print(str(int(S[i][j])), end = " ")
        print("]")
        
    for i in range(m):
        print("[", end = " ")
        for j in range(m):
            print(str(int(T[i][j])), end = " ")
        print("]")
    print("--------------")

#read_A()
smith_nf(A)
