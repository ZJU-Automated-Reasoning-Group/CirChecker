from CircomVisitor import CircomVisitor
from CircomLexer import CircomLexer
from CircomParser import CircomParser
from AST import *
import Errors
import os
from antlr4 import *
import sys
from Report import Report, ReportType

sys.setrecursionlimit(5000)


class ASTGeneration(CircomVisitor):
    def generate_ast(self, filename, tree, path_env):
        print("[Info]       Generating AST for:", filename)
        self.file_name = filename
        ast_tree = self.visit(tree)
        base_dir = os.path.dirname(filename)
        for include in ast_tree.includes:
            raw_include_path = include.path.strip('"').strip("'")
            absolute_path = os.path.abspath(
                os.path.join(base_dir, raw_include_path))
            if not os.path.isfile(absolute_path):
                Report(ReportType.ERROR, ast_tree.locate,
                       Errors.IncludeNotFound(absolute_path)).show()
                return None
            if absolute_path in path_env:
                continue
            path_env.append(absolute_path)
            inputstream = FileStream(absolute_path, encoding='utf-8')
            lexer = CircomLexer(inputstream)
            listener = Errors.NewErrorListener.INSTANCE
            tokens = CommonTokenStream(lexer)
            parser = CircomParser(tokens)
            parser.removeErrorListeners()
            parser.addErrorListener(listener)
            try:
                tree = parser.program()
            except Errors.SyntaxException as f:
                Report(ReportType.ERROR, FileLocation(
                    absolute_path, None, None), f.message, False).show()
                return None
            except Exception as e:
                Report(ReportType.ERROR, FileLocation(
                    absolute_path, None, None), str(e), False).show()
                return None
            try:
                asttree = ASTGeneration().generate_ast(absolute_path, tree, path_env)
                if asttree.main_component:
                    Report(ReportType.ERROR, FileLocation(
                        absolute_path, None, None), "Main component found in include file", False).show()
                    return None
                ast_tree.definitions += asttree.definitions
            except Exception as e:
                Report(ReportType.ERROR, FileLocation(
                    absolute_path, None, None), str(e), False).show()
                return None
        return ast_tree

    # program: pragma_definition? custom_gate? include_list definition_list main_option EOF;
    def visitProgram(self, ctx: CircomParser.ProgramContext):
        compile_version = self.visit(
            ctx.pragma_definition()) if ctx.pragma_definition() else None
        custom_gates = True if ctx.custom_gate() else False
        definitions = self.visit(ctx.definition_list())
        custom_gates_declare = False
        includes = self.visit(ctx.include_list())
        main_component = self.visit(ctx.main_option())
        for definition in definitions:
            if isinstance(definition, Template) and definition.is_custom_gate:
                custom_gates_declare = True
                break
        return Program(FileLocation(self.file_name, ctx.start, ctx.stop), compile_version, custom_gates,
                       custom_gates_declare, includes, definitions, main_component)

    # version: NUMBER '.' NUMBER '.' NUMBER ;
    def visitVersion(self, ctx: CircomParser.VersionContext):
        return (int(ctx.NUMBER(0).getText()), int(ctx.NUMBER(1).getText()), int(ctx.NUMBER(2).getText()))

    # main_option: main_component | ;
    def visitMain_option(self, ctx: CircomParser.Main_optionContext):
        return self.visit(ctx.main_component()) if ctx.main_component() else None

    # definition_block: function_definition | template_definition;
    def visitDefinition_block(self, ctx: CircomParser.Definition_blockContext):
        return self.visit(ctx.getChild(0))

    # definition_list: definition_block definition_list | ;
    def visitDefinition_list(self, ctx: CircomParser.Definition_listContext):
        return [self.visit(ctx.definition_block())] + self.visit(
            ctx.definition_list()) if ctx.definition_block() else []

    # pragma_definition: PRAGMA CIRCOM version SEMICOLON;
    def visitPragma_definition(self, ctx: CircomParser.Pragma_definitionContext):
        return self.visit(ctx.version())

    # custom_gate: PRAGMA CUSTOM_TEMPLATES SEMICOLON;
    def visitCustom_gate(self, ctx: CircomParser.Custom_gateContext):
        pass

    # include_list: include_definition include_list | ;
    def visitInclude_list(self, ctx: CircomParser.Include_listContext):
        return [self.visit(ctx.include_definition())] + self.visit(
            ctx.include_list()) if ctx.include_definition() else []

    # include_definition: INCLUDE STRING SEMICOLON;
    def visitInclude_definition(self, ctx: CircomParser.Include_definitionContext):
        return Include(FileLocation(self.file_name, ctx.start, ctx.stop), ctx.STRING().getText())

    # public_list: LC PUBLIC LB identifier_list RB RC | ;
    def visitPublic_list(self, ctx: CircomParser.Public_listContext):
        return self.visit(ctx.identifier_list()) if ctx.identifier_list() else []

    # main_component: COMPONENT MAIN public_list ASSIGNMENT expression SEMICOLON;
    def visitMain_component(self, ctx: CircomParser.Main_componentContext):
        return MainComponent(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.public_list()),
                             self.visit(ctx.expression()))

    # function_definition: FUNCTION IDENTIFIER LP identifier_list_option RP block;
    def visitFunction_definition(self, ctx: CircomParser.Function_definitionContext):
        return Function(FileLocation(self.file_name, ctx.start, ctx.stop), ctx.IDENTIFIER().getText(),
                        self.visit(ctx.identifier_list_option()), self.visit(ctx.block()))

    # template_definition: TEMPLATE custom_option parallel_option IDENTIFIER LP identifier_list_option RP block;
    def visitTemplate_definition(self, ctx: CircomParser.Template_definitionContext):
        is_custom = self.visit(ctx.custom_option())
        is_parallel = self.visit(ctx.parallel_option())
        return Template(FileLocation(self.file_name, ctx.start, ctx.stop), ctx.IDENTIFIER().getText(),
                        self.visit(ctx.identifier_list_option()), self.visit(ctx.block()), is_parallel, is_custom)

    # identifier_list_option: identifier_list | ;
    def visitIdentifier_list_option(self, ctx: CircomParser.Identifier_list_optionContext):
        return self.visit(ctx.identifier_list()) if ctx.identifier_list() else []

    # custom_option: CUSTOM | ;
    def visitCustom_option(self, ctx: CircomParser.Custom_optionContext):
        return ctx.CUSTOM().getText() if ctx.CUSTOM() else None

    # parallel_option: PARALLEL | ;
    def visitParallel_option(self, ctx: CircomParser.Parallel_optionContext):
        return ctx.PARALLEL().getText() if ctx.PARALLEL() else None

    # block: LC statement_list RC;
    def visitBlock(self, ctx: CircomParser.BlockContext):
        return Block(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.statement_list()))

    # statement
    #     : declaration_statement
    #     | if_statement
    #     | regular_statement
    #     ;
    def visitStatement(self, ctx: CircomParser.StatementContext):
        return self.visit(ctx.getChild(0))

    # statement_list: statement statement_list | ;
    def visitStatement_list(self, ctx: CircomParser.Statement_listContext):
        return [self.visit(ctx.statement())] + self.visit(ctx.statement_list()) if ctx.statement() else []

    # declaration_statement: declaration SEMICOLON;
    def visitDeclaration_statement(self, ctx):
        return self.visit(ctx.declaration())

    # expression_statement: expression SEMICOLON;
    def visitExpression_statement(self, ctx: CircomParser.Expression_statementContext):
        return MultiSubstitution(FileLocation(self.file_name, ctx.start, ctx.stop),
                                 TupleExpr(FileLocation(self.file_name, ctx.start, ctx.stop), []), "<==",
                                 self.visit(ctx.expression()))

    # substitutions
    #     : expression assign_opcode expression
    #     | expression RIGHT_ASSIGNMENT expression
    #     | expression RIGHT_CONSTRAINT expression
    #     | variable ASSIGNMENT_WITH_OP expression
    #     | variable SELF_OP
    #     ;
    def visitSubstitutions(self, ctx: CircomParser.SubstitutionsContext):
        if ctx.SELF_OP():
            op = ctx.SELF_OP().getText()[0]
            variable = self.visit(ctx.variable())
            return Substitution(FileLocation(self.file_name, ctx.start, ctx.stop), variable.name, variable.access, "=",
                                InfixOp(FileLocation(self.file_name, ctx.start, ctx.stop), variable, op,
                                        Number(FileLocation(self.file_name, ctx.start, ctx.stop), 1)))
        elif ctx.ASSIGNMENT_WITH_OP():
            op = ctx.ASSIGNMENT_WITH_OP().getText()[:-1]
            variable = self.visit(ctx.variable())
            return Substitution(FileLocation(self.file_name, ctx.start, ctx.stop), variable.name, variable.access, "=",
                                InfixOp(FileLocation(self.file_name, ctx.start, ctx.stop), variable, op,
                                        self.visit(ctx.expression(0))))
        elif ctx.RIGHT_ASSIGNMENT() or ctx.RIGHT_CONSTRAINT():
            if ctx.RIGHT_ASSIGNMENT():
                op = ctx.RIGHT_ASSIGNMENT().getText()
            else:
                op = ctx.RIGHT_CONSTRAINT().getText()
            var = self.visit(ctx.expression(1))
            return Substitution(FileLocation(self.file_name, ctx.start, ctx.stop), var.name, var.access, op,
                                self.visit(ctx.expression(0))) if isinstance(var, Variable) else MultiSubstitution(
                FileLocation(self.file_name, ctx.start, ctx.stop), var, op, self.visit(ctx.expression(0)))
        else:
            op = self.visit(ctx.assign_opcode())
            var = self.visit(ctx.expression(0))
            return Substitution(FileLocation(self.file_name, ctx.start, ctx.stop), var.name, var.access, op,
                                self.visit(ctx.expression(1))) if isinstance(var, Variable) else MultiSubstitution(
                FileLocation(self.file_name, ctx.start, ctx.stop), var, op, self.visit(ctx.expression(1)))

    # substitutions_statement: substitutions SEMICOLON;
    def visitSubstitutions_statement(self, ctx: CircomParser.Substitutions_statementContext):
        return self.visit(ctx.getChild(0))

    # if_statement
    #     : IF LP expression RP if_statement
    #     | IF LP expression RP regular_statement
    #     | IF LP expression RP regular_statement ELSE if_statement
    #     | IF LP expression RP regular_statement ELSE regular_statement
    #     ;
    def visitIf_statement(self, ctx: CircomParser.If_statementContext):
        if ctx.ELSE():
            return IfThenElse(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression()),
                              self.visit(ctx.regular_statement(0)),
                              self.visit(ctx.if_statement()) if ctx.if_statement() else self.visit(
                                  ctx.regular_statement(1)))
        else:
            return IfThenElse(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression()),
                              self.visit(ctx.if_statement()) if ctx.if_statement() else self.visit(
                                  ctx.regular_statement(0)), None)

    # regular_statement
    #     : block
    #     | expression_statement
    #     | substitutions_statement
    #     | for_statement
    #     | while_statement
    #     | equal_constraint_statement
    #     | return_statement
    #     | assert_statement
    #     | log_statement
    #     ;
    def visitRegular_statement(self, ctx: CircomParser.Regular_statementContext):
        return self.visit(ctx.getChild(0))

    # for_statement
    #     : FOR LP declaration SEMICOLON expression SEMICOLON substitutions RP regular_statement
    #     | FOR LP substitutions SEMICOLON expression SEMICOLON substitutions RP regular_statement
    #     ;
    def visitFor_statement(self, ctx: CircomParser.For_statementContext):
        if ctx.declaration():
            init = self.visit(ctx.declaration())
            while_body = Block(FileLocation(self.file_name, ctx.start, ctx.stop), [
                self.visit(ctx.regular_statement()), self.visit(ctx.substitutions(0))])
        else:
            init = self.visit(ctx.substitutions(0))
            while_body = Block(FileLocation(self.file_name, ctx.start, ctx.stop), [
                self.visit(ctx.regular_statement()), self.visit(ctx.substitutions(1))])
        while_statement = While(FileLocation(self.file_name,
                                             ctx.start, ctx.stop), self.visit(ctx.expression()), while_body)
        return Block(FileLocation(self.file_name, ctx.start, ctx.stop), [init, while_statement])

    # while_statement: WHILE LP expression RP regular_statement;
    def visitWhile_statement(self, ctx: CircomParser.While_statementContext):
        return While(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression()),
                     self.visit(ctx.regular_statement()))

    # equal_constraint_statement: expression EQ_CONSTRAINT expression SEMICOLON;
    def visitEqual_constraint_statement(self, ctx: CircomParser.Equal_constraint_statementContext):
        return ConstraintEquality(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression(0)),
                                  self.visit(ctx.expression(1)))

    # return_statement: RETURN expression SEMICOLON;
    def visitReturn_statement(self, ctx: CircomParser.Return_statementContext):
        return Return(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression()))

    # assert_statement: ASSERT LP expression RP SEMICOLON;
    def visitAssert_statement(self, ctx: CircomParser.Assert_statementContext):
        return Assert(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression()))

    # log_statement
    #     : LOG LP log_list RP SEMICOLON
    #     | LOG LP RP SEMICOLON
    #     ;
    def visitLog_statement(self, ctx: CircomParser.Log_statementContext):
        return LogCall(FileLocation(self.file_name, ctx.start, ctx.stop),
                       self.visit(ctx.log_list()) if ctx.log_list() else [])

    # declaration
    #     : var_decl
    #     | signal_decl
    #     | component_decl
    #     ;
    def visitDeclaration(self, ctx: CircomParser.DeclarationContext):
        return self.visit(ctx.getChild(0))

    # identifier_list: IDENTIFIER COMMA identifier_list | IDENTIFIER;
    def visitIdentifier_list(self, ctx: CircomParser.Identifier_listContext):
        return [ctx.IDENTIFIER().getText()] + self.visit(ctx.identifier_list()) if ctx.identifier_list() else [
            ctx.IDENTIFIER().getText()]

    # tag_list: LC identifier_list RC;
    def visitTag_list(self, ctx: CircomParser.Tag_listContext):
        return self.visit(ctx.identifier_list())

    # tuple_initialization: assign_opcode expression;
    def visitTuple_initialization(self, ctx: CircomParser.Tuple_initializationContext):
        return (self.visit(ctx.assign_opcode()), self.visit(ctx.expression()))

    # simple_symbol: IDENTIFIER array_access_list;
    def visitSimple_symbol(self, ctx: CircomParser.Simple_symbolContext):
        return (ctx.IDENTIFIER().getText(), self.visit(ctx.array_access_list()), None)

    # simple_symbol_list: simple_symbol COMMA simple_symbol_list | simple_symbol;
    def visitSimple_symbol_list(self, ctx: CircomParser.Simple_symbol_listContext):
        return [self.visit(ctx.simple_symbol())] + self.visit(
            ctx.simple_symbol_list()) if ctx.simple_symbol_list() else [self.visit(ctx.simple_symbol())]

    # complex_symbol: IDENTIFIER array_access_list ASSIGNMENT expression;
    def visitComplex_symbol(self, ctx: CircomParser.Complex_symbolContext):
        return (ctx.IDENTIFIER().getText(), self.visit(ctx.array_access_list()), self.visit(ctx.expression()))

    # some_symbol: simple_symbol | complex_symbol;
    def visitSome_symbol(self, ctx: CircomParser.Some_symbolContext):
        return self.visit(ctx.getChild(0))

    # some_symbol_list: some_symbol COMMA some_symbol_list | some_symbol;
    def visitSome_symbol_list(self, ctx: CircomParser.Some_symbol_listContext):
        return [self.visit(ctx.some_symbol())] + self.visit(ctx.some_symbol_list()) if ctx.some_symbol_list() else [
            self.visit(ctx.some_symbol())]

    # var_decl
    #     : VAR some_symbol_list
    #     | VAR LP simple_symbol_list RP
    #     | VAR LP simple_symbol_list RP tuple_initialization
    #     ;
    def visitVar_decl(self, ctx: CircomParser.Var_declContext):
        initializations = []
        if ctx.some_symbol_list():
            symbols = self.visit(ctx.some_symbol_list())
            for symbol in symbols:
                name, dimensions, init = symbol
                initializations.append(Declaration(FileLocation(self.file_name,
                                                                ctx.start, ctx.stop), Var(), name, dimensions, True))
                if init:
                    initializations.append(Substitution(FileLocation(self.file_name,
                                                                     ctx.start, ctx.stop), name, [], "=", init))
        else:
            values = []
            symbols = self.visit(ctx.simple_symbol_list())
            for symbol in symbols:
                name, dimensions, init = symbol
                initializations.append(Declaration(FileLocation(self.file_name,
                                                                ctx.start, ctx.stop), Var(), name, dimensions, True))
                values.append(Variable(FileLocation(self.file_name,
                                                    ctx.start, ctx.stop), name, []))
            if ctx.tuple_initialization():
                op, expr = self.visit(ctx.tuple_initialization())
                initializations.append(MultiSubstitution(FileLocation(self.file_name, ctx.start, ctx.stop), TupleExpr(
                    FileLocation(self.file_name, ctx.start, ctx.stop), values), op, expr))
        return InitializationBlock(FileLocation(self.file_name, ctx.start, ctx.stop), Var(), initializations)

    # signal_decl
    #     : signal_header signal_symbol_list
    #     | signal_header LP simple_symbol_list RP
    #     | signal_header LP simple_symbol_list RP tuple_initialization
    #     ;
    def visitSignal_decl(self, ctx: CircomParser.Signal_declContext):
        xtype = self.visit(ctx.signal_header())
        initializations = []
        if ctx.signal_symbol_list():
            symbols = self.visit(ctx.signal_symbol_list())
            for symbol in symbols:
                name, dimensions, init, sym_op = symbol
                initializations.append(Declaration(FileLocation(self.file_name,
                                                                ctx.start, ctx.stop), xtype, name, dimensions, True))
                if init:
                    initializations.append(Substitution(FileLocation(self.file_name,
                                                                     ctx.start, ctx.stop), name, [], sym_op, init))
        else:
            values = []
            symbols = self.visit(ctx.simple_symbol_list())
            for symbol in symbols:
                name, dimensions, init, sym_op = symbol
                initializations.append(Declaration(FileLocation(self.file_name,
                                                                ctx.start, ctx.stop), xtype, name, dimensions, True))
                values.append(Variable(FileLocation(self.file_name,
                                                    ctx.start, ctx.stop), name, []))
            if ctx.tuple_initialization():
                op, expr = self.visit(ctx.tuple_initialization())
                initializations.append(MultiSubstitution(FileLocation(self.file_name, ctx.start, ctx.stop), TupleExpr(
                    FileLocation(self.file_name, ctx.start, ctx.stop), values), op, expr))
        return InitializationBlock(FileLocation(self.file_name, ctx.start, ctx.stop), xtype, initializations)

    # signal_header
    #     : SIGNAL
    #     | SIGNAL SIGNAL_TYPE
    #     | SIGNAL tag_list
    #     | SIGNAL SIGNAL_TYPE tag_list
    #     ;
    def visitSignal_header(self, ctx: CircomParser.Signal_headerContext):
        return Signal(FileLocation(self.file_name, ctx.start, ctx.stop),
                      ctx.SIGNAL_TYPE().getText() if ctx.SIGNAL_TYPE() else "intermediate",
                      self.visit(ctx.tag_list()) if ctx.tag_list() else [])

    # signal_symbol
    #     : simple_symbol
    #     | IDENTIFIER array_access_list LEFT_CONSTRAINT expression
    #     | IDENTIFIER array_access_list LEFT_ASSIGNMENT expression
    #     ;
    def visitSignal_symbol(self, ctx: CircomParser.Signal_symbolContext):
        if ctx.simple_symbol():
            name, dimensions, init = self.visit(ctx.simple_symbol())
            op = ""
        else:
            name, dimensions, init = ctx.IDENTIFIER().getText(), self.visit(
                ctx.array_access_list()), self.visit(ctx.expression())
            op = ctx.LEFT_ASSIGNMENT().getText() if ctx.LEFT_ASSIGNMENT(
            ) else ctx.LEFT_CONSTRAINT().getText()
        return (name, dimensions, init, op)

    # signal_symbol_list: signal_symbol COMMA signal_symbol_list | signal_symbol;
    def visitSignal_symbol_list(self, ctx: CircomParser.Signal_symbol_listContext):
        return [self.visit(ctx.signal_symbol())] + self.visit(
            ctx.signal_symbol_list()) if ctx.signal_symbol_list() else [self.visit(ctx.signal_symbol())]

    # component_decl
    #     : COMPONENT some_symbol_list
    #     | COMPONENT LP simple_symbol_list RP
    #     | COMPONENT LP simple_symbol_list RP tuple_initialization
    #     ;
    def visitComponent_decl(self, ctx: CircomParser.Component_declContext):
        initializations = []
        if ctx.some_symbol_list():
            symbols = self.visit(ctx.some_symbol_list())
            for symbol in symbols:
                name, dimensions, init = symbol
                initializations.append(Declaration(FileLocation(self.file_name,
                                                                ctx.start, ctx.stop), Component(), name, dimensions,
                                                   True))
                if init:
                    initializations.append(Substitution(FileLocation(self.file_name,
                                                                     ctx.start, ctx.stop), name, [], "=", init))
        else:
            values = []
            symbols = self.visit(ctx.simple_symbol_list())
            for symbol in symbols:
                name, dimensions, init = symbol
                initializations.append(Declaration(FileLocation(self.file_name,
                                                                ctx.start, ctx.stop), Component(), name, dimensions,
                                                   True))
                values.append(Variable(FileLocation(self.file_name,
                                                    ctx.start, ctx.stop), name, []))
            if ctx.tuple_initialization():
                op, expr = self.visit(ctx.tuple_initialization())
                initializations.append(MultiSubstitution(FileLocation(self.file_name, ctx.start, ctx.stop), TupleExpr(
                    FileLocation(self.file_name, ctx.start, ctx.stop), values), op, expr))
        return InitializationBlock(FileLocation(self.file_name, ctx.start, ctx.stop), Component(), initializations)

    # var_access: array_access | component_access;
    def visitVar_access(self, ctx: CircomParser.Var_accessContext):
        return ArrayAccess(FileLocation(self.file_name, ctx.start, ctx.stop),
                           self.visit(ctx.array_access())) if ctx.array_access() else ComponentAccess(
            FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.component_access()))

    # var_access_list: var_access var_access_list | ;
    def visitVar_access_list(self, ctx: CircomParser.Var_access_listContext):
        return [self.visit(ctx.var_access())] + self.visit(ctx.var_access_list()) if ctx.getChildCount() == 2 else []

    # array_access: LB expression RB;
    def visitArray_access(self, ctx: CircomParser.Array_accessContext):
        return self.visit(ctx.expression())

    # array_access_list: array_access array_access_list | ;
    def visitArray_access_list(self, ctx: CircomParser.Array_access_listContext):
        return [self.visit(ctx.array_access())] + self.visit(ctx.array_access_list()) if ctx.array_access() else []

    # component_access: DOT IDENTIFIER;
    def visitComponent_access(self, ctx: CircomParser.Component_accessContext):
        return ctx.IDENTIFIER().getText()

    # variable: IDENTIFIER var_access_list;
    def visitVariable(self, ctx: CircomParser.VariableContext):
        return Variable(FileLocation(self.file_name, ctx.start, ctx.stop), ctx.IDENTIFIER().getText(),
                        self.visit(ctx.var_access_list()))

    # expression
    #     : PARALLEL expression1
    #     | expression1
    #     ;
    def visitExpression(self, ctx: CircomParser.ExpressionContext):
        return ParallelOp(FileLocation(self.file_name, ctx.start, ctx.stop),
                          self.visit(ctx.expression1())) if ctx.PARALLEL() else self.visit(ctx.expression1())

    # expression1
    #     : expression2 TERNARY_CONDITION expression2 TERNARY_ALTERNATIVE expression2
    #     | expression2
    #     ;
    def visitExpression1(self, ctx: CircomParser.Expression1Context):
        return InlineSwitchOp(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression2(0)),
                              self.visit(ctx.expression2(1)),
                              self.visit(ctx.expression2(2))) if ctx.TERNARY_ALTERNATIVE() else self.visit(
            ctx.expression2(0))

    # expression2
    #     : expression2 OR expression3
    #     | expression3
    #     ;
    def visitExpression2(self, ctx: CircomParser.Expression2Context):
        return InfixOp(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression2()),
                       ctx.OR().getText(), self.visit(ctx.expression3())) if ctx.OR() else self.visit(ctx.expression3())

    # expression3
    #     : expression3 AND expression4
    #     | expression4
    #     ;
    def visitExpression3(self, ctx: CircomParser.Expression3Context):
        return InfixOp(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression3()),
                       ctx.AND().getText(), self.visit(ctx.expression4())) if ctx.AND() else self.visit(
            ctx.expression4())

    # expression4
    #     : expression4 compareOpcode expression5
    #     | expression5
    #     ;
    def visitExpression4(self, ctx: CircomParser.Expression4Context):
        return InfixOp(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression4()),
                       self.visit(ctx.compareOpcode()),
                       self.visit(ctx.expression5())) if ctx.compareOpcode() else self.visit(ctx.expression5())

    # expression5
    #     : expression5 BOR expression6
    #     | expression6
    #     ;
    def visitExpression5(self, ctx: CircomParser.Expression5Context):
        return InfixOp(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression5()),
                       ctx.BOR().getText(), self.visit(ctx.expression6())) if ctx.BOR() else self.visit(
            ctx.expression6())

    # expression6
    #     : expression6 BXOR expression7
    #     | expression7
    #     ;
    def visitExpression6(self, ctx: CircomParser.Expression6Context):
        return InfixOp(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression6()),
                       ctx.BXOR().getText(), self.visit(ctx.expression7())) if ctx.BXOR() else self.visit(
            ctx.expression7())

    # expression7
    #     : expression7 BAND expression8
    #     | expression8
    #     ;
    def visitExpression7(self, ctx: CircomParser.Expression7Context):
        return InfixOp(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression7()),
                       ctx.BAND().getText(), self.visit(ctx.expression8())) if ctx.BAND() else self.visit(
            ctx.expression8())

    # expression8
    #     : expression8 shiftOpcode expression9
    #     | expression9
    #     ;
    def visitExpression8(self, ctx: CircomParser.Expression8Context):
        return InfixOp(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression8()),
                       self.visit(ctx.shiftOpcode()),
                       self.visit(ctx.expression9())) if ctx.shiftOpcode() else self.visit(ctx.expression9())

    # expression9
    #     : expression9 add_sub_opcode expression10
    #     | expression10
    #     ;
    def visitExpression9(self, ctx: CircomParser.Expression9Context):
        return InfixOp(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression9()),
                       self.visit(ctx.add_sub_opcode()),
                       self.visit(ctx.expression10())) if ctx.add_sub_opcode() else self.visit(ctx.expression10())

    # expression10
    #     : expression10 mul_div_opcode expression11
    #     | expression11
    #     ;
    def visitExpression10(self, ctx: CircomParser.Expression10Context):
        return InfixOp(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression10()),
                       self.visit(ctx.mul_div_opcode()),
                       self.visit(ctx.expression11())) if ctx.mul_div_opcode() else self.visit(ctx.expression11())

    # expression11
    #     : expression11 POW expression12
    #     | expression12
    #     ;
    def visitExpression11(self, ctx: CircomParser.Expression11Context):
        return InfixOp(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.expression11()),
                       ctx.POW().getText(), self.visit(ctx.expression12())) if ctx.POW() else self.visit(
            ctx.expression12())

    # expression12
    #     : prefixOpcode expression12
    #     | expression13
    #     ;
    def visitExpression12(self, ctx: CircomParser.Expression12Context):
        return PrefixOp(FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.prefixOpcode()),
                        self.visit(ctx.expression12())) if ctx.prefixOpcode() else self.visit(ctx.expression13())

    # expression13
    #     : IDENTIFIER LP listable RP LP listableAnon RP
    #     | IDENTIFIER LP listable RP
    #     | LB listable_prime RB
    #     | LP twoElemsListable RP
    #     | expression14
    #     ;
    def visitExpression13(self, ctx: CircomParser.Expression13Context):
        if ctx.listableAnon():
            listableAnon = self.visit(ctx.listableAnon())
            signals = []
            names = []
            for anon in listableAnon:
                signals.append(anon[0])
                names.append(anon[1])
            return AnonymousComponentExpr(FileLocation(self.file_name, ctx.start, ctx.stop), ctx.IDENTIFIER().getText(),
                                          False, self.visit(ctx.listable()), signals, names)
        elif ctx.getChildCount() == 4:
            return Call(FileLocation(self.file_name, ctx.start, ctx.stop), ctx.IDENTIFIER().getText(),
                        self.visit(ctx.listable()))
        elif ctx.getChildCount() == 3:
            return ArrayInLine(FileLocation(self.file_name, ctx.start, ctx.stop),
                               self.visit(ctx.listable_prime())) if ctx.listable_prime() else TupleExpr(
                FileLocation(self.file_name, ctx.start, ctx.stop), self.visit(ctx.twoElemsListable()))
        else:
            return self.visit(ctx.expression14())

    # expression14
    #     : variable
    #     | UNDERSCORE
    #     | NUMBER
    #     | HEXNUMBER
    #     | LP expression RP
    #     ;
    def visitExpression14(self, ctx: CircomParser.Expression14Context):
        if ctx.variable():
            return self.visit(ctx.variable())
        elif ctx.UNDERSCORE():
            return Variable(FileLocation(self.file_name, ctx.start, ctx.stop), ctx.UNDERSCORE().getText(), [])
        elif ctx.NUMBER():
            return Number(FileLocation(self.file_name, ctx.start, ctx.stop), int(ctx.NUMBER().getText(), 10))
        elif ctx.HEXNUMBER():
            return Number(FileLocation(self.file_name, ctx.start, ctx.stop), int(ctx.HEXNUMBER().getText(), 16))
        else:
            return self.visit(ctx.expression())

    # twoElemsListable
    #     : twoElemsListable COMMA expression
    #     | expression COMMA expression
    #     ;
    def visitTwoElemsListable(self, ctx: CircomParser.TwoElemsListableContext):
        return self.visit(ctx.twoElemsListable()) + [self.visit(ctx.expression(0))] if ctx.twoElemsListable() else [
            self.visit(ctx.expression(0)), self.visit(ctx.expression(1))]

    # log_arguement: expression | STRING;
    def visitLog_arguement(self, ctx: CircomParser.Log_arguementContext):
        return LogExp(FileLocation(self.file_name, ctx.start, ctx.stop),
                      self.visit(ctx.expression())) if ctx.expression() else LogStr(
            FileLocation(self.file_name, ctx.start, ctx.stop), ctx.STRING().getText())

    # log_list: log_arguement COMMA log_list | log_arguement;
    def visitLog_list(self, ctx: CircomParser.Log_listContext):
        return [self.visit(ctx.log_arguement())] + self.visit(ctx.log_list()) if ctx.log_list() else [
            self.visit(ctx.log_arguement())]

    # listable: listable_prime | ;
    def visitListable(self, ctx: CircomParser.ListableContext):
        return self.visit(ctx.listable_prime()) if ctx.listable_prime() else []

    # listable_prime: expression | expression COMMA listable_prime;
    def visitListable_prime(self, ctx: CircomParser.Listable_primeContext):
        return [self.visit(ctx.expression())] + self.visit(ctx.listable_prime()) if ctx.listable_prime() else [
            self.visit(ctx.expression())]

    # listableAnon: listableAnon_prime | ;
    def visitListableAnon(self, ctx: CircomParser.ListableAnonContext):
        return self.visit(ctx.listableAnon_prime()) if ctx.listableAnon_prime() else []

    # listableAnon_prime: listable_prime | listableWithInputNames;
    def visitListableAnon(self, ctx: CircomParser.ListableAnon_primeContext):
        return list(map(lambda x: (x, None), self.visit(ctx.listable_prime()))) if ctx.listable_prime() else self.visit(
            ctx.listableWithInputNames())

    # listableWithInputNames
    #     : listableWithInputNames COMMA IDENTIFIER assign_opcode expression
    #     | IDENTIFIER assign_opcode expression
    #     ;

    def visitListableWithInputNames(self, ctx: CircomParser.ListableWithInputNamesContext):
        return self.visit(ctx.listableWithInputNames()) + [(self.visit(ctx.expression()), (
        self.visit(ctx.assign_opcode()), ctx.IDENTIFIER().getText()))] if ctx.listableWithInputNames() else [
            (self.visit(ctx.expression()), (self.visit(ctx.assign_opcode()), ctx.IDENTIFIER().getText()))]

    # prefixOpcode: NOT | BNOT | SUB;
    def visitPrefixOpcode(self, ctx: CircomParser.PrefixOpcodeContext):
        return ctx.getChild(0).getText()

    # compareOpcode
    #     : EQ
    #     | NEQ
    #     | GT
    #     | LT
    #     | GE
    #     | LE
    #     ;
    def visitCompareOpcode(self, ctx: CircomParser.CompareOpcodeContext):
        return ctx.getChild(0).getText()

    # shiftOpcode: SHL | SHR;
    def visitShiftOpcode(self, ctx: CircomParser.ShiftOpcodeContext):
        return ctx.getChild(0).getText()

    # add_sub_opcode: ADD | SUB;
    def visitAdd_sub_opcode(self, ctx: CircomParser.Add_sub_opcodeContext):
        return ctx.getChild(0).getText()

    # mul_div_opcode: MUL | DIV | QUO | MOD;
    def visitMul_div_opcode(self, ctx: CircomParser.Mul_div_opcodeContext):
        return ctx.getChild(0).getText()

    # assign_opcode: ASSIGNMENT | LEFT_ASSIGNMENT | LEFT_CONSTRAINT;
    def visitAssign_opcode(self, ctx: CircomParser.Assign_opcodeContext):
        return ctx.getChild(0).getText()
