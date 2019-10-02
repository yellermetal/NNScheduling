#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 10:13:32 2019

@author: ariell
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical


gamma = 1

def init_weights(m):
    if type(m) == nn.Linear:
        torch.nn.init.xavier_uniform(m.weight)
        m.bias.data.fill_(0.01)
        
        
class Normalizer():
    def __init__(self, num_inputs):
        self.n = torch.zeros(num_inputs)
        self.mean = torch.zeros(num_inputs)
        self.mean_diff = torch.zeros(num_inputs)
        self.var = torch.zeros(num_inputs)

    def observe(self, x):
        self.n += 1.
        last_mean = self.mean.clone()
        self.mean += (x-self.mean)/self.n
        self.mean_diff += (x-last_mean)*(x-self.mean)
        self.var = torch.clamp(self.mean_diff/self.n, min=1e-2)

    def normalize(self, inputs):
        obs_std = torch.sqrt(self.var)
        return (inputs - self.mean)/obs_std

class Policy(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(Policy, self).__init__()
        
        self.in_layer = nn.Linear(input_size, hidden_size)        
        self.hidden_layer_1 = nn.Linear(hidden_size, hidden_size) 
        self.hidden_layer_2 = nn.Linear(hidden_size, hidden_size) 
        self.out_layer = nn.Linear(hidden_size, 2)
        
        self.saved_log_probs = []
        self.rewards = []
        
        self.apply(init_weights)
        
    def forward(self, state):
        
        normalizer = Normalizer(len(state))
        normalizer.observe(state)
        new_state = normalizer.normalize(state)
        
        new_state = F.relu(self.in_layer(new_state))
        new_state = F.relu(self.hidden_layer_1(new_state))
        new_state = F.relu(self.hidden_layer_2(new_state))
        return F.softmax(self.out_layer(new_state), dim=0)
    
    


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
    policy_loss = torch.stack(policy_loss).sum()
    policy_loss.backward()
    optimizer.step()
    del policy.rewards[:]
    del policy.saved_log_probs[:]


        
'''
input_size = 4
hidden_size = 4

policy = Policy(input_size, hidden_size)
optimizer = optim.Adam(policy.parameters(), lr=1e-2)
eps = np.finfo(np.float32).eps.item()
'''