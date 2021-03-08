
#reference with link:
# https://www.educative.io/edpresso/how-to-implement-a-graph-in-python
#https://stackoverflow.com/questions/28372127/add-edge-weights-to-plot-output-in-networkx
#https://networkx.org/documentation/latest/auto_examples/drawing/plot_weighted_graph.html

# Add a vertex to the set of vertices and the graph
import networkx as netx  # nice (di-)graph Python package
import matplotlib.pyplot as plt
# Driver code
# stores the vertices in the graph
vertices = []
# stores the number of vertices in the graph
vertices_no = 0
graph = []
adjacent=[]

weight=[]

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
    for i in range(vertices_no):
        for j in range(vertices_no):
            if graph[i][j] != 0:
                weight = graph[i][j]
                G.add_edge(i, j, weight=weight)
                
   #WORK ON ADDING NODE TO G
    #G.add_node(add_vertex())

    edlist = [(u, v) for (u, v, d) in G.edges(data=True)]

    epos = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0]
    eneg = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] < 0]

    pos = netx.spring_layout(G, seed=160)  # positions for all nodes - seed for reproducibility

        # nodes
    netx.draw_networkx_nodes(G, pos)

        # edges
    netx.draw_networkx_edges(G, pos, edgelist=edlist, width=6)

    labels = netx.get_edge_attributes(G, 'weight')
    netx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

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


