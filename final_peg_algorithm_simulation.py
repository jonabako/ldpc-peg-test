from builtins import enumerate, int, list, map, print, range
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def create_graph(n, m, s_node_degrees):
    # Create an empty graph
    graph = nx.Graph()

    # Create symbol nodes (s_type)
    s_nodes = ['s{}'.format(i) for i in range(n)]
    graph.add_nodes_from(s_nodes, node_type='s')

    # Create check nodes (c_type)
    c_nodes = ['c{}'.format(i) for i in range(m)]
    graph.add_nodes_from(c_nodes, node_type='c')

    # Initialize check node degrees
    c_degrees = [0] * m

    # PEG Algorithm for edge creation
    for s_i in s_nodes:
        for d_i in range(s_node_degrees[int(s_i[1:])]):
            if d_i == 0:
                # Connect s_i to check node with lowest degree
                min_degree = min(c_degrees)
                min_degree_c_nodes = [c_nodes[i] for i, deg in enumerate(c_degrees) if deg == min_degree]
                c_node = min_degree_c_nodes[0]
                graph.add_edge(s_i, c_node)
                c_degrees[c_nodes.index(c_node)] += 1
                print("Edge Creation: Scenario #1")
                print_parity_check_matrix(graph, s_nodes, c_nodes)
            else:
                # Build subgraph of s_i
                depth = 0
                prev_subgraph_nodes = set()
                current_subgraph_nodes = set(create_subgraph(graph, s_i, depth).nodes)

                # Continue building subgraph until it no longer expands
                while current_subgraph_nodes != prev_subgraph_nodes:
                    depth += 1
                    prev_subgraph_nodes = current_subgraph_nodes
                    current_subgraph_nodes = set(create_subgraph(graph, s_i, depth).nodes)

                subgraph_c_nodes = [node for node in create_subgraph(graph, s_i, depth).nodes if create_subgraph(graph, s_i, depth).nodes[node]['node_type'] == 'c']

                if set(subgraph_c_nodes) == set(c_nodes):
                    # Connect s_i to the check node with the lowest degree among the farthest nodes in the subgraph
                    farthest_check_nodes = get_farthest_check_nodes(graph, s_i, depth, c_nodes, c_degrees)

                    min_degree = min([c_degrees[c_nodes.index(c)] for c in farthest_check_nodes])
                    min_degree_c_nodes = [c for c in farthest_check_nodes if c_degrees[c_nodes.index(c)] == min_degree]
                    c_node = min_degree_c_nodes[0]
                    graph.add_edge(s_i, c_node)
                    c_degrees[c_nodes.index(c_node)] += 1
                    print("Edge Creation: Scenario #2.2")
                    print_parity_check_matrix(graph, s_nodes, c_nodes)
                else:
                    # Connect s_i to check node with lowest degree among check nodes not present in the subgraph
                    check_nodes_not_in_subgraph = list(set(c_nodes) - set(subgraph_c_nodes))
                    min_degree = min([c_degrees[c_nodes.index(c)] for c in check_nodes_not_in_subgraph])
                    min_degree_c_nodes = [c for c in check_nodes_not_in_subgraph if c_degrees[c_nodes.index(c)] == min_degree]

                    # Sort min_degree_c_nodes based on their index to prioritize the lowest index
                    min_degree_c_nodes.sort(key=lambda x: c_nodes.index(x))

                    c_node = min_degree_c_nodes[0]
                    graph.add_edge(s_i, c_node)
                    c_degrees[c_nodes.index(c_node)] += 1
                    print("Edge Creation: Scenario #2.1")
                    print_parity_check_matrix(graph, s_nodes, c_nodes)

    return graph

def get_farthest_check_nodes(graph, selected_node, depth, c_nodes, c_degrees):
    subgraph = create_subgraph(graph, selected_node, depth)
    subgraph_c_nodes = [node for node in subgraph.nodes if subgraph.nodes[node]['node_type'] == 'c']

    # Find the nodes at the maximum depth in the subgraph
    max_depth_nodes = [node for node, node_depth in nx.shortest_path_length(subgraph, selected_node).items() if node_depth == depth]

    # If no nodes are found at the maximum depth, try depth - 1
    if not max_depth_nodes and depth > 0:
        max_depth_nodes = [node for node, node_depth in nx.shortest_path_length(subgraph, selected_node).items() if node_depth == depth - 1]

    # Among these max_depth_nodes, filter out only the check nodes
    farthest_check_nodes = [node for node in max_depth_nodes if node in subgraph_c_nodes]

    # If there are no farthest check nodes, use the check node with the lowest degree
    if not farthest_check_nodes:
        min_degree = min(c_degrees)
        min_degree_c_nodes = [c_nodes[i] for i, deg in enumerate(c_degrees) if deg == min_degree]
        farthest_check_nodes = [min_degree_c_nodes[0]]  # Use the first node with minimum degree

    # Sort farthest_check_nodes based on their degree in c_degrees
    farthest_check_nodes.sort(key=lambda x: c_degrees[c_nodes.index(x)])

    return farthest_check_nodes

