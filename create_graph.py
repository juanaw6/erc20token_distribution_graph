import plotly.graph_objects as go
import networkx as nx
import json

def create_graph():
    # Read data from the file
    with open('result.json', 'r') as file:
        data = json.load(file)

    # Create a graph
    G = nx.Graph()

    # Add a node for the 'token'
    token_addr = '0x0d8ca4b20b115D4DA5c13DC45Dd582A5de3e78BF'[:5]
    contract_addr = ["0x0000",
                    "0x0000"]
    contract_addr_list = [addr[:5] for addr in contract_addr]
    G.add_node(token_addr)

    # Add edges from each holder to the 'token' node
    for holder in data:
        if holder is None :
            continue
        holder_addr = holder['holder_addr'][:5]
        if holder_addr in contract_addr_list :
            continue
        G.add_edge(holder_addr, token_addr, weight=0)  # Truncate for simplicity
        for addr, freq in holder['recent_tx_freq'].items():
            truncated_addr = addr[:5]  # Truncate for simplicity
            if truncated_addr in contract_addr_list :
                continue
            # If the edge already exists, update its weight
            if G.has_edge(holder_addr, truncated_addr):
                G[holder_addr][truncated_addr]['weight'] += freq
            else:
                # Otherwise, add a new edge with the initial weight
                G.add_edge(holder_addr, truncated_addr, weight=freq)

    # Generate positions for the nodes
    pos = nx.spring_layout(G)

    # Extract the x and y coordinates and weights
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
        
        # Calculate the midpoint of the edge for annotation
        edge_annotations.append(
            dict(
                x=(x0 + x1) / 2,
                y=(y0 + y1) / 2,
                xref="x",
                yref="y",
                text=str(weight),
                showarrow=False,
                font=dict(size=10)
            )
        )

    # Create the edge trace
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create the node trace
    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="bottom center",
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            color=[],
            line_width=2))

    # Set node hover text
    node_adjacencies = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))

    node_trace.marker.color = node_adjacencies

    # Create the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='<br>Network graph of token holders',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    annotations=edge_annotations  # Add edge annotations
                    ))

    fig.show()

create_graph()