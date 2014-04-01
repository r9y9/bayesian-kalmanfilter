#!/usr/bin/python
# coding: utf-8

import numpy as np
import scipy as sp
from pylab import *

class KalmanFilter:
    def __init__(self, A, B, u, Q, H, R, mu, Sigma):
        # parameters for linear state space model
        # state: x = A*x_ + B*u + w, w ~ N(0,Q)
        # observation: Y = H*x + v, v ~ N(0,R)
        self.A = A
        self.B = B
        self.u = u
        self.Q = Q
        self.H = H
        self.R = R
        # initialize
        self.mu = mu
        self.Sigma = Sigma
    
    def update(self, y):
        # 1. prediction step
        mu_ = self.A * self.mu + self.B * self.u
        Sigma_ = self.Q + self.A * self.Sigma * self.A.T
        # 2. correction step
        error = y - self.H * mu_
        S = self.H * Sigma_ * self.H.T + self.R
        K = Sigma_ * self.H.T * S.I
        self.mu = mu_ + K * error
        self.Sigma = Sigma_ - K * self.H * Sigma_

        return self.mu,self.Sigma
