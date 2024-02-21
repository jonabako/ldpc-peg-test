import numpy as np

def generate_ldpc_parity_check_matrix(n, m, dv, dc):
    """
    Generate a parity check matrix for a LDPC code with given parameters.
    
    Args:
    - n: Number of variable nodes (codeword length).
    - m: Number of check nodes.
    - dv: Variable node degree.
    - dc: Check node degree.
    
    Returns:
    - H: Parity check matrix.
    """
    # Initialize empty parity check matrix
    H = np.zeros((m, n), dtype=int)
    
    print("Intermediate Parity Check Matrices:")
    
    # Generate variable node connections
    for i in range(n):
        # Randomly select dv check nodes to connect to variable node i
        connected_check_nodes = np.random.choice(m, dv, replace=False)
        H[connected_check_nodes, i] = 1
        print("Step", i+1, ":")
        print_matrix_without_brackets(H)
        print()
    
    # Generate check node connections
    for j in range(m):
        # Randomly select dc variable nodes to connect to check node j
        connected_variable_nodes = np.random.choice(n, dc, replace=False)
        H[j, connected_variable_nodes] = 1
        print("Step", n+j+1, ":")
        print_matrix_without_brackets(H)
        print()
    
    return H

def print_matrix_without_brackets(matrix):
    """
    Print the matrix without brackets.
    
    Args:
    - matrix: Input matrix.
    """
    for row in matrix:
        print(*row)

# Take user input for parameters
n = int(input("Enter codeword length (n): "))
m = int(input("Enter number of check nodes (m): "))
dv = int(input("Enter variable node degree (dv): "))
dc = int(input("Enter check node degree (dc): "))

# Generate LDPC parity check matrix
H = generate_ldpc_parity_check_matrix(n, m, dv, dc)

print("Final Parity Check Matrix (H):")
print_matrix_without_brackets(H)
