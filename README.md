# Tensorflow Deployment
I use *Tensorflow Serving*, *Tensorflow Lite Model*, *TensorRT Quantization* to deploy my project.
___
#### Content
1. **Tensorflow Serving**
2. **Tensorflow Lite Model**
3. **TensorRT Quantization**

#### 1 Tensorflow Serving

---


#### 2 Tensorflow Lite Model

---

#### 3 TensorRT Quantization
##### 3.1 what is TensorRT?
TensorRT is an inference frame(engine) that can accelerate model(about 4 times). TensorRT belongs to nvidia, so you must use CUDA and nvidia card. If you don't use GPU to infer you can use openvino provided by Intel.

| Model  | TensorRT-Precision |  Device   | Resolution |  FPS   |
| :----: | :----------------: | :-------: | :--------: | :----: |
| YOLOv4 |         No         | TeslaV100 |    416     | 86fps  |
| YOLOv4 |        INT8        | TeslaV100 |    416     | 250fps |

##### 3.2 what is TensorRT doing?
* Quantization
  Exchange fp32 model to fp16 or int8 to speed up model.

  **why we need to quantize model?**

  

  **why quantization can work in neural network?**

  

  **How does TensorRT quantize model?**

  

*  Architecture Optimization
**Prune model automatically and dicard neurons that are not important.**
**Merge Conv2D, BN and ReLU together.**
**Merge same shape layers.**
**Do not use concat layer rather than feed the inputs into next layer directly.**

##### 3.3 How to use TensorRT?
* Environment
**Ubuntu16.04**(Windows is not recommended because two points. First, there are no python API in windows zip package and you can only use c++ to use tensorRT in windows. Second, tensorflow API for tensorRT does not support windows.)
**python3.7**
**tensorRT-6.0.1.5**
**tensorflow2.3.0**
**CUDA-10.1**
**CUDNN-7.6.5**
* Installation
* create conda virtual environment:
```
conda create --name python37 python=3.7
```
* install tensorflow

```
conda activate python37
pip install tensorflow==2.3.0
```
* easily install CUDA-10.1 AND CUDNN=7.6.5

```
conda install cudatoolkit=10.1
conda install cudnn=7.6.5
```
* install tensorRT
  * use tar package to install tensorRT

```
# decompress
tar xzvf TensorRT.tar.gz -C {your work directory}
# add tensorRT lib path to environment variable LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:TensorRT-6.0.1.5/lib
# install tensorRT whell file
pip install tensorrt-6.0.1.5-cp37-none-linux_x86_64.whl
# install uff whell file
pip install uff-0.6.5-py2.py3-none-any.whl
# install graphsurgeon whell file
pip install graphsurgeon-0.4.1-py2.py3-none-any.whl
```

* use tensorflow API to convert saved_model
  your need to save the model with saved_model format.
  |--- assets
  |--- saved_model.pb
  |--- variables
```shell
python tf2trt.py --precision "INT8" --model_path "./saved_model"
```

```python
from tensorflow.python.compiler.tensorrt import trt_convert as trt

def convert(saved_model_file):
	print('Converting to TF-TRT FP32...')
	conversion_params = trt.DEFAULT_TRT_CONVERSION_PARAMS._replace(precision_mode=trt.TrtPrecisionMode.FP32,                                                                    max_workspace_size_bytes=8000000000)
    converter = trt.TrtGraphConverterV2(input_saved_model_dir=saved_model_file,                         ·		                                    conversion_params=conversion_params)
    converter.convert()
    converter.save(output_saved_model_dir='saved_model_TFTRT_FP32')
    print('Done Converting to TF-TRT FP32')
```

