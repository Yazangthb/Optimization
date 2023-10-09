import numpy as np
from fractions import Fraction  # so that numbers are not displayed in decimal.

def print_table():
    for row in table:
        for el in row:
            print(Fraction(str(el)).limit_denominator(100), end='\t')
        print()
    print()


def calculate_relative_profits():
    global rel_prof
    rel_prof = []
    for i in range(len(A[0])):
        rel_prof.append(c[i] - np.sum(table[:, 1] * table[:, 3 + i]))
    return rel_prof


def check_for_alternate_solution():
    global alternate
    b_var = table[:, 0]
    for i in range(len(A[0])):
        present = 0
        for j in range(len(b_var)):
            if int(b_var[j]) == i:
                present = 1
                break
        if present == 0:
            if rel_prof[i] == 0:
                alternate = 1
                print("Case of Alternate found")


def perform_min_ratio_test():
    global r
    min = 99999
    r = -1
    for i in range(len(table)):
        if table[:, 2][i] > 0 and table[:, 3 + k][i] > 0:
            val = table[:, 2][i] / table[:, 3 + k][i]
            if val < min:
                min = val
                r = i  # leaving variable
    return r


def perform_row_operations():
    global pivot
    pivot = table[r][3 + k]
    table[r, 2:len(table[0])] = table[r, 2:len(table[0])] / pivot
    for i in range(len(table)):
        if i != r:
            table[i, 2:len(table[0])] = table[i, 2:len(table[0])] - table[i][3 + k] * table[r, 2:len(table[0])]


if __name__ == '__main__':

    print("\n\t\t\t\t ****Simplex Algorithm ****\n\n")

    # Input the number of constraints, decision variables, and whether it's a minimization or maximization problem
    num_constraints = int(input("Enter the number of constraints: "))
    num_variables = int(input("Enter the number of decision variables: "))
    problem_type = input("Is this a minimization (min) or maximization (max) problem? ")

    # Initialize the A matrix (coefficients of constraints)
    A = []
    for i in range(num_constraints):
        constraint_coefficients = list(map(float, input(f"Enter coefficients for constraint {i + 1} separated by spaces: ").split()))
        A.append(constraint_coefficients)

    A = np.array(A)

    # Input the b matrix (amounts of resources)
    b = list(map(float, input("Enter the amounts of resources separated by spaces: ").split()))
    b = np.array(b)

    # Input the c matrix (coefficients of the objective function)
    c = list(map(float, input("Enter coefficients of the objective function separated by spaces: ").split()))
    c = np.array(c)

    # Initialize B (basic variables that make an identity matrix)
    B = np.arange(num_constraints, num_constraints + num_variables)
    cb = c[B]

    xb = np.transpose([b])
    table = np.hstack((B.reshape(-1, 1), cb.reshape(-1, 1), xb))
    table = np.hstack((table, A))
    table = np.array(table, dtype='float')

    MIN = 1 if problem_type.lower() == "min" else 0

    print("Simplex Working....\n")

    # when optimality reached it will be made 1
    reached = 0
    itr = 1
    unbounded = 0
    alternate = 0

    while reached == 0:

        print("Iteration: ", end=' ')
        print(itr)
        print("B \tCB \tXB \ty1 \ty2 \ty3 \ty4")
        print_table()

        # calculate Relative profits-> cj - zj for non-basics
        i = 0
        rel_prof = calculate_relative_profits()

        print("rel profit: ", end=" ")
        for profit in rel_prof:
            print(Fraction(str(profit)).limit_denominator(100), end=", ")
        print()
        i = 0

        # checking for alternate solution
        check_for_alternate_solution()

        print()
        flag = 0
        for profit in rel_prof:
            if profit > 0:
                flag = 1
                break
        # if all relative profits <= 0
        if flag == 0:
            print("All profits are <= 0, optimality reached")
            reached = 1
            break

        # kth var will enter the basis
        k = rel_prof.index(max(rel_prof))
        r = perform_min_ratio_test()

        # if no min ratio test was performed
        if r == -1:
            unbounded = 1
            print("Case of Unbounded")
            break

        print("pivot element index:", end=' ')
        print(np.array([r, 3 + k]))

        pivot = table[r][3 + k]
        print("pivot element: ", end=" ")
        print(Fraction(pivot).limit_denominator(100))

        # perform row operations
        # divide the pivot row with the pivot element
        table[r, 2:len(table[0])] = table[
                                    r, 2:len(table[0])] / pivot

        # do row operation on other rows
        for i in range(len(table)):
            if i != r:
                table[i, 2:len(table[0])] = table[i, 2:len(table[0])] - table[i][3 + k] * table[r, 2:len(table[0])]

        # assign the new basic variable
        table[r][0] = k
        table[r][1] = c[k]
        itr += 1

    print('\n\n')
    

    print()

    print("***************************************************************")
    if unbounded == 1:
        print("UNBOUNDED LPP")
        exit()
    if alternate == 1:
        print("ALTERNATE Solution")

    print("optimal table:")
    print("B \tCB \tXB \ty1 \ty2 \ty3 \ty4")
    print_table()

    print("value of Z at optimality: ", end=" ")

    basis = []
    i = 0
    sum = 0
    while i < len(table):
        sum += c[int(table[i][0])] * table[i][2]
        temp = "x" + str(int(table[i][0]) + 1)
        basis.append(temp)
        i += 1
    # if MIN problem make z negative
    if MIN == 1:
        print(-Fraction(str(sum)).limit_denominator(100))
    else:
        print(Fraction(str(sum)).limit_denominator(100))
    print("Final Basis: ", end=" ")
    print(basis)

    print("Values of Final Basis:", end=" ")
    print("[", end=" ")
    for i in range(len(table)):
        print(f'{Fraction(str(table[i][2])).limit_denominator(100)}', end=", ")
    print("]")

    print("Simplex Finished...")
    print()
