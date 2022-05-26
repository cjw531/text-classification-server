FROM jchoi531/textcls:latest

WORKDIR /app
COPY . /app

COPY environment.yml .
RUN conda env create -f environment.yml
RUN conda activate textcls
# RUN pip install -r requirements.txt

CMD ["python3", "app.py"]