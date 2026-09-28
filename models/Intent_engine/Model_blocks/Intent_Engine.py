import torch
import torch.nn as nn
import encoder as enc

class IntentEngine(nn.Module):
    def __init__(self,tokenizer,embed_dim,context_len,classes=2):
        super().__init__()
        self.token_embedding=nn.Embedding((tokenizer.n_vocab)+1,embed_dim)
        self.pos_embedding=nn.Embedding(context_len,embed_dim)
        self.tr_blocks=nn.ModuleList([enc.TransformerBlock(embed_dim=embed_dim) for _ in range(6)])
        self.classifier=nn.Linear(embed_dim,classes)

    def forward(self,input_ids,attention_mask):
        pos=torch.arange(
            input_ids.size(1),
            device=input_ids.device
        )
        x=self.token_embedding(input_ids)

        x=x+self.pos_embedding(pos)

        for blocks in self.tr_blocks:
            x=blocks(x,attention_mask)
             
        mask=attention_mask.unsqueeze(-1)
        x=x*mask
        x=x.sum(dim=1)/mask.sum(dim=1).clamp(min=1)
        logits=self.classifier(x)

        return logits