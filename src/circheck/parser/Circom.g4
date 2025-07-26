grammar Circom;

@lexer::header {
    from Errors import *
}

@lexer::members {

}

options{
	language = Python3;
}

// Parser's Part

program: pragma_definition? custom_gate? include_list definition_list main_option EOF;

version: NUMBER '.' NUMBER '.' NUMBER ;
main_option: main_component | ;

definition_block: function_definition | template_definition;
definition_list: definition_block definition_list | ;

pragma_definition: PRAGMA CIRCOM version SEMICOLON;
custom_gate: PRAGMA CUSTOM_TEMPLATES SEMICOLON;

include_list: include_definition include_list | ;
include_definition: INCLUDE STRING SEMICOLON;

// Definition
public_list: LC PUBLIC LB identifier_list RB RC | ;

main_component: COMPONENT MAIN public_list ASSIGNMENT expression SEMICOLON;

function_definition: FUNCTION IDENTIFIER LP identifier_list_option RP block;

template_definition: TEMPLATE custom_option parallel_option IDENTIFIER LP identifier_list_option RP block;

identifier_list_option: identifier_list | ;
custom_option: CUSTOM | ;
parallel_option: PARALLEL | ;

// Statements
block: LC statement_list RC;

statement
    : declaration_statement
    | if_statement
    | regular_statement
    ;
statement_list: statement statement_list | ;

declaration_statement: declaration SEMICOLON;
expression_statement: expression SEMICOLON;

substitutions
    : expression assign_opcode expression
    | expression RIGHT_ASSIGNMENT expression
    | expression RIGHT_CONSTRAINT expression
    | variable ASSIGNMENT_WITH_OP expression
    | variable SELF_OP
    ;
substitutions_statement: substitutions SEMICOLON;

if_statement
    : IF LP expression RP if_statement
    | IF LP expression RP regular_statement
    | IF LP expression RP regular_statement ELSE if_statement
    | IF LP expression RP regular_statement ELSE regular_statement
    ;

regular_statement
    : block
    | expression_statement
    | substitutions_statement
    | for_statement
    | while_statement
    | equal_constraint_statement
    | return_statement
    | assert_statement
    | log_statement
    ;

for_statement
    : FOR LP declaration SEMICOLON expression SEMICOLON substitutions RP regular_statement
    | FOR LP substitutions SEMICOLON expression SEMICOLON substitutions RP regular_statement
    ;

while_statement: WHILE LP expression RP regular_statement;

equal_constraint_statement: expression EQ_CONSTRAINT expression SEMICOLON;

return_statement: RETURN expression SEMICOLON;

assert_statement: ASSERT LP expression RP SEMICOLON;

log_statement
    : LOG LP log_list RP SEMICOLON
    | LOG LP RP SEMICOLON
    ;

// Declaration
declaration
    : var_decl
    | signal_decl
    | component_decl
    ;

identifier_list: IDENTIFIER COMMA identifier_list | IDENTIFIER;
tag_list: LC identifier_list RC;

tuple_initialization: assign_opcode expression;
simple_symbol: IDENTIFIER array_access_list;
simple_symbol_list: simple_symbol COMMA simple_symbol_list | simple_symbol;
complex_symbol: IDENTIFIER array_access_list ASSIGNMENT expression;

some_symbol: simple_symbol | complex_symbol;
some_symbol_list: some_symbol COMMA some_symbol_list | some_symbol;

var_decl
    : VAR some_symbol_list
    | VAR LP simple_symbol_list RP
    | VAR LP simple_symbol_list RP tuple_initialization
    ;

signal_decl
    : signal_header signal_symbol_list
    | signal_header LP simple_symbol_list RP
    | signal_header LP simple_symbol_list RP tuple_initialization
    ;
signal_header
    : SIGNAL
    | SIGNAL SIGNAL_TYPE
    | SIGNAL tag_list
    | SIGNAL SIGNAL_TYPE tag_list
    ;

signal_symbol
    : simple_symbol
    | IDENTIFIER array_access_list LEFT_CONSTRAINT expression
    | IDENTIFIER array_access_list LEFT_ASSIGNMENT expression
    ;
signal_symbol_list: signal_symbol COMMA signal_symbol_list | signal_symbol;

component_decl
    : COMPONENT some_symbol_list
    | COMPONENT LP simple_symbol_list RP
    | COMPONENT LP simple_symbol_list RP tuple_initialization
    ;

// Variable
var_access: array_access | component_access;
var_access_list: var_access var_access_list | ;

array_access: LB expression RB;
array_access_list: array_access array_access_list | ;
component_access: DOT IDENTIFIER;

variable: IDENTIFIER var_access_list;

// Expression
expression
    : PARALLEL expression1
    | expression1
    ;
expression1
    : expression2 TERNARY_CONDITION expression2 TERNARY_ALTERNATIVE expression2
    | expression2
    ;
expression2
    : expression2 OR expression3
    | expression3
    ;
expression3
    : expression3 AND expression4
    | expression4
    ;
expression4
    : expression4 compareOpcode expression5
    | expression5
    ;
