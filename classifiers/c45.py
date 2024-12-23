#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

from sklearn.tree import DecisionTreeClassifier
import universal
import timeit

X_train, X_test, Y_train, Y_test = universal.sklearn()
clf = DecisionTreeClassifier().fit(X_train, Y_train)

universal.conclude_skl(clf, X_test, Y_test)

# benchmark
print("benchmarking...")
t=timeit.timeit(lambda: clf.predict(X_test), number=10)
print(f"result: {(10*len(X_test))/t} pkt/s")
