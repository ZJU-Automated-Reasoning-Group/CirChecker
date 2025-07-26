from __future__ import annotations
from dataclasses import dataclass, fields
from typing import Optional, List, Tuple
from abc import ABC, abstractmethod
from Visitor import Visitor
from antlr4 import Token


class AST(ABC):
    @abstractmethod
    def accept(self, v: Visitor, param):
        return v.visit(self, param)

    def __str__(self, indent: str = "", is_last: bool = True):
        label = self.__class__.__name__
        branch = "└── " if is_last else "├── "
        output = [f"{indent}{branch}{label}"]
        indent += "    " if is_last else "│   "

        for i, field in enumerate(fields(self)):
            value = getattr(self, field.name)
            is_last_field = i == len(fields(self)) - 1
            branch = "└── " if is_last_field else "├── "
            line = f"{indent}{branch}{field.name}:"

            if isinstance(value, AST):
                output.append(line)
                output.append(value.__str__(
                    indent + ("    " if is_last_field else "│   "), True))
            elif isinstance(value, list):
                output.append(line)
                for j, item in enumerate(value):
                    is_last_item = j == len(value) - 1
                    if isinstance(item, AST):
                        output.append(item.__str__(
                            indent + ("    " if is_last_field else "│   "), is_last_item))
                    else:
                        branch = "└── " if is_last_item else "├── "
                        output.append(f"{indent}    {branch}{item}")
            else:
                output.append(f"{line} {value}")

        return "\n".join(output)


class Expression(AST):
    pass


class Definition(AST):
    pass


class Statement(AST):
    pass


class VariableType(AST):
    pass


class Access(AST):
    pass


class LogArgument(AST):
    pass


@dataclass
class FileLocation(AST):
    path: str
    start: Token
    stop: Token

    def __str__(self, indent: str = "", is_last: bool = True):
        label = self.__class__.__name__
        branch = "└── " if is_last else "├── "
        output = [f"{indent}{branch}{label}"]
        indent += "    " if is_last else "│   "
        output.append(f"{indent}├── path: {self.path}")

        start_line = self.start.line
        start_column = self.start.column
        output.append(
            f"{indent}├── start: line {start_line}, column {start_column}")
        stop_line = self.stop.line
        stop_column = self.stop.column
        output.append(
            f"{indent}└── stop: line {stop_line}, column {stop_column}")

        return "\n".join(output)

    def accept(self, v: Visitor, param):
        return v.visitFileLocation(self, param)


@dataclass
class MainComponent(AST):
    locate: FileLocation
    publics: List[str]
    expr: Expression

    def accept(self, v: Visitor, param):
        return v.visitMainComponent(self, param)


@dataclass
class Include(AST):
    locate: FileLocation
    path: str

    def accept(self, v: Visitor, param):
        return v.visitInclude(self, param)


@dataclass
class Program(AST):
    locate: FileLocation
    compile_version: Optional[Tuple[int, int, int]]
    custom_gates: bool
    custom_gates_declare: bool
    includes: List[Include]
    definitions: List[Definition]
    main_component: Optional[MainComponent]

    def accept(self, v: Visitor, param):
        return v.visitProgram(self, param)


@dataclass
class Template(Definition):
    locate: FileLocation
    name_field: str
    args: List[str]
    body: Statement
    parallel: bool
    is_custom_gate: bool

    def accept(self, v: Visitor, param):
        return v.visitTemplate(self, param)


@dataclass
class Function(Definition):
    locate: FileLocation
    name_field: str
    args: List[str]
    body: Statement

    def accept(self, v: Visitor, param):
        return v.visitFunction(self, param)


@dataclass
class IfThenElse(Statement):
    locate: FileLocation
    cond: Expression
    if_case: Statement
    else_case: Optional[Statement]

    def accept(self, v: Visitor, param):
        return v.visitIfThenElse(self, param)


@dataclass
class While(Statement):
    locate: FileLocation
    cond: Expression
    stmt: Statement

    def accept(self, v: Visitor, param):
        return v.visitWhile(self, param)


@dataclass
class Return(Statement):
    locate: FileLocation
    value: Expression

    def accept(self, v: Visitor, param):
        return v.visitReturn(self, param)


@dataclass
class InitializationBlock(Statement):
    locate: FileLocation
    xtype: VariableType
    initializations: List[Statement]

    def accept(self, v: Visitor, param):
        return v.visitInitializationBlock(self, param)


@dataclass
class Declaration(Statement):
    locate: FileLocation
    xtype: VariableType
    name: str
    dimensions: List[Expression]
    is_constant: bool

    def accept(self, v: Visitor, param):
        return v.visitDeclaration(self, param)


