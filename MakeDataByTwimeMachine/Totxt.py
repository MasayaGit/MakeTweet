
# coding: utf-8

# In[1]:


import re
import csv
#txtファイルを開く
readfile = open("maguroTweet.txt",'r',encoding='utf-8')
#書き込むtxtファイル
writefile = open('maguroTweetimprove.txt', 'w',encoding='utf-8') 
    
#ファイルから一行ずつ読み込む
for line in readfile:
    Arraytext = line.split(" ")
    for text in Arraytext:
        #正規表現で抽出
        select_text = re.sub(r"http.*|Mon.*|Tue.*|Wed.*|Thu.*|Fri.*|Sat.*|Sun.*|#.*|RT.*|@.*|Sep.*|\+.*|[0-9].*", "", text)
        #""と'\n'の時はcsvファイルに書き込まない
        if select_text == "" or select_text == '\n'or select_text == "Aug" or select_text == "Jul":
            continue
        writefile.write(select_text + "\n") 
writefile.close()        
readfile.close() 

