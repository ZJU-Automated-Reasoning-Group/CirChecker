# Generated from circheck/parser/Circom.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys

if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO

    from Errors import *


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2M")
        buf.write("\u0214\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\4B\tB\4C\t")
        buf.write("C\4D\tD\4E\tE\4F\tF\4G\tG\4H\tH\4I\tI\4J\tJ\4K\tK\4L\t")
        buf.write("L\3\2\3\2\5\2\u009c\n\2\3\3\3\3\3\4\3\4\3\5\3\5\3\6\3")
        buf.write("\6\3\7\3\7\3\b\3\b\3\t\3\t\3\n\3\n\3\13\3\13\3\f\3\f\3")
        buf.write("\r\3\r\3\16\3\16\3\17\3\17\3\17\3\17\3\20\3\20\3\20\3")
        buf.write("\20\3\21\3\21\3\21\3\21\3\22\3\22\3\22\3\22\3\23\3\23")
        buf.write("\3\23\3\23\3\24\3\24\3\24\3\24\5\24\u00ce\n\24\3\25\3")
        buf.write("\25\3\26\3\26\3\27\3\27\3\27\3\30\3\30\3\31\3\31\3\32")
        buf.write("\3\32\3\33\3\33\3\34\3\34\3\35\3\35\3\36\3\36\3\36\3\37")
        buf.write("\3\37\3\37\3 \3 \3!\3!\3\"\3\"\3#\3#\3#\3$\3$\3$\3%\3")
        buf.write("%\3&\3&\3\'\3\'\3\'\3(\3(\3(\3)\3)\3)\3*\3*\3*\3+\3+\3")
        buf.write(",\3,\3,\3,\3,\3,\3,\3,\3,\3,\3,\3,\3,\3,\3,\3,\3,\3,\3")
        buf.write(",\3,\3,\3,\3,\3,\3,\3,\3,\5,\u0122\n,\3-\3-\3-\3-\3-\3")
        buf.write("-\3-\3.\3.\3.\3.\3.\3.\3/\3/\3/\3/\3/\3/\3/\3\60\3\60")
        buf.write("\3\60\3\60\3\60\3\60\3\60\3\61\3\61\3\61\3\61\3\61\3\61")
        buf.write("\3\61\3\61\3\61\3\62\3\62\3\62\3\62\3\62\3\62\3\62\3\62")
        buf.write("\3\62\3\62\3\63\3\63\3\63\3\63\3\64\3\64\3\64\3\64\3\64")
        buf.write("\3\64\3\64\3\64\3\64\3\65\3\65\3\65\3\65\3\65\3\65\3\65")
        buf.write("\3\66\3\66\3\66\3\67\3\67\3\67\3\67\3\67\38\38\38\38\3")
        buf.write("9\39\39\39\39\39\3:\3:\3:\3;\3;\3;\3;\3<\3<\3<\3<\3<\3")
        buf.write("<\3<\3=\3=\3=\3=\3=\3=\3=\3=\3>\3>\3>\3>\3>\3>\3>\3>\3")
        buf.write(">\3?\3?\3?\3?\3?\3?\3?\3@\3@\3@\3@\3A\3A\3A\3A\3A\3A\3")
        buf.write("A\3B\3B\3B\3B\3B\3B\3B\3B\3B\3B\3B\3B\3B\3B\3B\3B\3B\3")
        buf.write("C\3C\3C\3C\3C\3C\3C\3D\3D\3D\3D\3D\3E\3E\3E\3E\7E\u01ca")
        buf.write("\nE\fE\16E\u01cd\13E\3E\3E\3F\3F\3F\3F\7F\u01d5\nF\fF")
        buf.write("\16F\u01d8\13F\3F\3F\3F\3F\3F\3G\3G\7G\u01e1\nG\fG\16")
        buf.write("G\u01e4\13G\3G\3G\3H\6H\u01e9\nH\rH\16H\u01ea\3I\3I\3")
        buf.write("I\3I\7I\u01f1\nI\fI\16I\u01f4\13I\3J\7J\u01f7\nJ\fJ\16")
        buf.write("J\u01fa\13J\3J\3J\7J\u01fe\nJ\fJ\16J\u0201\13J\3K\6K\u0204")
        buf.write("\nK\rK\16K\u0205\3K\3K\3L\3L\3L\3L\7L\u020e\nL\fL\16L")
        buf.write("\u0211\13L\3L\3L\4\u01d6\u020f\2M\3\3\5\4\7\5\t\6\13\7")
        buf.write("\r\b\17\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21")
        buf.write("!\22#\23%\24\'\25)\26+\27-\30/\31\61\32\63\33\65\34\67")
        buf.write("\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+U,W-Y.[/]\60_\61")
        buf.write("a\62c\63e\64g\65i\66k\67m8o9q:s;u<w=y>{?}@\177A\u0081")
        buf.write("B\u0083C\u0085D\u0087E\u0089F\u008bG\u008dH\u008fI\u0091")
        buf.write("J\u0093K\u0095L\u0097M\3\2\n\4\2\f\f\17\17\3\2$$\3\2\62")
        buf.write(";\5\2\62;CHch\4\2&&aa\4\2C\\c|\7\2&&\62;C\\aac|\5\2\n")
        buf.write("\f\16\17\"\"\2\u0229\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2")
        buf.write("\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2")
        buf.write("\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31")
        buf.write("\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2")
        buf.write("\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3")
        buf.write("\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2")
        buf.write("\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3")
        buf.write("\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G")
        buf.write("\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2")
        buf.write("Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2")
        buf.write("\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2")
        buf.write("\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2")
        buf.write("\2\2\2o\3\2\2\2\2q\3\2\2\2\2s\3\2\2\2\2u\3\2\2\2\2w\3")
        buf.write("\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2")
        buf.write("\2\u0081\3\2\2\2\2\u0083\3\2\2\2\2\u0085\3\2\2\2\2\u0087")
        buf.write("\3\2\2\2\2\u0089\3\2\2\2\2\u008b\3\2\2\2\2\u008d\3\2\2")
        buf.write("\2\2\u008f\3\2\2\2\2\u0091\3\2\2\2\2\u0093\3\2\2\2\2\u0095")
        buf.write("\3\2\2\2\2\u0097\3\2\2\2\3\u009b\3\2\2\2\5\u009d\3\2\2")
        buf.write("\2\7\u009f\3\2\2\2\t\u00a1\3\2\2\2\13\u00a3\3\2\2\2\r")
        buf.write("\u00a5\3\2\2\2\17\u00a7\3\2\2\2\21\u00a9\3\2\2\2\23\u00ab")
        buf.write("\3\2\2\2\25\u00ad\3\2\2\2\27\u00af\3\2\2\2\31\u00b1\3")
        buf.write("\2\2\2\33\u00b3\3\2\2\2\35\u00b5\3\2\2\2\37\u00b9\3\2")
        buf.write("\2\2!\u00bd\3\2\2\2#\u00c1\3\2\2\2%\u00c5\3\2\2\2\'\u00cd")
        buf.write("\3\2\2\2)\u00cf\3\2\2\2+\u00d1\3\2\2\2-\u00d3\3\2\2\2")
        buf.write("/\u00d6\3\2\2\2\61\u00d8\3\2\2\2\63\u00da\3\2\2\2\65\u00dc")
        buf.write("\3\2\2\2\67\u00de\3\2\2\29\u00e0\3\2\2\2;\u00e2\3\2\2")
        buf.write("\2=\u00e5\3\2\2\2?\u00e8\3\2\2\2A\u00ea\3\2\2\2C\u00ec")
        buf.write("\3\2\2\2E\u00ee\3\2\2\2G\u00f1\3\2\2\2I\u00f4\3\2\2\2")
        buf.write("K\u00f6\3\2\2\2M\u00f8\3\2\2\2O\u00fb\3\2\2\2Q\u00fe\3")
        buf.write("\2\2\2S\u0101\3\2\2\2U\u0104\3\2\2\2W\u0121\3\2\2\2Y\u0123")
        buf.write("\3\2\2\2[\u012a\3\2\2\2]\u0130\3\2\2\2_\u0137\3\2\2\2")
        buf.write("a\u013e\3\2\2\2c\u0147\3\2\2\2e\u0151\3\2\2\2g\u0155\3")
        buf.write("\2\2\2i\u015e\3\2\2\2k\u0165\3\2\2\2m\u0168\3\2\2\2o\u016d")
        buf.write("\3\2\2\2q\u0171\3\2\2\2s\u0177\3\2\2\2u\u017a\3\2\2\2")
        buf.write("w\u017e\3\2\2\2y\u0185\3\2\2\2{\u018d\3\2\2\2}\u0196\3")
        buf.write("\2\2\2\177\u019d\3\2\2\2\u0081\u01a1\3\2\2\2\u0083\u01a8")
        buf.write("\3\2\2\2\u0085\u01b9\3\2\2\2\u0087\u01c0\3\2\2\2\u0089")
        buf.write("\u01c5\3\2\2\2\u008b\u01d0\3\2\2\2\u008d\u01de\3\2\2\2")
        buf.write("\u008f\u01e8\3\2\2\2\u0091\u01ec\3\2\2\2\u0093\u01f8\3")
        buf.write("\2\2\2\u0095\u0203\3\2\2\2\u0097\u0209\3\2\2\2\u0099\u009c")
        buf.write("\5[.\2\u009a\u009c\5]/\2\u009b\u0099\3\2\2\2\u009b\u009a")
        buf.write("\3\2\2\2\u009c\4\3\2\2\2\u009d\u009e\7*\2\2\u009e\6\3")
        buf.write("\2\2\2\u009f\u00a0\7+\2\2\u00a0\b\3\2\2\2\u00a1\u00a2")
        buf.write("\7]\2\2\u00a2\n\3\2\2\2\u00a3\u00a4\7_\2\2\u00a4\f\3\2")
        buf.write("\2\2\u00a5\u00a6\7}\2\2\u00a6\16\3\2\2\2\u00a7\u00a8\7")
        buf.write("\177\2\2\u00a8\20\3\2\2\2\u00a9\u00aa\7=\2\2\u00aa\22")
        buf.write("\3\2\2\2\u00ab\u00ac\7\60\2\2\u00ac\24\3\2\2\2\u00ad\u00ae")
        buf.write("\7.\2\2\u00ae\26\3\2\2\2\u00af\u00b0\7a\2\2\u00b0\30\3")
        buf.write("\2\2\2\u00b1\u00b2\7A\2\2\u00b2\32\3\2\2\2\u00b3\u00b4")
        buf.write("\7<\2\2\u00b4\34\3\2\2\2\u00b5\u00b6\7?\2\2\u00b6\u00b7")
        buf.write("\7?\2\2\u00b7\u00b8\7?\2\2\u00b8\36\3\2\2\2\u00b9\u00ba")
        buf.write("\7>\2\2\u00ba\u00bb\7?\2\2\u00bb\u00bc\7?\2\2\u00bc \3")
        buf.write("\2\2\2\u00bd\u00be\7>\2\2\u00be\u00bf\7/\2\2\u00bf\u00c0")
        buf.write("\7/\2\2\u00c0\"\3\2\2\2\u00c1\u00c2\7?\2\2\u00c2\u00c3")
        buf.write("\7?\2\2\u00c3\u00c4\7@\2\2\u00c4$\3\2\2\2\u00c5\u00c6")
        buf.write("\7/\2\2\u00c6\u00c7\7/\2\2\u00c7\u00c8\7@\2\2\u00c8&\3")
        buf.write("\2\2\2\u00c9\u00ca\7-\2\2\u00ca\u00ce\7-\2\2\u00cb\u00cc")
        buf.write("\7/\2\2\u00cc\u00ce\7/\2\2\u00cd\u00c9\3\2\2\2\u00cd\u00cb")
        buf.write("\3\2\2\2\u00ce(\3\2\2\2\u00cf\u00d0\7#\2\2\u00d0*\3\2")
        buf.write("\2\2\u00d1\u00d2\7\u0080\2\2\u00d2,\3\2\2\2\u00d3\u00d4")
        buf.write("\7,\2\2\u00d4\u00d5\7,\2\2\u00d5.\3\2\2\2\u00d6\u00d7")
        buf.write("\7,\2\2\u00d7\60\3\2\2\2\u00d8\u00d9\7\61\2\2\u00d9\62")
        buf.write("\3\2\2\2\u00da\u00db\7^\2\2\u00db\64\3\2\2\2\u00dc\u00dd")
        buf.write("\7\'\2\2\u00dd\66\3\2\2\2\u00de\u00df\7-\2\2\u00df8\3")
        buf.write("\2\2\2\u00e0\u00e1\7/\2\2\u00e1:\3\2\2\2\u00e2\u00e3\7")
        buf.write(">\2\2\u00e3\u00e4\7>\2\2\u00e4<\3\2\2\2\u00e5\u00e6\7")
        buf.write("@\2\2\u00e6\u00e7\7@\2\2\u00e7>\3\2\2\2\u00e8\u00e9\7")
        buf.write("(\2\2\u00e9@\3\2\2\2\u00ea\u00eb\7`\2\2\u00ebB\3\2\2\2")
        buf.write("\u00ec\u00ed\7~\2\2\u00edD\3\2\2\2\u00ee\u00ef\7?\2\2")
        buf.write("\u00ef\u00f0\7?\2\2\u00f0F\3\2\2\2\u00f1\u00f2\7#\2\2")
        buf.write("\u00f2\u00f3\7?\2\2\u00f3H\3\2\2\2\u00f4\u00f5\7@\2\2")
        buf.write("\u00f5J\3\2\2\2\u00f6\u00f7\7>\2\2\u00f7L\3\2\2\2\u00f8")
        buf.write("\u00f9\7>\2\2\u00f9\u00fa\7?\2\2\u00faN\3\2\2\2\u00fb")
        buf.write("\u00fc\7@\2\2\u00fc\u00fd\7?\2\2\u00fdP\3\2\2\2\u00fe")
        buf.write("\u00ff\7(\2\2\u00ff\u0100\7(\2\2\u0100R\3\2\2\2\u0101")
        buf.write("\u0102\7~\2\2\u0102\u0103\7~\2\2\u0103T\3\2\2\2\u0104")
        buf.write("\u0105\7?\2\2\u0105V\3\2\2\2\u0106\u0107\7-\2\2\u0107")
        buf.write("\u0122\7?\2\2\u0108\u0109\7/\2\2\u0109\u0122\7?\2\2\u010a")
        buf.write("\u010b\7,\2\2\u010b\u0122\7?\2\2\u010c\u010d\7,\2\2\u010d")
        buf.write("\u010e\7,\2\2\u010e\u0122\7?\2\2\u010f\u0110\7\61\2\2")
        buf.write("\u0110\u0122\7?\2\2\u0111\u0112\7^\2\2\u0112\u0122\7?")
        buf.write("\2\2\u0113\u0114\7\'\2\2\u0114\u0122\7?\2\2\u0115\u0116")
        buf.write("\7>\2\2\u0116\u0117\7>\2\2\u0117\u0122\7?\2\2\u0118\u0119")
        buf.write("\7@\2\2\u0119\u011a\7@\2\2\u011a\u0122\7?\2\2\u011b\u011c")
        buf.write("\7(\2\2\u011c\u0122\7?\2\2\u011d\u011e\7`\2\2\u011e\u0122")
        buf.write("\7?\2\2\u011f\u0120\7~\2\2\u0120\u0122\7?\2\2\u0121\u0106")
        buf.write("\3\2\2\2\u0121\u0108\3\2\2\2\u0121\u010a\3\2\2\2\u0121")
        buf.write("\u010c\3\2\2\2\u0121\u010f\3\2\2\2\u0121\u0111\3\2\2\2")
        buf.write("\u0121\u0113\3\2\2\2\u0121\u0115\3\2\2\2\u0121\u0118\3")
        buf.write("\2\2\2\u0121\u011b\3\2\2\2\u0121\u011d\3\2\2\2\u0121\u011f")
        buf.write("\3\2\2\2\u0122X\3\2\2\2\u0123\u0124\7u\2\2\u0124\u0125")
        buf.write("\7k\2\2\u0125\u0126\7i\2\2\u0126\u0127\7p\2\2\u0127\u0128")
        buf.write("\7c\2\2\u0128\u0129\7n\2\2\u0129Z\3\2\2\2\u012a\u012b")
        buf.write("\7k\2\2\u012b\u012c\7p\2\2\u012c\u012d\7r\2\2\u012d\u012e")
        buf.write("\7w\2\2\u012e\u012f\7v\2\2\u012f\\\3\2\2\2\u0130\u0131")
        buf.write("\7q\2\2\u0131\u0132\7w\2\2\u0132\u0133\7v\2\2\u0133\u0134")
        buf.write("\7r\2\2\u0134\u0135\7w\2\2\u0135\u0136\7v\2\2\u0136^\3")
        buf.write("\2\2\2\u0137\u0138\7r\2\2\u0138\u0139\7w\2\2\u0139\u013a")
        buf.write("\7d\2\2\u013a\u013b\7n\2\2\u013b\u013c\7k\2\2\u013c\u013d")
        buf.write("\7e\2\2\u013d`\3\2\2\2\u013e\u013f\7v\2\2\u013f\u0140")
        buf.write("\7g\2\2\u0140\u0141\7o\2\2\u0141\u0142\7r\2\2\u0142\u0143")
        buf.write("\7n\2\2\u0143\u0144\7c\2\2\u0144\u0145\7v\2\2\u0145\u0146")
        buf.write("\7g\2\2\u0146b\3\2\2\2\u0147\u0148\7e\2\2\u0148\u0149")
        buf.write("\7q\2\2\u0149\u014a\7o\2\2\u014a\u014b\7r\2\2\u014b\u014c")
        buf.write("\7q\2\2\u014c\u014d\7p\2\2\u014d\u014e\7g\2\2\u014e\u014f")
        buf.write("\7p\2\2\u014f\u0150\7v\2\2\u0150d\3\2\2\2\u0151\u0152")
        buf.write("\7x\2\2\u0152\u0153\7c\2\2\u0153\u0154\7t\2\2\u0154f\3")
        buf.write("\2\2\2\u0155\u0156\7h\2\2\u0156\u0157\7w\2\2\u0157\u0158")
        buf.write("\7p\2\2\u0158\u0159\7e\2\2\u0159\u015a\7v\2\2\u015a\u015b")
        buf.write("\7k\2\2\u015b\u015c\7q\2\2\u015c\u015d\7p\2\2\u015dh\3")
        buf.write("\2\2\2\u015e\u015f\7t\2\2\u015f\u0160\7g\2\2\u0160\u0161")
        buf.write("\7v\2\2\u0161\u0162\7w\2\2\u0162\u0163\7t\2\2\u0163\u0164")
        buf.write("\7p\2\2\u0164j\3\2\2\2\u0165\u0166\7k\2\2\u0166\u0167")
        buf.write("\7h\2\2\u0167l\3\2\2\2\u0168\u0169\7g\2\2\u0169\u016a")
        buf.write("\7n\2\2\u016a\u016b\7u\2\2\u016b\u016c\7g\2\2\u016cn\3")
        buf.write("\2\2\2\u016d\u016e\7h\2\2\u016e\u016f\7q\2\2\u016f\u0170")
        buf.write("\7t\2\2\u0170p\3\2\2\2\u0171\u0172\7y\2\2\u0172\u0173")
        buf.write("\7j\2\2\u0173\u0174\7k\2\2\u0174\u0175\7n\2\2\u0175\u0176")
        buf.write("\7g\2\2\u0176r\3\2\2\2\u0177\u0178\7f\2\2\u0178\u0179")
        buf.write("\7q\2\2\u0179t\3\2\2\2\u017a\u017b\7n\2\2\u017b\u017c")
        buf.write("\7q\2\2\u017c\u017d\7i\2\2\u017dv\3\2\2\2\u017e\u017f")
        buf.write("\7c\2\2\u017f\u0180\7u\2\2\u0180\u0181\7u\2\2\u0181\u0182")
        buf.write("\7g\2\2\u0182\u0183\7t\2\2\u0183\u0184\7v\2\2\u0184x\3")
        buf.write("\2\2\2\u0185\u0186\7k\2\2\u0186\u0187\7p\2\2\u0187\u0188")
        buf.write("\7e\2\2\u0188\u0189\7n\2\2\u0189\u018a\7w\2\2\u018a\u018b")
        buf.write("\7f\2\2\u018b\u018c\7g\2\2\u018cz\3\2\2\2\u018d\u018e")
        buf.write("\7r\2\2\u018e\u018f\7c\2\2\u018f\u0190\7t\2\2\u0190\u0191")
        buf.write("\7c\2\2\u0191\u0192\7n\2\2\u0192\u0193\7n\2\2\u0193\u0194")
        buf.write("\7g\2\2\u0194\u0195\7n\2\2\u0195|\3\2\2\2\u0196\u0197")
        buf.write("\7r\2\2\u0197\u0198\7t\2\2\u0198\u0199\7c\2\2\u0199\u019a")
        buf.write("\7i\2\2\u019a\u019b\7o\2\2\u019b\u019c\7c\2\2\u019c~\3")
        buf.write("\2\2\2\u019d\u019e\7d\2\2\u019e\u019f\7w\2\2\u019f\u01a0")
        buf.write("\7u\2\2\u01a0\u0080\3\2\2\2\u01a1\u01a2\7e\2\2\u01a2\u01a3")
        buf.write("\7k\2\2\u01a3\u01a4\7t\2\2\u01a4\u01a5\7e\2\2\u01a5\u01a6")
        buf.write("\7q\2\2\u01a6\u01a7\7o\2\2\u01a7\u0082\3\2\2\2\u01a8\u01a9")
        buf.write("\7e\2\2\u01a9\u01aa\7w\2\2\u01aa\u01ab\7u\2\2\u01ab\u01ac")
        buf.write("\7v\2\2\u01ac\u01ad\7q\2\2\u01ad\u01ae\7o\2\2\u01ae\u01af")
        buf.write("\7a\2\2\u01af\u01b0\7v\2\2\u01b0\u01b1\7g\2\2\u01b1\u01b2")
        buf.write("\7o\2\2\u01b2\u01b3\7r\2\2\u01b3\u01b4\7n\2\2\u01b4\u01b5")
        buf.write("\7c\2\2\u01b5\u01b6\7v\2\2\u01b6\u01b7\7g\2\2\u01b7\u01b8")
        buf.write("\7u\2\2\u01b8\u0084\3\2\2\2\u01b9\u01ba\7e\2\2\u01ba\u01bb")
        buf.write("\7w\2\2\u01bb\u01bc\7u\2\2\u01bc\u01bd\7v\2\2\u01bd\u01be")
        buf.write("\7q\2\2\u01be\u01bf\7o\2\2\u01bf\u0086\3\2\2\2\u01c0\u01c1")
        buf.write("\7o\2\2\u01c1\u01c2\7c\2\2\u01c2\u01c3\7k\2\2\u01c3\u01c4")
        buf.write("\7p\2\2\u01c4\u0088\3\2\2\2\u01c5\u01c6\7\61\2\2\u01c6")
        buf.write("\u01c7\7\61\2\2\u01c7\u01cb\3\2\2\2\u01c8\u01ca\n\2\2")
        buf.write("\2\u01c9\u01c8\3\2\2\2\u01ca\u01cd\3\2\2\2\u01cb\u01c9")
        buf.write("\3\2\2\2\u01cb\u01cc\3\2\2\2\u01cc\u01ce\3\2\2\2\u01cd")
        buf.write("\u01cb\3\2\2\2\u01ce\u01cf\bE\2\2\u01cf\u008a\3\2\2\2")
        buf.write("\u01d0\u01d1\7\61\2\2\u01d1\u01d2\7,\2\2\u01d2\u01d6\3")
        buf.write("\2\2\2\u01d3\u01d5\13\2\2\2\u01d4\u01d3\3\2\2\2\u01d5")
        buf.write("\u01d8\3\2\2\2\u01d6\u01d7\3\2\2\2\u01d6\u01d4\3\2\2\2")
        buf.write("\u01d7\u01d9\3\2\2\2\u01d8\u01d6\3\2\2\2\u01d9\u01da\7")
        buf.write(",\2\2\u01da\u01db\7\61\2\2\u01db\u01dc\3\2\2\2\u01dc\u01dd")
        buf.write("\bF\2\2\u01dd\u008c\3\2\2\2\u01de\u01e2\7$\2\2\u01df\u01e1")
        buf.write("\n\3\2\2\u01e0\u01df\3\2\2\2\u01e1\u01e4\3\2\2\2\u01e2")
        buf.write("\u01e0\3\2\2\2\u01e2\u01e3\3\2\2\2\u01e3\u01e5\3\2\2\2")
        buf.write("\u01e4\u01e2\3\2\2\2\u01e5\u01e6\7$\2\2\u01e6\u008e\3")
        buf.write("\2\2\2\u01e7\u01e9\t\4\2\2\u01e8\u01e7\3\2\2\2\u01e9\u01ea")
        buf.write("\3\2\2\2\u01ea\u01e8\3\2\2\2\u01ea\u01eb\3\2\2\2\u01eb")
        buf.write("\u0090\3\2\2\2\u01ec\u01ed\7\62\2\2\u01ed\u01ee\7z\2\2")
        buf.write("\u01ee\u01f2\3\2\2\2\u01ef\u01f1\t\5\2\2\u01f0\u01ef\3")
        buf.write("\2\2\2\u01f1\u01f4\3\2\2\2\u01f2\u01f0\3\2\2\2\u01f2\u01f3")
        buf.write("\3\2\2\2\u01f3\u0092\3\2\2\2\u01f4\u01f2\3\2\2\2\u01f5")
        buf.write("\u01f7\t\6\2\2\u01f6\u01f5\3\2\2\2\u01f7\u01fa\3\2\2\2")
        buf.write("\u01f8\u01f6\3\2\2\2\u01f8\u01f9\3\2\2\2\u01f9\u01fb\3")
        buf.write("\2\2\2\u01fa\u01f8\3\2\2\2\u01fb\u01ff\t\7\2\2\u01fc\u01fe")
        buf.write("\t\b\2\2\u01fd\u01fc\3\2\2\2\u01fe\u0201\3\2\2\2\u01ff")
        buf.write("\u01fd\3\2\2\2\u01ff\u0200\3\2\2\2\u0200\u0094\3\2\2\2")
        buf.write("\u0201\u01ff\3\2\2\2\u0202\u0204\t\t\2\2\u0203\u0202\3")
        buf.write("\2\2\2\u0204\u0205\3\2\2\2\u0205\u0203\3\2\2\2\u0205\u0206")
        buf.write("\3\2\2\2\u0206\u0207\3\2\2\2\u0207\u0208\bK\2\2\u0208")
        buf.write("\u0096\3\2\2\2\u0209\u020a\7\61\2\2\u020a\u020b\7,\2\2")
        buf.write("\u020b\u020f\3\2\2\2\u020c\u020e\13\2\2\2\u020d\u020c")
        buf.write("\3\2\2\2\u020e\u0211\3\2\2\2\u020f\u0210\3\2\2\2\u020f")
        buf.write("\u020d\3\2\2\2\u0210\u0212\3\2\2\2\u0211\u020f\3\2\2\2")
        buf.write("\u0212\u0213\bL\3\2\u0213\u0098\3\2\2\2\17\2\u009b\u00cd")
        buf.write("\u0121\u01cb\u01d6\u01e2\u01ea\u01f2\u01f8\u01ff\u0205")
        buf.write("\u020f\4\b\2\2\3L\2")
        return buf.getvalue()


