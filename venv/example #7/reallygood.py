
#https://www.inf.ufpr.br/andre/textos/Understanding_and_Using_Linear_Programming.pdf
#https://energie.labs.fhv.at/~kr/effsys-en/Gurobi.html

import gurobipy as gp
from gurobipy import GRB

nodes_list = ['s', 'a', 'b', 'c', 'd', 'e', 't']
data_dict = {('s','a'):3,
             ('s','b'):1,
             ('s','c'):1,
             ('a','b'):1,
             ('a','d'):1,
             ('b','e'):3,
             ('c','e'):4,
             ('c','d'):4,
             ('d','t'):4,
             ('e','t'):1
            }
edges_list = list(data_dict.keys())


# create optimization model:
model = gp.Model('maximum network flow')

# create tuplelist of edges from dictionary keys:
edges_tuplelist = gp.tuplelist(edges_list)
print(edges_tuplelist)
ub = data_dict
lb = {edge:-val for (edge,val) in data_dict.items()}

# create gurobi variables:
flow = model.addVars(edges_tuplelist, name="flow", lb=lb, ub=ub)

model.setObjective(flow['s','a'] + flow['s','b'] + flow['s','c'], gp.GRB.MAXIMIZE)
# model.setObjective(flow.sum('s','*'), gp.GRB.MAXIMIZE)

inter_nodes_list = nodes_list
inter_nodes_list.remove('s')
inter_nodes_list.remove('t')

model.addConstrs( (flow.sum('*',j) == flow.sum(j,'*')
                   for j in inter_nodes_list), "node");

# print the model:
model.update()
model.display()
if True:  # suppress verbose output
    model.Params.OutputFlag = 0

# optimize/solve the model:
model.optimize()

# print solution: optimal value and optimal point
print('Obj: %g' % model.objVal)
#print(f"optimal value = {model.objVal:.2f}")
for v in model.getVars():
        print('%s %g' % (v.varName, v.x))
