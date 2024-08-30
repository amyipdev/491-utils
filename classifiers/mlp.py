#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

from sklearn.neural_network import MLPClassifier
import universal
import sys

if len(sys.argv) >= 2 and sys.argv[1] == "ta":
    X_train, X_test, Y_train, Y_test = universal.sklearn_ta()
else:
    X_train, X_test, Y_train, Y_test = universal.sklearn()

clf = MLPClassifier(hidden_layer_sizes=(950,950,950),
                    verbose=True,
                    max_iter=300,
                    tol=0.000000001).fit(X_train, Y_train)
tp, fp, fn, tn = 0, 0, 0, 0
preds = clf.predict(X_test)
for i, a in enumerate(preds):
    if Y_test[i] == 1:
        if a == 1: tp += 1
        else: fn += 1
    else:
        if a == 1: fp += 1
        else: tn += 1
print(f"TP={tp},FP={fp},TN={tn},FN={fn}")
