# src/main\Circom/cli.py
import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.getcwd()))
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../../", "src")))


def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    sys.path.append(os.path.abspath(os.getcwd()))

    for sub in ["parser", "astgen", "typecheck", "utils", "cdggen", "detect", "target"]:
        path = os.path.join(BASE_DIR, "circheck", sub)
        if path not in sys.path:
            sys.path.append(path)

    from .core import detect, print_reports, report_to_file

    parser = argparse.ArgumentParser(
        description="Circheck: Static analysis tool to detect ZKP vulnerabilities in Circom circuits.")
    parser.add_argument("input", help="Path to Circom file to analyze")
    parser.add_argument(
        "--json", help="Output JSON report to file", default=None)
    args = parser.parse_args()

    graphs, reports = detect(args.input)
    if not graphs or not reports:
        print("[Error] Analysis failed.")
        return

    print_reports(graphs, reports)

    if args.json:
        if not args.json.endswith(".json"):
            print(f"[Error] Output file must end with '.json': {args.json}")
            return
        try:
            report_to_file(graphs, reports, args.json)
            print(f"[Success] Saved report to {args.json}")
        except Exception as e:
            print(f"[Error] Failed to write JSON report: {e}")
