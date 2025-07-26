from AST import *
from Visitor import *
from Errors import *
from Report import Report, ReportType
from enum import Enum, auto


class Symbol:
    def __init__(self, name, mtype, xtype, ast=None, value=None):
        self.name = name
        self.mtype = mtype  # PrimeField, ArrayCircom, TemplateCircom, FunctionCircom
        self.xtype = xtype  # VarCircom, SignalCircom, ComponentCircom, AnonymousComponentCircom
        self.ast = ast
        self.value = value


class Type:
    pass


class SignalType(Enum):
    INPUT = auto()
    OUTPUT = auto()
    INTERMEDIATE = auto()


class PrimeField(Type):
    pass


class SignalCircom(Type):
    def __init__(self, signal_type):
        self.signal_type = signal_type


class VarCircom(Type):
    pass


class ComponentCircom(Type):
    pass


class AnonymousComponentCircom(Type):
    pass


class ArrayCircom(Type):
    def __init__(self, eleType, dims):
        self.dims = dims
        self.eleType = eleType


class TemplateCircom(Type):
    def __init__(self, name, params, signals={}, signals_in=[], signals_out=[], args=[], signals_ast={}):
        self.name = name
        self.params = params
        self.signals = signals
        self.signals_in = signals_in
        self.signals_out = signals_out
        self.args = args
        self.signals_ast = signals_ast


class FunctionCircom(Type):
    def __init__(self, name, params, return_type, body, args):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body
        self.args = args


def is_same_type(type1, type2):
    if type(type1) != type(type2):
        return False
    if isinstance(type1, ArrayCircom) and isinstance(type2, ArrayCircom):
        return type1.dims == type2.dims and is_same_type(type1.eleType, type2.eleType)
    return True


