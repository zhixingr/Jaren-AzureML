import csv
import lda
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF
 
corpus = []
titles = []
inputfile = "C:\\tests\\myinput.csv"
outputfile = "C:\\tests\\myoutput.txt"

with open(inputfile, "r") as msdninput_file:
    reader = csv.reader(msdninput_file, delimiter = ",")
    #reader.next()
    for row in reader:
        titles.append(row[0])
        corpus.append(row[0] + " " + row[1])
 
numtopics = 12
n_top_words = 11
num_gram_start = 1
num_gram_end = 3
 
vectorizer = CountVectorizer(analyzer='word', ngram_range=(num_gram_start,num_gram_end), min_df = 1, stop_words = 'english')
matrix =  vectorizer.fit_transform(corpus)
feature_names = vectorizer.get_feature_names()
 
vocab = feature_names
f = open(outputfile, "w")
 
model = lda.LDA(n_topics=numtopics, n_iter=500, random_state=1)
model.fit(matrix)
topic_word = model.topic_word_
topic_summary = [] 
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
    print('Topic {}: {}'.format(i, ', '.join(topic_words)))
    print >> f, 'Topic {}, {}'.format(i, ', '.join(topic_words))
    print >> f, 'Probability: {}'.format(topic_dist[np.argsort(topic_dist)[:-n_top_words:-1]])
    topic_summary.append(format(', '.join(topic_words)))

doc_topic = model.doc_topic_
instance_summary = []
for i in range(0, len(titles)):
    print("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))
    print >> f, "{} (top topic: {})".format(titles[i], doc_topic[i].argmax())
    print("Top 3 topics: {} Probabilities: {}".format(doc_topic[i].argsort()[::-1][:3], doc_topic[i][doc_topic[i].argsort()[::-1][:3]]))
    print >> f, "Top 3 topics: {} Probabilities: {}".format(doc_topic[i].argsort()[::-1][:3], doc_topic[i][doc_topic[i].argsort()[::-1][:3]])
    instance_summary.append(doc_topic[i].argmax())

for i in range(0, len(topic_summary)):
    print("(Topic_{} : {})".format(i, topic_summary[i]))
    print >> f, "(Topic_{} : {})".format(i, topic_summary[i])
    for j in range(0, len(instance_summary)):
        if (instance_summary[j] == i):
            print("(    Document_{} [{}] : {})".format(j, doc_topic[j][doc_topic[j].argmax()], titles[j]))
            print >> f, "(    Document_{} [{}] : {})".format(j, doc_topic[j][doc_topic[j].argmax()], titles[j])

f.close()
print("Done!")