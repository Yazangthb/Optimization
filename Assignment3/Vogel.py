import numpy as np
import sys

max_val = sys.float_info.max

def display_parameter_table(supply_vector, cost_matrix, demand_vector):
    """
    Display the parameter table with supply vector, cost matrix, and demand vector.
    
    Args:
    supply_vector: Numpy array representing the supply for each source
    cost_matrix: 2D numpy array representing the cost of transportation between sources and destinations
    demand_vector: Numpy array representing the demand for each destination
    """
    # Print header
    header = 'Sources/Dest.\t'
    for j in range(len(demand_vector)):
        header += 'Dest.' + str(j + 1) + '\t'
    header += 'Supply'
    print(header)

    # Separator
    print("-" * 100)

    # Print cost matrix and supply vector
    for i in range(len(supply_vector)):
        source_line = 'Source ' + str(i + 1) + '\t'
        for j in range(len(demand_vector)):
            source_line += str(cost_matrix[i][j]) + '\t'
        source_line += str(supply_vector[i])
        print(source_line)

    print("-" * 100)

    # Print demand vector
    demand_line = "Demand" + "\t\t"
    for j in range(len(demand_vector)):
        demand_line += str(demand_vector[j]) + '\t'
    print(demand_line + "\n")


def display_allocation(allocation_matrix):
    """
    Display the allocation matrix.
    
    Args:
    allocation_matrix: 2D numpy array representing the allocation matrix
    """
    for row in allocation_matrix:
        print(row)

def calculate_row_diffs_and_col_diffs(cost_matrix):
    row_diffs = np.array([np.sort(row)[1] - np.sort(row)[0] for row in cost_matrix])
    col_diffs = np.array([np.sort(cost_matrix[:, col])[1] - np.sort(cost_matrix[:, col])[0] for col in range(cost_matrix.shape[1])])
    return row_diffs, col_diffs
    
def initialize_allocations(supply, demand):
    return np.zeros((len(supply), len(demand)), dtype=int)

def find_max_and_indices(arr):
    max_val = np.max(arr)
    indices = np.where(arr == max_val)[0]
    return max_val, indices

def allocate_goods(cost_matrix, supply, demand, allocations, ans):
    n, m = cost_matrix.shape
    while np.max(supply) != 0 or np.max(demand) != 0:
        row_diff, col_diff = calculate_row_diffs_and_col_diffs(cost_matrix)
        max_row_diff, max_row_indices = find_max_and_indices(row_diff)
        max_col_diff, max_col_indices = find_max_and_indices(col_diff)

        if max_row_diff >= max_col_diff:
            for ind in max_row_indices:
                ind2 = np.argmin(cost_matrix[ind])
                min_supply_demand = min(supply[ind], demand[ind2])
                ans += min_supply_demand * cost_matrix[ind, ind2]
                allocations[ind, ind2] = min_supply_demand
                supply[ind] -= min_supply_demand
                demand[ind2] -= min_supply_demand
                if demand[ind2] == 0:
                    cost_matrix[:, ind2] = max_val
                else:
                    cost_matrix[ind, :] = max_val
        else:
            for ind in max_col_indices:
                min_cost = max_val
                for j in range(n):
                    min_cost = min(min_cost, cost_matrix[j, ind])
                ind2 = np.argmin(cost_matrix[:, ind])
                min_supply_demand = min(supply[ind2], demand[ind])
                ans += min_supply_demand * min_cost
                allocations[ind2, ind] = min_supply_demand
                supply[ind2] -= min_supply_demand
                demand[ind] -= min_supply_demand
                if demand[ind] == 0:
                    cost_matrix[:, ind] = max_val
                else:
                    cost_matrix[ind2, :] = max_val
    return allocations, ans


if __name__ == "__main__":
    supply_vector = np.array([float(x) for x in input("Enter the supply vector (S): ").split()])
    if len(supply_vector) != 3:
        print("Wrong input!")
        print("The size of supply must be 3")
        exit(1)

    if not np.all(supply_vector >= 0):
        print("The method is not applicable!")
        print("All elements in supply must be >= 0.")
        exit(2)

    print("Enter the cost matrix (C):")
    cost_matrix = np.array([[float(x) for x in input().split()] for _ in range(3)])

    if not np.all(cost_matrix > 0):
        print("The method is not applicable!")
        print("All elements in cost must be > 0.")
        exit(3)

    if not cost_matrix.shape == (3, 4):
        print("Wrong input!")
        print("Wrong cost shape (should be (3,4))")
        exit(4)

    demand_vector = np.array([float(x) for x in input("Enter the demand vector (D): ").split()])
    if len(demand_vector) != 4:
        print("Wrong input!")
        print("Wrong length of demand (should be equal to 4)")
        exit(5)

    if not np.all(demand_vector >= 0):
        print("The method is not applicable!")
        print("All elements in the demand vector must be >= zero.")
        exit(6)

    display_parameter_table(supply_vector, cost_matrix, demand_vector)
    if np.sum(supply_vector) != np.sum(demand_vector):
        print("The problem is not balanced!")
        exit(7)

    # Initialize the allocations matrix
    allocations = initialize_allocations(supply_vector, demand_vector)
    total_cost = 0

    # Call the allocation function
    allocations, total_cost = allocate_goods(cost_matrix, supply_vector, demand_vector, allocations, total_cost)
    print("Basic Feasible Solution:", total_cost)
    display_allocation(allocations)
