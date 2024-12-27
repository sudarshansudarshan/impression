import networkx as nx
import community as cm
import matplotlib.pyplot as plt


def create_graph_from_csv(file_name):
    G = nx.Graph()
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip()
            nodes = line.split(',')
            for node in nodes[1:]:
                G.add_edge(nodes[0], node)
    return G


G=create_graph_from_csv('impression1.csv')      # creating graph

G.remove_edges_from(nx.selfloop_edges(G))      #removing self loops

G.remove_node('')       #deleting empty nodes

partition = cm.best_partition(G)    #using the louvain community dtection algorithm to group nodes

communities = {}    #storing the different communities for further visualisation
for node, community_id in partition.items():
    if community_id not in communities:
        communities[community_id] = []
    communities[community_id].append(node)

# print("Detected Communities:")
# for community_id, nodes in communities.items():
#     print(f"Community {community_id}: {nodes}")


pos = nx.spring_layout(G, seed=7, k=0.2, iterations=2)

community_colors = [partition[node] for node in G.nodes]

cmap = plt.cm.get_cmap("Set3", len(set(community_colors))) 


#plotting the graph
plt.figure(figsize=(20,20))

nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color="gray", width=0.5)
nx.draw_networkx_nodes(G, pos, node_color=community_colors, node_size=200, cmap=cmap, alpha=0.8)

plt.axis('off')
plt.title("Community Detection using Louvain Method", fontsize=16)

plt.show()

#so in the final output graph the nodes of the same color belong to the same community we can infer they are people of similar behaviour or traits


#link to the journal/research papers for the louvain algorithm: https://perso.uclouvain.be/vincent.blondel/publications/08BG.pdf
#link to a youtube video explaing the algorithm in detail: https://youtu.be/Xt0vBtBY2BU?si=YeQaUnIi4arCz_Zw