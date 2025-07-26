from functools import wraps
import time
from antlr4 import *
import sys
import traceback
import os


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[Timeit]     Analysis completed in {(end - start):.2f} s")
        return result

    return wrapper


def generate_ast(filename):
    from CircomLexer import CircomLexer
    from CircomParser import CircomParser
    from ASTGeneration import ASTGeneration
    import Errors
    from Report import Report, ReportType
    from AST import FileLocation

    try:
        inputstream = FileStream(filename, encoding='utf-8')
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
                filename, None, None), f.message, False).show()
            return None
        except Exception as e:
            Report(ReportType.ERROR, FileLocation(
                filename, None, None), str(e), False).show()
            return None
        path_env = [filename]
        asttree = ASTGeneration().generate_ast(filename, tree, path_env)
        return asttree
    except Exception as e:
        Report(ReportType.ERROR, FileLocation(filename, None, None),
               "Error generating AST: " + str(e), False).show()
        return None


def typecheck(ast):
    from StaticCheck import TypeCheck
    from Report import Report, ReportType
    from AST import FileLocation
    checked = TypeCheck(ast)
    try:
        checked.check()
    except Exception as e:
        # traceback.print_exc()
        print(e)
        return None, None, None
    return checked.global_env, checked.list_function, checked.list_template


def generate_cdg(ast, param, list_function, list_template):
    from CDGGeneration import CDGGeneration
    try:
        graphs = CDGGeneration(ast, param, list_function,
                               list_template).generateCDG()
        return graphs
    except Exception as e:
        traceback.print_exc()
        print(e)
        return None


def print_reports(graphs, reports):
    from Report import Report, ReportType
    from colorama import Fore
    to_print = {}
    total_reports = 0
    for graph in graphs.values():
        for report_list in reports[graph.name].values():
            for report in report_list:
                path = report.location.path
                line = report.location.start.line
                col = report.location.start.column
                path += f":{line}:{col}"
                if path not in to_print:
                    total_reports += 1
                    to_print[path] = Report(
                        report.type, report.location, report.message)
                else:
                    if report.message not in to_print[path].message:
                        total_reports += 1
                        to_print[path].message += "\n" + \
                                                  ' ' * 13 + report.message
    print("\n" + "=" * 50)
    for report in to_print.values():
        report.show()
    print(Fore.YELLOW + f"⚠ Total warnings: {total_reports}")


def report_to_file(graphs, reports, filename="report.json"):
    import json
    output = {}
    for graph in graphs.values():
        has_report = False
        for report_list in reports[graph.name].values():
            if len(report_list) > 0:
                has_report = True
        if not has_report:
            continue
        output[graph.name] = {}
        for vul in reports[graph.name].keys():
            if len(reports[graph.name][vul]) == 0:
                continue
            output[graph.name][vul] = {}
            for report in reports[graph.name][vul]:
                path = report.location.path
                line = report.location.start.line
                col = report.location.start.column
                path += f":{line}:{col}"
                if path not in output[graph.name][vul]:
                    output[graph.name][vul][path] = []
                if report.message not in output[graph.name][vul][path]:
                    output[graph.name][vul][path].append(report.message)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)


@timeit
def detect(absolute_path):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)

    for sub in ["parser", "astgen", "typecheck", "utils", "cdggen", "detect", "target"]:
        path = os.path.join(BASE_DIR, "circheck", sub)
        if path not in sys.path:
            sys.path.append(path)

    ast = generate_ast(absolute_path)
    if ast is None:
        print("[Error]      Failed to generate AST.")
        return None, None
    print("[Success]    AST generated successfully.")

    checked, list_function, list_template = typecheck(ast)
    if checked is None:
        print("[Error]      Type checking failed.")
        return None, None
    print("[Success]    Type checking passed.")

    graphs = generate_cdg(ast, checked, list_function, list_template)
    if graphs is None:
        print("[Error]      Created CDG failed.")
        return None, None
    print("[Success]    CDG created successfully.")

    from Detect import Detector
    try:
        reports = Detector(graphs).detect()
        print("[Success]    Detection completed successfully.")
    except Exception as e:
        traceback.print_exc()
        print(f"[Error]      An error occurred during detection. {str(e)}")
        return None, None

    return graphs, reports
