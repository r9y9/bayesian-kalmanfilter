#!/usr/bin/python
# coding: utf-8

import numpy as np
import scipy as sp
from pylab import *
import kalmanfilter as kf

if __name__ == '__main__':
    # 初期化
    T = 30 # 観測数
    x = np.mat([[0],[0]]) # 初期位置
    X = [np.mat([[0],[0]])] # 状態
    Y = [np.mat([[0],[0],[0]])] # 観測
 
    # state x = A * x_ + B * u + w, w~N(0,Q)
    A = np.mat([[1,0],[0,1]])
    B = np.mat([[1,0],[0,1]])
    u = np.mat([[2],[2]])
    Q = np.mat([[1,0],[0,1]])

    # observation Y = C * x + v, v~N(0,R)
    C = np.mat([[1,0],[0,1]])
    R = np.mat([[2,0],[0,2]])

    # 観測データの生成
    for i in range(T):
        x = A * x + B * u + np.random.multivariate_normal([0,0],Q,1).T
        X.append(x)
        y = C * x + np.random.multivariate_normal([0,0],R,1).T
        Y.append(y)
    
    # initialize
    mu = np.mat([[0],[0]])
    Sigma = np.mat([[0,0],[0,0]])    
    M = [mu] # 推定

    # Kalman filter
    kf = kf.KalmanFilter(A, B, u, Q, C, R, mu, Sigma)
    for i in range(T):
        mu,Sigma = kf.update(Y[i+1])
        M.append(mu)

    # 描画
    a,b = np.array(np.concatenate(X,axis=1))
    plt.plot(a,b,'rs-')
    a,b = np.array(np.concatenate(M,axis=1))
    plt.plot(a,b,'bo-')
    #plt.axis('equal')
    xlabel("sample")
    plt.show()
