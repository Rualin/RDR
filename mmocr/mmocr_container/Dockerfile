# syntax=docker/dockerfile:1

FROM pytorch/pytorch:1.12.0-cuda11.3-cudnn8-devel

RUN apt-get update && apt-get install -y git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

RUN pip install -U openmim==0.3.9
RUN mim install mmengine==0.10.6
RUN pip install mmcv==2.1.0 -f https://download.openmmlab.com/mmcv/dist/cu113/torch1.12/index.html
RUN mim install mmdet==3.3.0
RUN git clone https://github.com/open-mmlab/mmocr.git /mmocr
WORKDIR /mmocr
ENV FORCE_CUDA="1"
RUN pip install -v -e .
RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -e .
RUN pip install -r requirements/albu.txt