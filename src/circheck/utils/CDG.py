from enum import Enum, auto
from StaticCheck import SignalType
from tqdm import tqdm
from collections import defaultdict


class NodeType(Enum):
    SIGNAL = auto()
    CONSTANT = auto()


class EdgeType(Enum):
    DEPEND = auto()
    CONSTRAINT = auto()


class Node:
    def __init__(self, locate, id, node_type, signal_type, component):
        self.locate = locate
        self.id = id
        self.node_type = node_type
        self.signal_type = signal_type
        self.component = component
        # node == edge.node_from
        self.flow_to = []
        # node = edge.node_to
        self.flow_from = []

    def __repr__(self):
        return f"Node({self.id})"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id

    def is_signal(self):
        return self.node_type == NodeType.SIGNAL

    def is_signal_in(self):
        return self.is_signal() and self.signal_type == SignalType.INPUT

    def is_signal_out(self):
        return self.is_signal() and self.signal_type == SignalType.OUTPUT

    def is_signal_in_of(self, component):
        return self.is_signal_in() and self.component == component

    def is_signal_out_of(self, component):
        return self.is_signal_out() and self.component == component

    def is_signal_of(self, component):
        return self.is_signal() and self.component == component


class Edge:
    def __init__(self, node_from, node_to, edge_type, name, ast, count_constraint=0):
        self.node_from = node_from
        self.node_to = node_to
        self.edge_type = edge_type
        self.name = name
        self.ast = ast
        self.count_constraint = count_constraint


def getEdgeName(edge_type, nFrom, nTo):
    if edge_type == EdgeType.DEPEND:
        return f"data:{nFrom.id}-{nTo.id}"
    else:
        return f"constraint:{nFrom.id}-{nTo.id}"


