import torch
import torch.nn as nn

class MultiHeadAttention(nn.Module):
    def __init__(self,embed_dim,heads=4):
        super().__init__()
        self.embed_dim=embed_dim
        self.W_k,self.W_q,self.W_v=[nn.Linear(self.embed_dim,self.embed_dim) for i in range(3)]         #dim=[128,128]
        self.head=heads
        if self.embed_dim%self.head!=0:
            raise ValueError("Model Dimension must be divisible by Head")
        self.head_dim=self.embed_dim//self.head                   #32
        self.W_o=nn.Linear(self.embed_dim,self.embed_dim)          #[128,128]

    def forward(self,X,attention_mask=None):            
        K,Q,V=[i(X).reshape(X.shape[0],X.shape[1],self.head,self.head_dim).transpose(2,1) for i in [self.W_k,self.W_q,self.W_v]] #after reshape=[batchsize,nm of inp rows,4,32] | after transpose=[batchsize,heads,no of inp rows,32]
        d_k=torch.tensor(K.shape[-1])
        score=(Q@K.transpose(-1,-2)/torch.sqrt(d_k))
        if attention_mask is not None:
            attention_mask=attention_mask[:,None,None,:]
            score=score.masked_fill(attention_mask==0,float('-inf'))
        weight=torch.softmax(score,-1)
        output=(weight@V).transpose(2,1).reshape(X.shape[0],X.shape[1],self.embed_dim)         #[batchsize,no of inp,128]
        projection=self.W_o(output)
        return projection
    
class FeedForwardNetwork(nn.Module):
    def __init__(self,embed_dim):
        super().__init__()
        self.embed_dim=embed_dim
        d_ff=4*self.embed_dim
        self.ffn=nn.Sequential(nn.Linear(self.embed_dim,d_ff),nn.GELU(),nn.Linear(d_ff,self.embed_dim))

    def forward(self,X):
        return self.ffn(X)

class TransformerBlock(nn.Module):
    def __init__(self,embed_dim):
        super().__init__()
        self.embed_dim=embed_dim
        self.Layernorm1=nn.LayerNorm(self.embed_dim)
        self.Layernorm2=nn.LayerNorm(self.embed_dim)
        self.mha=MultiHeadAttention(self.embed_dim)
        self.ffn=FeedForwardNetwork(self.embed_dim)

    def forward(self,X,attention_mask=None):
        mha_out=self.mha(X,attention_mask)
        X=self.Layernorm1(X+mha_out)
        ffn_out=self.ffn(X)
        X=self.Layernorm2(X+ffn_out)        #512,128

        return X
