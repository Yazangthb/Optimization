import numpy as np
from fractions import Fraction  # so that numbers are not displayed in decimal.


# def print_table():
#     for row in table:
#         for el in row:
#             print(Fraction(str(el)).limit_denominator(100000), end='\t')
#         print()
#     print()


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
                # print("Case of Alternate found")


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

def add_identity_matrix(A):
    num_constraints = len(A)
    identity_matrix = np.eye(num_constraints)
    A_with_identity = np.hstack((A, identity_matrix))
    return A_with_identity

def initialize_simplex():
    global table, A, c, b, MIN

    problem_type = input("Is this a minimization (min) or maximization (max) problem? ")

    # Input the coefficients of the objective function as a list
    c_list = list(map(int, input("Enter the coefficients of the objective function separated by spaces: ").split()))

    # Input the number of constraints
    num_constraints = int(input("Enter the number of constraints: "))

    # Initialize the A matrix with zeros
    A = np.zeros((num_constraints, len(c_list)))

    # Input the constraint coefficients without slack variables
    print(f"Enter the coefficients of the {num_constraints} constraints (without slack variables): ")
    for i in range(num_constraints):
        A[i] = list(map(int, input().split()))

    # Input the resources as a list
    b_list = list(map(int, input("Enter the resources separated by spaces: ").split()))

    # Create NumPy arrays c and b
    c = np.array(c_list + [0] * num_constraints)
    b = np.array(b_list)

    MIN = 1 if problem_type.lower() == "min" else 0

    if MIN == 1:
      c = -1 * c

    # Add the identity matrix to A
    A = add_identity_matrix(A)

    # Combine matrices B, cb, and xb to form the initial table
    B = np.arange(num_constraints) + len(c_list)  # Basic variables
    cb = np.array(c[-num_constraints:])  # Coefficients of basic variables in Z
    xb = np.transpose([b])  # Resources
    table = np.column_stack((B, cb, xb, A))

    # Change the type of the table to float
    table = np.array(table, dtype='float')
    return len(A[0])


if __name__ == '__main__':


    A0_len = initialize_simplex()


    # when optimality reached it will be made 1
    reached = 0
    itr = 1
    unbounded = 0
    alternate = 0

    while reached == 0:

        # print("Iteration: ", end=' ')
        # print(itr)
        # print("B \tCB \tXB \ty1 \ty2 \ty3 \ty4")
        # print_table()

        # calculate Relative profits-> cj - zj for non-basics
        i = 0
        rel_prof = calculate_relative_profits()

        # print("rel profit: ", end=" ")
        # for profit in rel_prof:
        #     print(Fraction(str(profit)).limit_denominator(100000), end=", ")
        # print()
        i = 0

        # checking for alternate solution
        check_for_alternate_solution()

        # print()
        flag = 0
        for profit in rel_prof:
            if profit > 0:
                flag = 1
                break
        # if all relative profits <= 0
        if flag == 0:
            # print("All profits are <= 0, optimality reached")
            reached = 1
            break

        # kth var will enter the basis
        k = rel_prof.index(max(rel_prof))
        r = perform_min_ratio_test()

        # if no min ratio test was performed
        if r == -1:
            unbounded = 1
            break

        # print("pivot element index:", end=' ')
        # print(np.array([r, 3 + k]))

        pivot = table[r][3 + k]
        # print("pivot element: ", end=" ")
        # print(Fraction(pivot).limit_denominator(100000))

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

    # print('\n\n')

    if unbounded == 1:
        print("The method is not applicable!")
    else:
        # print("***************************************************************")
        if alternate == 1:
            pass
            # print("ALTERNATE Solution")

        # print("optimal table:")
        # print("B \tCB \tXB \ty1 \ty2 \ty3 \ty4")
        # for row in table:
        #     for el in row:
        #         print(Fraction(str(el)).limit_denominator(100000), end='\t')
        #     print()
        # print()

        print("value of Z at optimality: ", end=" ")

        basis = []
        i = 0
        sum = 0
        used_num =[]
        while i < len(table):
            sum += c[int(table[i][0])] * table[i][2]
            temp = "x" + str(int(table[i][0]) + 1)
            used_num.append(int(table[i][0]) + 1)
            basis.append(temp)
            i += 1
        i=1
        while i<= A0_len:
            if i in used_num:
                pass
            else:
                tmp = "x" + str(i)
                basis.append(tmp)
            i+=1
        # if MIN problem make z negative
        if MIN == 1:
            print(-Fraction(str(sum)).limit_denominator(100000))
        else:
            print(Fraction(str(sum)).limit_denominator(100000))
        print("Final Basis: ", end=" ")
        print(basis)

        print("Values of Final Basis:", end=" ")
        print("[", end=" ")
        print_str=""
        for i in range(A0_len):
            if i < len(table) - 1:
                print_str += str(Fraction(str(table[i][2])).limit_denominator(100000))
                print_str += ", "
            elif i == len(table)-1:
                print_str += str(Fraction(str(table[i][2])).limit_denominator(100000))
                print_str += ","
            else:
                print_str += " 0,"

        print(print_str[:-1],end="")
        print(" ]")
