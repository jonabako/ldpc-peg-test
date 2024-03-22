## Python / React Simulation Tool
https://jonabako.github.io/ldpc-peg-app/

## JS Simulation Tool (for testing):
https://jonabako.github.io/ldpc-peg-test/

## Using networkx and matplotlib.pyplot for graph & subgraph generation:

![image](https://github.com/jonabako/ldpc-peg-test/assets/87908322/1920750b-83ed-4256-82aa-0cb679738d71)

![image](https://github.com/jonabako/ldpc-peg-test/assets/87908322/dc9f01d9-d28c-4b67-859c-272cf45473ae)

## Core Steps of PEG Algorithm for edge creation:

The PEG algorithm starts with 3 parameters: number of check nodes, number of symbol nodes and the symbol degree sequence. The algorithm goes over the symbol nodes one by one and it starts working on another node only after all the edges required by that node's degree is established. 

If this is the first edge of the current symbol node, the algorithm picks the check node with the lowest check node degree, i.e the node with the least number of edges in the graph's current setting. 

If this is not the first edge for that symbol node, then there are 2 scenarios:

1. There are nodes which are not covered by the subgraph expanded from the current symbol node. In this case, the algorithm selects the node with the lowest check node number from the set of nodes which are not covered by the subgraph expanded from the current symbol node.

2. The subgraph expanded from the current symbol node already covers all the check nodes in the system. In this case, the algorthm needs to find the check nodes which are at the farthest distance from that symbol node. In order to find them, it looks at the previous depth of the expansion tree, just before all check nodes are covered. The check nodes which are uncovered by this previous subgraph are the ones that are added last. Then the algorithm again chooses the one with the lowest check node degree from this set.

When the algorithm creates enough edges for every symbol node, it terminates.
