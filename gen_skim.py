import itertools
import joblib

import networkx as nx
assert nx.__version__ == "2.1"


def process_g(nodes):
    l = [nx.algorithms.shortest_path_length(road_graph,
                                           ix1, ix2) for ix1, ix2 in nodes]
    return l

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def gen_skim_graph(write_path=None, n_jobs=12):
    print("==={} rows to process===".format(len(road_graph) * len(road_graph)))
    nodes = batch(list(itertools.permutations(list(road_graph.nodes), 2)), n=3000)
    g = (joblib.delayed(process_g)(n)\
         for n in nodes)

    p = joblib.Parallel(n_jobs=n_jobs, verbose=1)(g)

    skim_graph = nx.DiGraph()
    counter = 0
    for (ix1, ix2), p in zip(nodes, itertools.chain(*p)):
            skim_graph.add_edge(ix1, ix2, weight=p[counter])
            counter += 1

    if write_path:
        nx.write_gpickle(skim_graph, write_path)

    return skim_graph


if __name__ == "__main__":
    import sys
    road_graph = nx.read_gpickle(sys.argv[1])
    gen_skim_graph(write_path=sys.argv[2])
