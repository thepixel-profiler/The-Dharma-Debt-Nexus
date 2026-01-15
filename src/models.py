import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class DharmaGCN(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        """
        GCN Architecture for Dharma-Debt Nexus.
        input_dim: 3 (Age, Income, Dharma Score)
        hidden_dim: 16 (Learned relational patterns)
        output_dim: 2 (Safe vs. High Risk)
        """
        super(DharmaGCN, self).__init__()
        # Standard GCN layers from PyTorch Geometric
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, output_dim)

    def forward(self, x, edge_index):
        """
        The Forward Pass. 
        IMPORTANT: Must accept 'edge_index' to avoid the 500 error!
        """
        # First layer: Graph Convolution + ReLU activation
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        
        # Second layer: Graph Convolution + Log Softmax for classification
        x = self.conv2(x, edge_index)
        
        # log_softmax is standard for NLLLoss (Negative Log Likelihood)
        return F.log_softmax(x, dim=1)