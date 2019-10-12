import numpy as np
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import SGD
from keras.metrics import categorical_accuracy
import pickle

dt1 = pd.read_csv('processed_deck_1_round_2000.csv', header=None)
dt1.columns = ['nCards', 'nTen', 'nOne', 'nAce', 'small', 'large', 'isFirst', 'canSplit', 'dealerHand', 'nDeck', 'action']
dt2 = pd.read_csv('processed_deck_6_round_2000.csv', header=None)
dt2.columns = ['nCards', 'nTen', 'nOne', 'nAce', 'small', 'large', 'isFirst', 'canSplit', 'dealerHand', 'nDeck', 'action']


def preprocess_features(dt):
    selected_features = dt[[
#         'nCards',
        'nTen',
#         'nOne',
#         'nAce',
        'small',
        'large',
        'isFirst',
#         'canSplit',
#         'dealerHand',
        'nDeck']]

    processed_features = selected_features.copy()
    processed_features['pTen'] = (16 * dt['nDeck'] - dt['nTen']) / (52 * dt['nDeck'] - dt['nCards'])
    processed_features['pAce'] = (4 * dt['nDeck'] - dt['nAce']) / (52 * dt['nDeck'] - dt['nCards'])
    processed_features['pOne'] = (32 * dt['nDeck'] - dt['nOne']) / (52 * dt['nDeck'] - dt['nCards'])
    processed_features['dealerHasTenOrAce'] = dt['dealerHand'] > 9
    return processed_features


def preprocess_targets(dt):
    output_targets = pd.DataFrame()
    output_targets['action'] = dt['action']
    #     output_targets['action'] -= ((dt['large']==21) & (dt['action']==3))
    return output_targets

dt = dt1.append(dt2).sample(frac=1).reset_index(drop=True)
splitSet = dt[dt['canSplit']==1]
noneSplitSet = dt[dt['canSplit']==0]




## None Split Set model

# noneSplitSet_training_size = 158000
# noneSplitSet_validation_size = noneSplitSet.shape[0] - noneSplitSet_training_size
# training_examples = preprocess_features(noneSplitSet.head(noneSplitSet_training_size))
# training_targets = preprocess_targets(noneSplitSet.head(noneSplitSet_training_size))
training_examples = preprocess_features(noneSplitSet)
training_targets = preprocess_targets(noneSplitSet)


model = Sequential()
model.add(Dense(5, input_shape=(training_examples.shape[1],), activation="relu"))
model.add(Dense(20, activation='relu'))
model.add(Dense(90, activation='relu'))
model.add(Dense(30, activation='relu'))
model.add(Dense(5, activation='relu'))
model.add(Dense(4, activation='softmax')) # only 4 actions for none split set
model.compile(loss='mse', optimizer='adam', metrics= [categorical_accuracy])
model.summary()

model.fit(training_examples, pd.get_dummies(training_targets['action']), batch_size=100, epochs=15)

with open('keras_model_none_split.pkl', 'wb') as f:
    pickle.dump(model, f)

## Split Set model

# splitSet_training_size = 13270
# splitSet_validation_size = splitSet.shape[0] - splitSet_training_size
# training_examples = preprocess_features(splitSet.head(splitSet_training_size))
# training_targets = preprocess_targets(splitSet.head(splitSet_training_size))
# validation_examples = preprocess_features(splitSet.tail(splitSet_validation_size))
# validation_targets = preprocess_targets(splitSet.tail(splitSet_validation_size))
training_examples = preprocess_features(splitSet)
training_targets = preprocess_targets(splitSet)

model = Sequential()
model.add(Dense(5, input_shape=(training_examples.shape[1],), activation="relu"))
model.add(Dense(20, activation='relu'))
model.add(Dense(90, activation='relu'))
model.add(Dense(30, activation='relu'))
model.add(Dense(5, activation='relu'))
model.add(Dense(5, activation='softmax')) # 5 actions for split set
model.compile(loss='mse', optimizer='adam', metrics= [categorical_accuracy])
model.summary()

model.fit(training_examples, pd.get_dummies(training_targets['action']), batch_size=100, epochs=15)

with open('keras_model_split.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('keras_model_features_types.pkl', 'wb') as f:
    pickle.dump(training_examples.dtypes, f)