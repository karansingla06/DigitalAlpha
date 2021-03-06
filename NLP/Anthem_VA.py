# -*- coding: utf-8 -*-
"""
@author: karan
"""

#-----------------------------------------------    
# =============================================================================
# import tika
# from tika import parser
# parsed = parser.from_file(r'C:\Users\user\Downloads\Anthem.docx', xmlContent=True)
# 
# =============================================================================

import mammoth
with open(r"C:\Users\user.A713DCOK\Desktop\Prabal\Anthem1Final.docx", "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html = result.value # The generated HTML
    messages = result.messages # Any messages, such as warnings during conversion
f = open(r"C:\Users\user.A713DCOK\Desktop\Prabal\Anthem1Final.html","w")
f.write(html)

from bs4 import BeautifulSoup
soup = BeautifulSoup(html,'html.parser')
#soup.prettify()

blacklist = ["img" ]
for tag in soup.findAll():
        if tag.name.lower() in blacklist:
            # blacklisted tags are removed in their entirety
            tag.extract()





from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from string import punctuation
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")





#user_input=input("please enter your query:\n")
user_input="surgery eye"
sents = sent_tokenize(user_input)
word_sent = word_tokenize(user_input.lower())

_stopwords = set(stopwords.words('english') + list(punctuation))
user_input_words=[word for word in word_sent if word not in _stopwords]
user_input_words=[stemmer.stem(i) for i in user_input_words]
# =============================================================================
# 
# key_section={}
# for i in user_input_words:
#     temp=[]
#     for key,val in d_stem.items(): 
#         if i in val:
#             temp.append(key)
#     key_section[i]=temp
# # =============================================================================
# =============================================================================
# for item in word_sent[2:4]:
#         tokenized = nltk.word_tokenize(item)
#         tagged = nltk.pos_tag(tokenized)
#         print(tagged)
# 
# 
# =============================================================================

all_h1=soup.find_all('h1')

d_ms={}
for item in all_h1:
    first=item
    second=first.find_next('h1')
    temp=""
    
    while first.findNext()!=second:
        if str(first.findNext().text) != "":
            temp+= str(first.findNext().text)+" "
        first=first.findNext()
    if temp!=" Please see “Therapy Services” later in this section. " and temp!=' See “Therapy Services” later in this section. ' and temp!="":
        temp=temp.replace('.'," . ")
        d_ms[str(item.text)]=temp

#for item,value in d_ms.items():
 #   print(item,"\n",value,'-----------------','\n')    
    


d_kwds={}
for key,val in d_ms.items():
    if val is not None:
        sents = sent_tokenize(val)
        word_sent = word_tokenize(val.lower())
        _stopwords = set(stopwords.words('english') + list(punctuation)+['·',
  '’',
  '“',
  '”'])
        section_words=[word for word in word_sent if word not in _stopwords]
        d_kwds[key]=list(word for word in set(section_words) if (word.isalpha() and len(word)>2 and len(set(word))!=1))
        
    
d_stem={}
for key,val in d_kwds.items():
    singles = [stemmer.stem(i) for i in val]
    temp=set(singles)
    d_stem[key]=list(temp)
    
    

        

####$sjdnaskdsad''
    
# =============================================================================
# all_sent=soup.text
# all_sent=all_sent.replace("\t"," ")
# all_sent=all_sent.replace(".",". ")
# 
# =============================================================================


bag_of_words2=[]
for i,j in d_stem.items():
    bag_of_words2.append(j)
new_bag=[]
for list_word in bag_of_words2:
    for i in list_word:
        if i.isalpha():
            new_bag.append(i) 
new_bag=list(set(new_bag))
    
# =============================================================================
# sents = sent_tokenize(all_sent)
# sents=[i.replace('.',' ') for i in sents]
# word_sent = word_tokenize(all_sent.lower())
# _stopwords = set(stopwords.words('english') + list(punctuation)+['·','“','”'])
# bag=[word for word in word_sent if word not in _stopwords]
# bag_of_words=[stemmer.stem(i) for i in bag]
# bag_of_words=set(bag_of_words)
# bag_of_words2=list(bag_of_words)
# =============================================================================

# =============================================================================
# columns_main=[bag_of_words]
# columns_main.append('Class')
# =============================================================================

# =============================================================================
# maindf=pd.DataFrame(columns=new_bag)
# maindf['Class']=[0]*len(d_stem.keys())
# temp_count=0
# d_mapping={}
# 
# for i,j in d_stem.items():
#     #temp=[0]*len(bag_of_words)
#     m=int(temp_count)
# 
#     for k in j:
#         if k in maindf.columns.values:
#             maindf.loc[m,k]=1
#     d_mapping[m]=i
#     maindf.iloc[m,-1]=m
#     temp_count+=1    
# =============================================================================

final_dict_of_subheading=list(d_kwds.keys())
final_output_vector=[]
final_list_of_vector=[]

for i,j in d_ms.items():
        one_hot_encoder=[]
        for _ in range(len(new_bag)):
            one_hot_encoder.append(0)
        sents = sent_tokenize(j)
        for w in sents:
            word_to_match = word_tokenize(w.lower())
            _stopwords = set(stopwords.words('english') + list(punctuation)+list('“')+list('–')+list('·')+list('”')+list('’')+list('e.g.'))
            word_sent=[word for word in word_to_match if word not in _stopwords]
            word_sent=[stemmer.stem(i) for i in word_sent if i.isalpha()]
            word_sent=list(set(word_sent))
            for wr in word_sent:
                if wr in new_bag:
                    one_hot_encoder[new_bag.index(wr)]=1
            final_list_of_vector.append(one_hot_encoder)
            final_output_vector.append(final_dict_of_subheading.index(i))
        

for item,val in d_stem.items():
     one_hot_encoder=[]
     for _ in range(len(new_bag)):
         one_hot_encoder.append(0)
     for v in val:
         if v in new_bag:
             one_hot_encoder[new_bag.index(v)]=1
     final_list_of_vector.append(one_hot_encoder)
     final_output_vector.append(final_dict_of_subheading.index(i))  

    
maindf=pd.DataFrame(columns=list(set(new_bag)))
for insert in range(len(final_list_of_vector)):
    maindf.loc[insert]=final_list_of_vector[insert]
maindf['Class']=final_output_vector


tables = soup.find_all('table')
table1=tables[0]   

##### finding heading in tables
# =============================================================================
# tables = soup.find_all('table')
# table1=tables[0]
# 
# t=pd.read_html(str(soup),header=0)
# 
# t[1].columns.values[0]=t[1].columns.values[0].replace('\t','#$%^&')
# t[1]=t[1].apply(lambda x: x.str.replace('\t','#$%^&'))
# t[1]=t[1].apply(lambda x: x.str.replace('”',''))
# t[1]=t[1].apply(lambda x: x.str.replace('“',''))
# 
# #t[1].to_csv("C:/Users/user/Downloads/test.csv",sep=';')
# import numpy as np
# temp=np.array(t[1])
# temp=np.array(temp).ravel()
# temp2=[]
# for i in temp:
#     temp2.append(i.split('#$%^&'))
# 
# df=pd.DataFrame(temp2)
# =============================================================================

#df= pd.read_csv('C:/Users/user/Downloads/test.csv',sep=';')


# =============================================================================
# t1=pd.read_html(tables.string,header=0)
# 
# from docx import *
# 
# wordDoc = Document(r'C:\Users\Prabal\Desktop\PdfDocument\Anthem.docx')
# 
# for table in wordDoc.tables:
#     for row in table.rows:
#         for cell in row.cells:
#             print(cell.text)
# 
# from tabula import read_pdf
# df=read_pdf(r"C:\Users\Prabal\Desktop\PdfDocument\Anthem3.pdf","test.json",output_format="json")
# print(df)
# 
# =============================================================================


# =============================================================================
# from textblob import TextBlob
# from nltk.corpus import stopwords
# from string import punctuation
# from nltk.stem.snowball import SnowballStemmer
# stemmer = SnowballStemmer("english")
# text="Your Plan includes benefits for durable medical equipment and medical devices when the equipment meets the following criteria Is meant for repeated use and is not disposable Is used for a medical purpose and is of no further use when medical need ends Is meant for use outside a medical Facility Is only for the use of the patient Is made to serve a medical use Benefits include purchase-only equipment and devices (e.g., crutches and customized equipment),purchase or rent-to-purchase equipment and devices (e.g., Hospital beds and wheelchairs), andcontinuous rental equipment and devices (e.g., oxygen concentrator, ventilator, and negative pressurewound therapy devices). Continuous rental equipment must be approved by us. We may limit theamount of coverage for ongoing rental of equipment. We may not cover more in rental costs than the costof simply purchasing the equipment."
# #coverting the text into TextBlob
# text_b=TextBlob(text)
# print(text_b.noun_phrases)
# _stopwords = set(stopwords.words('english') + list(punctuation))
# input_words=text_b.words
# user_input_words=[word for word in input_words if word not in _stopwords]
# user_input_words=[stemmer.stem(i) for i in user_input_words]
# user_blob=TextBlob(str(user_input_words))
# #making n-grams
# ng2=user_blob.ngrams(2)
# ng3=user_blob.ngrams(3)
# 
# 
# =============================================================================



# =============================================================================
# from nltk.collocations import *
# 
# #bigram
# bigram_measures = nltk.collocations.BigramAssocMeasures()
# text=d_ms['Durable Medical Equipment and Medical Devices']
# sents = sent_tokenize(text)
# word_sent = word_tokenize(text.lower())
# 
# _stopwords = set(stopwords.words('english') + list(punctuation))
# user_input_words=[word for word in word_sent if word not in _stopwords]
# user_input_words=[stemmer.stem(i) for i in user_input_words]
# finder1 = BigramCollocationFinder.from_words(user_input_words)
# finder1Tr=sorted(finder1.ngram_fd.items())
# 
# #trigram
# finder2 = TrigramCollocationFinder.from_words(user_input_words)
# finder2Tr=sorted(finder2.ngram_fd.items())
# 
# durableList=[]
# for i,j in finder2Tr:
#     temp=" "
#     durableList.append(temp.join(i))
# 
# 
# 
# 
# bigram_measures = nltk.collocations.BigramAssocMeasures()
# text=d_ms['Rehabilitation Services']
# sents = sent_tokenize(text)
# word_sent = word_tokenize(text.lower())
# 
# _stopwords = set(stopwords.words('english') + list(punctuation))
# user_input_words=[word for word in word_sent if word not in _stopwords]
# user_input_words=[stemmer.stem(i) for i in user_input_words]
# finder1 = BigramCollocationFinder.from_words(user_input_words)
# finder1Tr=sorted(finder1.ngram_fd.items())
# 
# #trigram
# finder2 = TrigramCollocationFinder.from_words(user_input_words)
# finder2Tr=sorted(finder2.ngram_fd.items())
# 
# RSList=[]
# for i,j in finder2Tr:
#     temp=" "
#     RSList.append(temp.join(i))
# 
# 
# df2=pd.DataFrame()
# df2['column1']=durableList
# df2['class']=np.repeat("Durable Medical Equipment and Medical Devices",len(durableList))
# 
# df3=pd.DataFrame()
# df3['column1']=RSList
# df3['class']=np.repeat("Rehabilitation Services",len(RSList))
# 
# df2=df2.append(df3)
# 
# 
# 
# =============================================================================



#------------
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
#from sklearn.linear_model import LogisticRegression
#from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn import tree
 
import numpy as np

y = maindf['Class']

x = maindf.drop('Class',axis=1)

nb = GaussianNB()
clf2=SVC()
logistic_regression = LogisticRegression()
logistic_regression=logistic_regression.fit(x,y)
clf1 = tree.DecisionTreeClassifier()
nb=nb.fit(x,y)
clf1=clf1.fit(x,y)
clf2=clf2.fit(x,y)

userinp="continued eligibility"
user_kwds=[stemmer.stem(i) for i in list(userinp.split())]

temp=[]
for i in range(len(new_bag)):
    temp.append(0)
    
for i in user_kwds:
    if i in new_bag:
        temp[new_bag.index(i)]=1
        
temp2=np.array(temp).reshape(1,-1)

print(clf1.predict(temp2),clf2.predict(temp2),nb.predict(temp2))


#==============================================================================
# print(user_blob.noun_phrases.count('wheelchair'))
# print(text_b.sentences)
# for i in text_b.sentences:
#     print(i.noun_phrases.count('wheelchairs'))
# print(text_b.parse())
#==============================================================================
# =============================================================================
# from textblob.classifiers import NaiveBayesClassifier
# tup_lis=[]
# count=0
# for i in ng2:
#     if
#     val=tuple(i,"Durable Medical Equipment")
#     print(val)
#     #print(type(i))
# train=[]
# =============================================================================
#==============================================================================
# train = [
#     ('I love this sandwich.', 'simple'),
#     ('This is an amazing place!', 'simple'),
#     ('I feel very good about these beers.', 'pos'),
#     ('This is my best work.', 'pos'),
#     ("What an awesome view", 'pos'),
#     ('I do not like this restaurant', 'neg'),
#     ('I am tired of this stuff.', 'neg'),
#     ("I can't deal with this", 'neg'),
#     ('He is my sworn enemy!', 'simple'),
#     ('My boss is horrible.', 'simple')
# ]
# test = [
#==============================================================================
# =============================================================================
#     ('The beer was good.', 'pos'),
#     ('I do not enjoy my job', 'neg'),
#     ("I ain't feeling dandy today.", 'simple'),
#     ("I feel amazing!", 'simple'),
#     ('Gary is a friend of mine.', 'pos'),
#     ("I can't believe I'm doing this.", 'neg')
# ]
# 
# cl = NaiveBayesClassifier(ng2)
# cl.classify("purchas euip")
# 
# =============================================================================
    

    
