#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import tensorflow as tf
from keras import losses, layers, models, metrics
import universal

# TODO: TA port
X_train, X_test, Y_train, Y_test = universal.tensorflow()
print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)

clf = models.Sequential()
clf.add(layers.Dense(950, input_shape=(1500,)))
clf.add(layers.Dense(950, activation="relu"))
clf.add(layers.Dense(950, activation="relu"))
clf.add(layers.Dense(1, activation="sigmoid"))
clf.compile(optimizer="adam",
            loss=losses.BinaryCrossentropy(from_logits=True),
            metrics=['accuracy',
                     'precision',
                     'recall',
                     metrics.F1Score])
clf.summary()
clf.fit(X_train, Y_train, epochs=500, validation_data=(X_test, Y_test))
universal.conclude_tensorflow(clf, X_test, Y_test)