expression5
    : expression5 BOR expression6
    | expression6
    ;
expression6
    : expression6 BXOR expression7
    | expression7
    ;
expression7
    : expression7 BAND expression8
    | expression8
    ;
expression8
    : expression8 shiftOpcode expression9
    | expression9
    ;
expression9
    : expression9 add_sub_opcode expression10
    | expression10
    ;
expression10
    : expression10 mul_div_opcode expression11
    | expression11
    ;
expression11
    : expression11 POW expression12
    | expression12
    ;
expression12
    : prefixOpcode expression12
    | expression13
    ;
expression13
    : IDENTIFIER LP listable RP LP listableAnon RP
    | IDENTIFIER LP listable RP
    | LB listable_prime RB
    | LP twoElemsListable RP
    | expression14
    ;
expression14
    : variable
    | UNDERSCORE
    | NUMBER
    | HEXNUMBER
    | LP expression RP
    ;

twoElemsListable
    : twoElemsListable COMMA expression
    | expression COMMA expression
    ;

log_arguement: expression | STRING;
log_list: log_arguement COMMA log_list | log_arguement;

listable: listable_prime | ;
listable_prime: expression | expression COMMA listable_prime;
listableAnon: listableAnon_prime | ;
listableAnon_prime: listable_prime | listableWithInputNames;
listableWithInputNames
    : listableWithInputNames COMMA IDENTIFIER assign_opcode expression
    | IDENTIFIER assign_opcode expression
    ;

// Terminals
prefixOpcode: NOT | BNOT | SUB;

compareOpcode
    : EQ
    | NEQ
    | GT
    | LT
    | GE
    | LE
    ;

shiftOpcode: SHL | SHR;

add_sub_opcode: ADD | SUB;

mul_div_opcode: MUL | DIV | QUO | MOD;

assign_opcode: ASSIGNMENT | LEFT_ASSIGNMENT | LEFT_CONSTRAINT;

// Lexer's Part

SIGNAL_TYPE: INPUT | OUTPUT ;

// SYMBOLS
LP: '(' ;
RP: ')' ;

LB: '[' ;
RB: ']' ;

LC: '{' ;
RC: '}' ;

SEMICOLON: ';' ;

DOT: '.' ;
COMMA: ',' ;

UNDERSCORE: '_' ;

// operators
TERNARY_CONDITION: '?' ;
TERNARY_ALTERNATIVE: ':' ;

EQ_CONSTRAINT: '===' ;

LEFT_CONSTRAINT: '<==' ;
LEFT_ASSIGNMENT: '<--' ;

RIGHT_CONSTRAINT: '==>' ;
RIGHT_ASSIGNMENT: '-->' ;

// Unary operators
SELF_OP: '++' | '--' ;

NOT: '!' ;
BNOT: '~' ;

// left to right associativity
POW: '**' ;

MUL: '*' ;
DIV: '/' ;
QUO: '\\' ;
MOD: '%' ;

ADD: '+' ;
SUB: '-' ;

SHL: '<<' ;
SHR: '>>' ;

BAND: '&' ;
BXOR: '^' ;
BOR: '|' ;

// Require parentheses associativity
EQ: '==' ;
NEQ: '!=' ;
GT: '>' ;
LT: '<' ;
LE: '<=' ;
GE: '>=' ;

// left to right associativity
AND: '&&' ;
OR: '||' ;

// right to left associativity
ASSIGNMENT: '=' ;
ASSIGNMENT_WITH_OP: '+=' | '-=' | '*=' | '**=' | '/=' | '\\=' | '%=' | '<<=' | '>>=' | '&=' | '^=' | '|=' ;

// Reserved Keywords
SIGNAL: 'signal';
INPUT: 'input';
OUTPUT: 'output';
PUBLIC: 'public';
TEMPLATE: 'template';
COMPONENT: 'component';
VAR: 'var';
FUNCTION: 'function';
RETURN: 'return';
IF: 'if';
ELSE: 'else';
FOR: 'for';
WHILE: 'while';
DO: 'do';
LOG: 'log';
ASSERT: 'assert';
INCLUDE: 'include';
PARALLEL: 'parallel';
PRAGMA: 'pragma';
BUS: 'bus';
CIRCOM: 'circom';
CUSTOM_TEMPLATES: 'custom_templates';
CUSTOM: 'custom';
MAIN: 'main';

// Comment Lines
SINGLE_LINE_COMMENT: '//' (~[\r\n])* -> skip;
MULTI_LINES_COMMENT: '/*' .*? '*/' -> skip;

// Identifiers
STRING : '"' ~'"'* '"' ;
NUMBER: [0-9]+;
HEXNUMBER : '0x' [0-9A-Fa-f]* ;
IDENTIFIER: [$_]*[a-zA-Z] [a-zA-Z$_0-9]*;

WHITESPACE : [ \t\b\f\r\n]+ -> skip ; // skip spaces, tabs
UnclosedComment: '/*' .*? {
    import Errors
    raise Errors.UnclosedComment(self.line, self.column)
};
