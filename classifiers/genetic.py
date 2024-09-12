#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import pygad as pg
import pygad.kerasga
from keras import losses, layers, models, metrics
import universal
import sys

X_train, X_test, Y_train, Y_test = universal.tensorflow()

def fitness(_ga, sol, _sol_idx) -> float:
    global X_test, Y_test, clf, kga
    preds = pygad.kerasga.predict(model=clf,
                                  solution=sol,
                                  data=X_test)
    bce = losses.BinaryCrossentropy(from_logits=True)
    loss = bce(Y_test, preds).numpy() + 0.00000001
    return 1.0/loss

def cycle(ga):
    print(f"gen={ga.generations_completed},fit={ga.best_solution()[1]}")

clf = models.Sequential()
clf.add(layers.Dense(950, activation="relu", input_shape=(1500,)))
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
kga = pg.kerasga.KerasGA(model=clf, num_solutions=400)
ga = pygad.GA(num_generations=1,
              num_parents_mating=100,
              initial_population=kga.population_weights,
              fitness_func=fitness,
              on_generation=cycle)
ga.run()
z=ga.best_solution()
print(f"fitness final: {fitness(ga,z[0],z[2])}")
universal.conclude_tensorflow(clf, X_test, Y_test)
