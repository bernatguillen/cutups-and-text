import datetime
from urllib import request
from bs4 import BeautifulSoup
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import spacy

npr_page = "https://text.npr.org/"
base_page = request.urlopen(npr_page)
base_data = BeautifulSoup(base_page, 'lxml')

"""If I was afraid of changes, or for generalization, I would look at base_data.contents and look for the position in
which list(base_data.body.contents[i].children) == ['Top News Stories'], then look for the next element. As of now I think it is faster
to just use base_data.ul"""

news = {}
for title in base_data.ul.children:
    newpage = title.a
    url_news = newpage["href"]
    open_page = request.urlopen(npr_page+url_news)
    open_data = BeautifulSoup(open_page, 'lxml')
    j = 0
    title = 0
    news[newpage.contents[0]] = []
    for stuff in open_data.body.children:
        try:
            aux = stuff.contents
            if aux == newpage.contents:
                title = 1
            else:
                if title:
                    j += 1
            if title and j>=3:
                if '\n' in aux:
                    break
                else:
                    news[newpage.contents[0]] += [stuff.get_text()]
        except:
            pass
    news[newpage.contents[0]] = ' '.join(news[newpage.contents[0]])

nlp = spacy.load('en')
sid = SentimentIntensityAnalyzer()
allsents = []
allscores = []
for new in news:
    doc = nlp(news[new])
    for sent in doc.sents:
        allsents.append(sent.text+' ')
        if np.random.rand() < 0.3:
            allsents[-1] += '\n\n'
        ss = sid.polarity_scores(sent.text)
        allscores.append(ss)

tuples = list(zip(allsents, allscores))
with open(str(datetime.date.today())+".md", 'w') as file:
    s = ' '.join([t[0] for t in sorted(tuples, key = lambda t:t[1]['compound'])])
    s = re.sub(r'( )\1+', r'\1', s)
    file.write("# News of {}\n\n".format(str(datetime.date.today())))
    file.write("## From saddest to happiest, guaranteed bliss\n\n")
    file.write(s)

allsents = []
allscores = []
for new in news:
    doc = nlp(news[new])
    for sent in doc.sents:
        if np.random.rand() < 0.04:
            allsents.append(sent.text+' ')
            if np.random.rand() < 0.3:
                allsents[-1] += '\n\n'
            ss = sid.polarity_scores(sent.text)
            allscores.append(ss)

tuples = list(zip(allsents, allscores))
with open(str(datetime.date.today())+"-short.md", 'w') as file:
    s = ' '.join([t[0] for t in sorted(tuples, key = lambda t:t[1]['compound'])])
    s = re.sub(r'( )\1+', r'\1', s)
    file.write("# News of {}\n\n".format(str(datetime.date.today())))
    file.write("## From saddest to happiest, guaranteed bliss\n\n")
    file.write("### Shorter version, just for you!\n\n")
    file.write(s)
