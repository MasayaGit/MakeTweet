
# coding: utf-8

# In[1]:


import MeCab

def mecab_list(text):
    tagger = MeCab.Tagger("-Ochasen")
    tagger.parse('')
    node = tagger.parseToNode(text)
    word_class = []
    while node:
        word = node.surface
        wclass = node.feature.split(',')
        if wclass[0] != u'BOS/EOS':
            if wclass[6] == None:
                word_class.append((word,wclass[0]))
            else:
                word_class.append((word,wclass[0]))
        node = node.next
    return word_class

