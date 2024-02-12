def create_ldpc_matrix(symbol_nodes, check_nodes, s_node_degrees):
    # Initialize an empty parity check matrix
    parity_check_matrix = [[0] * symbol_nodes for _ in range(check_nodes)]
    print("Initial Parity Check Matrix:")
    print_matrix(parity_check_matrix)

    # Iterate over each symbol node
    for symbol_node in range(symbol_nodes):
        print(f"\nProcessing Symbol Node S{symbol_node}:")

        # Initialize a list to keep track of covered check nodes
        covered_check_nodes = []

        # Iterate over the degree of the current symbol node
        for edge_number in range(1, s_node_degrees[symbol_node] + 1):
            print(f"Processing edge {edge_number}:")
            # If it's the first edge of the symbol node
            if len(covered_check_nodes) == 0:
                # Find the check node with the least number of edges
                check_node = find_check_node_with_lowest_degree(parity_check_matrix)
                # Connect the symbol node to the check node
                parity_check_matrix[check_node][symbol_node] = 1
                covered_check_nodes.append(check_node)
            else:
                # Check if there are nodes not covered by the subgraph expanded from the current symbol node
                if len(covered_check_nodes) < check_nodes:
                    uncovered_check_nodes = list(set(range(check_nodes)) - set(covered_check_nodes))
                    # Find the check node with the lowest degree among the uncovered nodes
                    check_node = find_check_node_with_lowest_degree(parity_check_matrix, uncovered_check_nodes)
                else:
                    # Find the check node with the lowest degree among the farthest nodes
                    check_node = find_check_node_with_lowest_degree(parity_check_matrix, covered_check_nodes)
                # Connect the symbol node to the check node
                parity_check_matrix[check_node][symbol_node] = 1
                covered_check_nodes.append(check_node)

            # Print the current Parity Check Matrix
            print(f"Parity Check Matrix after processing edge {edge_number}:")
            print_matrix(parity_check_matrix)

    return parity_check_matrix


def find_check_node_with_lowest_degree(matrix, nodes=None):
    # If nodes are provided, consider only those nodes
    if nodes:
        min_degree = float('inf')
        min_degree_node = None
        for node in nodes:
            degree = sum(row[node] for row in matrix)
            if degree < min_degree:
                min_degree = degree
                min_degree_node = node
        return min_degree_node
    else:
        # Find the check node with the lowest degree
        min_degree = min(sum(row) for row in matrix)
        for node, row in enumerate(matrix):
            if sum(row) == min_degree:
                return node


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))


def main():
    # Get user input for symbol nodes, check nodes, and S-node degrees
    symbol_nodes = int(input("Enter the number of symbol nodes: "))
    check_nodes = int(input("Enter the number of check nodes: "))
    s_node_degrees = list(map(int, input("Enter the S-node degrees (comma separated): ").split(',')))

    # Create the LDPC parity check matrix
    ldpc_matrix = create_ldpc_matrix(symbol_nodes, check_nodes, s_node_degrees)

    # Print the final LDPC parity check matrix
    print("\nFinal LDPC Parity Check Matrix:")
    print_matrix(ldpc_matrix)


if __name__ == "__main__":
    main()
