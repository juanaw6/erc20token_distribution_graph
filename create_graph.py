import plotly.graph_objects as go
import networkx as nx
import json
import community

def create_graph():
    with open('holders.json', 'r') as file:
        data = json.load(file)

    G = nx.Graph()

    token_sym = 'TOKEN'
    G.add_node(token_sym)
    with open('contract_addr.json', 'r') as file :
        contract_addr_list = json.load(file)
    contract_addr = [addr['contract_addr'] for addr in contract_addr_list]
    
    total_holder_addr = 0
    for holder in data:
        if holder is None:
            continue
        total_holder_addr += 1
        holder_addr = holder['holder_addr']
        if holder_addr in contract_addr:
            continue
        G.add_edge(holder_addr, token_sym, weight=0)
        for addr, freq in holder['recent_tx_freq'].items():
            if addr in contract_addr:
                continue
            if G.has_edge(holder_addr, addr):
                G[holder_addr][addr]['weight'] += freq
            else:
                G.add_edge(holder_addr, addr, weight=freq)

    pos = nx.spring_layout(G, seed=42, k=0.2)

    partition = community.best_partition(G, weight='weight')

    num_communities = len(set(partition.values())) - 1
    print(f"Number of holders: {total_holder_addr}")
    print(f"Number of communities: {num_communities}")

    community_colors = {node: partition.get(node) for node in G.nodes()}

    pos[token_sym] = [0, 0]

    edge_x = []
    edge_y = []
    edge_weights = []
    edge_annotations = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

        weight = G[edge[0]][edge[1]]['weight']
        edge_weights.append(weight)

        if weight > 0:
            edge_annotations.append(
                dict(
                    x=(x0 + x1) / 2,
                    y=(y0 + y1) / 2,
                    xref="x",
                    yref="y",
                    text=str(weight),
                    showarrow=False,
                    font=dict(size=8),
                )
            )

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        if node != 'TOKEN' :
            node_text.append(str(node)[:5] + '..' + str(node)[-2:])
        else :
            node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="bottom center",
        hoverinfo='text',
        marker=dict(
            colorscale='YlGnBu',
            size=10,
            color=[],
            line_width=2))

    node_adjacencies = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))

    node_trace.marker.color = node_adjacencies
    node_trace.marker.color = [community_colors[node] for node in G.nodes()]

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=f'<br>Network Graph of Token Holders, Total Holders: {total_holder_addr}, Total Communities: {num_communities}, Total Contract Addresses: {len(contract_addr)}, Total Actual Holders: {num_communities + len(contract_addr)}',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        annotations=edge_annotations
                    ))
    fig.show()

create_graph()