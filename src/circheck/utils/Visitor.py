from abc import ABC, abstractmethod


class Visitor(ABC):
    def visit(self, ast, param):
        return ast.accept(self, param)

    @abstractmethod
    def visitFileLocation(self, param):
        pass

    @abstractmethod
    def visitMainComponent(self, param):
        pass

    @abstractmethod
    def visitInclude(self, param):
        pass

    @abstractmethod
    def visitTemplate(self, param):
        pass

    @abstractmethod
    def visitFunction(self, param):
        pass

    @abstractmethod
    def visitProgram(self, param):
        pass

    @abstractmethod
    def visitIfThenElse(self, param):
        pass

    @abstractmethod
    def visitWhile(self, param):
        pass

    @abstractmethod
    def visitReturn(self, param):
        pass

    @abstractmethod
    def visitInitializationBlock(self, param):
        pass

    @abstractmethod
    def visitDeclaration(self, param):
        pass

    @abstractmethod
    def visitSubstitution(self, param):
        pass

    @abstractmethod
    def visitMultiSubstitution(self, param):
        pass

    @abstractmethod
    def visitConstraintEquality(self, param):
        pass

    @abstractmethod
    def visitLogCall(self, param):
        pass

    @abstractmethod
    def visitBlock(self, param):
        pass

    @abstractmethod
    def visitAssert(self, param):
        pass

    @abstractmethod
    def visitVar(self, param):
        pass

    @abstractmethod
    def visitSignal(self, param):
        pass

    @abstractmethod
    def visitComponent(self, param):
        pass

    @abstractmethod
    def visitAnonymousComponent(self, param):
        pass

    @abstractmethod
    def visitInfixOp(self, param):
        pass

    @abstractmethod
    def visitPrefixOp(self, param):
        pass

    @abstractmethod
    def visitInlineSwitchOp(self, param):
        pass

    @abstractmethod
    def visitParrallelOp(self, param):
        pass

    @abstractmethod
    def visitVariable(self, param):
        pass

    @abstractmethod
    def visitNumber(self, param):
        pass

    @abstractmethod
    def visitCall(self, param):
        pass

    @abstractmethod
    def visitAnonymousComponentExpr(self, param):
        pass

    @abstractmethod
    def visitArrayInLine(self, param):
        pass

    @abstractmethod
    def visitTupleExpr(self, param):
        pass

    @abstractmethod
    def visitComponentAccess(self, param):
        pass

    @abstractmethod
    def visitArrayAccess(self, param):
        pass

    @abstractmethod
    def visitLogStr(self, param):
        pass

    @abstractmethod
    def visitLogExp(self, param):
        pass


class BaseVisitor(Visitor):
    def visitFileLocation(self, param):
        return None

    def visitMainComponent(self, param):
        return None

    def visitInclude(self, param):
        return None

    def visitTemplate(self, param):
        return None

    def visitFunction(self, param):
        return None

    def visitProgram(self, param):
        return None

    def visitIfThenElse(self, param):
        return None

    def visitWhile(self, param):
        return None

    def visitReturn(self, param):
        return None

    def visitInitializationBlock(self, param):
        return None

    def visitDeclaration(self, param):
        return None

    def visitSubstitution(self, param):
        return None

    def visitMultiSubstitution(self, param):
        return None

    def visitConstraintEquality(self, param):
        return None

    def visitLogCall(self, param):
        return None

    def visitBlock(self, param):
        return None

    def visitAssert(self, param):
        return None

    def visitVar(self, param):
        return None

    def visitSignal(self, param):
        return None

    def visitComponent(self, param):
        return None

    def visitAnonymousComponent(self, param):
        return None

    def visitInfixOp(self, param):
        return None

    def visitPrefixOp(self, param):
        return None

    def visitInlineSwitchOp(self, param):
        return None

    def visitParrallelOp(self, param):
        return None

    def visitVariable(self, param):
        return None

    def visitNumber(self, param):
        return None

    def visitCall(self, param):
        return None

    def visitAnonymousComponentExpr(self, param):
        return None

    def visitArrayInLine(self, param):
        return None

    def visitTupleExpr(self, param):
        return None

    def visitComponentAccess(self, param):
        return None

    def visitArrayAccess(self, param):
        return None

    def visitLogStr(self, param):
        return None

    def visitLogExp(self, param):
        return None
