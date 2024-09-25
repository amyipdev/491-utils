#!/usr/bin/env python3

import scipy
import math
import os

ALPHA = 0.01

X = []
for p in os.listdir("../translator/postacc/"):
    with open("../translator/postacc/" + p, "rb") as f:
        X.append(f.read())
Z = []
for p in os.listdir("../collector/captures/"):
    with open("../collector/captures/" + p, "rb") as f:
        Z.append(f.read())

def convert_list(l: list[bytes]) -> list[(float, int)]:
    res = []
    for el in l:
        bc = len(el)*8
        ax = sum(n.bit_count() for n in el)
        res.append((ax/bc, bc))
    return res

def gtz(i: (float, int)) -> float:
    return math.sqrt(i[0]*(1-i[0])/i[1])

Ya = convert_list(X)
del X
Yb = convert_list(Z)
del Z

tp,fp,tn,fn=0,0,0,0
for pset in Ya:
    z = gtz(pset)
    pv = scipy.stats.norm.cdf(z) - scipy.stats.norm.cdf(-z)
    if pv <= ALPHA: fn += 1
    else: tp += 1
for pset in Yb:
    z = gtz(pset)
    pv = scipy.stats.norm.cdf(z) - scipy.stats.norm.cdf(-z)
    if pv <= ALPHA: tn += 1
    else: fp += 1

print(f"TP={tp},FP={fp},TN={tn},FN={fn}")
print(f"Accuracy={(tp+tn)/(tp+tn+fp+fn)}")
print(f"Precision={tp/(tp+fp)}")
print(f"Recall={tp/(tp+fn)}")
print(f"F1={2*tp/(2*tp+fp+fn)}")
print(f"CollateralDamage={fp/(fp+tn)}")
