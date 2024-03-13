from builtins import any, enumerate, input, int, len, list, map, print, range, set, zip
import networkx as nx
import matplotlib.pyplot as plt

def create_graph(n, m, s_node_degrees):
    # Create an empty graph
    G = nx.Graph()

    # Create symbol nodes (s_type)
    s_nodes = ['s{}'.format(i) for i in range(n)]
    G.add_nodes_from(s_nodes, node_type='s')

    # Create check nodes (c_type)
    c_nodes = ['c{}'.format(i) for i in range(m)]
    G.add_nodes_from(c_nodes, node_type='c')

    # Ask for connections between s-nodes and c-nodes
    for s_node, degree in zip(s_nodes, s_node_degrees):
        for _ in range(degree):
            c_index = int(input(f"Enter index of a c-node connected to {s_node}: "))
            if c_index >= m:
                print(f"Error: Invalid c-node index {c_index}.")
                return
            c_node = 'c{}'.format(c_index)
            G.add_edge(s_node, c_node)
    
    return G

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

# Ask for n and m
n = int(input("Number of symbol nodes (n): "))
m = int(input("Number of check nodes (m): "))
s_node_degrees = list(map(int, input("S-node degrees (comma separated): ").split(',')))

# Create the graph
graph = create_graph(n, m, s_node_degrees)

# Divide nodes into 's' and 'c' nodes
s_nodes = [node for node in graph.nodes if graph.nodes[node]['node_type'] == 's']
c_nodes = [node for node in graph.nodes if graph.nodes[node]['node_type'] == 'c']

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
