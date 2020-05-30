# -*- coding:utf-8 -*-
# author:平手友梨奈ii
# e-mail:1353593259@qq.com
# datetime:1993/12/01
# filename:mnist_model_version2.py
# software: PyCharm

import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import tensorflow as tf


def mnist_model_v2():
    inputs = keras.Input(shape=(784,))
    x = layers.Dense(120)(inputs)
    # x = layers.Activation(tf.nn.swish)(x)
    x = layers.Lambda(lambda y: tf.nn.swish(y))(x)

    x = layers.Dense(100)(x)
    x = layers.ReLU()(x)

    x = layers.Dense(10)(x)
    x = layers.Softmax()(x)

    model = keras.Model(inputs, x)

    return model


def get_data():
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    # preprocess data
    x_train = tf.reshape(x_train, shape=(-1, 784))
    x_train = (tf.cast(x_train, tf.float32) - 127.5) / 127.5
    x_test = tf.reshape(x_test, (-1, 784))
    x_test = (tf.cast(x_test, tf.float32) - 127.5) / 127.5

    return [x_train, y_train, x_test, y_test]


if __name__ == '__main__':

    model_v2 = mnist_model_v2()
    # model_v2.summary()
    model_v2.compile(optimizer=keras.optimizers.RMSprop(),
                     loss=keras.losses.SparseCategoricalCrossentropy(),
                     metrics=[keras.metrics.SparseCategoricalAccuracy()])

    # get train data
    x_train, y_train, x_test, y_test = get_data()

    # start training
    model_v2.fit(x_train, y_train, batch_size=8, epochs=1, validation_split=0.1, verbose=2)

    # save model
    model_v2.save('./checkpoint/2', save_format='tf')