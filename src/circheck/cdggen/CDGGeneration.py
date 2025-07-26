from typing import Union
from CDG import *
from Visitor import *
from Errors import *
from AST import *
from Report import Report, ReportType
from StaticCheck import *

# Define the prime modulus p used in Circom field arithmetic
p = 21888242871839275222246405745257275088548364400416034343698204186575808495617


def val(z: int) -> int:
    """Definition of val(z) function used for relational operators."""
    if z >= (p // 2 + 1):
        return z - p
    return z


def mod(x: int) -> int:
    return x % p


def circom_add(a: int, b: int) -> int:
    return (a + b) % p


def circom_sub(a: int, b: int) -> int:
    return (a - b) % p


def circom_mul(a: int, b: int) -> int:
    return (a * b) % p


def circom_pow(a: int, b: int) -> int:
    return pow(a, b, p)


def circom_div(a: int, b: int) -> int:
    return (a * pow(b, -1, p)) % p


def circom_int_div(a: int, b: int) -> int:
    return (a // b) % p


def circom_mod(a: int, b: int) -> int:
    return (a % b) % p


def circom_eq(a: int, b: int) -> bool:
    return mod(a) == mod(b)


def circom_neq(a: int, b: int) -> bool:
    return mod(a) != mod(b)


def circom_lt(a: int, b: int) -> bool:
    return val(mod(a)) < val(mod(b))


def circom_leq(a: int, b: int) -> bool:
    return val(mod(a)) <= val(mod(b))


def circom_gt(a: int, b: int) -> bool:
    return val(mod(a)) > val(mod(b))


def circom_geq(a: int, b: int) -> bool:
    return val(mod(a)) >= val(mod(b))


def circom_and(a: bool, b: bool) -> bool:
    return a and b


def circom_or(a: bool, b: bool) -> bool:
    return a or b


def circom_not(a: bool) -> bool:
    return not a


def circom_bitand(a: int, b: int) -> int:
    return mod(a) & mod(b)


def circom_bitor(a: int, b: int) -> int:
    return mod(a) | mod(b)


def circom_bitxor(a: int, b: int) -> int:
    return mod(a) ^ mod(b)


def circom_bitnot(a: int) -> int:
    b = p.bit_length()
    mask = (1 << b) - 1
    return (~a) & mask


def circom_shr(a: int, k: int) -> int:
    if 0 <= k <= p // 2:
        return a // (2 ** k)
    else:
        return circom_shl(a, p - k)


def circom_shl(a: int, k: int) -> int:
    b = p.bit_length()
    mask = (1 << b) - 1
    if 0 <= k <= p // 2:
        return ((a * (2 ** k)) & mask) % p
    else:
        return circom_shr(a, p - k)


def circom_cond(condition: bool, true_val: Union[int, bool], false_val: Union[int, bool]) -> Union[int, bool]:
    return true_val if condition else false_val


def create_nested_array(dimensions):
    if not dimensions:
        return None
    size = dimensions[0]
    return [create_nested_array(dimensions[1:]) for _ in range(size)]


def check_none(lst):
    for item in lst:
        if item is None:
            return True
        if isinstance(item, list):
            if check_none(item):
                return True
    return False


class CDGGeneration(BaseVisitor):
    def __init__(self, ast: AST, env, list_function, list_template):
        self.graphs = {}
        self.remaining = []
        self.ast = ast
        self.in_template = False
        self.env = env
        self.temp_component = 0
        self.comp_id = 0
        self.in_function = False
        self.block = False
        self.return_value = None
        self.list_function = list_function
        self.list_template = list_template
        self.params = {}

    def generateCDG(self):
        self.visit(self.ast, {})
        for graph in self.graphs.values():
            graph.params = self.params[graph.name]
            graph.build_graph(self.graphs)
        return self.graphs

    def getComponentName(self):
        self.temp_component += 1
        return f"temp_comp[{self.temp_component}"

    def getEdgeName(self, edge_type, nFrom, nTo):
        if edge_type == EdgeType.DEPEND:
            return f"depend:{nFrom}-{nTo}"
        else:
            return f"constraint:{nFrom}-{nTo}"

    def getGraphName(self, template_name, template_args, args):
        name = template_name
        for i in range(len(args)):
            name += "@" + template_args[i] + "=" + str(args[i])
        return name

    def visitFileLocation(self, ast: FileLocation, param):
        return None

    def visitMainComponent(self, ast: MainComponent, param):
        param = {
            "env": self.env
        }
        self.remaining.append(self.visit(ast.expr, param))
        while len(self.remaining) > 0:
            template_type, args = self.remaining[0]
            self.remaining = self.remaining[1:]
            support_env = {
                "env": self.env,
                "component": {},
                "node": {},
                "name": "",
                "edge": {},
                "args": args,
                "var": {},
                "expr": {}
            }
            template_name = template_type.name.split("|")[0].split("@")[0]
            template_ast = self.env[0][template_name].ast
            self.visit(template_ast, support_env)

    def visitInclude(self, ast: Include, param):
        return None

    def visitTemplate(self, ast: Template, param):
        args = param["args"]
        graph_name = self.getGraphName(ast.name_field, ast.args, args)
        if graph_name in self.graphs:
            return None
        param["name"] = graph_name
        self.params[graph_name] = {}
        print(f"[Info]       Creating CDG: {graph_name}, in {ast.locate.path}")
        param["env"] = [{}] + param["env"]
        param["component"][graph_name] = {
            SignalType.INPUT: [],
            SignalType.OUTPUT: [],
            SignalType.INTERMEDIATE: []
        }
        template = self.list_template[ast.name_field].mtype
        for i in range(len(ast.args)):
            param["env"][0][ast.args[i]] = Symbol(
                ast.args[i], template.params[i], VarCircom(), ast, args[i])
            arg_name = ast.args[i]
            param["var"][arg_name] = 0
            arg_name += "[var0"
            param["node"][arg_name] = Node(
                ast.locate, arg_name, NodeType.CONSTANT, None, graph_name)
            param["expr"][arg_name] = set()
        self.in_template = True
        self.visit(ast.body, param)
        self.in_template = False
        self.graphs[graph_name] = CircuitDependenceGraph(
            param["edge"], param["node"], graph_name, param["component"])

    def visitFunction(self, ast: Function, param):
        return None

    def visitProgram(self, ast: Program, param):
        self.visit(ast.main_component, param)

    def visitIfThenElse(self, ast: IfThenElse, param):
        cond_type = self.visit(ast.cond, param).value
        if cond_type is None:
            raise Report(ReportType.ERROR, ast.cond.locate,
                         "Condition Type is None.")
        if cond_type:
            self.visit(ast.if_case, param)
        elif ast.else_case:
            self.visit(ast.else_case, param)

    def visitWhile(self, ast: While, param):
        cond_type = self.visit(ast.cond, param).value
        if cond_type is None:
            raise Report(ReportType.ERROR, ast.cond.locate,
                         "Condition Type is None.")
        while cond_type:
            self.visit(ast.stmt, param)
            if self.in_function and self.return_value:
                break
            cond_type = self.visit(ast.cond, param).value

    def visitReturn(self, ast: Return, param):
        self.return_value = self.visit(ast.value, param)

    def visitInitializationBlock(self, ast: InitializationBlock, param):
        for stmt in ast.initializations:
            self.visit(stmt, param)

    def visitDeclaration(self, ast: Declaration, param):
        checked = TypeCheck(ast)
        checked.count_visited = 1
        checked.visit(ast, param["env"])
        xtype = self.visit(ast.xtype, param)
        dimensions = []
        for dim in ast.dimensions:
            val = self.visit(dim, param).value
            if val is None:
                raise Report(ReportType.ERROR, ast.dimensions.locate,
                             "None value dims array.")
            dimensions.append(val)
        for env in param["env"]:
            if ast.name in env:
                symbol = env[ast.name]
                break
        symbol.value = create_nested_array(dimensions)
        if isinstance(xtype, ComponentCircom):
            return None
        nodes = [ast.name]
        for val in dimensions:
            temp = []
            for index in range(val):
                for node in nodes:
                    temp.append(node + "[" + str(index) + "]")
            nodes = temp
        for name in nodes:
            if isinstance(xtype, SignalCircom):
                param["node"][name] = Node(
                    ast.locate, name, NodeType.SIGNAL, xtype.signal_type, param["name"])
                param["component"][param["name"]
                ][xtype.signal_type].append(name)
            else:
                param["var"][name] = 0
                name += "[var0"
                param["node"][name] = Node(
                    ast.locate, name, NodeType.CONSTANT, None, param["name"])
                param["expr"][name] = set()

    def visitSubstitution(self, ast: Substitution, param):
        if ast.var == "_":
            return None
        for env in param["env"]:
            if ast.var in env:
                symbol = env[ast.var]
                break
        if ast.op == "=":
            if isinstance(symbol.xtype, VarCircom):
                value = symbol.value
                rhe_symbol = self.visit(ast.rhe, param)
                rhe_value = rhe_symbol.value
                if rhe_value is not None:
                    if len(ast.access) > 0:
                        for i in range(len(ast.access) - 1):
                            access_val = self.visit(ast.access[i], param)
                            value = value[access_val]
                        last_access = self.visit(ast.access[-1], param)
                        value[last_access] = rhe_value
                    else:
                        symbol.value = rhe_value
                if self.in_function:
                    return
                edge_type = EdgeType.DEPEND
                contains = FindNode().visit(ast.rhe, param)
                lhe = Variable(ast.locate, ast.var, ast.access)
                mtype = TypeCheck(ast).visit(lhe, param["env"])
                if not isinstance(mtype, ArrayCircom):
                    lhe_var = FindNode().visit(lhe, param)[0]
                    param["var"][lhe_var] += 1
                    name = self.visit(lhe, param).name
                    for fNode in contains:
                        if fNode in param["var"]:
                            if fNode == name.split("[var")[0]:
                                fNode += "[var" + str(param["var"][fNode] - 1)
                            else:
                                fNode += "[var" + str(param["var"][fNode])
                        if fNode == name:
                            continue
                        edge_name = self.getEdgeName(edge_type, fNode, name)
                        if edge_name not in param["edge"]:
                            edge = param["edge"][edge_name] = Edge(
                                param["node"][fNode], param["node"][name], edge_type, edge_name, ast)
                            param["node"][fNode].flow_to.append(edge)
                            param["node"][name].flow_from.append(edge)
                            if fNode in param["expr"]:
                                param["expr"][name] = param["expr"][name] | param["expr"][fNode]
                            else:
                                param["expr"][name].add(fNode)
                else:
                    lhe_array = FindNode().visit(lhe, param)[0]
                    lhe_vars = []
                    for var in param["var"].keys():
                        if lhe_array == var[:len(lhe_array)]:
                            lhe_vars.append(var)
                    if isinstance(ast.rhe, Call):
                        for lhe_var in lhe_vars:
                            param["var"][lhe_var] += 1
                            name = lhe_var + "[var" + \
                                   str(param["var"][lhe_var])
                            if name not in param["node"]:
                                param["node"][name] = Node(
                                    ast.locate, name, NodeType.CONSTANT, None, param["name"])
                                param["expr"][name] = set()
                            for fNode in contains:
                                if fNode in param["var"]:
                                    if fNode == name.split("[var")[0]:
                                        fNode += "[var" + \
                                                 str(param["var"][fNode] - 1)
                                    else:
                                        fNode += "[var" + \
                                                 str(param["var"][fNode])
                                if fNode == name:
                                    continue
                                if fNode not in param["node"]:
                                    continue
                                edge_name = self.getEdgeName(
                                    edge_type, fNode, name)
                                if edge_name not in param["edge"]:
                                    edge = param["edge"][edge_name] = Edge(
                                        param["node"][fNode], param["node"][name], edge_type, edge_name, ast)
                                    param["node"][fNode].flow_to.append(edge)
                                    param["node"][name].flow_from.append(edge)
                                    if fNode in param["expr"]:
                                        param["expr"][name] = param["expr"][name] | param["expr"][fNode]
                                    else:
                                        param["expr"][name].add(fNode)
                    elif isinstance(ast.rhe, Variable):
                        for lhe_var in lhe_vars:
                            param["var"][lhe_var] += 1
                            name = lhe_var + "[var" + \
                                   str(param["var"][lhe_var])
                            if name not in param["node"]:
                                param["node"][name] = Node(
                                    ast.locate, name, NodeType.CONSTANT, None, param["name"])
                                param["expr"][name] = set()
                            fNode = contains[0] + lhe_var[len(lhe_array):]
                            if fNode in param["var"]:
                                fNode += "[var" + str(param["var"][fNode])
                            if fNode == name:
                                continue
                            if isinstance(rhe_symbol.xtype, SignalCircom):
                                if fNode not in param["node"]:
                                    template_name = param["node"][rhe_symbol.name].component
                                    signal_type = rhe_symbol.xtype.signal_type
                                    param["node"][fNode] = Node(
                                        ast.rhe.locate, fNode, NodeType.SIGNAL, signal_type, template_name)
                                    param["component"][template_name][signal_type].append(
                                        fNode)
                            edge_name = self.getEdgeName(
                                edge_type, fNode, name)
                            if edge_name not in param["edge"]:
                                edge = param["edge"][edge_name] = Edge(
                                    param["node"][fNode], param["node"][name], edge_type, edge_name, ast)
                                param["node"][fNode].flow_to.append(edge)
                                param["node"][name].flow_from.append(edge)
                                if fNode in param["expr"]:
                                    param["expr"][name] = param["expr"][name] | param["expr"][fNode]
                                else:
                                    param["expr"][name].add(fNode)
            elif isinstance(symbol.xtype, ComponentCircom):
                template_type, args = self.visit(ast.rhe, param)
                value = symbol.value
                if isinstance(symbol.mtype, ArrayCircom):
                    symbol.mtype.eleType = template_type
                else:
                    symbol.mtype = template_type
                graph_name = self.getGraphName(
                    template_type.name, template_type.args, args) + "|id=" + str(self.comp_id)
                self.comp_id += 1
                if len(ast.access) > 0:
                    for i in range(len(ast.access) - 1):
                        access_val = self.visit(ast.access[i], param)
                        value = value[access_val]
                    last_access = self.visit(ast.access[-1], param)
                    value[last_access] = TemplateCircom(graph_name, template_type.params, template_type.signals,
                                                        template_type.signals_in, template_type.signals_out,
                                                        template_type.args, template_type.signals_ast)
                    append_template = value[last_access]
                else:
                    symbol.value = TemplateCircom(graph_name, template_type.params, template_type.signals,
                                                  template_type.signals_in, template_type.signals_out,
                                                  template_type.args, template_type.signals_ast)
                    append_template = symbol.value
                if not graph_name in param["component"]:
                    param["component"][graph_name] = {
                        SignalType.INPUT: [],
                        SignalType.OUTPUT: [],
                        SignalType.INTERMEDIATE: []
                    }
                    lhe = Variable(ast.locate, ast.var, ast.access)
                    lhe_name = self.visit(lhe, param).name
                    for signal_in in append_template.signals_in:
                        signal_name = lhe_name + "." + signal_in
                        param["node"][signal_name] = Node(
                            ast.rhe.locate, signal_name, NodeType.SIGNAL, SignalType.INPUT, graph_name)
                        param["component"][graph_name][SignalType.INPUT].append(
                            signal_name)
                    for signal_out in append_template.signals_out:
                        signal_name = lhe_name + "." + signal_out
                        param["node"][signal_name] = Node(
                            ast.rhe.locate, signal_name, NodeType.SIGNAL, SignalType.OUTPUT, graph_name)
                        param["component"][graph_name][SignalType.OUTPUT].append(
                            signal_name)
                self.remaining.append((append_template, args))
        else:
            lhe = Variable(ast.locate, ast.var, ast.access)
            name = self.visit(lhe, param).name
            self.visit(ast.rhe, param)
            contains = FindNode().visit(ast.rhe, param)
            if "--" in ast.op:
                for fNode in contains:
                    if fNode in param["var"]:
                        fNode += "[var" + str(param["var"][fNode])
                    if fNode == name:
                        continue
                    depend_edge_name = self.getEdgeName(
                        EdgeType.DEPEND, fNode, name)
                    if depend_edge_name not in param["edge"]:
                        edge_depend = param["edge"][depend_edge_name] = Edge(
                            param["node"][fNode], param["node"][name], EdgeType.DEPEND, depend_edge_name, ast)
                        param["node"][fNode].flow_to.append(edge_depend)
                        param["node"][name].flow_from.append(edge_depend)
            elif "==" in ast.op:
                contains = [name] + contains
                for i in range(len(contains)):
                    for j in range(i + 1, len(contains)):
                        name = contains[i]
                        fNode = contains[j]
                        if fNode in param["var"]:
                            fNode += "[var" + str(param["var"][fNode])
                        if name in param["var"]:
                            name += "[var" + str(param["var"][name])
                        if fNode == name:
                            continue
                        if fNode not in self.params[param["name"]]:
                            self.params[param["name"]][fNode] = set()
                        self.params[param["name"]][fNode].add(name)
                        constraint_edge_name = self.getEdgeName(
                            EdgeType.CONSTRAINT, fNode, name)
                        if constraint_edge_name not in param["edge"]:
                            edge_constraint = param["edge"][constraint_edge_name] = Edge(
                                param["node"][fNode], param["node"][name], EdgeType.CONSTRAINT, constraint_edge_name,
                                ast)
                            param["node"][fNode].flow_to.append(
                                edge_constraint)
                            param["node"][name].flow_from.append(
                                edge_constraint)
                        edge_name_reversed = self.getEdgeName(
                            EdgeType.CONSTRAINT, name, fNode)
                        if edge_name_reversed not in param["edge"]:
                            edge_reversed = param["edge"][edge_name_reversed] = Edge(
                                param["node"][name], param["node"][fNode], EdgeType.CONSTRAINT, edge_name_reversed, ast)
                            param["node"][name].flow_to.append(edge_reversed)
                            param["node"][fNode].flow_from.append(
                                edge_reversed)
                        if fNode in param["expr"]:
                            for add_name in param["expr"][fNode]:
                                cons_1 = self.getEdgeName(
                                    EdgeType.CONSTRAINT, add_name, name)
                                if cons_1 not in param["edge"]:
                                    edge_cons_1 = param["edge"][cons_1] = Edge(
                                        param["node"][add_name], param["node"][name], EdgeType.CONSTRAINT, cons_1, ast)
                                    param["node"][add_name].flow_to.append(
                                        edge_cons_1)
                                    param["node"][name].flow_from.append(
                                        edge_cons_1)
                                cons_2 = self.getEdgeName(
                                    EdgeType.CONSTRAINT, name, add_name)
                                if cons_2 not in param["edge"]:
                                    edge_cons_2 = param["edge"][cons_2] = Edge(
                                        param["node"][name], param["node"][add_name], EdgeType.CONSTRAINT, cons_2, ast)
                                    param["node"][name].flow_to.append(
                                        edge_cons_2)
                                    param["node"][add_name].flow_from.append(
                                        edge_cons_2)

    def visitMultiSubstitution(self, ast: MultiSubstitution, param):
        lhe_value = self.visit(ast.lhe, param)
        rhe_value = self.visit(ast.rhe, param)
        for i in range(len(lhe_value)):
            self.visit(Substitution(
                ast.locate, lhe_value[i].var, lhe_value[i].access, ast.op, rhe_value[i]))

    def visitConstraintEquality(self, ast: ConstraintEquality, param):
        self.visit(ast.lhe, param)
        self.visit(ast.rhe, param)
        find_node = FindNode()
        lhe_node = find_node.visit(ast.lhe, param)
        rhe_node = find_node.visit(ast.rhe, param)
        nodes_list = lhe_node + rhe_node
        for i in range(len(nodes_list)):
            for j in range(i + 1, len(nodes_list)):
                lnode = nodes_list[i]
                rnode = nodes_list[j]
                if lnode in param["var"]:
                    lnode += "[var" + str(param["var"][lnode])
                if rnode in param["var"]:
                    rnode += "[var" + str(param["var"][rnode])
                if lnode == rnode:
                    continue
                if lnode in param["expr"] and rnode in param["expr"]:
                    for add_l in param["expr"][lnode]:
                        for add_r in param["expr"][rnode]:
                            cons_1 = self.getEdgeName(
                                EdgeType.CONSTRAINT, add_l, add_r)
                            if cons_1 not in param["edge"]:
                                edge_cons_1 = param["edge"][cons_1] = Edge(
                                    param["node"][add_l], param["node"][add_r], EdgeType.CONSTRAINT, cons_1, ast)
                                param["node"][add_l].flow_to.append(
                                    edge_cons_1)
                                param["node"][add_r].flow_from.append(
                                    edge_cons_1)
                            cons_2 = self.getEdgeName(
                                EdgeType.CONSTRAINT, add_r, add_l)
                            if cons_2 not in param["edge"]:
                                edge_cons_2 = param["edge"][cons_2] = Edge(
                                    param["node"][add_r], param["node"][add_l], EdgeType.CONSTRAINT, cons_2, ast)
                                param["node"][add_r].flow_to.append(
                                    edge_cons_2)
                                param["node"][add_l].flow_from.append(
                                    edge_cons_2)
                elif lnode in param["expr"]:
                    add_r = rnode
                    for add_l in param["expr"][lnode]:
                        cons_1 = self.getEdgeName(
                            EdgeType.CONSTRAINT, add_l, add_r)
                        if cons_1 not in param["edge"]:
                            edge_cons_1 = param["edge"][cons_1] = Edge(
                                param["node"][add_l], param["node"][add_r], EdgeType.CONSTRAINT, cons_1, ast)
                            param["node"][add_l].flow_to.append(
                                edge_cons_1)
                            param["node"][add_r].flow_from.append(
                                edge_cons_1)
                        cons_2 = self.getEdgeName(
                            EdgeType.CONSTRAINT, add_r, add_l)
                        if cons_2 not in param["edge"]:
                            edge_cons_2 = param["edge"][cons_2] = Edge(
                                param["node"][add_r], param["node"][add_l], EdgeType.CONSTRAINT, cons_2, ast)
                            param["node"][add_r].flow_to.append(
                                edge_cons_2)
                            param["node"][add_l].flow_from.append(
                                edge_cons_2)
                elif rnode in param["expr"]:
                    add_l = lnode
                    for add_r in param["expr"][rnode]:
                        cons_1 = self.getEdgeName(
                            EdgeType.CONSTRAINT, add_l, add_r)
                        if cons_1 not in param["edge"]:
                            edge_cons_1 = param["edge"][cons_1] = Edge(
                                param["node"][add_l], param["node"][add_r], EdgeType.CONSTRAINT, cons_1, ast)
                            param["node"][add_l].flow_to.append(
                                edge_cons_1)
                            param["node"][add_r].flow_from.append(
                                edge_cons_1)
                        cons_2 = self.getEdgeName(
                            EdgeType.CONSTRAINT, add_r, add_l)
                        if cons_2 not in param["edge"]:
                            edge_cons_2 = param["edge"][cons_2] = Edge(
                                param["node"][add_r], param["node"][add_l], EdgeType.CONSTRAINT, cons_2, ast)
                            param["node"][add_r].flow_to.append(
                                edge_cons_2)
                            param["node"][add_l].flow_from.append(
                                edge_cons_2)
                edge_name = self.getEdgeName(EdgeType.CONSTRAINT, lnode, rnode)
                if edge_name not in param["edge"]:
                    edge = param["edge"][edge_name] = Edge(
                        param["node"][lnode], param["node"][rnode], EdgeType.CONSTRAINT, edge_name, ast)
                    param["node"][lnode].flow_to.append(edge)
                    param["node"][rnode].flow_from.append(edge)
                else:
                    param["edge"][edge_name].count_constraint += 1
                edge_name = self.getEdgeName(EdgeType.CONSTRAINT, rnode, lnode)
                if edge_name not in param["edge"]:
                    edge = param["edge"][edge_name] = Edge(
                        param["node"][rnode], param["node"][lnode], EdgeType.CONSTRAINT, edge_name, ast)
                    param["node"][rnode].flow_to.append(edge)
                    param["node"][lnode].flow_from.append(edge)
                else:
                    param["edge"][edge_name].count_constraint += 1

    def visitLogCall(self, ast: LogCall, param):
        return None

    def visitBlock(self, ast: Block, param):
        env = param["env"]
        if self.in_template:
            self.in_template = False
        elif self.block:
            self.block = False
        else:
            param["env"] = [{}] + env
        for stmt in ast.stmts:
            self.visit(stmt, param)
            if self.in_function and self.return_value:
                break
        param["env"] = env

    def visitAssert(self, ast: Assert, param):
        return None

    def visitVar(self, ast: Var, param):
        return VarCircom()

    def visitSignal(self, ast: Signal, param):
        if ast.signal_type == "input":
            signal_type = SignalType.INPUT
        elif ast.signal_type == "output":
            signal_type = SignalType.OUTPUT
        elif ast.signal_type == "intermediate":
            signal_type = SignalType.INTERMEDIATE
        return SignalCircom(signal_type)

    def visitComponent(self, ast: Component, param):
        return ComponentCircom()

    def visitAnonymousComponent(self, ast: AnonymousComponent, param):
        return AnonymousComponentCircom()

    def visitInfixOp(self, ast: InfixOp, param):
        lhe_val = self.visit(ast.lhe, param).value
        rhe_val = self.visit(ast.rhe, param).value
        if lhe_val is None or rhe_val is None:
            return Symbol("", PrimeField(), None, ast, None)
        op = ast.infix_op
        if op == "&&":
            return Symbol("", PrimeField(), None, ast, circom_and(lhe_val, rhe_val))
        elif op == "||":
            return Symbol("", PrimeField(), None, ast, circom_or(lhe_val, rhe_val))
        elif op == ">":
            return Symbol("", PrimeField(), None, ast, circom_gt(lhe_val, rhe_val))
        elif op == "<":
            return Symbol("", PrimeField(), None, ast, circom_lt(lhe_val, rhe_val))
        elif op == ">=":
            return Symbol("", PrimeField(), None, ast, circom_geq(lhe_val, rhe_val))
        elif op == "<=":
            return Symbol("", PrimeField(), None, ast, circom_leq(lhe_val, rhe_val))
        elif op == "+":
            return Symbol("", PrimeField(), None, ast, circom_add(lhe_val, rhe_val))
        elif op == "-":
            return Symbol("", PrimeField(), None, ast, circom_sub(lhe_val, rhe_val))
        elif op == "*":
            return Symbol("", PrimeField(), None, ast, circom_mul(lhe_val, rhe_val))
        elif op == "**":
            return Symbol("", PrimeField(), None, ast, circom_pow(lhe_val, rhe_val))
        elif op == "/":
            if rhe_val == 0:
                raise Report(ReportType.ERROR, ast.locate, "Division by zero")
            return Symbol("", PrimeField(), None, ast, circom_div(lhe_val, rhe_val))
        elif op == "\\":
            return Symbol("", PrimeField(), None, ast, circom_int_div(lhe_val, rhe_val))
        elif op == "%":
            return Symbol("", PrimeField(), None, ast, circom_mod(lhe_val, rhe_val))
        elif op == "&":
            return Symbol("", PrimeField(), None, ast, circom_bitand(lhe_val, rhe_val))
        elif op == "|":
            return Symbol("", PrimeField(), None, ast, circom_bitor(lhe_val, rhe_val))
        elif op == "^":
            return Symbol("", PrimeField(), None, ast, circom_bitxor(lhe_val, rhe_val))
        elif op == ">>":
            return Symbol("", PrimeField(), None, ast, circom_shr(lhe_val, rhe_val))
        elif op == "<<":
            return Symbol("", PrimeField(), None, ast, circom_shl(lhe_val, rhe_val))
        elif op == "==":
            return Symbol("", PrimeField(), None, ast, circom_eq(lhe_val, rhe_val))
        elif op == "!=":
            return Symbol("", PrimeField(), None, ast, circom_neq(lhe_val, rhe_val))

    def visitPrefixOp(self, ast: PrefixOp, param):
        rhe_val = self.visit(ast.rhe, param).value
        if rhe_val is None:
            return Symbol("", PrimeField(), None, ast, None)
        op = ast.prefix_op
        if op == "!":
            return Symbol("", PrimeField(), None, ast, circom_not(rhe_val))
        elif op == "-":
            return Symbol("", PrimeField(), None, ast, circom_sub(0, rhe_val))
        elif op == "+":
            return Symbol("", PrimeField(), None, ast, circom_add(0, rhe_val))
        elif op == "~":
            return Symbol("", PrimeField(), None, ast, circom_bitnot(rhe_val))
        elif op == "++":
            return Symbol("", PrimeField(), None, ast, circom_add(rhe_val, 1))
        elif op == "--":
            return Symbol("", PrimeField(), None, ast, circom_sub(rhe_val, 1))

    def visitInlineSwitchOp(self, ast: InlineSwitchOp, param):
        cond_val = self.visit(ast.cond, param).value
        FindNode.switch_op = cond_val
        if cond_val is None:
            return Symbol("", PrimeField(), None, ast, None)
        if cond_val:
            return self.visit(ast.if_true, param)
        else:
            return self.visit(ast.if_false, param)

    def visitParrallelOp(self, ast: ParallelOp, param):
        return self.visit(ast.rhe, param)

    def visitVariable(self, ast: Variable, param):
        name = ast.name
        symbol = None
        for env in param["env"]:
            if ast.name in env:
                symbol = env[ast.name]
                break
        value = symbol.value
        if isinstance(symbol.mtype, ArrayCircom):
            var_type = ArrayCircom(symbol.mtype.eleType, symbol.mtype.dims)
        else:
            var_type = symbol.mtype
        if isinstance(symbol.xtype, VarCircom):
            for i in range(len(ast.access)):
                access_value = self.visit(ast.access[i], param)
                if var_type.dims == 1:
                    var_type = var_type.eleType
                else:
                    var_type.dims -= 1
                if value:
                    value = value[access_value]
                name += "[" + str(access_value) + "]"
            if not isinstance(var_type, ArrayCircom):
                if name not in param["var"]:
                    param["var"][name] = 0
                name += "[var" + str(param["var"][name])
            if name not in param["node"]:
                param["node"][name] = Node(
                    ast.locate, name, NodeType.CONSTANT, None, param["name"])
                param["expr"][name] = set()
            return Symbol(name, var_type, VarCircom(), ast, value)
        elif isinstance(symbol.xtype, ComponentCircom):
            template_name = None
            is_access = True
            for i in range(len(ast.access)):
                access_value = self.visit(ast.access[i], param)
                if isinstance(access_value, str):
                    name += "." + access_value
                    template_name = value.name
                    if access_value in var_type.signals_in:
                        signal_type = SignalType.INPUT
                    else:
                        signal_type = SignalType.OUTPUT
                    temp_type = var_type.signals[access_value]
                    if isinstance(temp_type, ArrayCircom):
                        var_type = ArrayCircom(
                            temp_type.eleType, temp_type.dims)
                    else:
                        var_type = temp_type
                    is_access = False
                else:
                    if var_type.dims == 1:
                        var_type = var_type.eleType
                    else:
                        var_type.dims -= 1
                    name += "[" + str(access_value) + "]"
                    if is_access:
                        value = value[access_value]
            if template_name:
                if name not in param["node"]:
                    param["node"][name] = Node(
                        ast.locate, name, NodeType.SIGNAL, signal_type, template_name)
                    param["component"][template_name][signal_type].append(name)
                    var_name, signal_name = name.split(".")
                    signal_name = signal_name.split("[")[0]
                    del_name = var_name + "." + signal_name
                    if del_name in param["node"]:
                        del param["node"][del_name]
                        param["component"][template_name][signal_type].remove(
                            del_name)
                return Symbol(name, var_type, SignalCircom(signal_type), ast, None)
            else:
                return Symbol(name, var_type, ComponentCircom(), ast, None)
        elif isinstance(symbol.xtype, SignalCircom):
            for i in range(len(ast.access)):
                access_value = self.visit(ast.access[i], param)
                if var_type.dims == 1:
                    var_type = var_type.eleType
                else:
                    var_type.dims -= 1
                name += "[" + str(access_value) + "]"
            return Symbol(name, var_type, symbol.xtype, ast, None)

    def visitNumber(self, ast: Number, param):
        return Symbol("", PrimeField(), None, ast, ast.value)

    def visitCall(self, ast: Call, param):
        if ast.id in self.list_function:
            symbol = self.list_function[ast.id]
        elif ast.id in self.list_template:
            symbol = self.list_template[ast.id]
        if isinstance(symbol.mtype, TemplateCircom):
            args = []
            for arg in ast.args:
                val = self.visit(arg, param).value
                if val is None:
                    raise Report(ReportType.ERROR, arg.locate,
                                 "Arguement has None value.")
                args.append(val)
            return (symbol.mtype, args)
        else:
            args = []
            for arg in ast.args:
                val = self.visit(arg, param).value
                if val is None:
                    return Symbol("", PrimeField(), VarCircom(), ast, None)
                if isinstance(val, list) and check_none(val):
                    return Symbol("", PrimeField(), VarCircom(), ast, None)
                args.append(val)
            env = param["env"]
            param["env"] = [{}] + param["env"]
            for i in range(len(ast.args)):
                arg_type = TypeCheck(ast).visit(ast.args[i], env)
                param["env"][0][symbol.mtype.args[i]] = Symbol(
                    symbol.mtype.args[i], arg_type, VarCircom(), ast.args[i], args[i])
            self.in_function = True
            self.block = True
            self.visit(symbol.mtype.body, param)
            param["env"] = env
            ret_value = self.return_value
            self.return_value = None
            self.in_function = False
            return ret_value

    def visitAnonymousComponentExpr(self, ast: AnonymousComponentExpr, param):
        component_name = self.getComponentName()
        self.visit(Declaration(ast.locate, Component(),
                               component_name, [], True), param)
        self.visit(Substitution(ast.locate, component_name, [],
                                "=", Call(ast.locate, ast.id, ast.params)))
        for env in param["env"]:
            if ast.id in env:
                symbol = env[ast.id]
                break
        if ast.names and ast.names[0]:
            for i in range(len(ast.name)):
                op, name = ast.names[i]
                self.visit(Substitution(ast.locate, component_name,
                                        [name], "<==", ast.signals[i]), param)
        else:
            for i in range(len(ast.signals)):
                self.visit(Substituition(ast.locate, component_name, [
                    symbol.mtype.signals_in[i]], "<==", ast.signals[i]), param)
        return_tuple = []
        for name in symbol.mtype.signals_out:
            return_tuple.append(Variable(component_name, [name]))
        return return_tuple if len(return_tuple) > 1 else return_tuple[0]

    def visitArrayInLine(self, ast: ArrayInLine, param):
        values = []
        for expr in ast.values:
            value = self.visit(expr, param).value
            values.append(value)
        return Symbol("", ArrayCircom(1, PrimeField()), VarCircom(), ast, values)

    def visitTupleExpr(self, ast: TupleExpr, param):
        return ast.values

    def visitComponentAccess(self, ast: ComponentAccess, param):
        return ast.name

    def visitArrayAccess(self, ast: ArrayAccess, param):
        val = self.visit(ast.expr, param).value
        if val is None:
            raise Report(ReportType.ERROR, ast.locate,
                         "Array access with None value")
        return val

    def visitLogStr(self, ast: LogStr, param):
        return None

    def visitLogExp(self, ast: LogExp, param):
        return None


# Help Class to find Node in Expression
class FindNode(BaseVisitor):
    node_number = 0
    switch_op = None

    def visitInfixOp(self, ast: InfixOp, param):
        return self.visit(ast.lhe, param) + self.visit(ast.rhe, param)

    def visitPrefixOp(self, ast: PrefixOp, param):
        return self.visit(ast.rhe, param)

    def visitInlineSwitchOp(self, ast: InlineSwitchOp, param):
        cond = self.visit(ast.cond, param)
        if FindNode.switch_op is None:
            return cond
        elif FindNode.switch_op == True:
            return cond + self.visit(ast.if_true, param)
        elif FindNode.switch_op == False:
            return cond + self.visit(ast.if_false, param)

    def visitParrallelOp(self, ast: ParallelOp, param):
        return self.visit(ast.rhe, param)

    def visitVariable(self, ast: Variable, param):
        name = ast.name
        temp = CDGGeneration(ast, param, [], [])
        for access in ast.access:
            val = temp.visit(access, param)
            if isinstance(val, str):
                name += "." + val
            else:
                name += "[" + str(val) + "]"
        return [name]

    def visitNumber(self, ast: Number, param):
        name = "Number[" + str(FindNode.node_number)
        FindNode.node_number += 1
        param["node"][name] = Node(
            ast.locate, name, NodeType.CONSTANT, None, param["name"])
        return [name]

    def visitCall(self, ast: Call, param):
        ans = []
        for arg in ast.args:
            ans += self.visit(arg, param)
        return ans

    def visitAnonymousComponentExpr(self, ast: AnonymousComponent, param):
        ans = []
        for signal in ast.signals:
            ans += self.visit(signal, param)
        return ans

    def visitArrayInLine(self, ast: ArrayInLine, param):
        return []

    def visitTupleExpr(self, ast: TupleExpr, param):
        ans = []
        for val in ast.values:
            ans += self.visit(val, param)
        return ans
