
import networkx as nx
# importing matplotlib.pyplot
import matplotlib.pyplot as plt
import gurobipy as grb



#https://networkx.org/documentation/stable/reference/classes/digraph.html
G = nx.DiGraph()
H = nx.path_graph(6)
G.add_nodes_from(H)
G.add_edges_from([(0, 1), (1, 3),(3,5),(4,5),(4,3),(3,2),(2,4),(4,1),(0,2)])


print("Total number of nodes: ", int(G.number_of_nodes()))
print("Total number of edges: ", int(G.number_of_edges()))
print("List of all nodes: ", list(G.nodes()))
print("List of all edges: ", list(G.edges(data=True)))
print("Degree for all nodes: ", dict(G.degree()))
print("Total number of self-loops: ", (nx.selfloop_edges(G)))
print("List of all nodes with self-loops: ", list(nx.nodes_with_selfloops(G)))


# https://networkx.org/documentation/stable//reference/generated/networkx.classes.function.get_node_attributes.html
G.add_node(0 ,inflow ="0")
G.add_node(1 ,inflow ="1000")
G.add_node(2,inflow ="4700")
G.add_node(3,inflow ="5000")
G.add_node(4,inflow ="5400")
G.add_node(5,inflow ="7700")
print("list of inflows: ", list(G.nodes(data=True)))

nodes_h = nx.get_node_attributes(G, 'inflow')
nodes = G.nodes()

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
        print( nodes_h[i][k])

    if N == 0:
         N = len(j)

#for each arc i,j add index h for N commodities as third index of tuple
#list = N * number arcs in length

larcs = G.edges()
arcs_h = []

arcs = tuple(G.edges())
for i in range(len(larcs)):
    for k in range(N):
        ik = list(larcs[i])
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
m= Model('netflow')

flow = {}
for i,j,k in arcs_h:
    flow[i,j,k] = m.addVar(name ='flow_%s_%s_%s' % (i, j, k))
m.update()