import numpy as np
import networkx as nx

class SymbolNode:
    def __init__(self, id):
        self.id = id
        self.subgraph = []

class CheckNode:
    def __init__(self, id):
        self.id = id

def select_check_node(check_nodes, subgraph_check_nodes, symbol_node, check_degrees):
    num_check_nodes = len(check_nodes)
    num_covered_check_nodes = sum(1 for node in subgraph_check_nodes if node in check_nodes)
    num_uncovered_nodes = num_check_nodes - num_covered_check_nodes
    
    if num_uncovered_nodes > 0:
        return min(set(check_nodes) - set(subgraph_check_nodes), key=lambda node: check_degrees[node])
    else:
        prev_subgraph = nx.shortest_path_length(symbol_node.graph, source=symbol_node, target=None)
        uncovered_nodes = set(check_nodes) - set(prev_subgraph.keys())
        return min(uncovered_nodes, key=lambda node: check_degrees[node])

def update_subgraphs(ldpc_matrix, symbol_node, check_node, symbol_nodes):
    for node in symbol_nodes:
        if node.id == symbol_node.id:
            node.subgraph.append(check_node)
        elif ldpc_matrix[check_node.id][node.id] == 1:
            node.subgraph.append(check_node)

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))

def progressive_edge_growth(num_symbol_nodes, num_check_nodes, symbol_degrees):
    # Initialize LDPC matrix and graph
    ldpc_matrix = np.zeros((num_check_nodes, num_symbol_nodes), dtype=int)
    symbol_nodes = [SymbolNode(id=i) for i in range(num_symbol_nodes)]
    check_nodes = [CheckNode(id=i) for i in range(num_check_nodes)]
    check_degrees = {node: 0 for node in check_nodes}

    # Initialize graph
    graph = nx.Graph()
    for node in symbol_nodes:
        graph.add_node(node)
        node.graph = graph

    for node in check_nodes:
        graph.add_node(node)

    edge_number = 1
    for symbol_node in symbol_nodes:
        for _ in range(symbol_degrees[symbol_node.id]):
            print(f"Processing edge {edge_number}:")
            if _ == 0:
                check_node = min(check_nodes, key=lambda node: check_degrees[node])
            else:
                uncovered_nodes = set(check_nodes) - set(symbol_node.subgraph)
                if len(uncovered_nodes) > 0:
                    check_node = min(uncovered_nodes, key=lambda node: check_degrees[node])
                else:
                    prev_subgraph = nx.shortest_path_length(symbol_node.graph, source=symbol_node, target=None)
                    uncovered_nodes = set(check_nodes) - set(prev_subgraph.keys())
                    check_node = min(uncovered_nodes, key=lambda node: check_degrees[node])

            ldpc_matrix[check_node.id][symbol_node.id] = 1
            check_degrees[check_node] += 1
            update_subgraphs(ldpc_matrix, symbol_node, check_node, symbol_nodes)

            print(f"Parity Check Matrix after processing edge {edge_number}:")
            print_matrix(ldpc_matrix)
            edge_number += 1

    return ldpc_matrix

def main():
    num_symbol_nodes = int(input("Enter the number of symbol nodes: "))
    num_check_nodes = int(input("Enter the number of check nodes: "))
    symbol_degrees = list(map(int, input("Enter the degrees for symbol nodes separated by commas: ").split(',')))

    ldpc_matrix = progressive_edge_growth(num_symbol_nodes, num_check_nodes, symbol_degrees)
    print("Final LDPC matrix:")
    print_matrix(ldpc_matrix)

if __name__ == "__main__":
    main()
