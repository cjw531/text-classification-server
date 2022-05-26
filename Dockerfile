FROM jchoi531/textcls:latest

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

RUN pip3 uninstall tensorflow absl-py astunparse flatbuffers gast google-pasta grpcio h5py keras keras-preprocessing libclang numpy opt-einsum protobuf setuptools six tensorboard tensorflow-io-gcs-filesystem termcolor tf-estimator-nightly typing-extensions wrapt

RUN pip3 install --disable-pip-version-check --no-cache-dir tensorflow

CMD ["python3", "app.py"]