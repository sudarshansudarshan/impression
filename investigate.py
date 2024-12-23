import random
import networkx as nx
import matplotlib.pyplot as plt


def create_graph_from_csv(file_name):
    #Create a directed graph from the csv file impression1.csv
    #the first row contains the header the rest contains the adjacency list
    G = nx.DiGraph()
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip()
            nodes = line.split(',')
            for node in nodes[1:]:
                G.add_edge(nodes[0], node)
    return G


G1=create_graph_from_csv('impression1.csv')
G2=create_graph_from_csv('impression2.csv')

#remove edges that are self loops in G1 and G2
G1.remove_edges_from(nx.selfloop_edges(G1))
G2.remove_edges_from(nx.selfloop_edges(G2))

#remove the node '' from G1 and G2
G1.remove_node('')
G2.remove_node('')



k
#display the common edges across G1 and G2
common_edges = G1.edges() & G2.edges()
print('Common edges:', common_edges)
#display the number of common edges
print('Number of common edges:', len(common_edges))

#run pagerank on G1 and display the top 10 nodes
pr1 = nx.pagerank(G1)
sorted_pr1 = sorted(pr1.items(), key=lambda x: x[1], reverse=True)
print('Top 10 nodes in G1:', sorted_pr1[:10])
#run pagerank on G2 and display the top 10 nodes
pr2 = nx.pagerank(G2)
sorted_pr2 = sorted(pr2.items(), key=lambda x: x[1], reverse=True)
print('Top 10 nodes in G2:', sorted_pr2[:10])

#run pagerank on G1 and G2 and display the common nodes in the top 10
top_10_G1 = set([node for node, _ in sorted_pr1[:10]])
top_10_G2 = set([node for node, _ in sorted_pr2[:10]])
common_top_10 = top_10_G1 & top_10_G2
print('Common nodes in the top 10:', common_top_10)


