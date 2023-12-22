FROM runpod/pytorch:2.0.1-py3.10-cuda11.8.0-devel-ubuntu22.04
WORKDIR /diffusion
COPY diffusers ./diffusers
COPY Stable-Diffusion-Regularization-Images-person_ddim ./Stable-Diffusion-Regularization-Images-person_ddim
COPY handler.py handler.py
COPY training.py training.py
RUN cd diffusers && pip install -e . && \
    pip install bitsandbytes scipy runpod tqdm olefile && \
    pip install -r examples/dreambooth/requirements.txt
RUN cd diffusers/examples/dreambooth && accelerate config default
CMD ["python3.10", "handler.py"]
