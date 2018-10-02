
# coding: utf-8

# In[1]:


# https://github.com/fchollet/keras/blob/master/examples/lstm_text_generation.py
# -*- coding: utf-8 -*-
from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import mecab
import MeCab
import time

path = "/home/MakeTweet/MakedataByTwimeMachine/maguroTweetimprove.txt"
#一行ずつ
readfiletext = open(path,"r",encoding="utf-8").read().lower()
print('corpus length:', len(readfiletext))
#形態素解析をここで使う
mecabText = mecab.mecab_list(readfiletext)
mecabTextLen = len(mecabText)
print(mecabTextLen)
chars = sorted(list(set(mecabText)))
print('total chars:', len(chars))
#形態素解析にして単語ずつ。そしてそれを対して数値を与えている。
char_indices = dict((c, i) for i, c in enumerate(chars))
#char_indicesと逆の順番
indices_char = dict((i, c) for i, c in enumerate(chars))


#maxlenは入力する最大文字数を決めている（形態素解析での文字数）
maxlen = 6
step = 3
sentences = []
next_chars = []
for i in range(0, len(readfiletext) - maxlen, step):
    #ここで作っているのは実際に学習に使われていると思う。Xを作成するのに使われている
    #「imemachine」とtext[i: i + maxlen]にきたとき、text[i + maxlen]に「を」がきている。next_charsbに入るのは解答だと思う
    #next_charsに入るのは一文字だけだと思う
    #iはこれによってだぶりがなくなるのだと思う。ちょっとずつ文字列を進めていく
    if(mecabTextLen < maxlen + i ):
        break
    sentences.append(mecabText[i: i + maxlen])
    next_chars.append(mecabText[i + maxlen ])
    
print('nb sequences:', len(sentences))

print('Vectorization...')
X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)


#形態素解析した単語に対しての単語辞書を使う
#one_hotベクトルで作成していると思う i,t,char_indices[char] の3つ座標のとこに1格納だと思う
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i,t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1
    

print('Build model...')
model = Sequential()
model.add(LSTM(128, input_shape=(maxlen, len(chars))))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))

optimizer = RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

for iteration in range(1, 2000):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    model.fit(X, y,
              # batch_size=128,
              batch_size=512,
              epochs=1)

    start_index = random.randint(1, len(readfiletext) - maxlen - 1)

    for diversity in [1.0]:
        print()
        print('----- diversity:', diversity)

        generated = ''
        #適当に文字を取ってきていると思う
        sentence = mecabText[start_index: start_index + maxlen]
        #生成したのが[]の場合もう一回 そうなる原因はわからなかったです
        if len(sentence) == 0 :
            continue
        print(sentence)
        #generatedに渡すためにsentenceの内容を連結
        for char in sentence:
            generated += char
      
        print("----- Generating with seed: ")
        sys.stdout.write(generated)
        #実際に生成しているとこはここのfor文だと思う
        for i in range(10):
            x = np.zeros((1, maxlen, len(chars)))
            #enumerateはインデックス番号, 要素の順に取得できる。
            for t, char in enumerate(sentence):
                x[0, t, char_indices[char]] = 1.

            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]
            generated += next_char
            next_charlist = [next_char]
            sentence = sentence[1:] + next_charlist
            #追加後もう一回形態素解析を行う
            sys.stdout.write(next_char)
            sys.stdout.flush()
        print()
model.save('LSTM_Tweet.h5')

