# The Sequential model

**Author:** fchollet  
**Date created:** 2020/04/12  
**Last modified:** 2023/06/25

[:simple-googlecolab: Run in Google Colab](https://colab.research.google.com){ .md-button }
[:simple-github: View source on GitHub](https://github.com){ .md-button }
[:simple-keras: View on keras.io](https://keras.io){ .md-button }

## Setup

Aqui você importa as bibliotecas necessárias para começar.

```python
import keras
from keras import layers
from keras import ops
``` 

## When to use a Sequential model

A `Sequential` model is appropriate for **a plain stack of layers** 
where each layer has **exactly one input tensor and one output tensor**.

Schematically, the following `Sequential` model:

```python
model = keras.Sequential([
    layers.Dense(2, activation="relu"),
    layers.Dense(3, activation="relu"),
])