def create_subgraph(graph, selected_node, depth):
    subgraph = nx.Graph()
    queue = [(selected_node, 0)]  # (node, level)
    visited = set([selected_node])

    while queue:
        node, level = queue.pop(0)
        if level > depth:
            break
        subgraph.add_node(node, node_type=graph.nodes[node]['node_type'])

        if level < depth:
            neighbors = graph.neighbors(node)
            for neighbor in neighbors:
                if neighbor not in visited:
                    subgraph.add_node(neighbor, node_type=graph.nodes[neighbor]['node_type'])
                    subgraph.add_edge(node, neighbor)
                    queue.append((neighbor, level + 1))
                    visited.add(neighbor)
    
    return subgraph

def print_parity_check_matrix(graph, s_nodes, c_nodes):
    parity_check_matrix = np.zeros((len(c_nodes), len(s_nodes)), dtype=int)
    for c_node in c_nodes:
        c_index = int(c_node[1:])  # Extract check node index
        neighbors = list(graph.neighbors(c_node))
        for neighbor in neighbors:
            s_index = int(neighbor[1:])  # Extract symbol node index
            parity_check_matrix[c_index, s_index] = 1

    print(parity_check_matrix)

# Ask for n and m
n = int(input("Number of symbol nodes (n): "))
m = int(input("Number of check nodes (m): "))

# Validate the number of symbol nodes
while True:
    s_node_degrees = list(map(int, input("S-node degrees (comma separated): ").split(',')))
    if len(s_node_degrees) == n:
        break
    else:
        print(f"Error: Number of degrees provided ({len(s_node_degrees)}) does not match the number of symbol nodes (n={n}). Please provide {n} degrees.")

# Validate each degree does not exceed the number of check nodes
while True:
    if all(degree <= m for degree in s_node_degrees):
        break
    else:
        print(f"Error: Some degrees provided exceed the number of check nodes (m={m}). Please provide degrees less than or equal to {m}.")
        s_node_degrees = list(map(int, input("S-node degrees (comma separated): ").split(',')))

# Create the graph using PEG algorithm for edge creation
graph = create_graph(n, m, s_node_degrees)

# Divide nodes into 's' and 'c' nodes
s_nodes = [node for node in graph.nodes if graph.nodes[node]['node_type'] == 's']
c_nodes = [node for node in graph.nodes if graph.nodes[node]['node_type'] == 'c']

# Print the Parity Check Matrix for the final graph
print("Fianl Parity Check Matrix:")
print_parity_check_matrix(graph, s_nodes, c_nodes)

# Position nodes in two rows
pos = {}
for i, node in enumerate(s_nodes):
    pos[node] = (i, 1)  # Top row

for i, node in enumerate(c_nodes):
    pos[node] = (i, 0)  # Bottom row

# Draw the original graph with nodes in two rows
plt.figure(figsize=(8, 4))  # Adjust figure size as needed
nx.draw(graph, pos, with_labels=True, node_color=['aqua' if node in s_nodes else 'yellow' for node in graph.nodes], node_size=800, font_size=12, font_weight='bold')
plt.title('Original Graph')
plt.axis('off')
plt.show()

# Choose a specific node for subgraph visualization
selected_node = input(f"Select an 's' node to visualize its subgraph (e.g., s0, s1, ...): ")

# Check if the selected node is valid
if selected_node not in s_nodes:
    print("Error: Selected node is not a valid 's' node.")
else:
    depth = int(input("Enter depth for the subgraph: "))  # Depth of the subgraph

    # Create the subgraph
    subgraph = create_subgraph(graph, selected_node, depth)

    # Divide nodes into 's' and 'c' nodes
    subgraph_s_nodes = [node for node in subgraph.nodes if subgraph.nodes[node]['node_type'] == 's']
    subgraph_c_nodes = [node for node in subgraph.nodes if subgraph.nodes[node]['node_type'] == 'c']

    # Create fixed positions for nodes
    fixed_positions = {selected_node: (0.5, 1)}

    # Keep track of nodes at each level
    nodes_at_level = {0: [selected_node]}  # Starting with selected node

    for d in range(1, depth + 1):
        nodes_at_level[d] = []
        for node in nodes_at_level[d - 1]:
            neighbors = list(subgraph.neighbors(node))
            for neighbor in neighbors:
                if neighbor not in fixed_positions:
                    nodes_at_level[d].append(neighbor)
                    fixed_positions[neighbor] = (len(nodes_at_level[d]) - 0.5, 1 - d * 0.2)

    # Use spring layout with fixed positions for the subgraph
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(subgraph, pos=fixed_positions, fixed=fixed_positions.keys(), iterations=100)
    nx.draw(subgraph, pos, with_labels=True, node_color=['aqua' if node in subgraph_s_nodes else 'yellow' for node in subgraph.nodes],
            node_size=800, font_size=12, font_weight='bold')
    plt.title(f'Subgraph of {selected_node} at depth {depth} (Fixed Edge Length)')
    plt.axis('off')
    plt.show()
