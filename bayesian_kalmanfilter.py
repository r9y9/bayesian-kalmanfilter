#!/usr/bin/python
# coding: utf-8

import numpy as np
import scipy as sp
from pylab import *

# A variational bayesian kalman filter algorithm based on 
# "Recursive Noise Adaptive Kalman Filtering 
# by Variational Bayesian Approximations",
# http://www.lce.hut.fi/~ssarkka/pub/vb-akf-ieee.pdf

# state: x = A*x_ + B*u + w, w ~ N(0,Q)
# observation: Y = H*x + v, v ~ N(0,Sigma)
# Sigma ~ Inv-Gamma(alpha,beta)
# Assuming Sigma is a diagonal matrix.
class BayesianKalmanFilter:
    def __init__(self, A, B, u, Q, H, alpha, beta, rho, mu, Sigma, N=2):
        self.__init_lssm(A, B, u, Q, H)
        self.__init_hyper_parameters(alpha, beta)
        self.__init_state(mu, Sigma)
        # heuristic parameter
        self.rho = rho
        # the number of variational iterations
        self.N = N

    def __init_lssm(self, A, B, u, Q, H):
        # parameters for linear state space model (LSSM)
        self.A = A
        self.B = B
        self.u = u
        self.Q = Q
        self.H = H

    def __init_hyper_parameters(self, alpha, beta):
        # hyper parameters of Inv-Gamma
        self.alpha = alpha
        self.beta = beta

    def __init_state(self, mu, Sigma):
        # parameters of Gaussian
        self.mu = mu
        self.Sigma = Sigma

    def update(self, y):
        # 1. prediction
        mu_ = self.A * self.mu + self.B * self.u
        Sigma_ = self.Q + self.A * self.Sigma * self.A.T
        alpha_ = np.multiply(self.alpha, self.rho)
        beta_ = np.multiply(self.beta, self.rho)

        # 2. variational posteriori update
        # 論文に書いては以下のようにあるけど上手く行かなかったので変更
        #alpha_k = alpha_ + 0.5 
        alpha_k = alpha_
        beta_k = beta_
        for iter in range(self.N):
            # update for N(mu,Sigma)
            tmp = np.squeeze(np.asarray(np.divide(beta_k, alpha_k)))
            Sigma_k = np.mat(np.diag(tmp))
            yi = y - self.H * mu_
            S = self.H * Sigma_ * self.H.T + Sigma_k
            K = Sigma_ * self.H.T * S.I
            self.mu = mu_ + K * yi
            self.Sigma = Sigma_ - K * self.H * Sigma_

            # update for Inv-Gamma(alpha,beta)
            yii = y - self.H * self.mu
            SS = self.H * self.Sigma * self.H.T
            # alpha, betaともにiter毎に更新するように変更
            alpha_k = alpha_k + 0.5
            for i in range(len(self.beta)):
                # 論文の実装
                #beta_k[i] = beta_[i] + 0.5 * yii[i] * yii[i] + 0.5 * SS[i,i]
                beta_k[i] = beta_k[i] + 0.5 * yii[i] * yii[i] + 0.5 * SS[i,i]
        self.alpha = alpha_k
        self.beta = beta_k

        return self.mu,self.Sigma,np.divide(self.beta, self.alpha)
