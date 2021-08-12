# Add a vertex to the set of vertices and the graph
import networkx as netx  # nice (di-)graph Python package
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB
import xlrd
import csv
import pandas as pd
import pandas
from openpyxl import load_workbook
import pyexcel as fp

# Driver code
vertices = []
vertices_no = 0
weight = []
graph = []
leavingnode=[]
comingnode=[]
price ={}
maxcapacity=[]
comm=[]
tran=[]
demand ={}
start=[]
cnode=[]
nodes=[]
G = netx.DiGraph()
var_names = []
var_values = []
demands={}
commo=[]
origin=[]
destination=[]
dem=[]
price=[]


#loc1 = (r"C:\Users\rithi\pyprojnew\networkflow.xls")
#loc1=("/Users/fer/PycharmProjects/project/networkflow2d.xls")
loc2= ("/Users/fer/PycharmProjects/project/networkflow2d.xlsx")
loc3= ('/Users/fer/PycharmProjects/project/export.csv')

loc1 = ("/Users/fer/PycharmProjects/project/Input_lecct copy.xls")

wb = xlrd.open_workbook(loc1)
Vertex=wb.sheet_by_index(0)
Arcs=wb.sheet_by_index(1)
Commodities=wb.sheet_by_index(2)

################ adding vertex from excel ######################

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

################ adding vertex from excel ######################
def add_edge(v1, v2,e):
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
    netx.draw_networkx_edges(G, pos, edgelist=epos, width=10,edge_color="orange")
    # labels
    netx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    #plt.tight_layout()

    plt.show()
    #plt.savefig("graphp.png")

################ multicommodity######################

def max_flow(commodity,leavingnode,commingnode, origin,destination,cost,demandz,maxcapacity):
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

    pair,far = gp.multidict(dict(zip(listkeyPair, listvalueCap)))
    print("The dictionary after the merge of the pairs of nodes with the capacities:")
    print (far)


    listnodes=[]
    #for a in range(1):
    for i in range(vertices_no):
                listnodes.append((commodity,vertices[i]))
    print("lsit of nodes with each commodity:", listnodes)

    listactualnodes = []
    for i in range(vertices_no):
            listactualnodes.append((vertices[i]))
    print("lsit of actual nodes:", listactualnodes)



    nodes =leavingnode +commingnode
    print("list of all incoming and outgoingnodes: ", nodes)

    print("coming nodes", commingnode)
    print("leaving nodes",leavingnode)

    # Create optimization model


    m = gp.Model('netflow')

    # Create variables
    # flow = m.addVars(test,di, obj=cost, name="flow")
    #flow = m.addVars(commodity, pair, obj=cost, name="flow")
    flow = {}

    for p in range(len(leavingnode)):
        print("this is costm", cost[p])
        for k in range(len(commodity)):
            print("commodity", commodity[k])
            flow[commodity[k], leavingnode[p], commingnode[p]] = m.addVar(obj=cost[p], vtype="C",
                                                                name="flow(%s, %s, %s)" % (commodity[k], leavingnode[p], commingnode[p]))



    #flow = m.addVars(commodity, pair, obj=cost, name="flow")
    #m.setObjective(flow.prod(cost), gp.MINIMIZE)

    m.update()
    cap ={}
    # Arc-capacity constraints
    #for x, y in pair:
    #for f in range(len(listactualnodes)):
    for f in range(len(leavingnode)):
            cap[leavingnode[f],commingnode[f]]= m.addConstr(gp.quicksum(flow[commodity[k], leavingnode[f], commingnode[f]]
                                                                for k in range(len(commodity))),
                                                        '<=', maxcapacity[f], name="cap[%s]" % (f))

        #m.addConstr(sum(flow[h, x, y] for h in commodity) <= maxcapacity[x,y], "cap[%s, %s]" % (x,y))

        # Flow-conservation constraints
    for a in range(len(commodity)):
        print("commodity", commodity[a])
        for y in  range(len(listactualnodes)):
            print("demand", demandz[a])
            print ("originnn", origin[a])
            print ("destination", destination[a])
            #for p in leavingnode:
            print("y",leavingnode[y])
            if listactualnodes[y] == origin[a]:
                    print("test 1")
                    m.addConstr(
                         gp.quicksum(flow[commodity[a], listactualnodes[y], k] for listactualnodes[y], k in pair.select(listactualnodes[y], '*')) -
                         gp.quicksum(flow[commodity[a], i, listactualnodes[y]] for i, listactualnodes[y] in pair.select('*', listactualnodes[y])), '=', demandz[a],
                         name= "Continuity(%s,%s)" % (commodity[a], listactualnodes[y]))


            elif listactualnodes[y] == destination[a]:
                    print("test 2")
                    m.addConstr(
                        gp.quicksum(flow[commodity[a], listactualnodes[y], k] for listactualnodes[y], k in pair.select(listactualnodes[y], '*')) -
                        gp.quicksum(flow[commodity[a], i, listactualnodes[y]] for i, listactualnodes[y] in pair.select('*', listactualnodes[y])), '=', -(demandz[a])
                         , name= "Continuity(%s,%s)" % (commodity[a], listactualnodes[y]))
            else:
                    print("test 3")
                    m.addConstr(
                        gp.quicksum(flow[commodity[a], listactualnodes[y], k] for listactualnodes[y], k in pair.select(listactualnodes[y], '*')) -
                        gp.quicksum(flow[commodity[a], i, listactualnodes[y]] for i, listactualnodes[y] in pair.select('*', listactualnodes[y])), '=', 0
                         , name= "Continuity(%s,%s)" % (commodity[a], listactualnodes[y]))
            print("done")
    # Compute optimal solutions
    m.update()
    m.write("whynot.lp")
    m.write("whynot.mps")
    m.optimize()
    print (m.display())

    print("if model fesible it will print a 2 .", m.status)

    # Print solution

    # print solution: optimal value and optimal point
    print('Obj: %g' % m.objVal)
     #print(f"optimal value = {model.objVal:.2f}")
    for var in m.getVars():
       #print('%s %g' % (v.varName, v.x))
       if var.X > 0:
           var_names.append(str(var.varName))
           var_values.append(var.X)

    # Write to csv
    """with open('/Users/fer/PycharmProjects/project/export.csv', 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(zip(var_names, var_values))"""

