# Add a vertex to the set of vertices and the graph
import networkx as netx  # nice (di-)graph Python package
import matplotlib.pyplot as plt

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

G = netx.DiGraph()
# Add vertices to the graph
G.add_node("s")
G.add_node("x")
G.add_node("y")
G.add_node("z")
G.add_node("w")
G.add_node("t")

# Add the edges between the vertices by specifying
# the from and to vertex along with the edge weights.


G.add_edge("s" ,"x", weight=1000)
G.add_edge("s" ,"y",weight =-1500)
G.add_edge("x" ,"y", weight= 1300)
G.add_edge("x" ,"z", weight= 3000)
G.add_edge("x" ,"s", weight= -1000)
G.add_edge("z" ,"x", weight= 2000)
G.add_edge("z" ,"y",  weight= -1500)
G.add_edge("z" ,"w", weight= 1000)
G.add_edge("z" ,"t", weight= 1000)
G.add_edge("y" ,"z", weight= 1500)
G.add_edge("y" ,"w", weight= 2000)
G.add_edge("y" ,"x", weight= -1500)
G.add_edge("y" ,"x",weight=  -1500)
G.add_edge("w" ,"y", weight= 1000)
G.add_edge("w" ,"t",weight=  1000)
G.add_edge("w" ,"z", weight= -1000)
G.add_edge("t" ,"w", weight= -2000)
G.add_edge("t" ,"z", weight= -4000)

print_graph()
print("Internal representation: ", graph)



edlist = [(u, v) for (u, v, d) in G.edges(data=True) ]

epos = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0]
eneg = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] < 0]

pos = netx.spring_layout(G,seed=160)  # positions for all nodes - seed for reproducibility

# nodes
netx.draw_networkx_nodes(G,pos)

# edges
netx.draw_networkx_edges(G, pos, edgelist=edlist, width=6)

labels = netx.get_edge_attributes(G,'weight')
netx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

netx.draw_networkx_edges(G, pos, edgelist=epos, width=10)
netx.draw_networkx_edges(
    G, pos, edgelist=eneg, width=6, alpha=0.5, edge_color="b", style="dashed"
)

# labels
netx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()


plt.show()

# One (random) demand for each node
demand = np.random.randint(100, size=n)
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