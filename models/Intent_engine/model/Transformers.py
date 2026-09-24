import torch
import torch.nn as nn

class MultiHeadAttention(nn.Module):
    def __init__(self,embed_dim):
        super().__init__()
        self.embed_dim=embed_dim
        self.W_k,self.W_q,self.W_v=[nn.Linear(embed_dim,embed_dim) for i in range(3)]
        self.head=4
        if embed_dim%self.head!=0:
            raise ValueError("Model Dimension must be divisible by Head")
        self.head_dim=embed_dim/self.head
        self.W_o=nn.Linear(embed_dim,embed_dim)

    def forward(self,X):
        K,Q,V=[i(X).reshape(X.shape[0],self.head,self.head_dim).transpose(0,1) for i in [self.W_k,self.W_q,self.W_v]]
        d_k=torch.tensor(K.shape[-1])
        score=(Q(K.transpose(-1,-2))/torch.sqrt(d_k))
        weight=torch.softmax(score)
        output=(weight(V)).transpose(0,1).reshape(X.shape[0],self.embed_dim)
        projection=self.W_o(output)
        return projection
    
class FeedForwardNetwork(nn.Module):
    def __init__(self,embed_dim):
        super().__self__()
        d_ff=4*embed_dim
        self.ffn=nn.Sequential(nn.Linear(embed_dim,d_ff),nn.GELU(),nn.Linear(d_ff,embed_dim))

    def forward(self,X):
        return self.ffn(X)

class TransformerBlock(nn.Module):
    def __init__(self,embed_dim):
        super().__init__()
        self.Layernorm1=nn.LayerNorm(embed_dim)
        self.Layernorm2=nn.LayerNorm(embed_dim)
        self.mha=MultiHeadAttention(embed_dim)
        self.ffn=FeedForwardNetwork(embed_dim)

    def forward(self,X):
        mha_out=self.mha(X)
        X=self.Layernorm1(X+mha_out)
        ffn_out=self.ffn(X)
        X=self.Layernorm2(X+ffn_out)

        return X
