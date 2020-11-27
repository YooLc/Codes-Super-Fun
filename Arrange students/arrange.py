# Find a approximate solution to satisfy most students 
# by Simulated Annealing Algorithm
# Author: YooLc

import numpy as np
import math
import matplotlib.pyplot as plt
from random import randint

def CantorExpansion(A):
    n = len(A)
    rank = 0
    for i in range(n):
        cnt = 0
        for j in range(i + 1, n):
            if A[j] < A[i]:
                cnt = cnt + 1
        rank = rank + cnt * math.factorial(n - i - 1)
    return rank + 1

def revCantorExpansion(k, n):
    assert k <= math.factorial(n), 'k must not exceed n!'
    A = []
    remain = list(range(1, n + 1))
    r = 0
    nr = k - 1
    for i in reversed(range(n)):
        r = nr // math.factorial(i)
        nr = nr % math.factorial(i)
        A.append(remain[r])
        remain.remove(A[-1])
    return A

def order(A, row, col):
    return np.array(A).reshape(row, col)

row = 6
col = 7

def score(A, q):
    A = order(A, row, col)
    # print(A)
    score = 0
    for pair in q:
        pos1 = np.where(A == pair[0])
        pos2 = np.where(A == pair[1])
        if pos1[0] == pos2[0] and abs(pos1[1] - pos2[1]) == 1: # Check adjancency
            score = score + 1
    return score

require = []
for i in range(1, row * col - 1):
    require.append((i, i + 2))

def findByFate():
    scoremax = 0
    maxid = 0
    for i in range(10000):
        t = randint(1, math.factorial(row * col))
        s = score(revCantorExpansion(t, row * col), require)
        if scoremax < s:
            maxid = t
            scoremax = s
    print("Found", maxid, "th arrangement, score:", scoremax)
    print(order(revCantorExpansion(maxid, row * col), row, col))

def findBySAA():
    eps = 0.9
    delta = 0.999
    lim = math.factorial(row * col)
    T = lim // 2
    x = lim // 2
    scoreNow = score(revCantorExpansion(x, row * col), require)
    maxscore = 0
    maxid = 0
    while T > eps:
        f = ([-1, 1])[randint(0, 1)]
        nx = int(x + f * T)
        if nx >= 0 and nx <= lim:
            scoreNext = score(revCantorExpansion(nx, row * col), require)
            if scoreNext >= maxscore:
                maxscore = scoreNext 
                maxid = nx
            if scoreNow - scoreNext > eps:
                x = nx 
                scoreNow = scoreNext
        T = T * delta
    print("Found", maxid, "th arrangement, score:", maxscore)
    print(order(revCantorExpansion(maxid, row * col), row, col))
    print("Rate: ", maxscore / len(require))

findByFate()
findBySAA()

# Plot
# lim = math.factorial(row * col)
# x = []
# y = []
# for i in range(1, lim + 1):
#     x.append(i)
#     y.append(score(revCantorExpansion(i, row * col), require))

# plt.plot(x, y)
# plt.show()
