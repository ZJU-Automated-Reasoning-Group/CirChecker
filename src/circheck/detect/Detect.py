from CDG import *
from Report import *
from StaticCheck import SignalType
from AST import *
import sys
from tqdm import tqdm

sys.setrecursionlimit(5000)


class Detector:
    def __init__(self, graphs):
        self.graphs = graphs
        self.reports = {}

    def detect(self):
        for graph in self.graphs.values():
            self.reports[graph.name] = {}
            self.as_const = {}
            print(
                f"[Info]       Starting the analysis process of graph {graph.name}.")

            print("[Info]       Detecting unconstrainted output...")
            self.detect_unconstrainted_output(graph)

            print("[Info]       Detecting unconstrained component input...")
            self.detect_unconstrained_comp_input(graph)

            print("[Info]       Detecting data flow constraint discrepancy...")
            self.detect_data_flow_constraint_discrepancy(graph)

            print("[Info]       Detecting unused component output...")
            self.detect_unused_comp_output(graph)

            print("[Info]       Detecting type mismatch...")
            self.detect_type_mismatch(graph)

            print("[Info]       Detecting assignment misuse...")
            self.detect_assignment_misue(graph)

            print("[Info]       Detecting unused signals...")
            self.detect_unused_signal(graph)

            print("[Info]       Detecting divide by zero unsafe...")
            self.detect_divide_by_zero_unsafe(graph)

            print("[Info]       Detecting nondeterministic data flow...")
            self.detect_nondeterministic_data_flow(graph)
        return self.reports

    def detect_unconstrainted_output(self, graph):
        results = []
        for n_id in tqdm(graph.components[graph.name][SignalType.OUTPUT]):
            node = graph.nodes[n_id]
            if self.unconstrainted_ouput(graph, node):
                results.append(Report(ReportType.WARNING, node.locate,
                                      f"Output signal '{node.id}' is not constrained by any constraint."))
        self.reports[graph.name]["unconstrained_output"] = results

    def unconstrainted_ouput(self, graph, node):
        if not node.is_signal_out():
            return False
        constrainted_by_input = self.constrainted_by_input(graph, node)
        constrainted_as_const = self.constrainted_as_const(graph, node)
        return not (constrainted_by_input or constrainted_as_const)

    def constrainted_by_input(self, graph, node):
        for n1 in graph.nodes.values():
            if not n1.is_signal_in():
                continue
            if self.is_constrainted(graph, node, n1):
                return True
        return False

    def constrainted_as_const(self, graph, node):
        if node.id in self.as_const:
            return self.as_const[node.id]
        else:
            self.as_const[node.id] = False
        for edge in node.flow_to:
            if edge.edge_type == EdgeType.CONSTRAINT and edge.count_constraint == 0:
                if edge.node_to.node_type == NodeType.CONSTANT:
                    self.as_const[node.id] = True
                    return True
        for edge in node.flow_from:
            if edge.edge_type == EdgeType.CONSTRAINT:
                node_from = edge.node_from
                if node_from.node_type == NodeType.CONSTANT and edge.count_constraint == 0:
                    self.as_const[node.id] = True
                    return True
                if node_from.node_type == NodeType.SIGNAL and node_from.signal_type == SignalType.INTERMEDIATE:
                    if self.constrainted_as_const(graph, node_from):
                        self.as_const[node.id] = True
                        return True
                node_from_component = node_from.component.split("|")[0]
                if node_from_component != graph.name and node_from.is_signal_out():
                    node_from_out_name = node_from.id.split(".")[-1]
                    node_from_signal = self.graphs[node_from_component].nodes[node_from_out_name]
                    component_graph = self.graphs[node_from_component]
                    constrained_by_input = self.constrainted_by_input(
                        component_graph, node_from_signal)
                    constrained_as_const = self.constrainted_as_const(
                        component_graph, node_from_signal)
                    if constrained_by_input or constrained_as_const:
                        self.as_const[node.id] = True
                        return True
        self.as_const[node.id] = False
        return False

    def is_constrainted(self, graph, node_a, node_b):
        return graph.has_path_constraint(node_a, node_b)

    def is_depended(self, graph, node_a, node_b):
        if node_a.id not in graph.node_flows_to:
            return False
        return node_b.id in graph.node_flows_to[node_a.id]

    def unconstrained_comp_input(self, graph, node):
        component = node.component.split("|")[0]
        if graph.name == component or not node.is_signal_in():
            return False
        for edge in node.flow_from:
            if edge.edge_type == EdgeType.CONSTRAINT:
                node_from = edge.node_from
                node_from_var_name = node_from.id.split(".")[0]
                node_var_name = node.id.split(".")[0]
                if node_from_var_name != node_var_name:
                    return False
        for edge in node.flow_to:
            if edge.edge_type == EdgeType.CONSTRAINT:
                node_to = edge.node_to
                node_to_var_name = node_to.id.split(".")[0]
                node_var_name = node.id.split(".")[0]
                if node_to_var_name != node_var_name:
                    return False
            if edge.node_to.node_type == NodeType.CONSTANT:
                node_to = edge.node_to
                for e1 in node_to.flow_to:
                    if e1.edge_type == EdgeType.CONSTRAINT:
                        return False
                for e1 in node_to.flow_from:
                    if e1.edge_type == EdgeType.CONSTRAINT:
                        return False
        return True

    def detect_unconstrained_comp_input(self, graph):
        results = []
        for node in tqdm(graph.nodes.values()):
            if self.unconstrained_comp_input(graph, node):
                results.append(Report(ReportType.WARNING, node.locate,
                                      f"Input signal '{node.id}' is unconstrained and may accept unchecked values."))
        self.reports[graph.name]["unconstrained component input"] = results

    def detect_data_flow_constraint_discrepancy(self, graph):
        resutlts = []
        for n_id, n_set in tqdm(graph.node_flows_to.items()):
            for n1_id in n_set:
                node = graph.nodes[n_id]
                node_1 = graph.nodes[n1_id]
                if not self.is_constrainted(graph, node, node_1):
                    resutlts.append(Report(ReportType.WARNING, node_1.locate,
                                           f"Signal '{node_1.id}' depends on '{node.id}' via dataflow, but there is no corresponding constraint dependency."))
        self.reports[graph.name]["data flow constraint discrepancy"] = resutlts

    def is_checking_signal(self, node):
        for edge in node.flow_to:
            if edge.edge_type == EdgeType.DEPEND:
                return True
        return False

    def is_value_defining_constraint(self, component_graph, internal_output_node):
        constraint_edges = [edge for edge in (
                internal_output_node.flow_to + internal_output_node.flow_from) if edge.edge_type == EdgeType.CONSTRAINT]
        if len(constraint_edges) == 0:
            return True
        for edge in internal_output_node.flow_to:
            if edge.edge_type == EdgeType.CONSTRAINT:
                if internal_output_node.component == edge.node_to.component:
                    if component_graph.is_signal_in(edge.node_to):
                        return True
        for edge in internal_output_node.flow_from:
            if edge.edge_type == EdgeType.CONSTRAINT:
                if internal_output_node.component == edge.node_from.component:
                    if component_graph.is_signal_in(edge.node_from):
                        return True
        return False

    def unused_comp_output(self, graph, node):
        component = node.component.split("|")[0]
        if not node.is_signal_out() or component == graph.name:
            return False
        sub_graph = self.graphs[component]
        node_var_name, signal_name = node.id.split(".")
        if signal_name not in sub_graph.nodes:
            return False
        sub_o_node = sub_graph.nodes[signal_name]
        if self.is_checking_signal(sub_o_node):
            return False
        for edge in node.flow_to:
            node_to_var_name = edge.node_to.id.split(".")[0]
            if node_var_name != node_to_var_name:
                return False
        for edge in node.flow_from:
            node_from_var_name = edge.node_from.id.split(".")[0]
            if node_var_name != node_from_var_name:
                return False
        return self.is_value_defining_constraint(sub_graph, sub_o_node)

    def detect_unused_comp_output(self, graph):
        resuluts = []
        for node in tqdm(graph.nodes.values()):
            if self.unused_comp_output(graph, node):
                resuluts.append(Report(ReportType.WARNING, node.locate,
                                       f"This output '{node.id}' is not checked nor used from the call site."))
        self.reports[graph.name]["unused component output"] = resuluts

    def unsused_signal(self, graph, node):
        if node.is_signal_out():
            return False
        if node.node_type == NodeType.CONSTANT:
            return False
        return (len(node.flow_from) + len(node.flow_to)) == 0

    def detect_unused_signal(self, graph):
        results = []
        for node in tqdm(graph.nodes.values()):
            if self.unsused_signal(graph, node):
                results.append(Report(ReportType.WARNING, node.locate,
                                      f"This signal '{node.id}' is declared but never used in any computation or constraint."))
        self.reports[graph.name]["unused signal"] = results

    def detect_type_mismatch(self, graph):
        num2bits_required = {"LessThan", "LessEqThan",
                             "GreaterThan", "GreaterEqThan", "BigLessThan"}
        num2bits_like = {"Num2Bits", "Num2Bits_strict",
                         "RangeProof", "MultiRangeProof", "RangeCheck2D"}
        results = []
        for node in tqdm(graph.nodes.values()):
            component = node.component.split("|")[0]
            if not node.is_signal_in() or component == graph.name:
                continue
            template_name = component.split("@")[0]
            if template_name not in num2bits_required:
                continue
            input_nodes = []
            for edge in node.flow_from:
                # if edge.edge_type == EdgeType.CONSTRAINT:
                #     continue
                if edge.node_from.is_signal() and edge.node_from.component != edge.node_to.component:
                    input_nodes.append(edge.node_from)
                if edge.node_from.node_type == NodeType.CONSTANT:
                    for e1 in edge.node_from.flow_from:
                        if e1.edge_type == EdgeType.DEPEND and e1.node_from.is_signal():
                            input_nodes.append(e1.node_from)
            for n1 in input_nodes:
                is_checked = False
                flows_to = graph.flows_to(n1)
                if n1.id in graph.params:
                    flows_to = flows_to | graph.params[n1.id]
                for n2_id in flows_to:
                    n2 = graph.nodes[n2_id]
                    n2_comp = n2.component.split("|")[0]
                    if not n1.is_signal_in() or n2_comp == graph.name:
                        continue
                    template_name_n2 = n2_comp.split("@")[0]
                    if template_name_n2 in num2bits_like:
                        is_checked = True
                        break
                if not is_checked:
                    results.append(Report(ReportType.WARNING, node.locate,
                                          f"Signal '{n1.id}' flows into '{template_name}' without being properly range-checked."))
        self.reports[graph.name]["type mismatch"] = results

    def contains_variable(self, ast_node, var_name):
        if isinstance(ast_node, Variable) and ast_node.name == var_name:
            return True
        if isinstance(ast_node, InfixOp):
            return self.contains_variable(ast_node.lhe, var_name) or self.contains_variable(ast_node.rhe, var_name)
        if isinstance(ast_node, PrefixOp):
            return self.contains_variable(ast_node.rhe, var_name)
        return False

    def solve_recursively(self, target_var_name, current_expression, accumulated_expression):
        if isinstance(current_expression, (Variable, Signal)) and current_expression.name == target_var_name:
            return accumulated_expression

        if not isinstance(current_expression, InfixOp):
            return None

        op = current_expression.infix_op
        left_sub_expr = current_expression.lhe
        right_sub_expr = current_expression.rhe

        if self.contains_variable(left_sub_expr, target_var_name):
            # (target_expr OP X) = Y
            next_target_expr = left_sub_expr
            other_operand = right_sub_expr
            if op == '+':  # (target + X) = Y  =>  target = Y - X
                new_accumulated = InfixOp(
                    current_expression.locate, accumulated_expression, '-', other_operand)
            elif op == '-':  # (target - X) = Y  =>  target = Y + X
                new_accumulated = InfixOp(
                    current_expression.locate, accumulated_expression, '+', other_operand)
            elif op == '*':  # (target * X) = Y  =>  target = Y / X
                new_accumulated = InfixOp(
                    current_expression.locate, accumulated_expression, '/', other_operand)
            elif op == '/':  # (target / X) = Y  =>  target = Y * X
                new_accumulated = InfixOp(
                    current_expression.locate, accumulated_expression, '*', other_operand)
            else:
                return None
        elif self.contains_variable(right_sub_expr, target_var_name):
            # (X OP target_expr) = Y
            next_target_expr = right_sub_expr
            other_operand = left_sub_expr

            if op == '+':  # (X + target) = Y  =>  target = Y - X
                new_accumulated = InfixOp(
                    current_expression.locate, accumulated_expression, '-', other_operand)
            elif op == '-':  # (X - target) = Y  =>  target = X - Y
                new_accumulated = InfixOp(
                    current_expression.locate, other_operand, '-', accumulated_expression)
            elif op == '*':  # (X * target) = Y  =>  target = Y / X
                new_accumulated = InfixOp(
                    current_expression.locate, accumulated_expression, '/', other_operand)
            else:
                return None
        else:
            return None
        return self.solve_recursively(target_var_name, next_target_expr, new_accumulated)

    def normalize_for_variable(self, target_var_name: str, equation_ast: ConstraintEquality) -> Optional[Expression]:
        if not isinstance(equation_ast, ConstraintEquality):
            return None
        if self.contains_variable(equation_ast.lhe, target_var_name):
            side_with_target = equation_ast.lhe
            other_side = equation_ast.rhe
        elif self.contains_variable(equation_ast.rhe, target_var_name):
            side_with_target = equation_ast.rhe
            other_side = equation_ast.lhe
        else:
            return None
        return self.solve_recursively(target_var_name, side_with_target, other_side)

    def are_asts_equivalent(self, ast1, ast2):
        if type(ast1) is not type(ast2):
            return False
        if isinstance(ast1, Variable):
            return ast1.name == ast2.name
        if isinstance(ast1, Number):
            return ast1.value == ast2.value
        if isinstance(ast1, InfixOp):
            if ast1.infix_op != ast2.infix_op:
                return False
            if ast1.infix_op in ['+', '*']:
                return (self.are_asts_equivalent(ast1.lhe, ast2.lhe) and self.are_asts_equivalent(ast1.rhe,
                                                                                                  ast2.rhe)) or (
                            self.are_asts_equivalent(ast1.lhe, ast2.rhe) and self.are_asts_equivalent(ast1.rhe,
                                                                                                      ast2.lhe))
            else:
                return self.are_asts_equivalent(ast1.lhe, ast2.lhe) and self.are_asts_equivalent(ast1.rhe, ast2.rhe)
        return False

    def is_rewritable_assignment(self, edge, processed_edges):
        if edge.name in processed_edges or edge.edge_type != EdgeType.DEPEND or edge.ast is None or edge.ast.op == "=":
            return False

        node_to = edge.node_to
        dataflow_ast = edge.ast.rhe

        related_constraints = [e for e in node_to.flow_to if e.edge_type == EdgeType.CONSTRAINT] + [
            e for e in node_to.flow_from if e.edge_type == EdgeType.CONSTRAINT]
        if len(related_constraints) == 0:
            return False
        count_ast = 0
        for c_edge in related_constraints:
            if isinstance(c_edge.ast, Substitution):
                count_ast += 1
                continue
            processed_edges.add(c_edge.name)
            normalized_constraint_ast = self.normalize_for_variable(
                node_to.id, c_edge.ast)
            if normalized_constraint_ast is None:
                continue
            if self.are_asts_equivalent(dataflow_ast, normalized_constraint_ast):
                return False
            count_ast += 1
        if count_ast >= 1:
            return True
        else:
            return False

    def detect_assignment_misue(self, graph):
        results = []
        processed_edges = set()
        for edge in tqdm(graph.edges.values()):
            if self.is_rewritable_assignment(edge, processed_edges):
                results.append(Report(ReportType.WARNING, edge.ast.locate,
                                      f"The dataflow for signal '{edge.node_to.id}' does not mathematically match any of its constraints."))
        self.reports[graph.name]["assignment missue"] = results

    def flat_expr(self, graph, expr):
        if isinstance(expr, Variable):
            name = expr.name
            for node in graph.nodes.values():
                id_name = node.id.split(".")[0].split("[")[0]
                if name == id_name and node.is_signal():
                    return True
        elif isinstance(expr, InfixOp):
            return self.flat_expr(graph, expr.lhe) or self.flat_expr(graph, expr.rhe)
        elif isinstance(expr, PrefixOp):
            return self.flat_expr(graph, expr.rhe)
        elif isinstance(expr, InlineSwitchOp):
            return self.flat_expr(graph, expr.cond) or self.flat_expr(graph, expr.if_true) or self.flat_expr(graph,
                                                                                                             expr.if_false)
        elif isinstance(expr, Call):
            for arg in expr.args:
                if self.flat_expr(graph, arg):
                    return True
        return False

    def is_denominator_with_signal(self, graph, expr):
        if isinstance(expr, InfixOp):
            if expr.infix_op == "/":
                if self.flat_expr(graph, expr.rhe):
                    return True
            if self.is_denominator_with_signal(graph, expr.lhe) or self.is_denominator_with_signal(graph, expr.rhe):
                return True
        elif isinstance(expr, InlineSwitchOp):
            return self.is_denominator_with_signal(graph, expr.cond) or self.is_denominator_with_signal(graph,
                                                                                                        expr.if_true) or self.is_denominator_with_signal(
                graph, expr.if_false)
        return False

    def is_substituition_depend(self, ast):
        if ast and isinstance(ast, Substitution):
            if ast.op == "=" or "--" in ast.op:
                return True
        return False

    def detect_divide_by_zero_unsafe(self, graph):
        results = []
        for edge in tqdm(graph.edges.values()):
            if self.is_substituition_depend(edge.ast) and self.is_denominator_with_signal(graph, edge.ast.rhe):
                results.append(Report(ReportType.WARNING, edge.ast.locate,
                                      f"Potential divide-by-zero issue detected."))
        self.reports[graph.name]["divide by zero"] = results

    def is_branch_cond_with_signal(self, graph, expr):
        if isinstance(expr, InfixOp):
            if self.is_branch_cond_with_signal(graph, expr.lhe) or self.is_branch_cond_with_signal(graph, expr.rhe):
                return True
        elif isinstance(expr, InlineSwitchOp):
            return self.flat_expr(graph, expr.cond)
        return False

    def detect_nondeterministic_data_flow(self, graph):
        results = []
        for edge in tqdm(graph.edges.values()):
            if self.is_substituition_depend(edge.ast) and self.is_branch_cond_with_signal(graph, edge.ast.rhe):
                results.append(Report(ReportType.WARNING, edge.ast.locate,
                                      "Potential non-deterministic dataflow: conditional assignment depends on a signal."))
        self.reports[graph.name]["nondeterministic data flow"] = results
