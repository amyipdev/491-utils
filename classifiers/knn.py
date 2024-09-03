#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

from sklearn.neighbors import KNeighborsClassifier
import math
import universal

X_train, X_test, Y_train, Y_test = universal.sklearn()
clf = KNeighborsClassifier(n_neighbors=int(math.sqrt(len(Y_train))),
                           n_jobs=-1).fit(X_train, Y_train)

universal.conclude_skl(clf, X_test, Y_test)
