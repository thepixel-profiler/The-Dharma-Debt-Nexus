import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class DharmaGCN(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(DharmaGCN, self).__init__()
        # First Layer: Aggregates neighborhood info
        self.conv1 = GCNConv(input_dim, hidden_dim)
        # Second Layer: Refines embeddings for classification
        self.conv2 = GCNConv(hidden_dim, output_dim)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        # Layer 1 + Activation
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.5, training=self.training)

        # Layer 2 (Output)
        x = self.conv2(x, edge_index)
        
        # Log Softmax is used for classification (Default vs. Non-Default)
        return F.log_softmax(x, dim=1)