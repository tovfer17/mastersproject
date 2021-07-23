# Create optimization model
m = gp.Model('netflow')

# Create variables
flow = m.addVars(commodities, arcs, obj=cost, name="flow")

# Arc-capacity constraints
m.addConstrs(
    (flow.sum('*', i, j) <= capacity[i, j] for i, j in arcs), "cap")

# Equivalent version using Python looping
# for i, j in arcs:
#   m.addConstr(sum(flow[h, i, j] for h in commodities) <= capacity[i, j],
#               "cap[%s, %s]" % (i, j))


# Flow-conservation constraints
m.addConstrs(
    (flow.sum(h, '*', j) + inflow[h, j] == flow.sum(h, j, '*')
        for h in commodities for j in nodes), "node")

# Alternate version:
# m.addConstrs(
#   (gp.quicksum(flow[h, i, j] for i, j in arcs.select('*', j)) + inflow[h, j] ==
#     gp.quicksum(flow[h, j, k] for j, k in arcs.select(j, '*'))
#     for h in commodities for j in nodes), "node")

# Compute optimal solution
m.optimize()
#################################################################
for h in commodity:
    for x, y in pair:
        print("x", x)
        print("y", y)
        for a in range(len(commodity)):
            print ("originnn", origin[a])
            print ("destination", destination[a])
            if y == origin[a]:
                print("test 1")
                m.addConstrs(
                    gp.quicksum(flow[h, y, '*']) -
                    gp.quicksum(flow[h, '*', y]), '=', (abs(demandz[h, o, d])
                                                        for h in commodity for o in origin for d in destination),
                    name="node[%s, %s]" % (h, y))


            elif y == destination[a]:
                print("test 2")
                m.addConstrs(
                    gp.quicksum(flow[h, y, k] for y, k in pair.select(y, '*')) -
                    gp.quicksum(flow[h, x, y] for x, y in pair.select('*', y)), '=', (demandz[h, o, d]
                                                                                      for h in commodity for o in origin
                                                                                      for d in destination),
                    name="node[%s, %s]" % (h, y))
            else:
                print("test 3")
                m.addConstrs(
                    gp.quicksum(flow[h, y, k] for y, k in pair.select(y, '*')) -
                    gp.quicksum(flow[h, x, y] for x, y in pair.select('*', y)), '=', 0, name="node[%s, %s]" % (h, y))

#######################################

    for a in range(len(commodity)):
        for x, y in pair:
            print("x",x)
            print("y", y)
            print ("originnn", origin[a])
            print ("destination", destination[a])
            if y == origin[a]:
                    print("test 1")
                    m.addConstrs(
                        (flow.sum(flow[h, y, '*']) -
                          flow.sum(flow[h, '*', y]) == abs(demandz[h, o, d])
                         for h in commodity for y in nodes for o in origin for d in destination ),  "node[%s, %s]")


            elif y == destination[a]:
                    print("test 2")
                    m.addConstrs(
                        (flow.sum(flow[h, y, '*']) -
                         flow.sum(flow[h, '*', y]) == demandz[h, o, d]
                        for h in commodity for y in nodes for o in origin for d in destination), "node[%s, %s]" )
            else:
                    print("test 3")
                    m.addConstrs(
                        (flow.sum(flow[h, y, '*'])  -
                         flow.sum(flow[h, '*', y]) == 0  for h in commodity for y in leavingnode), "node[%s, %s]" )