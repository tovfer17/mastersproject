
#reference with link:
# https://www.educative.io/edpresso/how-to-implement-a-graph-in-python
#https://stackoverflow.com/questions/28372127/add-edge-weights-to-plot-output-in-networkx
#https://networkx.org/documentation/latest/auto_examples/drawing/plot_weighted_graph.html

# Add a vertex to the set of vertices and the graph
import networkx as netx  # nice (di-)graph Python package
import matplotlib.pyplot as plt
import numpy as np
import math
import xpress as xp



# Driver code
# stores the vertices in the graph
vertices = []
# stores the number of vertices in the graph
vertices_no = 0
weight=[]
graph=[]

G = netx.DiGraph()
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


def convert_graph():
    global graph
    global vertices_no
    global vertices
    global weight


    for i in range(vertices_no):
        for j in range(vertices_no):
            if graph[i][j] != 0:
                weight = graph[i][j]
                G.add_edge(vertices[i], vertices[j], weight=weight)

                

   # edlist = [(u, v) for (u, v, d) in G.edges(data=True)]

    epos = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0]
    eneg = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] < 0]

    pos = netx.spring_layout(G,k=150, seed=200)  # positions for all nodes - seed for reproducibility

        # nodes
    netx.draw_networkx_nodes(G, pos)

        # edges
    #netx.draw_networkx_edges(G, pos, edgelist=edlist, width=6)

    labels = netx.get_edge_attributes(G, 'weight')
    netx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    netx.draw_networkx_edges(G, pos, edgelist=epos, width=10, edge_color="orange")

    netx.draw_networkx_edges(
            G, pos, edgelist=eneg, width=6, alpha=0.5, edge_color="blue", style="dashed"
        )

        # labels
    netx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()

   # plt.show()
    plt.savefig("graph.png")


def max_flow():
    global graph
    global vertices_no
    global vertices
    global weight

    thres = 0.4  # density of network
    thresdem = 0.8  # density of demand mesh


    dem = []

    for i in range(vertices_no):
        for j in range(vertices_no):
            if i != j and np.random.random() < thresdem:
                 dem.append((vertices[i], vertices[j], math.ceil(200 * np.random.random())))
    print("This is a random demand for each node", dem)


    for i in range(vertices_no):
        for j in range(vertices_no):
            if graph[i][j] != 0:
                pair = vertices[i], vertices[j]
                print (pair)


    #***********************************************************************************************************************
    #flow variables
    f = {(i, j, d): xp.var(name='f_{0}_{1}_{2}_{3}'.format(i, j, dem[d][0],
                                                           dem[d][1]))
         for (i, j) in pair for d in range(len(dem))}

    # capacity variables
    x = {(i, j): xp.var(vartype=xp.integer, name='cap_{0}_{1}'.format(i, j))
         for (i,j) in pair}
    print("this is x", x)

    p = xp.problem('network flow')
    p.addVariable(f, x)

    def demand(i, d):
        if dem[d][0] == i:  # source
            return 1
        elif dem[d][1] == i:  # destination
            return -1
        else:
            return 0

    # Flow conservation constraints: total flow balance at node i for each demand d
    # must be 0 if i is an intermediate node, 1 if i is the source of demand d, and
    # -1 if i is the destination.

    flow = {(i, d):
                xp.constraint(constraint=xp.Sum(f[vertices[i], vertices[j], d]
                                                for j in range(vertices_no) if (vertices[i], vertices[j]) in weight) -
                                         xp.Sum(f[vertices[j], vertices[i], d] for j in range(vertices_no) if
                                                (vertices[j], vertices[i]) in weight)
                                         == demand(vertices[i], d),
                              name='cons_{0}_{1}_{2}'.format(i, dem[d][0], dem[d][1]))
            for d in range(len(dem)) for i in range(vertices_no)}

    # Capacity constraints: weighted sum of flow variables must be contained in the
    # total capacity installed on the arc (i, j)
    capacity = {(i, j):
                    xp.constraint(constraint=xp.Sum(dem[d][2] * f[vertices[i], vertices[j], d]
                                                    for d in range(len(dem)))
                                             <= x[vertices[i], vertices[j]],
                                  name='capacity_{0}_{1}'.format(vertices[i], vertices[j]))
                for (i, j) in weight}

    p.addConstraint(flow, capacity)

    p.setObjective(xp.Sum(x[i, j] for (i, j) in weight))
    p.solve()

    p.getSolution()
#******************************************************************************************************************************
# Add vertices to the graph
add_vertex("s")
add_vertex("x")
add_vertex("z")
add_vertex("t")
add_vertex("w")
add_vertex("y")

# Add the edges between the vertices by specifying
# the from and to vertex along with the edge weights.


add_edge("s" ,"x", 1000)
add_edge("s" ,"y",-1500)
add_edge("x" ,"s", -1000)
add_edge("x" ,"z", 3000)
add_edge("x" ,"y", 1300)
add_edge("z" ,"x", 2000)
add_edge("z" ,"t", 4000)
add_edge("z" ,"w", 1000)
add_edge("z" ,"y", -1500)
add_edge("t" ,"z", -4000)
add_edge("t" ,"w", -2000)
add_edge("w" ,"z",  -1000)
add_edge("w" ,"t",  2000)
add_edge("w" ,"y",  1000)
add_edge("y" ,"s", 1500)
add_edge("y" ,"x", -1300)
add_edge("y" ,"z", 1500)
add_edge("y" ,"w", 2000)

print_graph()
print("Internal representation: ", graph)
convert_graph()
max_flow()

