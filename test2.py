import networkx as nx
import matplotlib.pyplot as plt
import random

# Membuat fungsi untuk menghitung rata-rata weight dari sisi yang menghubungkan dua simpul
def average_weight(G, node):
    total_weight = 0
    count = 0
    for neighbor in G.neighbors(node):
        if G[node][neighbor].get('weight', 0) > 0:
            total_weight += G[node][neighbor]['weight']
            count += 1
    return total_weight / count if count else 0

def assign_group_colors(group_of_holders, G):
    color_map = {}
    unique_colors = plt.cm.get_cmap('hsv', len(group_of_holders) + 2)  # +2 untuk alamat token dan pemegang lain
    color_map["TokenX"] = unique_colors(0)

    for i, holder_group in enumerate(group_of_holders):
        for holder in holder_group:
            color_map[holder] = unique_colors(i + 1)
    
    # Memberikan warna default kepada pemegang yang tidak termasuk dalam grup
    default_color = unique_colors(len(group_of_holders) + 1)
    for node in G.nodes():
        if node not in color_map:
            color_map[node] = default_color

    return [color_map[node] for node in G.nodes()]

# Memberi warna pada setiap group
# Membuat graf tanpa deteksi komunitas
G = nx.Graph()
G.add_node("TokenX")

# Menambahkan 30 pemegang token
pemegang_token = ["" + str(i) for i in range(1, 31)]
for alamat in pemegang_token:
    G.add_edge("TokenX", alamat, weight=1)

# Menambahkan sisi antar pemegang token secara acak dengan weight acak
for i in range(len(pemegang_token)):
    for j in range(i+1, len(pemegang_token)):
        if random.random() > 0.98:  # 20% kemungkinan untuk membuat sisi
            # Weight acak antara 1 dan 10
            G.add_edge(pemegang_token[i], pemegang_token[j], weight=random.randint(1, 10))

# Menghitung rata-rata weight untuk setiap pemegang token
average_weights = {node: average_weight(G, node) for node in pemegang_token}

# Menentukan threshold untuk group of holder
# Misalnya, kita menggunakan rata-rata weight dari semua pemegang token sebagai threshold
threshold = sum(average_weights.values()) / len(average_weights)

# Membuat group of holders berdasarkan rata-rata weight di atas threshold
group_of_holders = [node for node, avg_weight in average_weights.items() if avg_weight > threshold]

colors = assign_group_colors(group_of_holders, G)

pos = nx.spring_layout(G)
# Visualisasi graf dengan menonjolkan group of holders
nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=500, alpha=0.8)
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos)
plt.title("Graf Pemegang Token dengan Group of Holders Berwarna Berbeda")
plt.show()