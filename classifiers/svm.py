#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

# Had to switch to LinearSVC because regular is far too slow
from sklearn.svm import LinearSVC
import sys
import universal

if len(sys.argv) >= 2 and sys.argv[1] == "ta":
    X_train, X_test, Y_train, Y_test = universal.sklearn_ta()
else:
    X_train, X_test, Y_train, Y_test = universal.sklearn()

clf = LinearSVC(tol=0.00000001).fit(X_train, Y_train)

universal.conclude_skl(clf, X_test, Y_test)
