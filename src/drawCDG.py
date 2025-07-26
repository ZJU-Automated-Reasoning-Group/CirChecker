# src/main\Circom/cli.py
import argparse
import sys
import os
import networkx as nx
import matplotlib.pyplot as plt
from enum import Enum, auto

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.getcwd()))


# sys.path.append(os.path.abspath(os.path.join(
#     os.path.dirname(__file__), "../../", "src")))


def draw_cdg(cdg, figsize=(12, 8)):
    from CDG import NodeType, SignalType, EdgeType
    G = nx.DiGraph()

    # Add nodes
    for node in cdg.nodes.values():
        shape = 'o'
        if node.node_type == NodeType.CONSTANT:
            color = 'orange'
            shape = '^'
        elif node.signal_type == SignalType.INPUT:
            color = 'lightblue'
        elif node.signal_type == SignalType.OUTPUT:
            color = 'lightgreen'
        else:
            color = 'lightgray'

        G.add_node(node.id, label=node.id, color=color, shape=shape)

    # Add edges
    for edge in cdg.edges.values():
        style = 'solid' if edge.edge_type == EdgeType.DEPEND else 'dashed'
        color = 'blue' if edge.edge_type == EdgeType.DEPEND else 'red'
        G.add_edge(edge.node_from.id,
                   edge.node_to.id,
                   style=style,
                   color=color)

    pos = nx.kamada_kawai_layout(G)

    # Draw nodes
    shapes = set(nx.get_node_attributes(G, 'shape').values())
    for shape in shapes:
        nodelist = [n for n in G.nodes if G.nodes[n]['shape'] == shape]
        colors = [G.nodes[n]['color'] for n in nodelist]
        nx.draw_networkx_nodes(G,
                               pos,
                               nodelist=nodelist,
                               node_color=colors,
                               node_shape=shape,
                               node_size=1000)

    # Draw edges by type
    for edge_type, style, color, label in [
        (EdgeType.DEPEND, 'solid', 'blue', 'DEPEND'),
        (EdgeType.CONSTRAINT, 'dashed', 'red', 'CONSTRAINT')
    ]:
        edgelist = [(u, v) for u, v, d in G.edges(data=True)
                    if d['style'] == style]
        nx.draw_networkx_edges(G,
                               pos,
                               edgelist=edgelist,
                               style=style,
                               edge_color=color,
                               width=2,
                               arrows=True,
                               arrowstyle='-|>',
                               min_source_margin=15,
                               min_target_margin=15,
                               connectionstyle='arc3,rad=0.1')

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='blue', lw=2, label='DEPEND'),
        Line2D([0], [0],
               color='red',
               lw=2,
               linestyle='dashed',
               label='CONSTRAINT'),
        Line2D([0], [0],
               marker='o',
               color='w',
               label='INPUT',
               markerfacecolor='lightblue',
               markersize=10),
        Line2D([0], [0],
               marker='o',
               color='w',
               label='OUTPUT',
               markerfacecolor='lightgreen',
               markersize=10),
        Line2D([0], [0],
               marker='^',
               color='w',
               label='CONSTANT',
               markerfacecolor='orange',
               markersize=10),
    ]
    plt.legend(handles=legend_elements, loc='upper right')

    plt.title(f"CDG for {cdg.name}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    sys.path.append(os.path.abspath(os.getcwd()))

    for sub in [
        "parser", "astgen", "typecheck", "utils", "cdggen", "detect",
        "target"
    ]:
        path = os.path.join(BASE_DIR, "circheck", sub)
        if path not in sys.path:
            sys.path.append(path)

    from circheck.core import detect, print_reports, report_to_file
    parser = argparse.ArgumentParser(
        description="Circheck: Static analysis tool to detect ZKP vulnerabilities in Circom circuits."
    )
    parser.add_argument("input", help="Path to Circom file to analyze")
    parser.add_argument("--json",
                        help="Output JSON report to file",
                        default=None)
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

    for graph in graphs.values():
        draw_cdg(graph)


main()
