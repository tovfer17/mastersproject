import gurobipy as gp
from openpyxl import load_workbook



# Objects
class Arc:
    def __init__(self, origin, destination, cost, capacity):
        self.From = origin
        self.To = destination
        self.Cost = cost
        self.Capac = capacity


class Commodity:
    def __init__(self, origin, destination, quantity):
        self.From = origin
        self.To = destination
        self.Quant = quantity


class Node:
    def __init__(self):
        self.InLinks = []
        self.OutLinks = []

    def addInLinks(self, Node):
        self.InLinks.append(Node)  # add new InLink to the node

    def addOutLinks(self, Node):
        self.OutLinks.append(Node)

if __name__ == '__main__':
# Input excel files with arcs data(sheet 1) and commodities data (sheet2)
# Generate lista to store 'objects'
    #Arcs = [(1,2,1,20),(1,3,1,10),(2,3,2,10),(2,4,4,20),(3,4,8,40),(3,5,5,10),(4,5,3,30)]
    #Nodes = [1,2,3,4,5]
    #Commodities = [(1,4,15),(1,5,5),(2,5,10),(3,5,5)]
    Arcs = []
    Nodes = []
    Commodities = []
# Open input file(excel) that is in the current folder



    loc1=("/Users/fer/PycharmProjects/project/Input_lecct.xlsx")

#loc1 = (r"C:\Users\rithi\pyprojnew\input_lecct.xls")


    wb = load_workbook(filename=loc1, read_only=True)
    ws = wb['Arcs']

    for row in ws.rows:
        for cell in row:
            print(cell.value)

# Close the workbook after reading


    #wb = openpyxl.load_workbook(loc1, read_only=True)
    #sheet=wb.active
    List_arcs = tuple(wb["Arcs"].iter_rows())
    List_commo = tuple(wb["Commodities"].iter_rows())

    print(List_commo)

    #play_data = wb['Arcs']
    #print(play_data)

    wb.close()

    # Objective function
    model = gp.Model("MCF")
    x = {}
    for m in range(len(Arcs)):
        for k in range(len(Commodities)):
            x[k, Arcs[m].From, Arcs[m].To] = model.addVar(obj = Arcs[m].Cost, vtype = "C",
                                                          name = "x(%d, %d, %d)" % (k, Arcs[m].From, Arcs[m].To))
    model.update()
    # constraints
     # capacity
    Capacity = {}
    for m in range(len(Arcs)):
                Capacity[Arcs[m].From, Arcs[m].To] = model.addConstr(gp.quicksum(x[k.Arcs[m].From.Arcs[m].To]
                                                                             for k in range(len(Commodities))),
                                                                    '<=', Arcs[m].Capac, name = 'Capacity(%d)' % (m))
    # conservation constraint
    Continuity = {}
    for k in range(len(Commodities)):
        for j in range(len(Nodes)):
                if j == Commodities[k].From:
                    Continuity[k, j] = model.addConstr(gp.quicksum(x[k, j, p] for p in Nodes[j].OutLinks
                                                     - gp.quicksum(x[k, p, j] for p in Nodes[j].InLinks)),
                                            '=', Commodities[k].Quant, name = 'Continuity(%d, %d)' % (k, j))

                elif j == Commodities[k].To:
                    Continuity[k, j] = model.addConstr(gp.quicksum(x[k, j, p] for p in Nodes[j].OutLinks)
                                                 - gp.quicksum(x[k, p, j] for p in Nodes[j].InLinks),
                                         '=', -Commodities[k].Quant, name = 'Continuity(%d, %d)' % (k, j))
                else:
                     Continuity[k, j] = model.addConstr(gp.quicksum(x[k, j, p] for p in Nodes[j].OutLinks)
                                                     - gp.quicksum( x[k, p, j] for p in Nodes[j].InLinks),
                                        '=', 0, name = 'Continuity(%d, %d)' % (k, j))


    model.update()
    model.write("MCF_Model.lp")
    model.optimize()

    status = model.status
    if status != gp.GRB.Status.OPTIMAL:
      if status == gp.GRB.Status.UNBOUNDED:
                print("The model cannot be solved because it is unbounded")
      elif status == gp.GRB.Status.INFEASIBLE:
                print('The model is infeasible; compute IIS')
                model.computeIIS()
                print('\n The following constraints cannot be satisfied:')
                for c in model.getConstrs():
                    if c.IISConstrs():
                          print('%s' % c.constrName)
      elif status != gp.GRB.Status.INF_OR_UNBD:
                print('Optimization was stopped with status %d' % status)
    exit(0)