@dataclass
class Substitution(Statement):
    locate: FileLocation
    var: str
    access: List[Access]
    op: str
    rhe: Expression

    def accept(self, v: Visitor, param):
        return v.visitSubstitution(self, param)


@dataclass
class MultiSubstitution(Statement):
    locate: FileLocation
    lhe: Expression
    op: str
    rhe: Expression

    def accept(self, v: Visitor, param):
        return v.visitMultiSubstitution(self, param)


@dataclass
class ConstraintEquality(Statement):
    locate: FileLocation
    lhe: Expression
    rhe: Expression

    def accept(self, v: Visitor, param):
        return v.visitConstraintEquality(self, param)


@dataclass
class LogCall(Statement):
    locate: FileLocation
    args: List[LogArgument]

    def accept(self, v: Visitor, param):
        return v.visitLogCall(self, param)


@dataclass
class Block(Statement):
    locate: FileLocation
    stmts: List[Statement]

    def accept(self, v: Visitor, param):
        return v.visitBlock(self, param)


@dataclass
class Assert(Statement):
    locate: FileLocation
    arg: Expression

    def accept(self, v: Visitor, param):
        return v.visitAssert(self, param)


@dataclass
class Var(VariableType):
    def accept(self, v: Visitor, param):
        return v.visitVar(self, param)


@dataclass
class Signal(VariableType):
    locate: FileLocation
    signal_type: str
    tag_list: List[str]

    def accept(self, v: Visitor, param):
        return v.visitSignal(self, param)


@dataclass
class Component(VariableType):
    def accept(self, v: Visitor, param):
        return v.visitComponent(self, param)


@dataclass
class AnonymousComponent(VariableType):
    def accept(self, v: Visitor, param):
        return v.visitAnonymousComponent(self, param)


@dataclass
class InfixOp(Expression):
    locate: FileLocation
    lhe: Expression
    infix_op: str
    rhe: Expression

    def accept(self, v: Visitor, param):
        return v.visitInfixOp(self, param)


@dataclass
class PrefixOp(Expression):
    locate: FileLocation
    prefix_op: str
    rhe: Expression

    def accept(self, v: Visitor, param):
        return v.visitPrefixOp(self, param)


@dataclass
class InlineSwitchOp(Expression):
    locate: FileLocation
    cond: Expression
    if_true: Expression
    if_false: Expression

    def accept(self, v: Visitor, param):
        return v.visitInlineSwitchOp(self, param)


@dataclass
class ParallelOp(Expression):
    locate: FileLocation
    rhe: Expression

    def accept(self, v: Visitor, param):
        return v.visitParallelOp(self, param)


@dataclass
class Variable(Expression):
    locate: FileLocation
    name: str
    access: List[Access]

    def accept(self, v: Visitor, param):
        return v.visitVariable(self, param)


@dataclass
class Number(Expression):
    locate: FileLocation
    value: int

    def accept(self, v: Visitor, param):
        return v.visitNumber(self, param)


@dataclass
class Call(Expression):
    locate: FileLocation
    id: str
    args: List[Expression]

    def accept(self, v: Visitor, param):
        return v.visitCall(self, param)


@dataclass
class AnonymousComponentExpr(Expression):
    locate: FileLocation
    id: str
    is_parallel: bool
    params: List[Expression]
    signals: List[Expression]
    names: Optional[List[Tuple[str, str]]]

    def accept(self, v: Visitor, param):
        return v.visitAnonymousComponentExpr(self, param)


@dataclass
class ArrayInLine(Expression):
    locate: FileLocation
    values: List[Expression]

    def accept(self, v: Visitor, param):
        return v.visitArrayInLine(self, param)


@dataclass
class TupleExpr(Expression):
    locate: FileLocation
    values: List[Expression]

    def accept(self, v: Visitor, param):
        return v.visitTupleExpr(self, param)


@dataclass
class ComponentAccess(Access):
    locate: FileLocation
    name: str

    def accept(self, v: Visitor, param):
        return v.visitComponentAccess(self, param)


@dataclass
class ArrayAccess(Access):
    locate: FileLocation
    expr: Expression

    def accept(self, v: Visitor, param):
        return v.visitArrayAccess(self, param)


@dataclass
class LogStr(LogArgument):
    locate: FileLocation
    value: str

    def accept(self, v: Visitor, param):
        return v.visitLogStr(self, param)


@dataclass
class LogExp(LogArgument):
    locate: FileLocation
    expr: Expression

    def accept(self, v: Visitor, param):
        return v.visitLogExp(self, param)
