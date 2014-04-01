#!/usr/bin/python
# coding: utf-8

import numpy as np
import scipy as sp
from pylab import *
import bayesian_kalmanfilter as bkf

if __name__ == '__main__':
    # 初期化
    T = 40000 # 観測数
    N = 2 # the number of variational iterations
    x = np.mat([[0],[0]]) # 初期位置
    X = [x] # 状態
    Y = [np.mat([[0],[0]])] # 観測
 
    # state x = A * x_ + B * u + w, w~N(0,Q)
    A = np.mat([[1,0],[0,1]])
    B = np.mat([[1,0],[0,1]])
    u = np.mat([[1],[1]])
    Q = np.mat([[1,0],[0,1]])

    # observation Y = C * x + v, v~N(0,R)
    C = np.mat([[1,0],[0,1]])
    R = np.mat([[10,0],[0,10]])

    # hyper parameters
    alpha = np.mat([[1],[1]])
    beta = np.mat([[1],[1]])
    rho = np.mat([[1-exp(-4)],[1-exp(-4)]])

    # 観測データの生成
    for i in range(T):
        if i >= T/4:
            R = np.mat([[0.2,0],[0,0.2]])
        if i >= 3*T/4:
            R = np.mat([[5.0,0],[0,5.0]])
        x = A * x + B * u + np.random.multivariate_normal([0,0],Q,1).T
        X.append(x)
        y = C * x + np.random.multivariate_normal([0,0],R,1).T
        Y.append(y)
    
    # initial value
    mu = np.mat([[0],[0]])
    Sigma = np.mat([[0.0,0.0],[0.0,0.0]])    
    M = [mu] # 状態推定の結果
    V = [np.divide(beta, alpha)] # 分散推定の結果

    # bayesian variational kalman filter
    bkf = bkf.BayesianKalmanFilter(A,B,u,Q,C,alpha,beta,rho,mu,Sigma,N)
    for i in range(T):
        mu,Sigma,obs_var = bkf.update(Y[i+1])
        M.append(mu)
        V.append(obs_var)
        print i,float(obs_var[0])
        
    # 描画
    subplot(311)
    a,b = np.array(np.concatenate(X,axis=1))
    plot(a,b,'r-')
    a,b = np.array(np.concatenate(M,axis=1))
    plot(a,b,'b--')
    a = np.array(np.concatenate(V,axis=1))
    subplot(312)
    plot(a[0], 'b-')
    subplot(313)
    plot(a[1], 'b-')
    
    show()
    
