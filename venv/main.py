# Add a vertex to the set of vertices and the graph
import networkx as netx  # nice (di-)graph Python package
import matplotlib.pyplot as plt
import numpy as np
import math
import gurobipy as gp
from gurobipy import GRB
import xlrd

# Driver code
vertices = []
vertices_no = 0
weight = []
graph = []
lnode=[]
cnode=[]
capnode=[]
vnode=[]

G = netx.DiGraph()
loc = ("/Users/fer/Desktop/data/networkflow.xls")

wb = xlrd.open_workbook(loc)
vertex=wb.sheet_by_index(0)
leavingnodes = wb.sheet_by_index(1)
comingnodes=wb.sheet_by_index(2)
capacities=wb.sheet_by_index(3)



################ adding vertex from xcel ######################

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

################ adding vertex from xcel ######################
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

################ print the pair of nodes and edgeweight ######################
def print_graph():
    global graph
    global vertices_no
    for i in range(vertices_no):
        for j in range(vertices_no):
            if graph[i][j] != 0:
                print(vertices[i], " -> ", vertices[j], \
                      " edge weight: ", graph[i][j])
                #print vertices

def draw_graph():
    global graph
    global vertices_no
    global vertices
    global weight

    for i in range(vertices_no):
        for j in range(vertices_no):
            if graph[i][j] != 0:
                weight=(graph[i][j])
                G.add_edge(vertices[i], vertices[j], weight=weight)


    epos = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0]

    pos = netx.spring_layout(G, k=150, seed=200)  # positions for all nodes - seed for reproducibility
    # nodes
    netx.draw_networkx_nodes(G, pos)
    # edges
    labels = netx.get_edge_attributes(G, 'weight')
    netx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    netx.draw_networkx_edges(G, pos, edgelist=epos, width=10, edge_color="orange")
    # labels
    netx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()

    plt.show()
    plt.savefig("greatgraph.png")

################ multicommodity######################

def max_flow():
    global graph
    global vertices_no
    global vertices
    global weight


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

    test = ['Pencils', 'Pens']
    f= tuple(test)
    print(f)

    listnodes=[]
    for a in range(1):
        for i in range(vertices_no):
                listnodes.append((f[a],vertices[i]))
    print("lsit of nodes with each commodity:", listnodes)

    listactualnodes = []
    for i in range(vertices_no):
            listactualnodes.append((vertices[i]))
    print("lsit of actual nodes:", listactualnodes)


    inter_nodes_list = listactualnodes

    inter_nodes_list.remove('Detroit')
    inter_nodes_list.remove('Tokyo')
    print("inter", inter_nodes_list)


    # Create optimization model
    m = gp.Model('netflow')

    # Create variables
    flow = m.addVars( f,di,obj=cost, name="flow")
   # for m in range(len(len(di))):
        #    for k in range(len(f)):
                  #  flow=m.addVars(f, di, obj=cost, name="flow")
    m.update()

     #Arc-capacity constraints
   # for x,y in di:
       #m.addConstr(sum(flow[h, x, y] for h in f) <= capacity[x, y], "cap[%s, %s]" % (x, y))
    #for m in range(len(di)):
      #  m.addConstr(quicksum(flow[h,m]
                          #   for k in range(len(f)))
                            # <= capacity[x, y], "cap[%s, %s]" % (x, y))

     #Flow-conservation constraints
    # they require that, for each commodity and node, the sum of the flow into the node
    # plus the quantity of external inflow at that node must be equal to the sum of the flow out of the node:
    m.addConstrs(
        (gp.quicksum(flow[h,x,y] for x, y in di.select('*', y)) + inflow[h,y]   ==
          gp.quicksum(flow[h, y, k] for y, k in di.select(y, '*'))
          for h in f for y in inter_nodes_list), "node")

    # Compute optimal solutions
    m.optimize()

    print (m.display())

    print("hi", m.status)


    # Print solution
    #if m.status == GRB.OPTIMAL:
      # solution = m.getAttr('x', flow)
       #for h in f:
           #print('\nOptimal flows for %s:' % h)
           #for x, y in di:
                    #if solution[h,x, y] > 0:
                       # print('%s -> %s: %g' % (x, y, solution[x, y]))

    # print solution: optimal value and optimal point
    print('Obj: %g' % m.objVal)
     #print(f"optimal value = {model.objVal:.2f}")
    for v in m.getVars():
       print('%s %g' % (v.varName, v.x))



#################Driver#########################

p = 1
while True:
    try:
        v = vertex.cell_value(p, 0)
        vnode.append(v)
        add_vertex(v)
        p = p+1
    except IndexError:
        break
i = 1

while True:
    try:

        l = leavingnodes.cell_value(i, 0)
        lnode.append(l)
        c = comingnodes.cell_value(i, 0)
        cnode.append(c)
        cap = capacities.cell_value(i,2)
        capnode.append(cap)
        add_edge(l,c,cap)

        i = i+1
    except IndexError:
        break



print_graph()
print("Internal representation: ", graph)
draw_graph()



