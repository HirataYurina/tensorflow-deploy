import tensorflow as tf
from tensorflow.python.compiler.tensorrt import trt_convert as trt
from argparse import ArgumentParser
from PIL import Image
import os
import numpy as np

# converter = tf.experimental.tensorrt.Converter()


def parser():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--precision', type=str, required=True)
    arg_parser.add_argument('--model_path', type=str, required=True)
    arg_parser.add_argument('--input_shape', type=tuple, default=(416, 416))
    arg_parser.add_argument('--img_path', type=str, default='./calibration_img')
    return arg_parser.parse_args()


auguments = parser()
precision = auguments.precision
model_path = auguments.model_path
input_shape = auguments.input_shape
img_path = auguments.img_path


def letterbox_image(image, size):
    iw, ih = image.size
    w, h = size
    scale = min(w / iw, h / ih)
    nw = int(iw * scale)
    nh = int(ih * scale)

    image = image.resize((nw, nh), Image.BICUBIC)
    new_image = Image.new('RGB', size, (128, 128, 128))
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))
    return new_image


def calibrate_data_gen():
    data_dir = img_path
    names = [os.path.join(data_dir, name) for path, _, file_names in os.walk(data_dir) for name in file_names]
    # print(names)
    for name in names:
        image = Image.open(name)
        image = letterbox_image(image, input_shape)
        image_array = np.expand_dims(np.array(image) / 255.0, axis=0)
        image_constant = tf.constant(image_array, dtype=tf.float32)
        yield (image_constant,)


def convert():
    if not (precision in ['FP32', 'FP16', 'IMT8']):
        raise ValueError('precision must be FP32, FP16 or INT8')

    if precision == 'FP32':
        print('Converting to TF-TRT FP32...')
        conversion_params = trt.DEFAULT_TRT_CONVERSION_PARAMS._replace(precision_mode=trt.TrtPrecisionMode.FP32,
                                                                       max_workspace_size_bytes=8000000000)

        converter = trt.TrtGraphConverterV2(input_saved_model_dir=model_path,
                                            conversion_params=conversion_params)
        converter.convert()
        converter.save(output_saved_model_dir='saved_model_TFTRT_FP32')
        print('Done Converting to TF-TRT FP32')

    if precision == 'FP16':
        print('Converting to TF-TRT FP32...')
        conversion_params = trt.DEFAULT_TRT_CONVERSION_PARAMS._replace(precision_mode=trt.TrtPrecisionMode.FP16,
                                                                       max_workspace_size_bytes=8000000000)

        converter = trt.TrtGraphConverterV2(input_saved_model_dir=model_path,
                                            conversion_params=conversion_params)
        converter.convert()
        converter.save(output_saved_model_dir='saved_model_TFTRT_FP16')
        print('Done Converting to TF-TRT FP16')

    if precision == 'INT8':
        print('Converting to TF-TRT INT8...')
        conversion_params = trt.DEFAULT_TRT_CONVERSION_PARAMS._replace(precision_mode=trt.TrtPrecisionMode.INT8,
                                                                       max_workspace_size_bytes=8000000000,
                                                                       use_calibration=True)

        converter = trt.TrtGraphConverterV2(input_saved_model_dir=model_path,
                                            conversion_params=conversion_params)
        # need to calibrate representative data
        converter.convert(calibration_input_fn=calibrate_data_gen)
        converter.save(output_saved_model_dir='saved_model_TFTRT_INT8')
        print('Done Converting to TF-TRT INT8')


if __name__ == '__main__':
    convert()
