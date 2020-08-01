import numpy as np
import math

n = 2
m = 3

z = 0

A = np.array([[4, 1, 5], [3, 6, 4]])

T = np.zeros((m, m))

S = np.zeros((n, n))

for i in range(n):
    S[i][i] = 1
for j in range(m):
    T[j][j] = 1

B = np.zeros((n, m))

def read_A():
    global A, T, S, n, m
    while True:
        try:
            n = int(input("Enter matrix dimension (n):"))
            m = int(input("Enter matrix dimension (m):"))
            break
        except ValueError:
            pass

    A = np.zeros((n, m))

    T = np.zeros((m, m))

    S = np.zeros((n, n))
    
    for i in range(n):
        S[i][i] = 1
        for j in range(m):
            if i == 0:
                T[j][j] = 1
            while True:
                try:
                    A[i][j] = int(input("Enter entry (" + str(i + 1) + ", " + str(j + 1) + "):"))
                    break
                except ValueError:
                    pass
                    
                
    return

def smith_nf(A):
    global T, S, B, n, m, z
    B = A.copy()
    if np.array_equal(B, np.zeros((n, m))):
        return

    print_full(B, S, T)
    while (z < n) and (z < m):
        min_to_first()
        
        divide_and_rest()
        test_divisor_property()
        z += 1
    if check_validity():
        print("Smith-NF was calculated correctly.")
    else:
        print("Smith-NF could not be calculated.")

def test_divisor_property():
    global T, S, B, n, m, z
    for i in range(z, n):
            for j in range(z, m):
                if not (B[i][j] % B[z][z] == 0):
                    B[z] += B[i]
                    S[z] += S[i]
                    
                    z-=1
                    return

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
    mm = None
    i_sel = z
    j_sel = z
    for i in range(z, n):
        for j in range(z, m):
            if (not abs(B[i][j]) == 0):
                if (mm == None) or (abs(B[i][j]) <= mm):
                    i_sel = i
                    j_sel = j
                    mm = abs(B[i][j])
                    
    #swap first row with i-th row:
    B[[z, i_sel]] = B[[i_sel, z]]
    S[[z, i_sel]] = S[[i_sel, z]]
    
    #swap first column with j-th column:
    B[:, [z, j_sel]] = B[:, [j_sel, z]]
    T[:, [z, j_sel]] = T[:, [j_sel, z]]
    
    if not z == i_sel:
        print("Swapped rows: " + str(z + 1) + " and " + str(i_sel + 1))
    if not z == j_sel:
        print("Swapped columns: " + str(z + 1) + " and " + str(j_sel + 1))
    if not (z == j_sel and z == i_sel):
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

read_A()
smith_nf(A)
print("--------------")
print("S = ")
print(S.astype(int))
print("A = ")
print(A.astype(int))
print("T = ")
print(T.astype(int))
print("B = ")
print(B.astype(int))
print("S*A*T = B")
