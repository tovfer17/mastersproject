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

    cost = {
        ('a', 's', 'x'): 10,
        ('a', 's', 'y'): 20,
        ('a', 'x', 's'): 60,
        ('a', 'x', 'z'): 40,
        ('a', 'x', 'y'): 40,
        ('a', 'z', 'x'): 30,
        ('a', 'z', 't'): 20,
        ('a', 'z', 'w'): 20,
        ('a', 'z', 'y'): 80,
        ('a', 't', 'z'): 60,
        ('a', 'z', 'w'): 70,
        ('a', 'w', 'z'): 30,
        ('a', 'w', 't'): 30,
        ('a', 'w', 'y'): 30,
        ('a', 'y', 's'): 30,
        ('a', 'y', 'x'): 30,
        ('a', 'y', 'z'): 30,
        ('a', 'y', 'w'): 30,

    }

    thresdem = 0.8  # density of demand mesh
    dem = [50,60,-50,-50,-10,60,40,-40,-30,-30]
    #dem = [0,0,0,0,0,0,0,0,0,0]



       # for j in range(vertices_no):
            #if i != j and np.random.random() < thresdem:
                #dem.append((vertices[i], vertices[j], math.ceil(200 * np.random.random())))
              #dem.append((math.ceil(200 * np.random.random())))
    #print("This is a random demand for each node", dem)
            #if i != j:
   # np.set_printoptions(precision=1)
   # dem.append((math.ceil(200 * np.random.random())))

    #dem.append( my_randoms)

    print("This is a random demand for each node", dem)


    listkeyPair=[]
    for i in range(vertices_no):
        for j in range(vertices_no):
           if graph[i][j] != 0:
                listkeyPair.append((vertices[i], vertices[j]))
    print("This prints out the nodes in the pair: ",listkeyPair)

    listvalueCap=[]
    for i in range(vertices_no):
        for j in range(vertices_no):
            if  graph[i][j] != 0:
                listvalueCap.append((graph[i][j]))
    print("This prints out the capacity of the node pair: ", listvalueCap)

    di,capacity = gp.multidict(dict(zip(listkeyPair, listvalueCap)))
    print("The dictionary after the merge of the pairs of nodes with the capacities:")
    print (capacity)

    test = ['a']
    print(tuple(test))

    listnodes=[]
    for a in range(1):
        for i in range(vertices_no):
                listnodes.append((test[a],vertices[i]))
    print("lsit of nodes with each commodity:", listnodes)

    listactualnodes = []
    for i in range(vertices_no):
            listactualnodes.append((vertices[i]))
    print("lsit of actual nodes:", listactualnodes)


    com,demand =gp.multidict(dict(zip(listnodes,dem)))
    print("The dictionary after the merge of the commodity with the nodes with demands :")
    print(com)
    print(demand)





    #*******************************************************************************************************************

    # Create optimization model
    m = gp.Model('netflow')

    # Create variables
    flow = m.addVars( test,di,obj=cost, name="flow")
    m.update()

     #Arc-capacity constraints
    for x,y in di:
       m.addConstr(sum(flow[h, x, y] for h in test) <= capacity[x, y], "cap[%s, %s]" % (x, y))


     #Flow-conservation constraints
    # they require that, for each commodity and node, the sum of the flow into the node
    # plus the quantity of external inflow at that node must be equal to the sum of the flow out of the node:
    m.addConstrs(
        (gp.quicksum(flow[h,x,y] for x, y in di.select('*', y)) + demand[h,y]   ==
          gp.quicksum(flow[h, y, k] for y, k in di.select(y, '*'))
          for h in test for y in listactualnodes), "node")

    # Compute optimal solutions
    m.optimize()

    print (m.display())

    print("hi", m.status)




    # Print solution
    if m.status == GRB.OPTIMAL:
       solution = m.getAttr('x', flow)
       for h in test:
           print('\nOptimal flows for %s:' % h)
           for x, y in di:
                    if solution[h,x, y] > 0:
                        print('%s -> %s: %g' % (x, y, solution[x, y]))

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
#add_edge("s", "y", -1500)
#add_edge("x", "s", -1000)
add_edge("x", "z", 3000)
add_edge("x", "y", 1300)
add_edge("z", "x", 2000)
add_edge("z", "t", 4000)
#add_edge("z", "w", 1000)
#add_edge("z", "y", -1500)
#add_edge("t", "z", -4000)
#add_edge("t", "w", -2000)
#add_edge("w", "z", -1000)
add_edge("w", "t", 2000)
#add_edge("w", "y", 1000)
add_edge("y", "s", 1500)
#add_edge("y", "x", -1300)
add_edge("y", "z", 1500)
add_edge("y", "w", 2000)


#add_edge("s", "x", 124)
#add_edge("x", "z", 124)
#add_edge("x", "y", 124)
#add_edge("z", "x", 124)
#add_edge("z", "t", 124)
#add_edge("z", "w", 124)
#add_edge("w", "t", 124)
#add_edge("w", "y", 124)
#add_edge("y", "s", 124)
#add_edge("y", "z", 124)
#add_edge("y", "w", 124)

print_graph()
print("Internal representation: ", graph)
convert_graph()
max_flow()

