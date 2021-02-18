# importing networkx
import networkx as nx
# importing matplotlib.pyplot
import matplotlib.pyplot as plt

edges = [(1, 2), (1, 6), (2, 3), (2, 4), (2, 6),
         (3, 4), (3, 5), (4, 8), (4, 9), (6, 7)]

G = nx.Graph()
G.add_edges_from(edges)


print("Total number of nodes: ", int(G.number_of_nodes()))
print("Total number of edges: ", int(G.number_of_edges()))
print("List of all nodes: ", list(G.nodes()))
print("List of all edges: ", list(G.edges(data=True)))
print("Degree for all nodes: ", dict(G.degree()))

nx.selfloop_edges(G)
print("Total number of self-loops: ", (nx.selfloop_edges(G)))
print("List of all nodes with self-loops: ", list(nx.nodes_with_selfloops(G)))

print("List of all nodes we can go to in a single step from node 2: ",
      list(G.neighbors(2)))

nx.draw_networkx(G, with_label=True)
plt.savefig("uwork.png")