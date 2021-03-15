# reference with link:
# https://www.educative.io/edpresso/how-to-implement-a-graph-in-python
# https://stackoverflow.com/questions/28372127/add-edge-weights-to-plot-output-in-networkx
# https://networkx.org/documentation/latest/auto_examples/drawing/plot_weighted_graph.html

# Add a vertex to the set of vertices and the graph
import networkx as netx  # nice (di-)graph Python package
import matplotlib.pyplot as plt
import numpy as np
import math
import gurobipy as gp
from gurobipy import GRB

# Driver code
# stores the vertices in the graph
vertices = []
# stores the number of vertices in the graph
vertices_no = 0
weight = []
graph = []

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
                #print vertices

def convert_graph():
    global graph
    global vertices_no
    global vertices
    global weight


    for i in range(vertices_no):
        for j in range(vertices_no):
            if graph[i][j] != 0:
                weight=(graph[i][j])
                G.add_edge(vertices[i], vertices[j], weight=weight)


    # edlist = [(u, v) for (u, v, d) in G.edges(data=True)]

    epos = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0]
    eneg = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] < 0]

    pos = netx.spring_layout(G, k=150, seed=200)  # positions for all nodes - seed for reproducibility

    # nodes
    netx.draw_networkx_nodes(G, pos)

    # edges
    # netx.draw_networkx_edges(G, pos, edgelist=edlist, width=6)

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


    thresdem = 0.8  # density of demand mesh
    dem = []
    for i in range(vertices_no):
        for j in range(vertices_no):
            if i != j and np.random.random() < thresdem:
                #dem.append((vertices[i], vertices[j], math.ceil(200 * np.random.random())))
                dem.append((math.ceil(200 * np.random.random())))
    print("This is a random demand for each node", dem)


    listkeys=[]
    for i in range(vertices_no):
        for j in range(vertices_no):
           if graph[i][j] != 0:
                listkeys.append((vertices[i], vertices[j]))
    print("bye1",listkeys)

    listvalues=[]
    for i in range(vertices_no):
        for j in range(vertices_no):
            if  graph[i][j] != 0:
                listvalues.append((graph[i][j]))
    print("bye2", listvalues)

    di,capacity = gp.multidict(dict(zip(listkeys, listvalues)))
    print("The dictionary after the merge of the pairs of nodes with the weights:")
    #print(di)
    print (capacity)

    hi,demand =gp.multidict(zip(listkeys,dem))
    print("The dictionary after the merge of the pairs of nodes with the demands:")
    print(demand)

    #*******************************************************************************************************************
    test=['a','b','c']
    # Create optimization model
    m = gp.Model('netflow')

    # Create variables
    flow = m.addVars( test,di, name="flow")
    m.update()

     #Arc-capacity constraints
    #m.addConstrs(
    #(flow.sum('*', x, y) <= capacity[x, y] for x, y in di), "cap")

    # Equivalent version using Python looping
    #print("why", di)

    for x,y in di:
        #print (x)
        #print(y)
        #print("capa", capacity[x, y])


       m.addConstr(sum(flow[h, x, y] for h in test) <= capacity[x, y], "cap[%s, %s]" % (x, y))


     #Flow-conservation constraints
    # hey require that, for each commodity and node, the sum of the flow into the node
    # plus the quantity of external inflow at that node must be equal to the sum of the flow out of the node:
    #.addConstrs(
    # (flow.sum('*', y) + demand[y] == flow.sum( y, '*')

    m.addConstrs(
        (gp.quicksum(flow[h,x, y] for x, y in di.select('*', y)) + demand[ y] ==
          gp.quicksum(flow[h, y, k] for y, k in di.select(y, '*'))
          for h in test for y in di), "node")
    # Compute optimal solutions
    m.optimize()

    print("hi",m.status)
    if m.status == GRB.INFEASIBLE:
        solution = m.getAttr('x', flow)
        for h in test:
            print('\nOptimal flows for %s:' % h)
            for x, y in di:
                if solution[h, x, y] > 0:
                    print('%s -> %s: %g' % (i, j, solution[i, j]))

    #if m.status == GRB.INFEASIBLE:
        #vars = m.getVars()
        #ubpen = [1.0] * m.numVars
        #m.feasRelax(1, False, vars, None, ubpen, None, None)
        #m.optimize()

    # Print solution
   # if m.status == GRB.OPTIMAL:
       # solution = m.getAttr('x', flow)
        #for h in test:
           # print('\nOptimal flows for %s:' % h)
           # for x, y in di:
                    #if solution[h,x, y] > 0:
                        #print('%s -> %s: %g' % (i, j, solution[i, j]))

#***********************************************************************************************************************
# Add vertices to the graph
add_vertex("s")
add_vertex("x")
add_vertex("z")
add_vertex("t")
add_vertex("w")
add_vertex("y")

# Add the edges between the vertices by specifying
# the from and to vertex along with the edge weights.


add_edge("s", "x", 1000)
add_edge("s", "y", -1500)
add_edge("x", "s", -1000)
add_edge("x", "z", 3000)
add_edge("x", "y", 1300)
add_edge("z", "x", 2000)
add_edge("z", "t", 4000)
add_edge("z", "w", 1000)
add_edge("z", "y", -1500)
add_edge("t", "z", -4000)
add_edge("t", "w", -2000)
add_edge("w", "z", -1000)
add_edge("w", "t", 2000)
add_edge("w", "y", 1000)
add_edge("y", "s", 1500)
add_edge("y", "x", -1300)
add_edge("y", "z", 1500)
add_edge("y", "w", 2000)

print_graph()
print("Internal representation: ", graph)
convert_graph()
max_flow()

