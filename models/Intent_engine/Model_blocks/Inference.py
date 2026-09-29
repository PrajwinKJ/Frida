import torch
import tiktoken
import Intent_Engine as ie
import json

with open("/home/prajwinkj/VSCode/Frida/models/Intent_engine/Model_blocks/config/config.json",'r') as f:
    config=json.load(f)

embed_dim=config['embed_dim']
context_length=config['context_len']
classes=config['classes']

tokenizer=tiktoken.get_encoding("gpt2")
model=ie.IntentEngine(tokenizer=tokenizer,embed_dim=embed_dim,context_len=context_length,classes=classes)
model.to("cpu")
checkpoint=torch.load("/home/prajwinkj/VSCode/Frida/models/Intent_engine/Model_blocks/Intent_Engine_/Intent_Engine_v1_checkpoint.pth",map_location="cpu")
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

intents={
    0:"TEXT_GENERATION",
    1:"TOOL_CALL"
}

def get_intent(X):
    X=tokenizer.encode(X)
    mask=[1]*len(X)
    mask+=[0]*(context_length-len(X))
    X+=[tokenizer.n_vocab]*(context_length-len(X))
    X=torch.tensor(X,dtype=torch.long).unsqueeze(0)
    mask=torch.tensor(mask,dtype=torch.long).unsqueeze(0)
    with torch.no_grad():
        logits=model(X,mask)
        predicted=logits.argmax(dim=1).item()

    return intents[predicted]
