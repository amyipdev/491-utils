#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import numpy as np
import os
from sklearn.model_selection import train_test_split

def uniload() -> (list[bytes], list[bytes]):
    X = []
    Y = []
    for p in os.listdir("../translator/postacc/"):
        with open("../translator/postacc/" + p, "rb") as f:
            X.append(f.read())
            Y.append(1)
    for p in os.listdir("./randoms"):
        with open("./randoms/" + p, "rb") as f:
            X.append(f.read())
            Y.append(0)
    return (X, Y)

def uni() -> (list[bytes], list[bytes]):
    X, Y = uniload()
    Xa = [[0 for _ in range(1500)] for __ in X]
    for i, a in enumerate(X):
        for k, b in enumerate(a):
            Xa[i][k] = b
    return (np.array(Xa), np.array(Y))

def uni_ta() -> (list[bytes], list[bytes]):
    X, Y = uniload()
    Xa = [[0 for _ in range(150000)] for __ in range(len(X)//100)]
    Ya = []
    for n in range(len(X)//100):
        for o in range(100):
            for i, p in enumerate(X[n*100+o]):
                Xa[n][o*1500+i] = p
        if sum(Y[n*100:(n+1)*100]) >= 50:
            Ya.append(1)
        else:
            Ya.append(0)
    return (np.array(Xa), np.array(Ya))

def sklearn() -> (np.array, np.array, np.array, np.array):
    X, Y = uni()
    return train_test_split(X, Y, shuffle=True)

def sklearn_ta() -> (np.array, np.array, np.array, np.array):
    X, Y = uni_ta()
    return train_test_split(X, Y, shuffle=True)

def tensorflow() -> (np.array, np.array, np.array, np.array):
    Xa, Xb, Ya, Yb = sklearn()
    return (np.array(Xa[..., None]),
            np.array(Xb[..., None]),
            np.array(Ya[..., None]),
            np.array(Yb[..., None]))

def conclude_skl(model, X_test, Y_test):
    tp, fp, fn, tn = 0,0,0,0
    preds = model.predict(X_test)
    for i, a in enumerate(preds):
        if Y_test[i] == 1:
            if a == 1: tp += 1
            else: fn += 1
        else:
            if a == 1: fp += 1
            else: tn += 1
    # TODO: loss
    print(f"TP={tp},FP={fp},TN={tn},FN={fn}")
    print(f"Accuracy={(tp+tn)/(tp+tn+fp+fn)}")
    print(f"Precision={tp/(tp+fp)}")
    print(f"Recall={tp/(tp+fn)}")
    print(f"F1={2*tp/(2*tp+fp+fn)}")
    print(f"CollateralDamage={fp/(fp+tn)}")

def conclude_tensorflow(model, X_test, Y_test):
    res = model.evaluate(X_test, Y_test)
    print(f"Loss={res[0]}")
    print(f"Accuracy={res[1]}")
    print(f"Precision={res[2]}")
    print(f"Recall={res[3]}")
    print(f"F1={res[4]}")
    print(f"CollateralDamage={((1-res[2])*res[3])/((1-res[2])*res[3]+(1-res[3])*res[2])}")
