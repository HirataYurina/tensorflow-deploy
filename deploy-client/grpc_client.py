# -*- coding:utf-8 -*-
# author:平手友梨奈ii
# e-mail:1353593259@qq.com
# datetime:1993/12/01
# filename:grpc_client.py
# software: PyCharm

import grpc
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

options = [('grpc.max_send_message_length', 1000 * 1024 * 1024),
           ('grpc.max_receive_message_length', 1000 * 1024 * 1024)]

channel = grpc.insecure_channel('ip', options=options)

stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

(_, _), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_test = tf.reshape(x_test, (10000, -1))
# print(x_test)
x_test = tf.cast(x_test, dtype=tf.float32)
x_test = (x_test - 127.5) / 127.5

request = predict_pb2.PredictRequest()
request.model_spec.name = "yoloV3"
request.model_spec.signature_name = 'serving_default'
request.inputs['input_1'].CopyFrom(tf.make_tensor_proto(x_test[:20], shape=(20, 784)))
response = stub.Predict(request, 10.0)
output = tf.make_ndarray(response.outputs['dense_2'])
output = tf.argmax(output, axis=-1)
print(output)
print(y_test[:20])
