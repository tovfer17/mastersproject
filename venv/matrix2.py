# Example: solving a min-cost-flow problem
# using the Xpress Python interface
#
# (C) Fair Isaac Corp., 1983-2020

from __future__ import print_function

try:
    import networkx as netx  # nice (di-)graph Python package
except ImportError:
    print("Install the NetworkX Python package to use this example")
    quit()

import numpy as np  # for matrix and vector products
import xpress as xp


######


# Add a vertex to the set of vertices and the graph
def add_vertex(v):
  global graph
  global vertices_no
  global vertices
  if v in vertices:
    print("Vertex ", v, " already exists")
  else:
    vertices_no = vertices_no + 1
    vertices.append(v)
    if vertices_no > 1:
        for vertex in graph:
            vertex.append(0)
    temp = []
    for i in range(vertices_no):
        temp.append(0)
    graph.append(temp)

# Add an edge between vertex v1 and v2 with edge weight e
def add_edge(v1, v2, e):
    global graph
    global vertices_no
    global vertices
    # Check if vertex v1 is a valid vertex
    if v1 not in vertices:
        print("Vertex ", v1, " does not exist.")
    # Check if vertex v1 is a valid vertex
    elif v2 not in vertices:
        print("Vertex ", v2, " does not exist.")
    # Since this code is not restricted to a directed or
    # an undirected graph, an edge between v1 v2 does not
    # imply that an edge exists between v2 and v1
    else:
        index1 = vertices.index(v1)
        index2 = vertices.index(v2)
        graph[index1][index2] = e

# Print the graph
def print_graph():
  global graph
  global vertices_no
  for i in range(vertices_no):
    for j in range(vertices_no):
      if graph[i][j] != 0:
        print(vertices[i], " -> ", vertices[j], \
        " edge weight: ", graph[i][j])

# Driver code
# stores the vertices in the graph
vertices = []
# stores the number of vertices in the graph
vertices_no = 0
graph = []

# digraph definition

V = [1, 2, 3, 4]                                   # vertices
E = [[1, 2, 1], [1,3,1], [2, 3,3], [3,4, 4], [4,1, 5]]  # arcs

n = len(V)  # number of nodes
m = len(E)  # number of arcs

G = netx.DiGraph(E)


######

# One (random) demand for each node
demand = np.random.randint(100, size=n)
print(demand)
# Balance demand at nodes
demand[0] = - sum(demand[1:])

cost = np.random.randint(20, size=m)  # (Random) costs

# Flow variables declared on arcs---use dtype parameter to ensure
# NumPy handles these as vectors of Xpress objects.
flow = np.array([xp.var() for i in E], dtype=xp.npvar)

p = xp.problem('network flow')

p.addVariable(flow)
p.addConstraint(xp.Dot(A, flow) == - demand)
p.setObjective(xp.Dot(cost, flow))

p.solve()

for i in range(m):
    print('flow on', E[i], ':', p.getSolution(flow[i]))