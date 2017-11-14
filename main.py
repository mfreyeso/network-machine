import pandas as pd
import networkx as nx
from networkx.algorithms.flow import shortest_augmenting_path

data = pd.read_csv('data/CollegeMsg.txt', sep=' ',
                   encoding='latin-1', header=None)

data.columns = ['fromNode', 'toNode', 'datetime']

graph_ins = nx.from_pandas_dataframe(data,
                                     source='fromNode',
                                     target='toNode',
                                     edge_attr=True,
                                     create_using=nx.DiGraph())


nodes_gb = max(nx.strongly_connected_components(graph_ins), key=len)
gb = graph_ins.subgraph(nodes_gb)
undgb = gb.to_undirected()


def write_result(result_dict):
    with open("result/results.txt", "a") as file_result:
        for i in result_dict.items():
            file_result.write("%s\t%s\n" % (i[0], i[1]))


def _calculate_kcomponents(graph):
    kcomponents = nx.k_components(graph, flow_func=shortest_augmenting_path)
    result = {"K-Components": ""}
    
    for kc in sorted(kcomponents):
        kp = "Level K-%s" % (kc)
        result[kp] = len(kcomponents[kc])
    
    write_result(result)


def _calculate_cuts(graph):
    cuts = list(nx.all_node_cuts(graph, flow_func=shortest_augmenting_path))
    result = {"Cuts": len(cuts)}
    write_result(result)


def main():
    _calculate_kcomponents(undgb)
    _calculate_cuts(undgb)

if __name__ == '__main__':
    main()
