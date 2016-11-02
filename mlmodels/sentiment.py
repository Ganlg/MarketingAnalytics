import pickle
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