class CircomLexer(Lexer):
    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    SIGNAL_TYPE = 1
    LP = 2
    RP = 3
    LB = 4
    RB = 5
    LC = 6
    RC = 7
    SEMICOLON = 8
    DOT = 9
    COMMA = 10
    UNDERSCORE = 11
    TERNARY_CONDITION = 12
    TERNARY_ALTERNATIVE = 13
    EQ_CONSTRAINT = 14
    LEFT_CONSTRAINT = 15
    LEFT_ASSIGNMENT = 16
    RIGHT_CONSTRAINT = 17
    RIGHT_ASSIGNMENT = 18
    SELF_OP = 19
    NOT = 20
    BNOT = 21
    POW = 22
    MUL = 23
    DIV = 24
    QUO = 25
    MOD = 26
    ADD = 27
    SUB = 28
    SHL = 29
    SHR = 30
    BAND = 31
    BXOR = 32
    BOR = 33
    EQ = 34
    NEQ = 35
    GT = 36
    LT = 37
    LE = 38
    GE = 39
    AND = 40
    OR = 41
    ASSIGNMENT = 42
    ASSIGNMENT_WITH_OP = 43
    SIGNAL = 44
    INPUT = 45
    OUTPUT = 46
    PUBLIC = 47
    TEMPLATE = 48
    COMPONENT = 49
    VAR = 50
    FUNCTION = 51
    RETURN = 52
    IF = 53
    ELSE = 54
    FOR = 55
    WHILE = 56
    DO = 57
    LOG = 58
    ASSERT = 59
    INCLUDE = 60
    PARALLEL = 61
    PRAGMA = 62
    BUS = 63
    CIRCOM = 64
    CUSTOM_TEMPLATES = 65
    CUSTOM = 66
    MAIN = 67
    SINGLE_LINE_COMMENT = 68
    MULTI_LINES_COMMENT = 69
    STRING = 70
    NUMBER = 71
    HEXNUMBER = 72
    IDENTIFIER = 73
    WHITESPACE = 74
    UnclosedComment = 75

    channelNames = [u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN"]

    modeNames = ["DEFAULT_MODE"]

    literalNames = ["<INVALID>",
                    "'('", "')'", "'['", "']'", "'{'", "'}'", "';'", "'.'", "','",
                    "'_'", "'?'", "':'", "'==='", "'<=='", "'<--'", "'==>'", "'-->'",
                    "'!'", "'~'", "'**'", "'*'", "'/'", "'\\'", "'%'", "'+'", "'-'",
                    "'<<'", "'>>'", "'&'", "'^'", "'|'", "'=='", "'!='", "'>'",
                    "'<'", "'<='", "'>='", "'&&'", "'||'", "'='", "'signal'", "'input'",
                    "'output'", "'public'", "'template'", "'component'", "'var'",
                    "'function'", "'return'", "'if'", "'else'", "'for'", "'while'",
                    "'do'", "'log'", "'assert'", "'include'", "'parallel'", "'pragma'",
                    "'bus'", "'circom'", "'custom_templates'", "'custom'", "'main'"]

    symbolicNames = ["<INVALID>",
                     "SIGNAL_TYPE", "LP", "RP", "LB", "RB", "LC", "RC", "SEMICOLON",
                     "DOT", "COMMA", "UNDERSCORE", "TERNARY_CONDITION", "TERNARY_ALTERNATIVE",
                     "EQ_CONSTRAINT", "LEFT_CONSTRAINT", "LEFT_ASSIGNMENT", "RIGHT_CONSTRAINT",
                     "RIGHT_ASSIGNMENT", "SELF_OP", "NOT", "BNOT", "POW", "MUL",
                     "DIV", "QUO", "MOD", "ADD", "SUB", "SHL", "SHR", "BAND", "BXOR",
                     "BOR", "EQ", "NEQ", "GT", "LT", "LE", "GE", "AND", "OR", "ASSIGNMENT",
                     "ASSIGNMENT_WITH_OP", "SIGNAL", "INPUT", "OUTPUT", "PUBLIC",
                     "TEMPLATE", "COMPONENT", "VAR", "FUNCTION", "RETURN", "IF",
                     "ELSE", "FOR", "WHILE", "DO", "LOG", "ASSERT", "INCLUDE", "PARALLEL",
                     "PRAGMA", "BUS", "CIRCOM", "CUSTOM_TEMPLATES", "CUSTOM", "MAIN",
                     "SINGLE_LINE_COMMENT", "MULTI_LINES_COMMENT", "STRING", "NUMBER",
                     "HEXNUMBER", "IDENTIFIER", "WHITESPACE", "UnclosedComment"]

    ruleNames = ["SIGNAL_TYPE", "LP", "RP", "LB", "RB", "LC", "RC", "SEMICOLON",
                 "DOT", "COMMA", "UNDERSCORE", "TERNARY_CONDITION", "TERNARY_ALTERNATIVE",
                 "EQ_CONSTRAINT", "LEFT_CONSTRAINT", "LEFT_ASSIGNMENT",
                 "RIGHT_CONSTRAINT", "RIGHT_ASSIGNMENT", "SELF_OP", "NOT",
                 "BNOT", "POW", "MUL", "DIV", "QUO", "MOD", "ADD", "SUB",
                 "SHL", "SHR", "BAND", "BXOR", "BOR", "EQ", "NEQ", "GT",
                 "LT", "LE", "GE", "AND", "OR", "ASSIGNMENT", "ASSIGNMENT_WITH_OP",
                 "SIGNAL", "INPUT", "OUTPUT", "PUBLIC", "TEMPLATE", "COMPONENT",
                 "VAR", "FUNCTION", "RETURN", "IF", "ELSE", "FOR", "WHILE",
                 "DO", "LOG", "ASSERT", "INCLUDE", "PARALLEL", "PRAGMA",
                 "BUS", "CIRCOM", "CUSTOM_TEMPLATES", "CUSTOM", "MAIN",
                 "SINGLE_LINE_COMMENT", "MULTI_LINES_COMMENT", "STRING",
                 "NUMBER", "HEXNUMBER", "IDENTIFIER", "WHITESPACE", "UnclosedComment"]

    grammarFileName = "Circom.g4"

    def __init__(self, input=None, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None

    def action(self, localctx: RuleContext, ruleIndex: int, actionIndex: int):
        if self._actions is None:
            actions = dict()
            actions[74] = self.UnclosedComment_action
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))

    def UnclosedComment_action(self, localctx: RuleContext, actionIndex: int):
        if actionIndex == 0:
            import Errors
            raise Errors.UnclosedComment(self.line, self.column)
