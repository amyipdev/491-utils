#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import tensorflow as tf
from keras import losses, layers, models, metrics
import universal
import sys

if len(sys.argv) >= 2 and sys.argv[1] == "ta":
    X_train, X_test, Y_train, Y_test = universal.sklearn_ta()
else:
    X_train, X_test, Y_train, Y_test = universal.sklearn()

clf = models.Sequential()
clf.add(layers.Embedding(input_dim=1500,output_dim=1500,input_shape=(1500,)))
clf.add(layers.Bidirectional(layers.LSTM(500)))
clf.add(layers.Dense(1, activation="sigmoid"))
clf.compile(optimizer="adam",
            loss=losses.BinaryCrossentropy(from_logits=True),
            metrics=['accuracy',
                     'precision',
                     'recall',
                     metrics.F1Score])
clf.summary()
clf.fit(X_train, Y_train, epochs=1, validation_data=(X_test, Y_test))
universal.conclude_tensorflow(clf, X_test, Y_test)
