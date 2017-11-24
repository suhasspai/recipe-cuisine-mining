import pandas as pd
import numpy as np; import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import math

df_train = pd.read_json('train.json')
data = pd.read_csv('matrix.csv')
data.set_index('cuisine',inplace=True)

plt.style.use('ggplot')
df_train['cuisine'].value_counts().plot(kind='bar')

cos = cosine_similarity(data)

#cosine similarity between various cuisines
fig  = plt.figure(figsize = (20,20))
cax = plt.matshow(cos,fignum =1)
fig.colorbar(cax)
plt.show()

df_dummy = pd.read_csv('result.csv')
df_dummy = df_dummy.drop('Max',1)

# preprocessing the result.csv for TF-IDF

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    string = string[3:len(string)-1] #(c for c in string if 0 < ord(c) < 127)
    return string

df_dummy.columns = [strip_non_ascii(x) for x in df_dummy.columns]

df_dummy.rename(columns = {'':'ingredients'},inplace = True)
df_dummy_t = df_dummy.set_index('ingredients').T
data1 = df_dummy_t

data1.columns = [strip_non_ascii(x) for x in data1.columns]

for i in range(0,20):
    data1.iloc[i,6787] = data1.iloc[i,6787][:len(data1.iloc[i,6787])-1]

idf = {}

#Calculating tf-idf
tmp = 0
for ing in data1.columns:
    count = 0
    for index,row in data1.iterrows():    
        if int(row[ing]) > 0:
            count+=1
    if count!=0:
        idf[ing] = math.log(21/count)
    else:
        idf[ing] = 0

#ingredients vs idf graph
x = range(0,6787)  
xTicks = list(idf.keys())
y = list(idf.values())
import pylab as pl
pl.xticks(x, xTicks)
pl.xticks(range(6787), xTicks,rotation = 90)
pl.plot(x,y,'.')
pl.show()

ls = {}
tfidf_data = data1
tmp = 0
for ingredient in tfidf_data.columns:
    max_ing = tfidf_data[ingredient].astype(int).max()
    for index,row in tfidf_data.iterrows():
        if max_ing!=0:
            row[ingredient] = idf[ingredient]*(float(float(row[ingredient])/float(max_ing)))
        else:
            row[ingredient] = 0


coss = cosine_similarity(tfidf_data)
#cosine similarity between various cuisines after tf-idf
fig = plt.figure(figsize = (20,20))
cax = plt.matshow(coss,fignum =1)
fig.colorbar(cax)
plt.show()

#counting number of dishes in each cuisine
cuisine_count = {}
for cui in df_train['cuisine']:
    if not cui in cuisine_count:
            cuisine_count[cui] = 1
    else:
        cuisine_count[cui] += 1

#preprocessing the training dataset
for index,row in df_train.iterrows():
    l = []
    for entry_in in df_train.loc[index,'ingredients']:
        symbols = " -./\\(),\'!&%1234567890"
        for symbol in symbols:
            entry_in = entry_in.replace(symbol,'')
        entry_in = entry_in.lower()
        entry_in = entry_in.encode('ascii','ignore').decode('utf-8')
        l.append(entry_in)
    df_train.set_value(index,'ingredients',l)


#Classification using naive bayes
for ing in data.columns:
    for index,row in data.iterrows():
        data.loc[index,ing] = float(float(row[ing])/float(cuisine_count[index]))

pred_cuisine = ''
pred_correct = 0
total_cuisine = 0
tmp = 0

for dish,row in df_train.iterrows():
    pred_prob = 0
    for cui, data_row in data.iterrows(): 
        if tmp==0:
            tmp = 1
            continue
        prob = 1
        for ing in df_train.loc[dish,'ingredients']:  
            prob *= data.loc[cui,ing]*float(cuisine_count[cui]) 
            if prob > pred_prob:
                pred_prob = prob
                pred_cuisine = cui
    if row['cuisine']==pred_cuisine:
        pred_correct+=1
    total_cuisine+=1
    print(row['cuisine'],":",pred_cuisine)

#Accuracy
print(pred_correct) #27428
print(total_cuisine) #39774
print((pred_correct/total_cuisine)*100)#68.96%