class CircuitDependenceGraph:
    def __init__(self, edges, nodes, name, components):
        self.edges = edges
        self.nodes = nodes
        self.name = name
        self.components = components
        self.node_flows_to = {}
        self._constraint_cache = {}
        self._constraint_cache_second = {}
        self._depend_cache = {}
        self._visit_state = {}
        self.params = None
        self.is_constraint_build = False

    def is_signal(self, node):
        return node.node_type == NodeType.SIGNAL

    def is_signal_in(self, node):
        return self.is_signal(node) and node.signal_type == SignalType.INPUT

    def is_signal_out(self, node):
        return self.is_signal(node) and node.signal_type == SignalType.OUTPUT

    def is_signal_of(self, node, component):
        return self.is_signal(node) and node.component == component

    def is_signal_in_of(self, node, component):
        return self.is_signal_of(node, component) and self.is_signal_in(node)

    def is_signal_out_of(self, node, component):
        return self.is_signal_of(node, component) and self.is_signal_out(node)

    def has_path_depend(self, a: Node, b: Node) -> bool:
        cache = self._depend_cache
        if a.id in cache:
            return b.id in cache[a.id]
        visited = set()
        stack = [a]
        while stack:
            current = stack.pop()
            if current.id in visited:
                continue
            visited.add(current.id)
            for edge in current.flow_to:
                if edge.edge_type == EdgeType.DEPEND:
                    stack.append(edge.node_to)
        cache[a.id] = visited
        return b.id in visited

    def has_path_constraint(self, a: Node, b: Node) -> bool:
        cache = self._constraint_cache
        if a.id in cache and b.id in cache[a.id]:
            return True
        if a.id in self._visit_state:
            stack = self._visit_state[a.id]
            visited = cache[a.id]
        else:
            visited = set()
            stack = [a]
        while stack:
            current = stack.pop()
            if current.id in visited:
                continue
            visited.add(current.id)
            for edge in current.flow_to:
                if edge.edge_type == EdgeType.CONSTRAINT:
                    stack.append(edge.node_to)
            if current.id == b.id:
                cache[a.id] = visited
                self._visit_state[a.id] = stack
                return True
        cache[a.id] = visited
        self._visit_state[a.id] = []
        return False

    def build_conditional_depend_edges(self, graphs):
        print(
            f"[Info]       Building conditional dependency edges of {self.name}...")
        for u in tqdm(self.nodes.values()):
            if self.is_signal_in(u):
                component = u.component
                for v_id in self.components[component][SignalType.OUTPUT]:
                    v = self.nodes[v_id]
                    if self.has_path_depend(u, v):
                        edge_name = getEdgeName(EdgeType.DEPEND, u, v)
                        if edge_name not in self.edges:
                            edge = self.edges[edge_name] = Edge(
                                u, v, EdgeType.DEPEND, edge_name, None)
                            u.flow_to.append(edge)
                            v.flow_from.append(edge)
                    else:
                        graph_name = component.split("|")[0]
                        if graph_name != self.name:
                            graph = graphs[graph_name]
                            a_id = u.id.split(".")[1]
                            b_id = v_id.split(".")[1]
                            if a_id not in graph.nodes or b_id not in graph.nodes:
                                continue
                            node_a = graph.nodes[a_id]
                            node_b = graph.nodes[b_id]
                            if graph.has_path_depend(node_a, node_b):
                                edge_name = getEdgeName(EdgeType.DEPEND, u, v)
                                if edge_name not in self.edges:
                                    edge = self.edges[edge_name] = Edge(
                                        u, v, EdgeType.DEPEND, edge_name, None)
                                    u.flow_to.append(edge)
                                    v.flow_from.append(edge)
                                    self._depend_cache[u.id].add(v.id)

    def build_constraint_recursive(self, graphs, u, v, is_not_subgraph):
        component = u.component
        v_id = v.id
        if is_not_subgraph:
            if self.has_path_constraint(u, v):
                edge_name = getEdgeName(EdgeType.CONSTRAINT, u, v)
                if edge_name not in self.edges:
                    edge = self.edges[edge_name] = Edge(
                        u, v, EdgeType.CONSTRAINT, edge_name, None)
                    u.flow_to.append(edge)
                    v.flow_from.append(edge)
                    edge_name_reversed = getEdgeName(
                        EdgeType.CONSTRAINT, v, u)
                    if edge_name_reversed not in self.edges:
                        edge = self.edges[edge_name] = Edge(
                            v, u, EdgeType.CONSTRAINT, edge_name_reversed, None)
                        v.flow_to.append(edge)
                        u.flow_from.append(edge)
        else:
            graph_name = component.split("|")[0]
            # if graph_name != g_name:
            graph = graphs[graph_name]
            a_id = u.id.split(".")[1]
            b_id = v_id.split(".")[1]
            if a_id not in graph.nodes or b_id not in graph.nodes:
                return False
            node_a = graph.nodes[a_id]
            node_b = graph.nodes[b_id]
            if graph.has_path_constraint(node_a, node_b):
                if u.id not in self._constraint_cache:
                    self._constraint_cache[u.id] = set()
                self._constraint_cache[u.id].add(v.id)
                if v.id not in self._constraint_cache:
                    self._constraint_cache[v.id] = set()
                self._constraint_cache[v.id].add(u.id)
                if u.id not in self._visit_state:
                    self._visit_state[u.id] = [u]
                for edge_v in v.flow_to:
                    if edge_v.edge_type == EdgeType.CONSTRAINT:
                        self._visit_state[u.id].append(edge_v.node_to)
                if v.id not in self._visit_state:
                    self._visit_state[v.id] = [v]
                for edge_u in u.flow_to:
                    if edge_u.edge_type == EdgeType.CONSTRAINT:
                        self._visit_state[v.id].append(edge_u.node_to)
                edge_name = getEdgeName(EdgeType.CONSTRAINT, u, v)
                if edge_name not in self.edges:
                    edge = self.edges[edge_name] = Edge(
                        u, v, EdgeType.CONSTRAINT, edge_name, None)
                    u.flow_to.append(edge)
                    v.flow_from.append(edge)
                    edge_name_reversed = getEdgeName(EdgeType.CONSTRAINT, v, u)
                    if edge_name_reversed not in self.edges:
                        edge = self.edges[edge_name] = Edge(
                            v, u, EdgeType.CONSTRAINT, edge_name_reversed, None)
                        v.flow_to.append(edge)
                        u.flow_from.append(edge)
                # has_constraint = self.build_constraint_recursive(
                #     graphs, node_a, node_b, graph_name)
                # if has_constraint:
                #     self._constraint_cache[u.id].add(v.id)
                #     if v.id not in self._constraint_cache:
                #         self._constraint_cache[v.id] = set()
                #     self._constraint_cache[v.id].add(u.id)
                #     edge_name = getEdgeName(EdgeType.CONSTRAINT, u, v)
                #     if edge_name not in self.edges:
                #         edge = self.edges[edge_name] = Edge(
                #             u, v, EdgeType.CONSTRAINT, edge_name, None)
                #         u.flow_to.append(edge)
                #         v.flow_from.append(edge)
                #         edge_name_reversed = getEdgeName(
                #             EdgeType.CONSTRAINT, v, u)
                #         if edge_name_reversed not in self.edges:
                #             edge = self.edges[edge_name] = Edge(
                #                 v, u, EdgeType.CONSTRAINT, edge_name_reversed, None)
                #             v.flow_to.append(edge)
                #             u.flow_from.append(edge)
                #     return True
                # return False

    def build_constraint_helper(self, graphs, current_graph):
        if current_graph.is_constraint_build:
            return
        current_graph.is_constraint_build = True
        for component in current_graph.components.keys():
            component_name = component.split("|")[0]
            if component_name == current_graph.name:
                continue
            self.build_constraint_helper(graphs, graphs[component_name])
        print(
            f"[Info]       Building condition constraint edges of {current_graph.name}...")
        for u in tqdm(current_graph.nodes.values()):
            if current_graph.is_signal_in(u):
                component_name = u.component.split("|")[0]
                if component_name == current_graph.name:
                    continue
                component = u.component
                for v_id in current_graph.components[component][SignalType.OUTPUT]:
                    v = current_graph.nodes[v_id]
                    current_graph.build_constraint_recursive(
                        graphs, u, v, False)
        for u in tqdm(current_graph.nodes.values()):
            if current_graph.is_signal_in(u):
                component_name = u.component.split("|")[0]
                if component_name == current_graph.name:
                    component = u.component
                    for v_id in current_graph.components[component][SignalType.OUTPUT]:
                        v = current_graph.nodes[v_id]
                        current_graph.build_constraint_recursive(
                            graphs, u, v, True)

    def build_condition_constraint_edges(self, graphs):
        self.build_constraint_helper(graphs, self)

    def flows_to(self, node):
        if node.id in self.node_flows_to:
            return self.node_flows_to[node.id]
        flows_to_set = set()
        for edge in node.flow_to:
            if edge.edge_type == EdgeType.CONSTRAINT:
                continue
            node_to = edge.node_to
            if node_to.is_signal():
                flows_to_sub = self.flows_to(node_to)
                flows_to_set.union(flows_to_sub)
                flows_to_set.add(node_to.id)
            else:
                for e1 in node_to.flow_to:
                    if e1.edge_type == EdgeType.CONSTRAINT:
                        continue
                    to_1 = e1.node_to
                    if to_1.is_signal():
                        flows_to_sub = self.flows_to(to_1)
                        flows_to_set.union(flows_to_sub)
                        flows_to_set.add(to_1.id)
        # if node.id in self.params:
        #     flows_to_set = flows_to_set | self.params[node.id]
        self.node_flows_to[node.id] = flows_to_set
        return flows_to_set

    def compute(self):
        for node in self.nodes.values():
            if node.is_signal():
                self.flows_to(node)

    def build_graph(self, graphs):
        self.build_conditional_depend_edges(graphs)
        self.build_condition_constraint_edges(graphs)
        self.compute()
