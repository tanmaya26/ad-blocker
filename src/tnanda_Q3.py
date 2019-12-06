import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import warnings
import argparse
warnings.filterwarnings("ignore")

df_macys = pd.read_csv("www.macys.com..csv")
df_macys.head()
macys_sites = list(df_macys.hostname.unique())
df_cnn = pd.read_csv("www.cnn.com..csv")
df_cnn.head()
cnn_sites = list(df_cnn.hostname.unique())
df_boa = pd.read_csv("www.bankofamerica.com..csv")
df_boa.head()
boa_sites = list(df_boa.hostname.unique())
macys = []
cnn = []
boa = []
for site in macys_sites:
    if "macys" not in site:
        macys.append(site)
for site in cnn_sites:
    if "cnn" not in site:
        cnn.append(site)
for site in boa_sites:
    if "bankofamerica" not in site:
        boa.append(site)

source_m = []
source_c = []
source_b = []
for i in range(0, len(macys)):
    source_m.append("www.macys.com")

for i in range(0, len(cnn)):
    source_c.append("www.cnn.com")

for i in range(0, len(boa)):
    source_b.append("www.bankofamerica.com")

macys_graph = map(lambda x, y: [x, y], source_m, macys)
cnn_graph = map(lambda x, y: [x, y], source_c, cnn)
boa_graph = map(lambda x, y: [x, y], source_b, boa)
all_labels = {}
third_party_sites = [macys, cnn, boa]
print("CNN Third-party domains")
for x in cnn:
    print x
print("Macys Third-party domains")
for x in macys:
    print x
print("Bank Of America Third-party domains")
for x in boa:
    print x
macys.append("www.macys.com")
cnn.append("www.cnn.com")
boa.append("www.bankofamerica.com")
sites = [macys, cnn, boa]
for site in sites:
    for m in site:
        m1 = m[::-1]
        flag = 0
        ind = 0
        for i, c in enumerate(m1):
            if c == '.' and flag == 0:
                flag = 1
            elif c == '.' and flag == 1:
                ind = i
                break
        x = len(m) - ind - 1
        wrd = m[x + 1:len(m)]
        all_labels[m] = wrd

g = macys_graph + cnn_graph + boa_graph

df = pd.DataFrame(g)
df.columns = ['source', 'target']

G = nx.DiGraph()
G = nx.from_pandas_edgelist(df, 'source', 'target', ['source', 'target'])
pos = nx.spring_layout(G)
labels = {}
for i, node in enumerate(G.nodes()):
    labels[node] = all_labels[node]
nx.draw_networkx_nodes(G, pos,
                       nodelist=G.nodes,
                       node_color='y',
                       node_size=15,
                       alpha=0.9)

nx.draw_networkx_edges(G, pos,
                       edgelist=G.edges,
                       width=1, alpha=0.1, edge_color='black')
plt.axis('off')
plt.tight_layout()
nx.draw_networkx_labels(G, pos, labels, font_size=4, color='violet', alpha=0.8)
plt.savefig('graph.png', dpi=200)
