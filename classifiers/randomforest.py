#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

from sklearn.ensemble import RandomForestClassifier
import universal
import sys

if len(sys.argv) >= 2 and sys.argv[1] == "ta":
    X_train, X_test, Y_train, Y_test = universal.sklearn_ta()
else:
    X_train, X_test, Y_train, Y_test = universal.sklearn()

clf = RandomForestClassifier(n_estimators=128,
                             n_jobs=-1).fit(X_train, Y_train)

universal.conclude_skl(clf, X_test, Y_test)
