
# coding: utf-8

# In[1]:


from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
from keras.models import load_model
from keras.models import model_from_json
import sys
import mecab
import MeCab
model = load_model('LSTM_Tweet.h5')


# path = get_file('nietzsche.txt', origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
path = "/home/MakeTweet/MakedataByTwimeMachine/maguroTweetimprove.txt"
#回復アイテム といった風に一行ずつ
readfiletext = open(path,"r",encoding="utf-8").read().lower()
print('corpus length:', len(readfiletext))
#'書', '替'とか使う漢字が入っているとおもう
#形態素解析をここで使う
mecabText = mecab.mecab_list(readfiletext)
mecabTextLen = len(mecabText)
print(mecabTextLen)
chars = sorted(list(set(mecabText)))
print('total chars:', len(chars))
#'便': 349, '係': 350,とかになっていたのを形態素解析にして単語ずつにしている。
char_indices = dict((c, i) for i, c in enumerate(chars))
#'便', 350: '係', 351:とかになっていたのを形態素解析にして単語ずつにしている。
indices_char = dict((i, c) for i, c in enumerate(chars))



def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def make(sentence):
    for i in range(10):
        x = np.zeros((1, 6, len(chars)))
        #enumerateはインデックス番号, 要素の順に取得できる。
        for t, char in enumerate(sentence):
            x[0, t, char_indices[char]] = 1.

        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, 1.0)
        next_char = indices_char[next_index]

        #generated += next_char
        #print(sentence[1:])
        #print(next_char)
        next_charlist = [next_char]
        sentence = sentence[1:] + next_charlist
        #追加後もう一回形態素解析を行う
        sys.stdout.write(next_char)
        sys.stdout.flush()
print()

for i in range(10):

    sentence = "私は鮪です。これ"
    sys.stdout.write(sentence)
    sentence = mecab.mecab_list(sentence)
    make(sentence)
    print()
    print()

    

    sentence = "モテ期キタコレ。プロ実"
    sys.stdout.write(sentence)
    sentence = mecab.mecab_list(sentence)
    make(sentence)
    print()
    print()

    sentence = "オタクが好きなアニメを"
    sys.stdout.write(sentence)
    sentence = mecab.mecab_list(sentence)
    make(sentence)
    print()
    print()

   





