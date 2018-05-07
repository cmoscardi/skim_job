import itertools

import dask.bag as db
from dask.diagnostics import ProgressBar
from dask.multiprocessing import get

import networkx as nx
assert nx.__version__ == "2.1"


def process_g(arg):
    ix1, ix2 = arg
    l = nx.algorithms.shortest_path_length(road_graph, 
                                           ix1,
                                           ix2)
    return (ix1, ix2, l)

def gen_skim_graph(write_path=None, n_jobs=12):
    print("==={} rows to process===".format(len(road_graph) * len(road_graph)))
    nodes = list(road_graph.nodes)
    nodedb = db.from_sequence(itertools.permutations(nodes, 2), npartitions=56)
    results = nodedb.map(process_g)
    with ProgressBar():
        final = results.compute(get=get)


    skim_graph = nx.DiGraph()
    for (ix1, ix2, p) in final:
        skim_graph.add_edge(ix1, ix2, weight=p[counter])

    if write_path:
        nx.write_gpickle(skim_graph, write_path)

    return skim_graph


if __name__ == "__main__":
    import sys
    road_graph = nx.read_gpickle(sys.argv[1])
    gen_skim_graph(write_path=sys.argv[2])