# Print solution
    if m.status == GRB.OPTIMAL:
        solution = m.getAttr('x', flow)
    for h in commodity:
        print('\nOptimal flows for %s:' % h)
        for i, j in pair:
            if solution[h, i, j] > 0:
                print('%s -> %s: %g' % (i, j, solution[h, i, j]))

#################Driver#########################
#adding the vertex sheet with all the nodes
p = 1
while True:
    try:
        v = Vertex.cell_value(p, 0)
        #adds it to list of vertices
        add_vertex(v)
        #adds it to draw graph
        nodes.append(v)
        print(nodes)
        p = p+1
    except IndexError:
        break

# adding the arcs sheet with i, j,capacity  and then matching them with a cost
i = 1
while True:
    try:

        l = Arcs.cell_value(i, 0)
        leavingnode.append(l)
        c = Arcs.cell_value(i, 1)
        comingnode.append(c)
        cap = Arcs.cell_value(i,3)
        maxcapacity.append(cap)
        add_edge(l,c,cap)
        i = i+1
    except IndexError:
        break




# adding the commodities sheet with #, origin, destination
i = 1
while True:
    try:
        item= Commodities.cell_value(i,0)
        commo.append(item)
        ori = Commodities.cell_value(i, 1)
        origin.append(ori)
        dest = Commodities.cell_value(i, 2)
        destination.append(dest)
        i = i+1
    except IndexError:
        break

z = 1
while True:
    try:
        c = Arcs.cell_value(z, 2)
        price.append(c)
        z= z+1
    except IndexError:
        break


a = 1
while True:
    try:
        #for it in commo:
           #ori = Commodities.cell_value(a, 1)
           #dest = Commodities.cell_value(a, 2)
        demands =Commodities.cell_value(a,3)
        dem.append(demands)
           #demands[it]=Commodities.cell_value(a,3)
           #print("Demands:", demands[it])
        print("Demands:", dem)
        a = a+1
    except IndexError:
        break

print_graph()
print("Internal representation: ", graph)
#draw_graph()

print("END:")
print("commo",commo)
print("origin:",origin)
print('destination',destination)

print("leaving", leavingnode)
print('coming', comingnode)
print("demands", dem)
print("cost",price)
print("capacity",maxcapacity)

max_flow(commo,leavingnode,comingnode, origin,destination, price, dem,maxcapacity)
#read_file = pd.read_csv(loc3)
#fp.save_book_as(file_name=loc1,
               #dest_file_name=loc2)

#book = load_workbook(loc2)
#writer = pandas.ExcelWriter(loc2, engine='openpyxl')
#writer.book = book

#writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
#read_file.to_excel(writer, "Max Z", header= False,startrow=1)
#writer.save()