import joblib

import networkx as nx
assert nx.__version__ == "2.1"


def process_g(ix1, ix2):
    l = nx.algorithms.shortest_path_length(road_graph, 
                                           ix1,
                                           ix2)
    return l

def gen_skim_graph(write_path=None, n_jobs=12):
    print("==={} rows to process===".format(len(road_graph) * len(road_graph)))
    nodes = list(road_graph.nodes)
    g = (joblib.delayed(process_g)(ix1, ix2)\
         for ix1 in nodes\
         for ix2 in nodes)

    p = joblib.Parallel(n_jobs=n_jobs, verbose=1)(g)

    skim_graph = nx.DiGraph()
    counter = 0
    for ix1 in nodes:
        for ix2 in nodes:
            skim_graph.add_edge(ix1, ix2, weight=p[counter])
            counter += 1

    if write_path:
        nx.write_gpickle(skim_graph, write_path)

    return skim_graph


if __name__ == "__main__":
    import sys
    road_graph = nx.read_gpickle(sys.argv[1])
    gen_skim_graph(write_path=sys.argv[2])
