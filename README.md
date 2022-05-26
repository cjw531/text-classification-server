# Ainize Server for Text Classification

[![Run on Ainize](https://ainize.ai/images/run_on_ainize_button.svg)](https://ainize.web.app/redirect?git_repo=https://github.com/cjw531/text-classification-server)

This is the backend server of the text classification project. To see the full implementation and the details, refer to: [Performance Comparison of Binary and Multi Class Text Classification Models With `scikit-learn` and `TensorFlow`](https://github.com/cjw531/text-classification).

For the frontend and the web demo, refer to: [`text_classification_front`](https://github.com/cjw531/text-classification-front).

## Environment Setup
After cloning the repository, you can install necessary libraries as follows:
```
pip install -r requirements.txt
```

## Docker
The docker image file that is used in this [`Dockerfile`](./Dockerfile) can be found here: https://hub.docker.com/r/jchoi531/textcls

This image contains the pre-trained `TensorFlow` based CNN and BERT + CNN models for both binary and multi class classifications.

## API
Run [`app.py`](./app.py) and execute with the curl requests on the local device:
```
$ curl -X POST "http://127.0.0.1:5000/predict" \
-H "accept: application/json" \
-H "Content-Type: multipart/form-data" \
-F "text= lots of peope assasinated in texas, total 10 killed" \
-F "type=1"
```

For more deails about the API, refer to the API documentation specified in [`Swagger.yaml`](./Swagger.yaml).

### Input
There are 2 variables are being used and required to be inputted: `text` and `type`.
1. `text`: the text that will be classified with the pre-trained models
2. `type`: to determine whether it is binary(`"type=1"`) or multi class (`"type=2"`) classification.

### Output
Following is the json output format:
```
{
    CNN predict: ...,
    BERT predict: ...
}
```
The prediction class is returned in `int` type data. Following is the class mappings:
1. Binary Class

    | Class Name | Non-Disaster Tweet | Disaster Tweet |
    |:----------:|:------------------:|:--------------:|
    | Class Encode |     0              |        1       |

2. Multi Class

    | Class Name | automobile | entertainment | politics | science | sports | technology | world |
    |:----------:|:--------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|
    | Class Encode |     0    |     1   |     2   |     3   |     4   |     5   |     6   |