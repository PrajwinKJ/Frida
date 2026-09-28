import pandas as pd
import tiktoken
import torch
import torch.nn as nn
from torch.utils.data import DataLoader,TensorDataset
import torch.optim as optim
import Intent_Engine as ie

data=pd.read_csv('/home/prajwinkj/VSCode/Frida/models/Intent_engine/Datas/data1081.csv')
tokenizer=tiktoken.get_encoding('gpt2')
torch.manual_seed(42)

def tokenize(text):
    token=tokenizer.encode(text)
    attention_mask=[1]*len(token)
    attention_mask+=[0]*(512-len(token))
    token+=[tokenizer.n_vocab]*(512-len(token))
    return token,attention_mask

data[['token','attention_mask']]=data['text'].apply(lambda x: pd.Series(tokenize(x)))

train_data=data[:int(len(data)*0.8)]
train_tokens=torch.tensor(train_data['token'].tolist(),dtype=torch.long)
train_att_mask=torch.tensor(train_data['attention_mask'].tolist(),dtype=torch.long)

label_id={
    'TEXT_GENERATION':0,
    'TOOL_CALL':1
}
train_labels=torch.tensor(train_data['label'].map(label_id).tolist(),dtype=torch.long)

tensor_data=TensorDataset(train_tokens,train_att_mask,train_labels)
train_loader=DataLoader(tensor_data,32,True)

test_data=data[int(len(data)*0.8):]
test_tokens=torch.tensor(test_data['token'].tolist(),dtype=torch.long)
test_mask=torch.tensor(test_data['attention_mask'].tolist(),dtype=torch.long)
test_target=torch.tensor(test_data['label'].map(label_id).tolist(),dtype=torch.long)

test_dataset=TensorDataset(test_tokens,test_mask,test_target)
test_loader=DataLoader(test_dataset,100,False)

device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using {device}")

model=ie.IntentEngine(tokenizer=tokenizer,embed_dim=128,context_len=512,classes=2).to(device)
loss_fn=nn.CrossEntropyLoss()
optimizer=optim.AdamW(model.parameters(),lr=0.0001)


def train_epoch(model,loader,optimizer,loss_fn,device):
    total=0
    correct=0
    for tokens,mask,label in loader:
        tokens,mask,label=[i.to(device) for i in (tokens,mask,label)]
        optimizer.zero_grad()
        logits=model(tokens,mask)
        loss=loss_fn(logits,label)
        loss.backward()
        optimizer.step()
        predicted=logits.argmax(dim=1)
        total+=label.size(0)
        correct+=predicted.eq(label).sum().item()
    return (correct/total)*100

def evaluate(model,loader,device):
    model.eval()
    correct=0
    total=0
    with torch.no_grad():
        for tokens,mask,target in loader:
            tokens,mask,target=[i.to(device) for i in (tokens,mask,target)]
            logits=model(tokens,mask)
            predicted=logits.argmax(dim=1)
            total+=target.size(0)
            correct+=predicted.eq(target).sum().item()

    return (correct/total)*100

epochs=10

for i in range(epochs):
    train_accuracy=train_epoch(model=model,loader=train_loader,optimizer=optimizer,loss_fn=loss_fn,device=device)
    test_accuracy=evaluate(model=model,loader=test_loader,device=device)
    print(f"Epoch: {i+1}")
    print(f"Train Accuracy: {train_accuracy:.5f}        Test Accuracy: {test_accuracy:.5f}")

torch.save({
    "model_state_dict":model.state_dict(),
    "optimizer_state_dict":optimizer.state_dict(),
    "epoch":epochs,
},"/home/prajwinkj/VSCode/Frida/models/Intent_engine/Model_blocks/Intent_Engine_/Intent_Engine_v1_checkpoint.pth")