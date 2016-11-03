import pickle
import numpy as np
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences

class SentimentModel(object):

    MAX_SEQUENCE_LENGTH = 40

    def __init__(self):
        with open('mlmodels/data/sentiment/tokenizer.pkl', 'rb') as f:
            self.tokenizer = pickle.load(f)

        with open('mlmodels/data/sentiment/model.json', 'r') as f:
            self.model = model_from_json(f.read())

        self.model.load_weights('mlmodels/data/sentiment/weights.hdf5')

    def predict(self, text):
        sequence = self.tokenizer.texts_to_sequences([text])
        sentiment = pad_sequences(sequence, maxlen=self.MAX_SEQUENCE_LENGTH, padding='post')
        return self.model.predict(sentiment)[0][0]

class SentimentModel2(object):

    MAX_SEQUENCE_LENGTH = 100

    def __init__(self):
        with open('mlmodels/data/sentiment/yelp_model/tokenizer.pkl', 'rb') as f:
            self.tokenizer = pickle.load(f)

        with open('mlmodels/data/sentiment/yelp_model/model.json', 'r') as f:
            self.model = model_from_json(f.read())

        self.model.load_weights('mlmodels/data/sentiment/yelp_model/weights.hdf5')

    def prob(self, text):
        if not isinstance(text, list):
            text = [text]
        sequence = self.tokenizer.texts_to_sequences(text)
        x = pad_sequences(sequence, maxlen=100)
        return self.model.predict(x)

    def predict(self, text):
        a = text.split()
        texts = []
        current = ""
        for word in a:
            current += word
            texts.append(current)
            current += " "
        prob = self.prob(texts)
        score = np.sum(prob * np.arange(20, 120, 20), axis=1)
        return [{'score': s, 'text': t} for s, t in zip(score, a)]

