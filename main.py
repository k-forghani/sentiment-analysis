import csv
import re
import nltk
from nltk.corpus import stopwords

def cleanup(s):
    
	stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
	
	string = s
	
	lower_string = string.lower()
	
	no_number_string = re.sub(r'\d+','',lower_string)
	no_punc_string = re.sub(r'[^\w\s]','', no_number_string)
	
	no_wspace_string = no_punc_string.strip()
	no_wspace_string
	
	lst_string = [no_wspace_string][0].split()	
	no_stpwords_string=""
	for i in lst_string:
		if not i in stop_words:
			no_stpwords_string += i+' '
			
	no_stpwords_string = no_stpwords_string[:-1]
        
	return no_stpwords_string
reviews=[]
keywords=[]


with open('data/data.csv', 'r') as file:

    reader = csv.reader(file)
    for row in reader:
        text=cleanup(row[0])
        text_class=row[1]
        reviews.append([text.split(),text_class])
        
print('s)')
test=reviews[4000:]
reviews=reviews[:4000]   
for t in reviews:
    keywords.extend(t[0])

keywords=sorted(list(set(keywords)))

print(len(keywords))
probabilities=[]

for i in range(len(reviews)):
    probabilities.append([])
    for j in keywords:
        probabilities[i].append(0)
        
for i in range(len(reviews)):
    for j in range(len(keywords)):
        if keywords[j] in reviews[i][0]:
            probabilities[i][j]+=reviews[i][0].count(keywords[j])

vocab=len(keywords)
totalpluswords=0
totalnegwords=0
totalplus=0
totalneg=0

for i in range(len(reviews)):
    if reviews[i][1]=='1':
        s=probabilities[i]
        totalplus+=1
        totalpluswords+=sum(s)
    else:
        s=probabilities[i]
        totalneg+=1
        totalnegwords+=sum(s)

tot=0
trueguess=0
j=0

for g in test:
    j+=1
    if j>1000:
        break
    to_find=g[0]

    temp=[]

    for i in to_find:
        count=0
        if i not in keywords:
            continue
        x=keywords.index(i)

        for k in range(len(probabilities)):
            if reviews[k][1]=='1':
                count+=probabilities[k][x]
        temp.append(count)
        count=0

    for i in range(len(temp)):
        temp[i]=format((temp[i]+1)/(vocab+totalpluswords),".4f")
    temp=[float(f) for f in temp]

    pplus=float(format((totalplus)/(totalplus+totalneg),".8f"))
    for i in temp:
        pplus=pplus*i

    pplus=format(pplus,".8f")

    temp=[]

    for i in to_find:
        count=0
        if i not in keywords:
            continue
        x=keywords.index(i)

        for k in range(len(probabilities)):
            if reviews[k][1]!='1':
                count+=probabilities[k][x]
        temp.append(count)
        count=0

    for i in range(len(temp)):
        temp[i]=format((temp[i]+1)/(vocab+totalpluswords),".4f")
    temp=[float(f) for f in temp]

    pneg=float(format((totalneg)/(totalplus+totalneg),".8f"))
    for i in temp:
        pneg=pneg*i

    pneg=format(pneg,".8f")
    pred='0'
    if pplus>pneg:
        pred='1'
    if pred==g[1]:
        trueguess+=1
    tot+=1

    print(pred,g[1])

print(trueguess,tot)

