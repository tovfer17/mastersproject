#https://www.inf.ufpr.br/andre/textos/Understanding_and_Using_Linear_Programming.pdf
#https://energie.labs.fhv.at/~kr/effsys-en/Gurobi.html
#https://www.youtube.com/watch?v=RqSMklpCTtA
#https://www.youtube.com/watch?v=y095F10iNzk


import gurobipy as gp
from gurobipy import GRB

commodities = ['Pencils','Pens']
nodes_list = ['Detroit', 'Boston', 'New York', 'Seattle', 'LA','JerseyCity',  'Tokyo' ]


edges,data_dict = gp.multidict({('Detroit','Boston'):3,
             ('Detroit','New York'):1,
             ('Detroit', 'Seattle'):1,
             ('Boston', 'New York'): 1,
             ('Boston', 'LA'): 1,
             ('New York',  'JerseyCity'):3,
             ('Seattle',  'JerseyCity'):4,
             ('Seattle',  'LA'):4,
             ('LA', 'Tokyo'): 4,
             ('JerseyCity', 'Tokyo'): 1
            })

cost = {
    ('Pencils', 'Detroit', 'Boston'):   10,
    ('Pencils', 'Detroit', 'New York'): 20,
    ('Pencils', 'Detroit', 'Seattle'):  30,
    ('Pencils', 'Detroit', 'LA'):      40,
    ('Pencils', 'Detroit', 'JerseyCity'): 10,
    ('Pencils', 'Detroit', 'Tokyo'): 20,
    ('Pens',    'Detroit',  'Boston'):   10,
    ('Pens',    'Detroit',  'New York'): 20,
    ('Pens',    'Detroit',  'Seattle'):  30,
    ('Pens',    'Detroit',  'LA'): 40,
    ('Pens', 'Detroit', 'JerseyCity'): 50,
    ('Pens', 'Detroit', 'Tokyo'): 25,
}



inflow = {
    ('Pencils', 'Detroit'):   50,
    ('Pencils', 'Boston'):   -50,
    ('Pencils', 'New York'): -50,
    ('Pencils', 'Seattle'):  -10,
    ('Pencils', 'LA'): -10,
    ('Pencils', 'JerseyCity'): -10,
    ('Pencils',  'Tokyo'):   60,
    ('Pens',    'Detroit'):    40,
    ('Pens',    'Boston'):   -40,
    ('Pens',    'New York'): -30,
    ('Pens',    'Seattle'):  -30,
    ('Pens', 'LA'): -10,
    ('Pens', 'JerseyCity'): -10,
    ('Pens', 'Tokyo'): 60,
}

# create optimization model:
model = gp.Model('maximum network flow')

# create tuplelist of edges from dictionary keys:
edges_tuplelist = gp.tuplelist(edges)
print(edges_tuplelist)
ub = data_dict
lb = {edge:-val for (edge,val) in data_dict.items()}

#print("edgestupleist", edges_tuplelist)
# create gurobi variables:
flow = model.addVars(commodities,edges_tuplelist, obj=cost, name="flow", lb=lb, ub=ub)

#for h in commodities:
#model.setObjective(flow['Pencils','Detroit','Boston'] + flow['Pencils','Detroit','New York'] + flow['Pencils', 'Detroit','Seattle']+ flow['Pens','Detroit','Boston'] + flow['Pens','Detroit','New York'] + flow['Pens', 'Detroit','Seattle'])
#model.setObjective(sum(flow['Detroit','*'], gp.GRB.MAXIMIZE))



inter_nodes_list = nodes_list

inter_nodes_list.remove('Detroit')
inter_nodes_list.remove('Tokyo')
print("inter", inter_nodes_list)


#model.addConstrs( (flow.sum(h,'*',j) == flow.sum(h,j,'*')
               #   for h in commodities for j in inter_nodes_list), "node");

#for x, y in edges_tuplelist:
  #  model.addConstr(gp.quicksum(flow[h, x, y] for h in commodities) <= data_dict[x, y],
               # 'cap_%s_%s' % (x, y))


#for h in commodities:
model.addConstrs( (flow.sum(h,'*',j) +  inflow[h, j] == flow.sum(h,j,'*')
                   for h in commodities for j in inter_nodes_list), "node")

# print the model:
model.optimize()
model.update()
model.display()
if True:  # suppress verbose output
    model.Params.OutputFlag = 0

# optimize/solve the model:
model.optimize()
print("hi", model.status)

# print solution: optimal value and optimal point
print('Obj: %g' % model.objVal)
#print(f"optimal value = {model.objVal:.2f}")
for v in model.getVars():
        print('%s %g' % (v.varName, v.x))
