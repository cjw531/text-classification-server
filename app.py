from tensorflow import keras
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
import tensorflow as tf
import tensorflow_text as text
import tensorflow_hub as hub
import numpy as np
import pickle

from flask import Flask, request, jsonify, abort

app = Flask(__name__)

with open('./model/tokenizer_binary_cnn.pickle', 'rb') as handle:
    binary_tokenizer = pickle.load(handle)

with open('./model/tokenizer_multi_cnn.pickle', 'rb') as handle:
    multi_tokenizer = pickle.load(handle)

binary_cnn = keras.models.load_model('./model/binary_cnn/1/')
multi_cnn = keras.models.load_model('./model/multi_cnn/1/')

binary_bert = tf.keras.models.load_model('./model/binary_bert/1')
multi_bert = tf.keras.models.load_model('./model/multi_bert/1')

def predict_binary_cnn(text):
    try:
        # preprocessing required for CNN model
        max_words = 32
        preprocessed_text = np.array([text,])
        tokenizer = Tokenizer(num_words=5000)
        tokenizer.fit_on_texts(text)
        preprocessed_text = tokenizer.texts_to_sequences(preprocessed_text)
        preprocessed_text = sequence.pad_sequences(preprocessed_text, maxlen=max_words)

        # cnn prediction
        cnn_pred = binary_cnn.predict(preprocessed_text)
        cnn_cls = np.where(cnn_pred > 0.5, 1,0)

        # bert prediction
        bert_pred = binary_bert.predict(np.asarray([text])) # no preprocess needed
        bert_cls = np.where(bert_pred > 0.5, 1,0)
        
        result = {"CNN prediction": str(cnn_cls[0][0]), "BERT prediction": str(bert_cls[0][0])}
        return jsonify(result)

    except Exception as e:
        print('Error occur in image classification!', e)
        return jsonify({'error': e}), 400

def predict_multi_cnn(text):
    try:
        # preprocessing required for CNN model
        max_words = 60
        preprocessed_text = np.array([text,])
        tokenizer = Tokenizer(num_words=5000)
        tokenizer.fit_on_texts(preprocessed_text)
        preprocessed_text = tokenizer.texts_to_sequences(preprocessed_text)
        preprocessed_text = sequence.pad_sequences(preprocessed_text, maxlen=max_words)

        # cnn prediction
        cnn_pred = multi_cnn.predict(preprocessed_text)
        cnn_cls = np.argmax(cnn_pred, axis=1)

        # bert prediction
        bert_pred = multi_bert.predict(np.asarray([text])) # no preprocess needed
        bert_cls = np.argmax(bert_pred, axis=1)

        result = {"CNN prediction": str(cnn_cls[0]), "BERT prediction": str(bert_cls[0])}
        return jsonify(result)

    except Exception as e:
        print('Error occur in image classification!', e)
        return jsonify({'error': e}), 400

@app.route("/predict", methods=["POST"])
def main():
    try:
        classify = request.form.get('type') # get whether it is binary or multiclass (code: 1/2)
        text = request.form.get('text') # get the text to classify

        if classify == '1': # binary classification
            prediction = predict_binary_cnn(text)
        elif classify == '2': # multiclass classification
            prediction = predict_multi_cnn(text)
        else:
            return jsonify({'message': f'Invalid [type] request, {classify}'}), 300

    except Exception as e:
        return jsonify({'message': f'Invalid request, {e}'}), 400

    return prediction


if __name__ == "__main__":
    '''
    curl command usage:
    curl -X POST "http://127.0.0.1:5000/predict" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "text= lots of peope assasinated in texas, total 10 killed" -F "type=1"
    curl -X POST "http://127.0.0.1:5000/predict" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "text= lots of peope assasinated in texas, total 10 killed" -F "type=2"
    '''
    app.run(host="0.0.0.0", port=5000)