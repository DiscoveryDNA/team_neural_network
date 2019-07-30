import torch.nn as nn
import torch.nn.functional as F
from torch.utils import data
import torch
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import time

# Reference for connecting Conv1D and LSTM: https://mxnet.incubator.apache.org/versions/master/tutorials/basic/reshape_transpose.html
class HybridNet(nn.Module):
    
    def __init__(self, pesudo_input, num_filters, filter_size, rnn_size, fc_out, dp1, dp2, 
                 num_rnn_layers=1, rnn_dropout=0):
        super(HybridNet, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=4, out_channels=num_filters, kernel_size=filter_size)
        out = self.conv1(pesudo_input)
        out = nn.MaxPool1d(kernel_size=15, stride=15)(out)
        ####################################################
        print('shape after conv1d {}'.format(out.shape))
        N, C, T = out.shape
        out = torch.transpose(out, 1, 2)
        print('shape before lstm {}'.format(out.shape))
        ####################################################
        # or input_size*seq_len
        self.bi_lstm = nn.LSTM(input_size=C, hidden_size=rnn_size, num_layers=num_rnn_layers,
                              batch_first=True, dropout=rnn_dropout, bidirectional=True)
        out, _ = self.bi_lstm(out)
        print('shape after lstm {}'.format(out.shape))
        N, T, C = out.shape
        #out = torch.transpose(out, 1, 2)
        out = out.reshape(N, -1)
        print('shape after flattening {}'.format(out.shape))
        self.fc1 = nn.Linear(T*C, fc_out, bias=True)
        self.fc2 = nn.Linear(fc_out, 1)
        self.p1 = dp1
        self.p2 = dp2
        
    def forward(self, seq):
        self.activation_seq = F.relu(self.conv1(seq))
        out = nn.MaxPool1d(kernel_size=15, stride=15)(self.activation_seq)
        
#         out = nn.Dropout(p=self.p1)(self.activation_seq)
        
        #################################################################################
        # Input of LSTM layer should have shape (sequence_length, batch_size, input_size)
        #     - Sequence length here should be the length of activation after downsampling
        #     - Input size should be the number of filters
        #################################################################################
        N, C, T = out.shape
#         out = out.view(bs, 1, -1)
        out = torch.transpose(out, 1, 2)
        out, _ = self.bi_lstm(out)
        out = F.relu(out)
        
        #################################################################################
        # Need to flatten the sequence before feeding them into fully connected layer
        #################################################################################
        N, T, C = out.shape
        #out = torch.transpose(out, 1, 2)
        out = out.reshape(N, -1)
        out = self.fc1(out)
        out = nn.Dropout(p=self.p1)(out)
        out = F.relu(out)
        out = self.fc2(out)
        out = nn.Dropout(p=self.p2)(out)
        out = torch.squeeze(out)
        return nn.Sigmoid()(out)

def train(model, train_dataset, val_dataset, config):
    # Unpack config
    epochs = config['epochs']
    device = config['device']
    optimizer = config['opt']
    criterion = config['criterion']
    log_interval = config['log_interval']
    batch_size = config['batch_size']
    
    def get_acc(y_hat, y):
        y_pred = np.where(y_hat >=0.5, 1, 0)
        return np.mean(y_pred == y)
    
    # Generate data loaders
    train_loader = data.DataLoader(train_dataset, batch_size=batch_size)
    val_loader = data.DataLoader(val_dataset, batch_size=batch_size)
    total_train_steps = len(train_loader)
    total_val_steps = len(val_loader)
    
    train_loss_list, val_loss_list = [], []
    train_acc_list, val_acc_list = [], []
    print("Train on {} samples, validate on {} samples".format(len(train_dataset), len(val_dataset)))
    # Start training
    for epoch in range(1, epochs+1):
        train_loss_sum, train_acc_sum = 0, 0
        tic = time.time()
        for i, (batch, labels) in enumerate(train_loader):
            # Forward pass and calculating loss
            batch, labels = batch.to(device), labels.to(device)
            y_hat = model(batch)
            loss = criterion(y_hat, labels)
            
            # Backward pass and updating weights
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_loss_sum += loss.item()
            train_acc_sum += get_acc(y_hat.cpu().detach().numpy(), labels.cpu().detach().numpy())
        tac = time.time()
        avg_train_loss = train_loss_sum/total_train_steps
        avg_train_acc = train_acc_sum/total_train_steps
        train_loss_list.append(avg_train_loss)
        train_acc_list.append(avg_train_acc)
        print('***************************************')
        print('Epoch {}: training loss {}, training acc {}'.format(epoch, avg_train_loss, avg_train_acc))
        print('Time: {} \n'.format(tac-tic))
        
        # Validation
        if epoch % log_interval == 0 or epoch == epochs:
            with torch.no_grad():
                val_loss_sum, val_acc_sum = 0, 0
                for j, (batch, labels) in enumerate(val_loader):
                    batch, labels = batch.to(device), labels.to(device)
                    y_hat = model(batch)
                    loss = criterion(y_hat, labels)
                    val_loss_sum += loss.item()
                    val_acc_sum += get_acc(y_hat.cpu().detach().numpy(), labels.cpu().detach().numpy())
                avg_val_loss = val_loss_sum/total_val_steps
                avg_val_acc = val_acc_sum/total_val_steps
                val_loss_list.append(avg_val_loss)
                val_acc_list.append(avg_val_acc)
                print('[Validation loss {}, validation acc {}] \n'.format(avg_val_loss, avg_val_acc))
    return model, train_loss_list, val_loss_list, train_acc_list, val_acc_list