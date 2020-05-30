# -*- coding:utf-8 -*-
# author:平手友梨奈ii
# e-mail:1353593259@qq.com
# datetime:1993/12/01
# filename:grpc_client_alias.py
# software: PyCharm


import grpc
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
import tensorflow as tf


channel = grpc.insecure_channel('ip')

stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

(_, _), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_test = tf.reshape(x_test, (10000, -1))
# print(x_test)
x_test = tf.cast(x_test, dtype=tf.float32)
x_test = (x_test - 127.5) / 127.5

# use version to control my model
request = predict_pb2.PredictRequest()
request.model_spec.name = "mlp"
request.model_spec.signature_name = 'serving_default'

# add alias
request.model_spec.version.value = 1

request.inputs['input_1'].CopyFrom(tf.make_tensor_proto(x_test[:20], shape=(20, 784)))
response = stub.Predict(request, 10.0)
output = tf.make_ndarray(response.outputs['dense_2'])
output = tf.argmax(output, axis=-1)
print(output)
