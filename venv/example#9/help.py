"""
Authors: www.tropofy.com and www.gurobi.com

Copyright 2015 Tropofy Pty Ltd, all rights reserved.
Copyright 2013, Gurobi Optimization, Inc.

This source file (where not indicated as under the copyright of Gurobi)
is part of Tropofy and governed by the Tropofy terms of service
available at: http://www.tropofy.com/terms_of_service.html

Parts of the formulation provided by Gurobi have been modified.
The original example is in the Gurobi installation in the example file dietmodel.py

Used with permission.

This source file is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the license files for details.
"""
import pkg_resources
import gurobipy  # Note eclipse has problems importing quicksum so we dont import selectively
from sqlalchemy.types import Text, Float
from sqlalchemy.schema import Column, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from simplekml import Kml, Style, IconStyle, Icon, LineStyle

from tropofy.app import AppWithDataSets, Step, StepGroup
from tropofy.widgets import ExecuteFunction, SimpleGrid, KMLMap, Chart
from tropofy.database.tropofy_orm import DataSetMixin
from tropofy.file_io import read_write_xl


class Commodity(DataSetMixin):
    name = Column(Text, nullable=False)

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_table_args(cls):
        return (UniqueConstraint('data_set_id', 'name'),)


class Node(DataSetMixin):
    name = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    @classmethod
    def get_table_args(cls):
        return (UniqueConstraint('data_set_id', 'name'),)


class Arc(DataSetMixin):
    orig_name = Column(Text, nullable=False)
    dest_name = Column(Text, nullable=False)
    capacity = Column(Float, nullable=False)

    # The primaryjoin argument to relationship is only needed when there is ambiguity
    orig_node = relationship(Node, primaryjoin="and_(Arc.data_set_id==Node.data_set_id, Arc.orig_name==Node.name)")
    dest_node = relationship(Node, primaryjoin="and_(Arc.data_set_id==Node.data_set_id, Arc.dest_name==Node.name)")

    @classmethod
    def get_table_args(cls):
        return (
            UniqueConstraint('data_set_id', 'orig_name', 'dest_name'),
            ForeignKeyConstraint(['orig_name', 'data_set_id'], ['node.name', 'node.data_set_id'], ondelete='CASCADE',
                                 onupdate='CASCADE'),
            ForeignKeyConstraint(['dest_name', 'data_set_id'], ['node.name', 'node.data_set_id'], ondelete='CASCADE',
                                 onupdate='CASCADE')
        )


class Cost(DataSetMixin):
    orig_name = Column(Text, nullable=False)
    dest_name = Column(Text, nullable=False)
    commod_name = Column(Text, nullable=False)
    cost = Column(Float, nullable=False)

    # The primaryjoin argument to relationship is only needed when there is ambiguity
    orig_node = relationship(Node, primaryjoin="and_(Cost.data_set_id==Node.data_set_id, Cost.orig_name==Node.name)")
    dest_node = relationship(Node, primaryjoin="and_(Cost.data_set_id==Node.data_set_id, Cost.dest_name==Node.name)")
    commodity = relationship(Commodity)

    @classmethod
    def get_table_args(cls):
        return (
            UniqueConstraint('data_set_id', 'orig_name', 'dest_name', 'commod_name'),
            ForeignKeyConstraint(['orig_name', 'data_set_id'], ['node.name', 'node.data_set_id'], ondelete='CASCADE',
                                 onupdate='CASCADE'),
            ForeignKeyConstraint(['dest_name', 'data_set_id'], ['node.name', 'node.data_set_id'], ondelete='CASCADE',
                                 onupdate='CASCADE'),
            ForeignKeyConstraint(['commod_name', 'data_set_id'], ['commodity.name', 'commodity.data_set_id'],
                                 ondelete='CASCADE', onupdate='CASCADE'),
            ForeignKeyConstraint(['orig_name', 'dest_name', 'data_set_id'],
                                 ['arc.orig_name', 'arc.dest_name', 'arc.data_set_id'], ondelete='CASCADE',
                                 onupdate='CASCADE'),
        )


class Inflow(DataSetMixin):
    commod_name = Column(Text, nullable=False)
    node_name = Column(Text, nullable=False)
    flow = Column(Float, nullable=False)

    @classmethod
    def get_table_args(cls):
        return (
            UniqueConstraint('data_set_id', 'commod_name', 'node_name'),
            ForeignKeyConstraint(['commod_name', 'data_set_id'], ['commodity.name', 'commodity.data_set_id'],
                                 ondelete='CASCADE', onupdate='CASCADE'),
            ForeignKeyConstraint(['node_name', 'data_set_id'], ['node.name', 'node.data_set_id'], ondelete='CASCADE',
                                 onupdate='CASCADE')
        )


class NetworkFlow(DataSetMixin):
    orig_name = Column(Text, nullable=False)
    dest_name = Column(Text, nullable=False)
    commod_name = Column(Text, nullable=False)
    flow = Column(Float, nullable=False)

    # The primaryjoin argument to relationship is only needed when there is ambiguity
    orig_node = relationship(Node,
                             primaryjoin="and_(NetworkFlow.data_set_id==Node.data_set_id, NetworkFlow.orig_name==Node.name)")
    dest_node = relationship(Node,
                             primaryjoin="and_(NetworkFlow.data_set_id==Node.data_set_id, NetworkFlow.dest_name==Node.name)")
    commodity = relationship(Commodity)

    @classmethod
    def get_table_args(cls):
        return (
            UniqueConstraint('data_set_id', 'orig_name', 'dest_name', 'commod_name'),
            ForeignKeyConstraint(['orig_name', 'data_set_id'], ['node.name', 'node.data_set_id'], ondelete='CASCADE',
                                 onupdate='CASCADE'),
            ForeignKeyConstraint(['dest_name', 'data_set_id'], ['node.name', 'node.data_set_id'], ondelete='CASCADE',
                                 onupdate='CASCADE'),
            ForeignKeyConstraint(['commod_name', 'data_set_id'], ['commodity.name', 'commodity.data_set_id'],
                                 ondelete='CASCADE', onupdate='CASCADE'),
            ForeignKeyConstraint(['orig_name', 'dest_name', 'data_set_id'],
                                 ['arc.orig_name', 'arc.dest_name', 'arc.data_set_id'], ondelete='CASCADE',
                                 onupdate='CASCADE'),
        )


class MapNodeInput(KMLMap):

    def get_kml(self, app_session):
        kml = Kml()

        node_style = Style(iconstyle=IconStyle(scale=0.8, icon=Icon(
            href='https://maps.google.com/mapfiles/kml/paddle/blu-circle-lv.png')))
        node_folder = kml.newfolder(name="Nodes")
        for p in [node_folder.newpoint(name=n.name, coords=[(n.longitude, n.latitude)]) for n in
                  app_session.data_set.query(Node).all()]:
            p.style = node_style

        return kml.kml()


class MapArcInput(KMLMap):

    @staticmethod
    def get_cycled_hex_colour(n):
        hex_colours = ['FFC86602', 'FF0101F9', 'FF0FB5F2', 'FF3B9300', ]
        return hex_colours[n % 1]

    def get_kml(self, app_session):
        kml = Kml()

        node_style = Style(iconstyle=IconStyle(scale=0.8, icon=Icon(
            href='https://maps.google.com/mapfiles/kml/paddle/blu-circle-lv.png')))
        node_folder = kml.newfolder(name="Nodes")
        for p in [node_folder.newpoint(name=n.name, coords=[(n.longitude, n.latitude)]) for n in
                  app_session.data_set.query(Node).all()]:
            p.style = node_style

        arc_folder = kml.newfolder(name="Arcs")
        Arcs = app_session.data_set.query(Arc).all()
        for arc in Arcs:
            arc_style = Style(linestyle=LineStyle(color=MapArcInput.get_cycled_hex_colour(Arcs.index(arc)), width=4))
            l = arc_folder.newlinestring(name="arc", coords=[(arc.orig_node.longitude, arc.orig_node.latitude),
                                                             (arc.dest_node.longitude, arc.dest_node.latitude)])
            l.style = arc_style

        return kml.kml()


class MapFlowOutput(KMLMap):

    @staticmethod
    def get_cycled_hex_colour(n):
        hex_colours = ['FFC86602', 'FF0101F9', 'FF0FB5F2', 'FF3B9300', ]
        return hex_colours[n % 4]

    def get_kml(self, app_session):

        kml = Kml()

        node_style = Style(iconstyle=IconStyle(scale=0.8, icon=Icon(
            href='https://maps.google.com/mapfiles/kml/paddle/blu-circle-lv.png')))
        node_folder = kml.newfolder(name="Nodes")
        for p in [node_folder.newpoint(name=n.name, coords=[(n.longitude, n.latitude)]) for n in
                  app_session.data_set.query(Node).all()]:
            p.style = node_style

        node_index = {}
        node_counter = 0

        arc_folder = kml.newfolder(name="Arcs")
        for flow in app_session.data_set.query(NetworkFlow).all():

            if not node_index.get(flow.orig_name, None):
                node_index.update({flow.orig_name: node_counter})
                node_counter += 1

            arc_style = Style(
                linestyle=LineStyle(color=MapFlowOutput.get_cycled_hex_colour(node_index.get(flow.orig_name)), width=4))
            l = arc_folder.newlinestring(name="arc", coords=[(flow.orig_node.longitude, flow.orig_node.latitude),
                                                             (flow.dest_node.longitude, flow.dest_node.latitude)])
            l.style = arc_style

        return kml.kml()


class NetworkInflowChart(Chart):

    def get_chart_type(self, app_session):
        return Chart.COLUMNCHART

    def get_table_schema(self, app_session):
        commodities = dict([(c.name, ("number", c.name)) for c in app_session.data_set.query(Commodity).all()])
        commodities["node"] = ("string", "Node")
        return commodities

    def get_table_data(self, app_session):
        data = []
        for n in app_session.data_set.query(Node).all():
            row = {"node": n.name}
            for c in app_session.data_set.query(Commodity).all():
                row[c.name] = sum([f.flow for f in app_session.data_set.query(NetworkFlow).all() if
                                   inflow_matches_node_and_commodity(f, n, c)])
            data.append(row)
        return data

    def get_column_ordering(self, app_session):
        return ["node"] + [n.name for n in app_session.data_set.query(Commodity).all()]

    def get_chart_options(self, app_session):
        return {'title': 'Node Inflows'}


class NetworkOutflowChart(Chart):

    def get_chart_type(self, app_session):
        return Chart.COLUMNCHART

    def get_table_schema(self, app_session):
        commodities = dict([(c.name, ("number", c.name)) for c in app_session.data_set.query(Commodity).all()])
        commodities["node"] = ("string", "Node")
        return commodities

    def get_table_data(self, app_session):
        data = []
        for n in app_session.data_set.query(Node).all():
            row = {"node": n.name}
            for c in app_session.data_set.query(Commodity).all():
                row[c.name] = sum([f.flow for f in app_session.data_set.query(NetworkFlow).all() if
                                   outflow_matches_node_and_commodity(f, n, c)])
            data.append(row)
        return data

    def get_column_ordering(self, app_session):
        return ["node"] + [n.name for n in app_session.data_set.query(Commodity).all()]

    def get_chart_options(self, app_session):
        return {'title': 'Node Outflows'}


class ExecuteSolverFunction(ExecuteFunction):

    def get_button_text(self, app_session):
        return "Solve Network Flow Problem"

    def execute_function(self, app_session):
        '''
        Copyright 2013, Gurobi Optimization, Inc.

        Solve a multi-commodity flow problem.  Two products ('Pencils' and 'Pens')
        are produced in 2 cities ('Detroit' and 'Denver') and must be sent to
        warehouses in 3 cities ('Boston', 'New York', and 'Seattle') to
        satisfy demand ('inflow[h,i]').

        Flows on the transportation network must respect arc capacity constraints
        ('capacity[i,j]'). The objective is to minimize the sum of the arc
        transportation costs ('cost[i,j]').
        '''

        app_session.task_manager.send_progress_message("Optimisation Started")

        commodities = [h.name for h in app_session.data_set.query(Commodity).all()]
        nodes = [n.name for n in app_session.data_set.query(Node).all()]
        arcs, capacity = gurobipy.multidict(
            dict([((a.orig_name, a.dest_name), a.capacity) for a in app_session.data_set.query(Arc).all()]))
        arcs = gurobipy.tuplelist(arcs)
        cost = dict(
            [((c.commod_name, c.orig_name, c.dest_name), c.cost) for c in app_session.data_set.query(Cost).all()])
        inflow = dict([((i.commod_name, i.node_name), i.flow) for i in app_session.data_set.query(Inflow).all()])

        # Create optimization model
        m = gurobipy.Model('netflow')

        # Create variables
        flow = {}
        for h in commodities:
            for i, j in arcs:
                flow[h, i, j] = m.addVar(ub=capacity[i, j], obj=cost[h, i, j],
                                         name='flow_%s_%s_%s' % (h, i, j))
        m.update()

        # Arc capacity constraints
        for i, j in arcs:
            m.addConstr(gurobipy.quicksum(flow[h, i, j] for h in commodities) <= capacity[i, j],
                        'cap_%s_%s' % (i, j))

        # NetworkFlow conservation constraints
        for h in commodities:
            for j in nodes:
                m.addConstr(
                    gurobipy.quicksum(flow[h, i, j] for i, j in arcs.select('*', j)) +
                    inflow[h, j] ==
                    gurobipy.quicksum(flow[h, j, k] for j, k in arcs.select(j, '*')),
                    'node_%s_%s' % (h, j))

        # Compute optimal solution
        m.optimize()

        # Print solution
        app_session.data_set.query(NetworkFlow).delete()

        if m.status == gurobipy.GRB.status.OPTIMAL:
            solution = m.getAttr('x', flow)
            for h in commodities:
                for i, j in arcs:
                    if solution[h, i, j] > 0:
                        app_session.data_set.add(
                            NetworkFlow(orig_name=i, dest_name=j, commod_name=h, flow=solution[h, i, j]))

        status = m.status
        if status == gurobipy.GRB.status.INF_OR_UNBD or status == gurobipy.GRB.status.INFEASIBLE or status == gurobipy.GRB.status.UNBOUNDED:
            app_session.task_manager.send_progress_message(
                'The model cannot be solved because it is infeasible or unbounded')
        else:
            app_session.task_manager.send_progress_message('Total cost = %s' % (str(m.objVal)))
        app_session.task_manager.send_progress_message("Optimisation Finished")


class NetworkFlowOptimisationApp(AppWithDataSets):

    def get_name(self):
        return 'Network Flow Optimiser'

    def get_examples(self):
        return {"Demo data set from Gurobi": self.load_network_flow_example_data}

    def get_static_content_path(self, app_session):
        return pkg_resources.resource_filename('te_gurobi_network_flow', 'static')

    def get_gui(self):
        step_group1 = StepGroup(name='Input')
        step_group1.add_step(Step(
            name='Commodities',
            widgets=[SimpleGrid(Commodity)],
            help_text="Enter the set of commodities"
        ))

        step_group1.add_step(Step(
            name='Nodes',
            widgets=[
                SimpleGrid(Node),
                MapNodeInput(),
            ],
            help_text="Enter the set of Nodes"
        ))

        step_group1.add_step(Step(
            name='Arcs',
            widgets=[
                SimpleGrid(Arc),
                MapArcInput()
            ],
            help_text="Enter the set of Arcs"
        ))

        step_group1.add_step(Step(
            name='Costs',
            widgets=[SimpleGrid(Cost)],
            help_text="Enter the costs associated with each Arc"
        ))

        step_group1.add_step(Step(
            name='Inflows',
            widgets=[SimpleGrid(Inflow)],
            help_text="Enter the set of inflow requirements for each Node"
        ))

        step_group2 = StepGroup(name='Engine')
        step_group2.add_step(Step(name='Solve Network Flow Problem', widgets=[ExecuteSolverFunction()]))

        step_group3 = StepGroup(name='Output')
        step_group3.add_step(Step(
            name='Flows',
            widgets=[SimpleGrid(NetworkFlow)],
            help_text="Optimal Flows"
        ))

        step_group3 = StepGroup(name='Output')
        step_group3.add_step(Step(
            name='Flows',
            widgets=[
                {'widget': NetworkInflowChart(), 'cols': 6},
                {'widget': NetworkOutflowChart(), 'cols': 6},
                {'widget': MapFlowOutput(), 'cols': 12},
                {'widget': SimpleGrid(NetworkFlow), 'cols': 12},
            ],
            help_text="The grid below shows the optimal Requests selected."
        ))

        return [step_group1, step_group2, step_group3]

    def get_icon_url(self):
        return "/{}/static/{}/network_flow.png".format(
            self.url_name,
            self.get_app_version(),
        )

    @staticmethod
    def load_network_flow_example_data(app_session):
        read_write_xl.ExcelReader.load_data_from_excel_file_on_disk(
            app_session,
            pkg_resources.resource_filename('te_gurobi_network_flow', 'network_flow_example_data.xlsx')
        )


def inflow_matches_node_and_commodity(flow, node, commodity):
    return flow.dest_name == node.name and flow.commod_name == commodity.name


def outflow_matches_node_and_commodity(flow, node, commodity):
    return flow.orig_name == node.name and flow.commod_name == commodity.name
