import numpy as np

def select_node(nodes, max_degree):
    # Randomly select a node from the list of unconnected nodes
    # Ensure the selected node has not reached its maximum degree
    available_nodes = [node for node in nodes if len(tanner_graph[node]) < max_degree]
    if not available_nodes:
        return None
    return np.random.choice(available_nodes)

def add_edge(graph, node1, node2):
    # Add an edge between node1 and node2 in the graph
    graph[node1].append(node2)
    graph[node2].append(node1)

# Ask user for input
N = int(input("Enter the code length (N): "))
n = int(input("Enter the number of symbol nodes (n): "))
m = int(input("Enter the number of check nodes (m): "))
d_v = int(input("Enter the maximum symbol node degree (d_v): "))
d_c = int(input("Enter the maximum check node degree (d_c): "))

# Initialize empty Tanner graph
tanner_graph = {symbol_node: [] for symbol_node in range(n)}

# Create empty lists for unconnected nodes
unconnected_symbol_nodes = list(range(n))
unconnected_check_nodes = list(range(m))

# Counter for total edges added
total_edges_added = 0

# Step 1: Initialization
while total_edges_added < (N - n):
    # Step 2: Node Selection
    symbol_node = select_node(unconnected_symbol_nodes, d_v)
    if symbol_node is None:
        break
    
    # Step 3: Edge Addition
    check_node = select_node(unconnected_check_nodes, d_c)
    if check_node is None:
        break
    
    add_edge(tanner_graph, symbol_node, check_node)
    total_edges_added += 1

    # Step 4: Check Node Update
    if len(tanner_graph[check_node]) >= d_c:
        unconnected_check_nodes.remove(check_node)

# Generate Parity Check Matrix
parity_check_matrix = np.zeros((m, n), dtype=int)
for check_node in range(m):
    for symbol_node in tanner_graph[check_node]:
        parity_check_matrix[check_node, symbol_node] = 1

# Print Parity Check Matrix without brackets
print("\nGenerated Parity Check Matrix:")
for row in parity_check_matrix:
    print(*row, sep=' ')
