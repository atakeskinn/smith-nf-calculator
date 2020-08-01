from sympy import *
import math

init_printing(use_unicode=True, wrap_line=False)

n = 0
m = 0
z = 0

A = []
T = []
S = []
B = []

def read_A():
    global S, A, T, n, m
    while True:
        try:
            n = int(input("Enter matrix dimension (n):"))
            m = int(input("Enter matrix dimension (m):"))
            break
        except ValueError:
            pass

    A = Matrix(n, m, readEntry)

    T = eye(m)

    S = eye(n)
    
    return

def readEntry(i, j):
    while True:
        try:
            return int(input("Enter entry (" + str(i + 1) + ", " + str(j + 1) + "):"))
        except ValueError:
            pass

def smith_nf(A):
    global S, B, T, n, m, z
    B = A.copy()
    if B.equals(zeros(n, m)):
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
    global S, B, T, n, m, z
    retry = True
    while retry:
        retry = False
        for i in range(z, n):
            for j in range(z, m):
                if (B[i, j] == B[z, z]):
                    continue
                if not (B[i, j] % B[z, z] == 0):
                    B = add_to_row(B, z, B.row(i))
                    S = add_to_row(S, z, S.row(i))
                    retry = True
                    
                    print("Entry at ("
                          + str(i + 1)
                          + ", " + str(j + 1)
                          + ") is not divisible by the invariant factor at ("
                          + str(z + 1)
                          + ", " + str(z + 1)
                          + ")")
                    print("Added row "
                      + str(z + 1)
                      + " to row "
                      + str(i + 1))
                    
                    divide_and_rest()
    return

def add_to_row(A, i, R):
    A = A.copy()
    R += A.row(i)
    A.row_del(i)
    A = A.row_insert(i, R)
    return A

def add_to_col(A, i, C):
    A = A.copy()
    C += A.col(i)
    A.col_del(i)
    A = A.col_insert(i, C)
    return A

def set_col(A, i, C):
    A = A.copy()
    A.col_del(i)
    A = A.col_insert(i, C)
    return A

def set_row(A, i, R):
    A = A.copy()
    A.row_del(i)
    A = A.row_insert(i, R)
    return A

def swap_rows(A, i1, i2):
    A = A.copy()
    R1 = A.row(i1)
    R2 = A.row(i2)
    
    A.row_del(i1)
    A = A.row_insert(i1, R2)
    
    A.row_del(i2)
    A = A.row_insert(i2, R1)
    
    return A

def swap_cols(A, i1, i2):
    A = A.copy()
    C1 = A.col(i1)
    C2 = A.col(i2)
    
    A.col_del(i1)
    A = A.col_insert(i1, C2)
    
    A.col_del(i2)
    A = A.col_insert(i2, C1)
    
    return A
                    

def divide_and_rest():
    global S, B, T, n, m, z
    
    j = z + 1    
    while j < max(n, m):
        if(B[z, z] == 0):
            continue

        if(j < m):
            q = math.floor(B[z, j] / B[z, z])
            B = add_to_col(B, j, -q * B.col(z))
            T = add_to_col(T, j, -q * T.col(z))

            if q != 0:
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

            if not B[z, j] == 0:
                j = z + 1
                min_to_first()
                continue

        if(j < n):
            
            q = math.floor(B[j, z] / B[z, z])
            B = add_to_row(B, j, -q * B.row(z))
            S = add_to_row(S, j, -q * S.row(z))

            if q != 0:
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
            
            if not B[j, z] == 0:
                j = z + 1
                min_to_first()
                continue

        j += 1
                
                
def min_to_first():
    global S, B, T, n, m, z
    #find min:
    mm = None
    i_sel = z
    j_sel = z
    for i in range(z, n):
        for j in range(z, m):
            if (not abs(B[i, j]) == 0):
                if (mm == None) or (abs(B[i, j]) <= mm):
                    i_sel = i
                    j_sel = j
                    mm = abs(B[i, j])
                    
    #swap first row with i-th row:
    B = swap_rows(B, z, i_sel)
    S = swap_rows(S, z, i_sel)
    
    #swap first column with j-th column:
    B = swap_cols(B, z, j_sel)
    T = swap_cols(T, z, j_sel)
    
    if not z == i_sel:
        print("Swapped rows: " + str(z + 1) + " and " + str(i_sel + 1))
    if not z == j_sel:
        print("Swapped columns: " + str(z + 1) + " and " + str(j_sel + 1))
    if not (z == j_sel and z == i_sel):
        print_full(B, S, T)

    #normalize if < 0
    if B[z, z] < 0:
        B = set_row(B, z, -B.row(z))
        S = set_row(S, z, -S.row(z))
        print("Multiplied row " + str(z + 1) + " by -1")
        print_full(B, S, T)

def check_validity():
    global S, A, T, B
    if(S * A * T).equals(B):
        return True

def print_full(B, S, T):
    print("----------------------------")
    pprint(B.col_insert(m, Matrix(n, 1, lambda i,j : symbols('||')).col_insert(m + 1, S)))

    pprint(T)
    print("----------------------------")

read_A()
smith_nf(A)
print("----------------------------")
print("S = ")
pprint(S)
print("A = ")
pprint(A)
print("T = ")
pprint(T)
print("B = ")
pprint(B)
print("S*A*T = B")
