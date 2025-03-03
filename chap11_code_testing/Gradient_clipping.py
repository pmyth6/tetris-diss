#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 18:17:47 2024

@author: theahellen
"""

import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

housing = fetch_california_housing()

X_train_full, X_test, y_train_full, y_test = train_test_split(
    housing.data, housing.target)
X_train, X_valid, y_train, y_valid = train_test_split(
    X_train_full, y_train_full)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_valid = scaler.transform(X_valid)
X_test = scaler.transform(X_test)

model = keras.models.Sequential([
    keras.layers.Dense(30, input_shape=X_train.shape[1:], activation="elu",
                       kernel_initializer="he_normal"),
    keras.layers.Dense(1)
    ])


#This optimizer will clip every component of the gradient vector to a value between –1.0 and 1.0
optimizer = keras.optimizers.SGD(clipvalue=1.0)

model.compile(loss="mean_squared_error", optimizer=optimizer, metrics=["accuracy"])
history = model.fit(X_train, y_train, epochs=20,
                    validation_data=(X_valid, y_valid))
mse_test = model.evaluate(X_test, y_test)
X_new = X_test[:3] #pretend these are new instances
y_pred = model.predict(X_new)


print(y_pred)

y_new = y_test[:3]
print(y_new) #shows the answer