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
    depth = 2  # Depth of the subgraph

    # Create the subgraph
    subgraph = nx.ego_graph(graph, selected_node, radius=depth)

    # Divide nodes into 's' and 'c' nodes
    subgraph_s_nodes = [node for node in subgraph.nodes if subgraph.nodes[node]['node_type'] == 's']
    subgraph_c_nodes = [node for node in subgraph.nodes if subgraph.nodes[node]['node_type'] == 'c']

    # Draw the subgraph with nodes in two colors
    plt.figure(figsize=(6, 6))
    nx.draw(subgraph, with_labels=True, node_color=['aqua' if node in subgraph_s_nodes else 'yellow' for node in subgraph.nodes], node_size=800, font_size=12, font_weight='bold')
    plt.title(f'Subgraph of {selected_node} at depth {depth} (Vertical Tree Layout)')
    plt.axis('off')
    plt.show()
