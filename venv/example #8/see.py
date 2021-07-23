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


    ##########
    # Flow-conservation constraints
    Continuity = {}
    for a in range(len(commodity)):
        # for a in commodity:
        print("d", demandz[a])
        print ("originnn", origin[a])
        print ("destination", destination[a])
        # for y in commingnode:
        # print("x", x)
        # print("y", y)
        for h in commodity:
            print("h", h)
            for y in commingnode:
                print("y", y)
                if y == origin[a]:
                    print("test 1")
                    Continuity[a, y] = m.addConstrs(
                        (gp.quicksum(flow[h, y, k] for k in leavingnode) -
                         gp.quicksum(flow[h, i, y] for i in leavingnode) == demandz[a]), "node")


                elif y == destination[a]:
                    print("test 2")
                    Continuity[a, y] = m.addConstrs(
                        (gp.quicksum(flow[h, y, k] for k in leavingnode) -
                         gp.quicksum(flow[h, i, y] for i in leavingnode) == -(demandz[a])), "node")
                else:
                    print("test 3")
                    Continuity[a, y] = m.addConstrs(
                        (gp.quicksum(flow[h, y, k] for k in leavingnode) -
                         gp.quicksum(flow[h, i, y] for i in leavingnode) == 0), "node")



######################
  # Flow-conservation constraints
    for  a in range(len(commodity)):
            print("a",commodity [a])
            for y in leavingnode:
                print("d", demandz[a])
                print ("originnn", origin[a])
                print ("destination", destination[a])
                if y == origin[a]:
                    print("test 1")
                    m.addConstrs(
                        (gp.quicksum(flow[commodity[a], y, k] for y, k in pair.select(y, '*')) -
                         gp.quicksum(flow[commodity[a], i, y] for i, y in pair.select('*', y)) == demandz[a]
                          for y in leavingnode), "Continuity(%s)" % (commodity[a] ))


                elif y == destination[a]:
                    print("test 2")
                    m.addConstrs(
                        (gp.quicksum(flow[commodity[a], y, k] for y, k in pair.select(y, '*')) -
                         gp.quicksum(flow[commodity[a], i, y] for i, y in pair.select('*', y)) == -(demandz[a])
                         for y in leavingnode ),  "Continuity(%s)" % (commodity[a] ))
                else:
                    print("test 3")
                    m.addConstrs(
                        (gp.quicksum(flow[commodity[a], y, k] for y, k in pair.select(y, '*')) -
                         gp.quicksum(flow[commodity[a], i, y] for i, y in pair.select('*', y)) == 0
                          for y in leavingnode),  "Continuity(%s)" % (commodity[a] ))
                print("done")
######################
    # Flow-conservation constraints
    for  a in range(len(commodity)):
            print("a",commodity [a])
            for y in range(len(nodes)):
                print("d", demandz[a])
                print ("originnn", origin[a])
                print ("destination", destination[a])
                if leavingnode[y] == origin[a]:
                    print("leavignode[]",leavingnode[y] )
                    print("test 1")
                    m.addConstrs(
                        (flow.sum(commodity[a], leavingnode[y], '*') -
                         flow.sum(commodity[a], '*', leavingnode[y]) == demandz[a]), "Continuity(%s,%s)" % (commodity[a],leavingnode[y]))


                elif leavingnode[y]  == destination[a]:
                    print("test 2")
                    m.addConstrs(
                        (flow.sum(commodity[a], leavingnode[y], '*') -
                         flow.sum(commodity[a], '*', leavingnode[y]) == -(demandz[a])),  "Continuity(%s,%s)" % (commodity[a],leavingnode[y]))
                else:
                    print("test 3")
                    m.addConstrs(
                        (flow.sum(commodity[a], leavingnode[y], '*') -
                         flow.sum(commodity[a], '*', leavingnode[y]) == 0),  "Continuity(%s,%s)" % (commodity[a],leavingnode[y]))
                print("done")
#####################
 # Flow-conservation constraints
        for a in range(len(commodity)):
            print("a", commodity[a])
            for y in range(len(leavingnode)):
                print("d", demandz[a])
                print ("originnn", origin[a])
                print ("destination", destination[a])
                if leavingnode[y] == origin[a]:
                    print("test 1")
                    m.addConstrs(
                        (gp.quicksum(flow[commodity[a], y, k] for y, k in pair.select(y, '*')) -
                         gp.quicksum(flow[commodity[a], i, y] for i, y in pair.select('*', y)) == demandz[a]
                         ), "Continuity(%s,%s)" % (commodity[a],leavingnode[y]))


                elif leavingnode[y] == destination[a]:
                    print("test 2")
                    m.addConstrs(
                        (gp.quicksum(flow[commodity[a], y, k] for y, k in pair.select(y, '*')) -
                         gp.quicksum(flow[commodity[a], i, y] for i, y in pair.select('*', y)) == -(demandz[a])
                         ), "Continuity(%s)" % (commodity[a]))
                else:
                    print("test 3")
                    m.addConstrs(
                        (gp.quicksum(flow[commodity[a], y, k] for y, k in pair.select(y, '*')) -
                         gp.quicksum(flow[commodity[a], i, y] for i, y in pair.select('*', y)) == 0
                        ), "Continuity(%s)" % (commodity[a]))
                print("done")