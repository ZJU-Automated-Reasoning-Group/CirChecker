# Generated from circheck/parser/Circom.g4 by ANTLR 4.9.2
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .CircomParser import CircomParser
else:
    from CircomParser import CircomParser


# This class defines a complete generic visitor for a parse tree produced by CircomParser.

class CircomVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CircomParser#program.
    def visitProgram(self, ctx: CircomParser.ProgramContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#version.
    def visitVersion(self, ctx: CircomParser.VersionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#main_option.
    def visitMain_option(self, ctx: CircomParser.Main_optionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#definition_block.
    def visitDefinition_block(self, ctx: CircomParser.Definition_blockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#definition_list.
    def visitDefinition_list(self, ctx: CircomParser.Definition_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#pragma_definition.
    def visitPragma_definition(self, ctx: CircomParser.Pragma_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#custom_gate.
    def visitCustom_gate(self, ctx: CircomParser.Custom_gateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#include_list.
    def visitInclude_list(self, ctx: CircomParser.Include_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#include_definition.
    def visitInclude_definition(self, ctx: CircomParser.Include_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#public_list.
    def visitPublic_list(self, ctx: CircomParser.Public_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#main_component.
    def visitMain_component(self, ctx: CircomParser.Main_componentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#function_definition.
    def visitFunction_definition(self, ctx: CircomParser.Function_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#template_definition.
    def visitTemplate_definition(self, ctx: CircomParser.Template_definitionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#identifier_list_option.
    def visitIdentifier_list_option(self, ctx: CircomParser.Identifier_list_optionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#custom_option.
    def visitCustom_option(self, ctx: CircomParser.Custom_optionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#parallel_option.
    def visitParallel_option(self, ctx: CircomParser.Parallel_optionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#block.
    def visitBlock(self, ctx: CircomParser.BlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#statement.
    def visitStatement(self, ctx: CircomParser.StatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#statement_list.
    def visitStatement_list(self, ctx: CircomParser.Statement_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#declaration_statement.
    def visitDeclaration_statement(self, ctx: CircomParser.Declaration_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression_statement.
    def visitExpression_statement(self, ctx: CircomParser.Expression_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#substitutions.
    def visitSubstitutions(self, ctx: CircomParser.SubstitutionsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#substitutions_statement.
    def visitSubstitutions_statement(self, ctx: CircomParser.Substitutions_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#if_statement.
    def visitIf_statement(self, ctx: CircomParser.If_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#regular_statement.
    def visitRegular_statement(self, ctx: CircomParser.Regular_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#for_statement.
    def visitFor_statement(self, ctx: CircomParser.For_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#while_statement.
    def visitWhile_statement(self, ctx: CircomParser.While_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#equal_constraint_statement.
    def visitEqual_constraint_statement(self, ctx: CircomParser.Equal_constraint_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#return_statement.
    def visitReturn_statement(self, ctx: CircomParser.Return_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#assert_statement.
    def visitAssert_statement(self, ctx: CircomParser.Assert_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#log_statement.
    def visitLog_statement(self, ctx: CircomParser.Log_statementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#declaration.
    def visitDeclaration(self, ctx: CircomParser.DeclarationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#identifier_list.
    def visitIdentifier_list(self, ctx: CircomParser.Identifier_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#tag_list.
    def visitTag_list(self, ctx: CircomParser.Tag_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#tuple_initialization.
    def visitTuple_initialization(self, ctx: CircomParser.Tuple_initializationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#simple_symbol.
    def visitSimple_symbol(self, ctx: CircomParser.Simple_symbolContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#simple_symbol_list.
    def visitSimple_symbol_list(self, ctx: CircomParser.Simple_symbol_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#complex_symbol.
    def visitComplex_symbol(self, ctx: CircomParser.Complex_symbolContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#some_symbol.
    def visitSome_symbol(self, ctx: CircomParser.Some_symbolContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#some_symbol_list.
    def visitSome_symbol_list(self, ctx: CircomParser.Some_symbol_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#var_decl.
    def visitVar_decl(self, ctx: CircomParser.Var_declContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#signal_decl.
    def visitSignal_decl(self, ctx: CircomParser.Signal_declContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#signal_header.
    def visitSignal_header(self, ctx: CircomParser.Signal_headerContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#signal_symbol.
    def visitSignal_symbol(self, ctx: CircomParser.Signal_symbolContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#signal_symbol_list.
    def visitSignal_symbol_list(self, ctx: CircomParser.Signal_symbol_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#component_decl.
    def visitComponent_decl(self, ctx: CircomParser.Component_declContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#var_access.
    def visitVar_access(self, ctx: CircomParser.Var_accessContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#var_access_list.
    def visitVar_access_list(self, ctx: CircomParser.Var_access_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#array_access.
    def visitArray_access(self, ctx: CircomParser.Array_accessContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#array_access_list.
    def visitArray_access_list(self, ctx: CircomParser.Array_access_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#component_access.
    def visitComponent_access(self, ctx: CircomParser.Component_accessContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#variable.
    def visitVariable(self, ctx: CircomParser.VariableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression.
    def visitExpression(self, ctx: CircomParser.ExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression1.
    def visitExpression1(self, ctx: CircomParser.Expression1Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression2.
    def visitExpression2(self, ctx: CircomParser.Expression2Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression3.
    def visitExpression3(self, ctx: CircomParser.Expression3Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression4.
    def visitExpression4(self, ctx: CircomParser.Expression4Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression5.
    def visitExpression5(self, ctx: CircomParser.Expression5Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression6.
    def visitExpression6(self, ctx: CircomParser.Expression6Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression7.
    def visitExpression7(self, ctx: CircomParser.Expression7Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression8.
    def visitExpression8(self, ctx: CircomParser.Expression8Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression9.
    def visitExpression9(self, ctx: CircomParser.Expression9Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression10.
    def visitExpression10(self, ctx: CircomParser.Expression10Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression11.
    def visitExpression11(self, ctx: CircomParser.Expression11Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression12.
    def visitExpression12(self, ctx: CircomParser.Expression12Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression13.
    def visitExpression13(self, ctx: CircomParser.Expression13Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#expression14.
    def visitExpression14(self, ctx: CircomParser.Expression14Context):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#twoElemsListable.
    def visitTwoElemsListable(self, ctx: CircomParser.TwoElemsListableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#log_arguement.
    def visitLog_arguement(self, ctx: CircomParser.Log_arguementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#log_list.
    def visitLog_list(self, ctx: CircomParser.Log_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#listable.
    def visitListable(self, ctx: CircomParser.ListableContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#listable_prime.
    def visitListable_prime(self, ctx: CircomParser.Listable_primeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#listableAnon.
    def visitListableAnon(self, ctx: CircomParser.ListableAnonContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#listableAnon_prime.
    def visitListableAnon_prime(self, ctx: CircomParser.ListableAnon_primeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#listableWithInputNames.
    def visitListableWithInputNames(self, ctx: CircomParser.ListableWithInputNamesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#prefixOpcode.
    def visitPrefixOpcode(self, ctx: CircomParser.PrefixOpcodeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#compareOpcode.
    def visitCompareOpcode(self, ctx: CircomParser.CompareOpcodeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#shiftOpcode.
    def visitShiftOpcode(self, ctx: CircomParser.ShiftOpcodeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#add_sub_opcode.
    def visitAdd_sub_opcode(self, ctx: CircomParser.Add_sub_opcodeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#mul_div_opcode.
    def visitMul_div_opcode(self, ctx: CircomParser.Mul_div_opcodeContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CircomParser#assign_opcode.
    def visitAssign_opcode(self, ctx: CircomParser.Assign_opcodeContext):
        return self.visitChildren(ctx)


del CircomParser
