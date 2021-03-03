
import networkx as nx
import matplotlib.pyplot as plt
import gurobipy as GRB

#https://networkx.org/documentation/stable/reference/classes/digraph.html
G = nx.DiGraph()
#H = nx.path_graph(6)
#G.add_nodes_from(H)

# https://networkx.org/documentation/stable//reference/generated/networkx.classes.function.get_node_attributes.html
G.add_node(0 ,inflow ="0")
G.add_node(1 ,inflow ="1000")
G.add_node(2,inflow ="4700")
G.add_node(3,inflow ="5000")
G.add_node(4,inflow ="5400")
G.add_node(5,inflow ="7700")

G.add_edges_from([(0, 1), (1, 3),(3,5),(4,5),(4,3),(3,2),(2,4),(4,1),(0,2)])


print("Total number of nodes: ", int(G.number_of_nodes()))
print("Total number of edges: ", int(G.number_of_edges()))
print("List of all nodes: ", list(G.nodes()))
print("List of all edges: ", list(G.edges()))
print("Degree for all nodes: ", dict(G.degree()))
#print("Total number of self-loops: ", (nx.selfloop_edges(G)))
#print("List of all nodes with self-loops: ", list(nx.nodes_with_selfloops(G)))
print("list of inflows: ", list(G.nodes(data=True)))

nodes_h = nx.get_node_attributes(G, 'inflow')
print (nodes_h[1])

#nx.draw_networkx(G)
#plt.show(True)
#plt.savefig("bwork.png")

# N is # of commodities and its based on the length of the inflow list so 6 commodities
N = 0

#for each node, have a list of N commodities length attached to give[][]
 #index feature for i nodes and h commodities

for i in nodes_h:
    count = 0
    j= nodes_h[i]
    print("i: ", i)
    print("j: ", j)
    for k in range(len(j)):

        print("K: ", k, ": ")
        print(nodes_h[i][k])
        #print( nodes_h[i][k])

    if N == 0:
         N = len(j)

#for each arc i,j add index h for N commodities as third index of tuple
#list = N * number arcs in length

larcs = G.edges()
arcs_h = []
arcs = tuple(G.edges())
#print ("piiza", list(larcs[1]))
for i in range(len(larcs)):
    for k in range(N):
        list(larcs[i])
        ik.extend([k])
        arcs_h.append(tuple(ik))

arcs_h = tuple(arcs_h)

supply ={}
demand={}

#remove super source/sink nodes 

inflow =nx.get_node_attributes(G,'inflow')

#loop through attribute data
for i,j in inflow:
    for k in range(len(j)):
        if j[k]>0:
            supply[(i,k)]=j[k]
            nodes_h.pop(i)
            break
        if j[k]<0:
            demand[(i,k)] = -j[k]
            nodes_h.pop(i)
            break

#seperate capacity for arc specific and link capacity

capacity_h={}
capacity_arc={}

#k index for commodities
c=nx.get_edge_attributes(G,'capacity')

#extract capacity from networkx graph
for i,j in c:
    for k in range(len(j)):
        if k < N:
            x=tuple([k],)
            capacity_h[i +x]= j[k]
        else:
            capacity_arc[i]=j[k]



#create optimization model
m= GRB.Model('netflow')



flow = {}
for i,j,k in arcs_h:
    flow[i,j,k] = m.addVar(name ='flow_%s_%s_%s' % (i, j, k))

m.update()

for i,j,k in arcs_h:
        m.addConstr(flow[i,j,k] <= capacity_h[i,j,k],
                    'cap_%s_%s_%s' % (i,j,k))
        m.addConsr(flow[i,j,k] >=0 )


for i,j in arcs:
        m.addConstr(m.quicksum(flow[i,j,k] for i,j,k in arcs_h.select(i,j,'*'))
                    <= capacity_arc[i,j], 'arccap_%s_%s' % (i,j))

for j,h in nodes_h.iteritems():
        for k in h:
            m.addConstr(
                m.quicksum(flow[i,j,k] for i,j,k in arcs_h.select('*',j,k))==
                m.quicksum(flow[j, i, k] for j, i, k in arcs_h.select(j, '*', k)),
                'nodes_%s_%s' % (j,k))

for j,k in supply:
        m.addConstr(
            m.quicksum(flow[j, i, k] for j, i, k in arcs_h.select(j, '*', k)) <=
            supply[j,k],
            'supply_%s_%s' (j,k))
        m.addConstr(
            m.quicksum(flow[i, j, k] for i, j, k in arcs_h.select('*', j, k))== 0)


for j,k in demand:
        m.addConstr(
            m.quicksum(flow[i, j, k] for j, i, k in arcs_h.select('*',j , k)) <=
            demand[j,k],
            'supply_%s_%s' (j,k))
        m.addConstr(
            m.quicksum(flow[j, i, k] for j, i, k in arcs_h.select(j, '*', k))== 0)


m.update()

unmetDemand= m.LinExpr()

for j,k in demand:
        flow_demand=arcs_h.select('*',j,k)
        for x,y,z in flow_demand:
            unmetDemand.addTerms(-1/demand[j,k],flow[x,y,z])
        unmetDemand.addConstant(1)

m.setObjective(unmetDemand,GRB.MINIMIZE)

m.update()

m.optimize()


flow_solution=m.getAttr('x',flow)


print flow_solution
