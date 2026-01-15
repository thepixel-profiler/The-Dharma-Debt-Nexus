import torch
import torch.nn.functional as F
import os
from models import DharmaGCN

# PyTorch 2.6 Fix: Allow loading of graph-specific structures
# Add this to avoid "WeightsUnpickler error"
from torch.serialization import add_safe_globals
try:
    import torch_geometric
    # If using newer PyG, allow its internal data structures
    # add_safe_globals([torch_geometric.data.data.Data]) 
except ImportError:
    pass

def train_model():
    # Ensure the models directory exists for saving weights
    os.makedirs('models', exist_ok=True)

    # 1. Load data with security settings adjusted for custom objects
    # If weights_only=True fails on your graph file, use weights_only=False locally
    data = torch.load('D:\THE BIG 3\The-Dharma-Debt-Nexus\data\dharma_graph.pt', weights_only=False)
    
    # 2. Initialize Model (3 input features: Age, Income, Dharma Score)
    model = DharmaGCN(input_dim=3, hidden_dim=16, output_dim=2)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    
    print("Starting Training...")
    model.train()
    for epoch in range(1, 201):
        optimizer.zero_grad()
        out = model(data)
        
        # Calculate loss (Negative Log Likelihood for log_softmax output)
        loss = F.nll_loss(out, data.y)
        loss.backward()
        optimizer.step()
        
        if epoch % 20 == 0:
            # Calculate accuracy for monitoring
            pred = out.argmax(dim=1)
            correct = (pred == data.y).sum()
            acc = int(correct) / int(data.num_nodes)
            print(f'Epoch {epoch:03d} | Loss: {loss.item():.4f} | Acc: {acc:.2%}')

    # 3. Save the state dictionary (Best Practice)
    torch.save(model.state_dict(), 'models/dharma_weights.pth')
    print("\nTraining Complete! Weights saved to models/dharma_weights.pth")

if __name__ == "__main__":
    train_model()