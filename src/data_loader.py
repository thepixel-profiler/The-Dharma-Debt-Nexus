import pandas as pd
import numpy as np
import torch
from torch_geometric.data import Data

def generate_dharma_data(num_nodes=1000, num_edges=2500):
    # 1. Generate Node Features
    np.random.seed(42)
    node_ids = np.arange(num_nodes)
    
    # Simulating Age (18-70), Income, and a base Credit Score
    age = np.random.randint(18, 70, size=num_nodes)
    income = np.random.normal(50000, 15000, size=num_nodes).clip(15000, 200000)
    
    # Dharma Score: Higher = more reliable. 
    # Influenced slightly by age and income for realism
    dharma_score = (age / 70 * 0.3) + (income / 200000 * 0.7) + np.random.normal(0, 0.1, size=num_nodes)
    dharma_score = dharma_score.clip(0, 1)

    # Combine into a feature matrix
    x = torch.tensor(np.stack([age, income, dharma_score], axis=1), dtype=torch.float)

    # 2. Generate Edges (Relationships)
    # We create random relationships, but favor connecting nodes with similar income (homophily)
    sources = np.random.randint(0, num_nodes, size=num_edges)
    targets = np.random.randint(0, num_nodes, size=num_edges)
    
    # Remove self-loops
    mask = sources != targets
    edge_index = torch.tensor(np.stack([sources[mask], targets[mask]], axis=0), dtype=torch.long)

    # 3. Generate Labels (y): 1 if Default, 0 if Recovered
    # Logic: High income + high dharma_score = low chance of default
    prob_default = 1 - (0.4 * (income/200000) + 0.6 * dharma_score)
    y = torch.tensor((prob_default > 0.6).astype(int), dtype=torch.long)

    return Data(x=x, edge_index=edge_index, y=y)

# Test the generator
if __name__ == "__main__":
    dataset = generate_dharma_data()
    print(f"Graph Generated!\nNodes: {dataset.num_nodes}\nEdges: {dataset.num_edges}")
    # Save for later
    torch.save(dataset, 'data/dharma_graph.pt')