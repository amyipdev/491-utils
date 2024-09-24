#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import tensorflow as tf
from keras import losses, layers, models, metrics
import universal

X_train, X_test, Y_train, Y_test = universal.tensorflow()
input_shape = (1500,1)

clf = models.Sequential()
clf.add(layers.Conv1D(1500, 32, activation="relu", input_shape=input_shape))
clf.add(layers.MaxPooling1D((5,)))
clf.add(layers.Conv1D(128, 32, activation="relu"))
clf.add(layers.MaxPooling1D((5,)))
clf.add(layers.Conv1D(128, 32, activation="relu"))
clf.add(layers.MaxPooling1D((5,)))
clf.add(layers.Flatten())
clf.add(layers.Dense(128, activation="relu"))
clf.add(layers.Dense(1, activation="sigmoid"))
clf.compile(optimizer="adam",
            loss=losses.BinaryCrossentropy(from_logits=True),
            metrics=['accuracy',
                     'precision',
                     'recall',
                     metrics.F1Score])
clf.summary()
clf.fit(X_train, Y_train, epochs=100, validation_data=(X_test, Y_test))
universal.conclude_tensorflow(clf, X_test, Y_test)
