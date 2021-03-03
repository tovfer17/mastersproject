
from __future__ import print_function


import networkx as netx  # nice (di-)graph Python package

import numpy as np  # for matrix and vector products


# digraph definition

V = [1, 2, 3, 4, 5]                                   # vertices
E = [[1, 2], [1, 4], [2, 3], [3, 4], [4, 5], [5, 1]]  # arcs

n = len(V)  # number of nodes
m = len(E)  # number of arcs

G = netx.DiGraph(E)

# Get NumPy representation
A = (netx.incidence_matrix(G, oriented=True).toarray())

print("incidence matrix:\n", A)

# One (random) demand for each node
demand = np.random.randint(100, size=n)
# Balance demand at nodes
demand[0] = - sum(demand[1:])

cost = np.random.randint(20, size=m)  # (Random) costs
