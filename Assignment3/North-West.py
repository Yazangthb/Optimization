import numpy as np

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


def northwest_corner_allocation(cost_matrix, supply_vector, demand_vector):
    """
    Perform Northwest Corner method for initial allocation in the transportation problem.
    
    Args:
    cost_matrix: 2D numpy array representing the cost of transportation between sources and destinations
    supply_vector: Numpy array representing the supply for each source
    demand_vector: Numpy array representing the demand for each destination
    
    Returns:
    allocation_matrix: 2D numpy array representing the initial allocation matrix based on Northwest Corner method
    """
    num_suppliers = len(supply_vector)
    num_consumers = len(demand_vector)

    allocation_matrix = np.zeros((num_suppliers, num_consumers))

    i, j = 0, 0

    # Iterate through all suppliers and consumers
    while i < num_suppliers and j < num_consumers:
        quantity = min(supply_vector[i], demand_vector[j])

        allocation_matrix[i][j] = quantity

        supply_vector[i] -= quantity
        demand_vector[j] -= quantity

        if supply_vector[i] == 0:
            i += 1
        else:
            j += 1

    return allocation_matrix


def display_allocation(allocation_matrix):
    """
    Display the allocation matrix.
    
    Args:
    allocation_matrix: 2D numpy array representing the allocation matrix
    """
    for row in allocation_matrix:
        print(row)


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

    allocation = northwest_corner_allocation(cost_matrix, supply_vector, demand_vector)

    print("Initial Basic Feasible Solution:")
    display_parameter_table(supply_vector, allocation, demand_vector)
    display_allocation(allocation)