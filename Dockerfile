FROM jchoi531/textcls:latest

WORKDIR /app
COPY . /app

# RUN pip install -r requirements.txt

pip3 install --disable-pip-version-check -r requirements.txt

CMD ["python3", "app.py"]