class TypeCheck(BaseVisitor):
    def __init__(self, ast):
        self.ast = ast
        self.global_env = [{}]
        self.list_function = {}
        self.in_function = False
        self.no_block = False
        self.return_func = None
        self.list_template = {}
        self.in_template = False
        self.template_signals = None
        self.signals_ast = None
        self.signal_in = None
        self.signal_out = None
        self.is_multi_sub = False
        self.count_visited = 0

    def infer_type(self, var, param, typ=PrimeField()):
        symbol = None
        for env in param:
            if var.name in env:
                symbol = env[var.name]
                break
        if isinstance(typ, PrimeField):
            if len(var.access) == 0:
                symbol.mtype = typ
            else:
                symbol.mtype = ArrayCircom(typ, len(var.access))
        elif isinstance(typ, ArrayCircom):
            if len(var.access) == 0:
                symbol.mtype = typ
            else:
                symbol.mtype = ArrayCircom(
                    typ.eleType, len(var.access) + typ.dims)
        self.visit(var, param)

    def check(self):
        self.visit(self.ast, self.global_env)

    def visitFileLocation(self, ast: FileLocation, param):
        return None

    def visitMainComponent(self, ast: MainComponent, param):
        template_type = self.visit(ast.expr, param)
        if not isinstance(template_type, TemplateCircom):
            raise Report(ReportType.ERROR, ast.locate,
                         f"Main component must be a template. Found {type(template_type).__name__} instead")
        for name in ast.publics:
            if name not in template_type.signals_in:
                raise Report(ReportType.ERROR, ast.locate,
                             f"Signal '{name}' not declared in template '{template_type.name}'")
        param[0]["main"] = Symbol(
            "main", template_type, ComponentCircom(), ast)

    def visitInclude(self, ast: Include, param):
        return None

    def visitTemplate(self, ast: Template, param):
        if self.count_visited == 0:
            if ast.name_field in self.list_template:
                raise Report(ReportType.ERROR, ast.locate,
                             f"Template '{ast.name_field}' already declared")
            env = [{}] + param
            for arg in ast.args:
                if arg in env[0]:
                    raise Report(ReportType.ERROR, ast.locate,
                                 f"Argument '{arg}' already declared")
                env[0][arg] = Symbol(arg, None, VarCircom())
            self.in_template = True
            self.template_signals = {}
            self.signals_ast = {}
            self.signal_in = []
            self.signal_out = []
            self.visit(ast.body, env)
            if self.return_func is not None:
                raise Report(ReportType.ERROR, ast.locate,
                             "Template can not have a return statement")
            self.in_template = False
            arg_list = []
            for arg in ast.args:
                arg_list.append(env[0][arg].mtype)
            self.list_template[ast.name_field] = param[0][ast.name_field] = Symbol(ast.name_field, TemplateCircom(
                ast.name_field, arg_list, self.template_signals, self.signal_in, self.signal_out, ast.args,
                self.signals_ast), None, ast)
            self.template_signals = None
            self.signals_ast = None
            self.signal_in = None
            self.signal_out = None
        else:
            env = [{}] + param
            for arg in ast.args:
                env[0][arg] = Symbol(arg, None, VarCircom())
            self.in_template = True
            self.visit(ast.body, env)
            arg_list = []
            for arg in ast.args:
                arg_list.append(env[0][arg].mtype)
            self.list_template[ast.name_field].mtype.params = arg_list
            if self.return_func is not None:
                raise Report(ReportType.ERROR, ast.locate,
                             "Template can not have a return statement")
            self.in_template = False

    def visitFunction(self, ast: Function, param):
        if self.count_visited == 0:
            if ast.name_field in self.list_function:
                raise Report(ReportType.ERROR, ast.locate,
                             f"Function '{ast.name_field}' already declared")
            env = [{}] + param
            for arg in ast.args:
                if arg in env[0]:
                    raise Report(ReportType.ERROR, ast.locate,
                                 f"Argument '{arg}' already declared")
                env[0][arg] = Symbol(arg, None, VarCircom())
            self.in_function = True
            self.no_block = True
            self.visit(ast.body, env)
            self.in_function = False
            if self.return_func is None:
                raise Report(ReportType.ERROR, ast.locate,
                             "Unable to infer the type of this function")
            arg_list = []
            for arg in ast.args:
                arg_list.append(env[0][arg].mtype)
            self.list_function[ast.name_field] = param[0][ast.name_field] = Symbol(ast.name_field, FunctionCircom(
                ast.name_field, arg_list, self.return_func, ast.body, ast.args), None, ast)
            self.return_func = None
        else:
            self.in_function = True
            self.no_block = True
            env = [{}] + param
            for arg in ast.args:
                env[0][arg] = Symbol(arg, None, VarCircom())
            self.visit(ast.body, env)
            if self.return_func is None:
                raise Report(ReportType.ERROR, ast.locate,
                             "Unable to infer the type of this function")
            self.return_func = None
            self.in_function = False

    def visitProgram(self, ast: Program, param):
        for _ in range(2):
            for definition in ast.definitions:
                self.visit(definition, param)
            self.count_visited += 1
        if ast.main_component is None:
            raise Report(ReportType.ERROR, ast.locate,
                         "Main component not declared")
        self.visit(ast.main_component, param)

    def visitIfThenElse(self, ast: IfThenElse, param):
        if self.count_visited == 0:
            self.visit(ast.if_case, param)
            if ast.else_case:
                self.visit(ast.else_case, param)
                return
        cond_type = self.visit(ast.cond, param)
        if isinstance(cond_type, TemplateCircom):
            raise Report(ReportType.ERROR, ast.cond.locate,
                         "Must be a single arithmetic expression. Found component")
        elif isinstance(cond_type, ArrayCircom):
            raise Report(ReportType.ERROR, ast.cond.locate,
                         "Must be a single arithmetic expression. Found array")
        self.visit(ast.if_case, param)
        if ast.else_case:
            self.visit(ast.else_case, param)

    def visitWhile(self, ast: While, param):
        if self.count_visited == 0:
            self.visit(ast.stmt, param)
            return
        cond_type = self.visit(ast.cond, param)
        if isinstance(cond_type, TemplateCircom):
            raise Report(ReportType.ERROR, ast.cond.locate,
                         "Must be a single arithmetic expression. Found component")
        elif isinstance(cond_type, ArrayCircom):
            raise Report(ReportType.ERROR, ast.cond.locate,
                         "Must be a single arithmetic expression. Found array")
        self.visit(ast.stmt, param)

    def visitReturn(self, ast: Return, param):
        if self.in_function:
            value_type = self.visit(ast.value, param)
            if isinstance(value_type, TemplateCircom):
                raise Report(ReportType.ERROR, ast.value.locate,
                             "Must be a single arithmetic expression. Found component")
            if self.return_func is None:
                self.return_func = value_type
            if not is_same_type(value_type, self.return_func):
                raise Report(ReportType.ERROR, ast.value.locate,
                             "Return type is not compatible with the function return type")
        else:
            raise Report(ReportType.ERROR, ast.locate,
                         "Return statement outside of a function")

    def visitInitializationBlock(self, ast: InitializationBlock, param):
        for init in ast.initializations:
            if self.count_visited == 0:
                if isinstance(init, Declaration):
                    self.visit(init, param)
            else:
                self.visit(init, param)

    def visitDeclaration(self, ast: Declaration, param):
        if ast.name in param[0]:
            raise Report(ReportType.ERROR, ast.locate,
                         f"Variable '{ast.name}' already declared")
        for expr in ast.dimensions:
            expr_type = self.visit(expr, param)
            if isinstance(expr_type, TemplateCircom):
                raise Report(ReportType.ERROR, expr.locate,
                             "Array indexes and lengths must be single arithmetic expressions. Found component instead of expression.")
            elif isinstance(expr_type, ArrayCircom):
                raise Report(ReportType.ERROR, expr.locate,
                             "Array indexes and lengths must be single arithmetic expressions. Found array instead of expression.")
        xtype = self.visit(ast.xtype, param)
        if isinstance(xtype, SignalCircom):
            if self.count_visited == 0:
                if ast.name in self.template_signals:
                    raise Report(ReportType.ERROR, ast.locate,
                                 f"Signal '{ast.name}' already declared")
                if xtype.signal_type == SignalType.INPUT:
                    self.signal_in.append(ast.name)
                elif xtype.signal_type == SignalType.OUTPUT:
                    self.signal_out.append(ast.name)
            if len(ast.dimensions) > 0:
                mtype = ArrayCircom(PrimeField(), len(ast.dimensions))
            else:
                mtype = PrimeField()
            if self.count_visited == 0:
                self.template_signals[ast.name] = mtype
                self.signals_ast[ast.name] = ast
            param[0][ast.name] = Symbol(ast.name, mtype, xtype, ast)
        elif isinstance(xtype, VarCircom):
            if len(ast.dimensions) > 0:
                mtype = ArrayCircom(PrimeField(), len(ast.dimensions))
            else:
                mtype = PrimeField()
            param[0][ast.name] = Symbol(ast.name, mtype, xtype, ast)
        elif isinstance(xtype, ComponentCircom):
            template_type = TemplateCircom("", None)
            if len(ast.dimensions) > 0:
                mtype = ArrayCircom(template_type, len(ast.dimensions))
            else:
                mtype = template_type
            param[0][ast.name] = Symbol(ast.name, mtype, xtype, ast)

    def visitSubstitution(self, ast: Substitution, param):
        if self.count_visited == 0:
            return
        symbol = None
        for env in param:
            if ast.var in env:
                symbol = env[ast.var]
                break
        if self.is_multi_sub:
            self.is_multi_sub = False
            rhe_type = ast.rhe
        else:
            rhe_type = self.visit(ast.rhe, param)
        if ast.var == "_":
            if isinstance(rhe_type, TemplateCircom):
                raise Report(ReportType.ERROR, ast.rhe.locate,
                             "Must be a single arithmetic expression. Found component")
        else:
            lhe_type = self.visit(
                Variable(ast.locate, ast.var, ast.access), param)
            symbol = None
            for env in param:
                if ast.var in env:
                    symbol = env[ast.var]
                    break
            if isinstance(symbol.xtype, SignalCircom):
                if symbol.xtype.signal_type == SignalType.INPUT:
                    raise Report(ReportType.ERROR, ast.locate,
                                 "Cannot assign to an input signal")
                if ast.op == "=":
                    raise Report(ReportType.ERROR, ast.locate,
                                 "Cannot assign to a signal")
                if rhe_type is None:
                    self.infer_type(ast.rhe, param, lhe_type)
                    rhe_type = lhe_type
                if isinstance(rhe_type, TemplateCircom):
                    raise Report(ReportType.ERROR, ast.rhe.locate,
                                 "Must be a single arithmetic expression. Found component")
                if not is_same_type(lhe_type, rhe_type):
                    raise Report(ReportType.ERROR, ast.rhe.locate,
                                 "Types of the two sides of the equality are not compatible")
            elif isinstance(symbol.xtype, VarCircom):
                if ast.op != "=":
                    raise Report(ReportType.ERROR, ast.locate,
                                 "Cannot use operator on a variable")
                if rhe_type is None:
                    self.infer_type(ast.rhe, param, lhe_type)
                    rhe_type = lhe_type
                if isinstance(rhe_type, TemplateCircom):
                    raise Report(ReportType.ERROR, ast.rhe.locate,
                                 "Must be a single arithmetic expression. Found component")
                if not is_same_type(lhe_type, rhe_type):
                    raise Report(ReportType.ERROR, ast.rhe.locate,
                                 "Types of the two sides of the equality are not compatible")
            elif isinstance(symbol.xtype, ComponentCircom):
                if isinstance(lhe_type, TemplateCircom):
                    if not isinstance(rhe_type, TemplateCircom):
                        raise Report(ReportType.ERROR, ast.rhe.locate,
                                     "Assignee and assigned types do not match.\n Expected template but found expression.")
                    if ast.op != "=":
                        raise Report(ReportType.ERROR, ast.locate,
                                     "Cannot use operator on a component")
                    if lhe_type.name == "":
                        lhe_type.name = rhe_type.name
                        lhe_type.params = rhe_type.params
                        lhe_type.signals = rhe_type.signals
                        lhe_type.signals_in = rhe_type.signals_in
                        lhe_type.signals_out = rhe_type.signals_out
                        lhe_type.args = rhe_type.args
                    else:
                        if lhe_type.name != rhe_type.name:
                            raise Report(ReportType.ERROR, ast.locate,
                                         "Assignee and assigned types do not match.")
                elif not is_same_type(lhe_type, rhe_type):
                    if rhe_type is None:
                        self.infer_type(ast.rhe, param, lhe_type)
                        return
                    raise Report(ReportType.ERROR, ast.rhe.locate,
                                 "Assignee and assigned types do not match.")

    def visitMultiSubstitution(self, ast: MultiSubstitution, param):
        if not isinstance(ast.lhe, TupleExpr):
            raise Report(ReportType.ERROR, ast.lhe.locate,
                         "Left hand side of the substitution must be a tuple")
        if not isinstance(ast.rhe, AnonymousComponentExpr):
            raise Report(ReportType.ERROR, ast.rhe.locate,
                         "Right hand side of the substitution must be a component")
        lhe_type = self.visit(ast.lhe, param)
        rhe_type = self.visit(ast.rhe, param)
        if len(lhe_type) != len(rhe_type):
            raise Report(ReportType.ERROR, ast.rhe.locate,
                         "Number of elements in the left hand side and right hand side must be the same")
        for i in range(len(lhe_type)):
            if not isinstance(lhe_type[i], Variable):
                raise Report(ReportType.ERROR, ast.lhe.locate, "Not variable")
            if lhe_type.name == "_":
                continue
            self.is_multi_sub = True
            self.visit(Substitution(
                ast.lhe[i].locate, lhe_type[i].name, lhe_type[i].access, ast.op, rhe_type[i]), param)

    def visitConstraintEquality(self, ast: ConstraintEquality, param):
        lhe_type = self.visit(ast.lhe, param)
        rhe_type = self.visit(ast.rhe, param)
        if isinstance(lhe_type, TemplateCircom):
            raise Report(ReportType.ERROR, ast.lhe.locate,
                         "Must be a single arithmetic expression. Found component")
        if isinstance(rhe_type, TemplateCircom):
            raise Report(ReportType.ERROR, ast.rhe.locate,
                         "Must be a single arithmetic expression. Found component")
        if not is_same_type(lhe_type, rhe_type):
            raise Report(ReportType.ERROR, ast.rhe.locate,
                         "Types of the two sides of the equality are not compatible")

    def visitLogCall(self, ast: LogCall, param):
        for arg in ast.args:
            if isinstance(arg, LogExp):
                arg_type = self.visit(arg, param)
                if isinstance(arg_type, TemplateCircom):
                    raise Report(ReportType.ERROR, arg.locate,
                                 "Must be a single arithmetic expression. Found component")
                elif isinstance(arg_type, ArrayCircom):
                    raise Report(ReportType.ERROR, arg.locate,
                                 "Must be a single arithmetic expression. Found array")

    def visitBlock(self, ast: Block, param):
        if self.in_template or self.no_block:
            env = param
            self.in_template = False
            self.no_block = False
        else:
            env = [{}] + param
        for stmt in ast.stmts:
            if self.count_visited == 0:
                if isinstance(stmt, InitializationBlock) or isinstance(stmt, Return) or isinstance(stmt,
                                                                                                   Block) or isinstance(
                        stmt, IfThenElse) or isinstance(stmt, While):
                    self.visit(stmt, env)
            else:
                self.visit(stmt, env)

    def visitAssert(self, ast: Assert, param):
        arg_type = self.visit(ast.arg, param)
        if isinstance(arg_type, TemplateCircom):
            raise Report(ReportType.ERROR, ast.locate,
                         "Must be a single arithmetic expression. Found component")
        elif isinstance(arg_type, ArrayCircom):
            raise Report(ReportType.ERROR, ast.locate,
                         "Must be a single arithmetic expression. Found array")

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
        lhe_type = self.visit(ast.lhe, param)
        if lhe_type is None:
            self.infer_type(ast.lhe, param)
            lhe_type = PrimeField()
        rhe_type = self.visit(ast.rhe, param)
        if rhe_type is None:
            self.infer_type(ast.rhe, param)
            rhe_type = PrimeField()
        if isinstance(lhe_type, TemplateCircom) or isinstance(lhe_type, ArrayCircom):
            raise Report(ReportType.ERROR, ast.lhe.locate,
                         "Type not allowed by the operator")
        if isinstance(rhe_type, TemplateCircom) or isinstance(rhe_type, ArrayCircom):
            raise Report(ReportType.ERROR, ast.rhe.locate,
                         "Type not allowed by the operator")
        return PrimeField()

    def visitPrefixOp(self, ast: PrefixOp, param):
        rhe_type = self.visit(ast.rhe, param)
        if rhe_type is None:
            self.infer_type(ast.rhe, param)
            rhe_type = PrimeField()
        if isinstance(rhe_type, TemplateCircom) or isinstance(rhe_type, ArrayCircom):
            raise Report(ReportType.ERROR, ast.rhe.locate,
                         "Type not allowed by the operator")
        return PrimeField()

    def visitInlineSwitchOp(self, ast: InlineSwitchOp, param):
        cond_type = self.visit(ast.cond, param)
        if isinstance(cond_type, TemplateCircom):
            raise Report(ReportType.ERROR, ast.cond.locate,
                         "Must be a single arithmetic expression. Found component")
        elif isinstance(cond_type, ArrayCircom):
            raise Report(ReportType.ERROR, ast.cond.locate,
                         "Must be a single arithmetic expression. Found array")
        if_true_type = self.visit(ast.if_true, param)
        if_false_type = self.visit(ast.if_false, param)
        if not is_same_type(if_true_type, if_false_type):
            raise Report(ReportType.ERROR, ast.if_false.locate,
                         "Inline switch operator branches types are non compatible")
        return if_true_type

    def visitParrallelOp(self, ast: ParallelOp, param):
        rhe_type = self.visit(ast.rhe, param)
        if not isinstance(rhe_type, TemplateCircom):
            raise Report(ReportType.ERROR, ast.rhe.locate,
                         "Type not allowed by the operator parallel (parallel operator can only be applied to templates)")
        return rhe_type

    def visitVariable(self, ast: Variable, param):
        symbol = None
        for env in param:
            if ast.name in env:
                symbol = env[ast.name]
                break
        if symbol is None:
            raise Report(ReportType.ERROR, ast.locate,
                         f"Variable '{ast.name}' not declared")
        typ = symbol.mtype
        if typ is None:
            return None
        if isinstance(typ, ArrayCircom):
            var_type = ArrayCircom(typ.eleType, typ.dims)
        else:
            var_type = typ
        for i in range(len(ast.access)):
            if isinstance(var_type, PrimeField):
                raise Report(ReportType.ERROR, ast.locate,
                             f"Variable '{ast.name}' is not an array or component")
            access_type = self.visit(ast.access[i], param)
            if isinstance(access_type, PrimeField):
                if not isinstance(var_type, ArrayCircom):
                    raise Report(ReportType.ERROR, ast.locate,
                                 f"Variable '{ast.name}' is not an array")
                if var_type.dims == 1:
                    var_type = var_type.eleType
                else:
                    var_type.dims -= 1
            else:
                if not isinstance(var_type, TemplateCircom):
                    raise Report(ReportType.ERROR, ast.locate,
                                 f"Variable '{ast.name}' is not a component")
                # print(ast.locate)
                signal_type = var_type.signals[access_type]
                if isinstance(signal_type, ArrayCircom):
                    var_type = ArrayCircom(
                        signal_type.eleType, signal_type.dims)
                else:
                    var_type = signal_type
        return var_type

    def visitNumber(self, ast: Number, param):
        return PrimeField()

    def visitCall(self, ast: Call, param):
        if ast.id in self.list_function:
            func_type = self.list_function[ast.id].mtype
        elif ast.id in self.list_template:
            func_type = self.list_template[ast.id].mtype
        else:
            raise Report(ReportType.ERROR, ast.locate,
                         f"Function or Template '{ast.id}' not declared")
        if not isinstance(func_type, (FunctionCircom, TemplateCircom)):
            raise Report(ReportType.ERROR, ast.locate,
                         f"'{ast.id}' is not a function or template")
        if len(ast.args) != len(func_type.params):
            raise Report(ReportType.ERROR, ast.locate,
                         f"Function '{ast.id}' has {len(func_type.params)} arguments, but {len(ast.args)} were provided")
        for arg in ast.args:
            self.visit(arg, param)
        if isinstance(func_type, FunctionCircom):
            return func_type.return_type
        elif isinstance(func_type, TemplateCircom):
            return func_type

    def visitAnonymousComponentExpr(self, ast: AnonymousComponentExpr, param):
        template_type = None
        for env in param:
            if ast.id in env:
                template_type = env[ast.id].mtype
                break
        if template_type is None or not isinstance(template_type, TemplateCircom):
            raise Report(ReportType.ERROR, ast.locate,
                         f"Template '{ast.id}' not declared")
        if len(ast.params) != len(template_type.params):
            raise Report(ReportType.ERROR, ast.locate,
                         "Don't have same size of params")
        for i in range(len(ast.params)):
            param_type = self.visit(ast.params[i], param)
            if not is_same_type(param_type, template_type.params[i]):
                raise Report(ReportType.ERROR, par.locate,
                             "Type Mismatch in parameter")
        if ast.names and ast.names[0]:
            if len(ast.names) != len(template_type.signals_in):
                raise Report(ReportType.ERROR, ast.locate,
                             f"Template '{ast.id}' has {len(template_type.signals_in)} input signals, but {len(ast.names)} were provided")
            for i in range(len(ast.names)):
                op, name = ast.names[i]
                if name not in template_type.signals:
                    raise Report(ReportType.ERROR, ast.locate,
                                 f"Signal '{name}' not declared in template '{ast.id}'")
                if name not in template_type.signals_in:
                    raise Report(ReportType.ERROR, ast.locate,
                                 f"Signal '{name}' is not an input signal")
                if not is_same_type(template_type.signals[name], self.visit(ast.signals[i], param)):
                    raise Report(ReportType.ERROR, ast.locate,
                                 f"Signal '{name}' type does not match the template '{ast.id}' input signal type")
        else:
            if len(ast.signals) != len(template_type.signals_in):
                raise Report(ReportType.ERROR, ast.locate,
                             f"Template '{ast.id}' has {len(template_type.signals_in)} input signals, but {len(ast.signals)} were provided")
            for i in range(len(ast.signals)):
                if not is_same_type(template_type.signals[template_type.signals_in[i]],
                                    self.visit(ast.signals[i], param)):
                    raise Report(ReportType.ERROR, ast.locate,
                                 f"Signal '{template_type.signals_in[i]}' type does not match the template '{ast.id}' input signal type")
        return_tuple = []
        for name in template_type.signals_out:
            return_tuple.append(template_type.signals[name])
        return return_tuple if len(return_tuple) > 1 else return_tuple[0]

    def visitArrayInLine(self, ast: ArrayInLine, param):
        type_list = []
        for value in ast.values:
            type_list.append(self.visit(value, param))
        first_type = type_list[0]
        if isinstance(first_type, TemplateCircom):
            raise Report(
                ReportType.ERROR, ast.values[0].locate, "Components can not be declared inside inline arrays")
        for i in range(1, len(type_list)):
            if isinstance(type_list[i], TemplateCircom):
                raise Report(
                    ReportType.ERROR, ast.values[i].locate, "Components can not be declared inside inline arrays")
            elif not is_same_type(first_type, type_list[i]):
                raise Report(ReportType.ERROR, ast.values[i].locate,
                             "All elements in the array must be of the same type")
        if isinstance(first_type, PrimeField):
            return ArrayCircom(first_type, 1)
        elif isinstance(first_type, ArrayCircom):
            return ArrayCircom(first_type.eleType, first_type.dims + 1)

    def visitTupleExpr(self, ast: TupleExpr, param):
        return ast.values

    def visitComponentAccess(self, ast: ComponentAccess, param):
        return ast.name

    def visitArrayAccess(self, ast: ArrayAccess, param):
        expr_type = self.visit(ast.expr, param)
        if isinstance(expr_type, TemplateCircom):
            raise Report(ReportType.ERROR, ast.expr.locate,
                         "Array indexes and lengths must be single arithmetic expressions. Found component instead of expression.")
        elif isinstance(expr_type, ArrayCircom):
            raise Report(ReportType.ERROR, ast.expr.locate,
                         "Array indexes and lengths must be single arithmetic expressions. Found array instead of expression.")
        return PrimeField()

    def visitLogStr(self, ast: LogStr, param):
        return None

    def visitLogExp(self, ast: LogExp, param):
        return self.visit(ast.expr, param)
