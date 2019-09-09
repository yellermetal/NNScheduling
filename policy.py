#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 10:13:32 2019

@author: ariell
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical

import numpy as np

gamma = 1

class Policy(nn.Module):
    def __init__(self, input_size, num_hidden_layers, hidden_size):
        super(Policy, self).__init__()
        
        self.in_layer = nn.Linear(input_size, hidden_size)        
        self.hidden_layer_1 = nn.Linear(hidden_size, hidden_size) 
        self.hidden_layer_2 = nn.Linear(hidden_size, hidden_size) 
        self.out_layer = nn.Linear(hidden_size, 1)
        
        self.saved_log_probs = []
        self.rewards = []
        
    def forward(self, x):
        x = F.relu(self.in_layer(x))
        x = F.relu(self.hidden_layer_1(x))
        x = F.relu(self.hidden_layer_2(x))
        return F.softmax(self.out_layer(x), dim = 1)
    


def select_action(policy, state):
    
    probs = policy(state)
    m = Categorical(probs)
    action = m.sample()
    policy.saved_log_probs.append(m.log_prob(action))
    return action.item()

def finish_episode(policy, optimizer, eps):
    R = 0
    policy_loss = []
    returns = []
    for r in policy.rewards[::-1]:
        R = r + gamma * R
        returns.insert(0, R)
    returns = torch.tensor(returns)
    returns = (returns - returns.mean()) / (returns.std() + eps)
    for log_prob, R in zip(policy.saved_log_probs, returns):
        policy_loss.append(-log_prob * R)
    optimizer.zero_grad()
    policy_loss = torch.cat(policy_loss).sum()
    policy_loss.backward()
    optimizer.step()
    del policy.rewards[:]
    del policy.saved_log_probs[:]


        


policy = Policy()
optimizer = optim.Adam(policy.parameters(), lr=1e-2)
eps = np.finfo(np.float32).eps.item()