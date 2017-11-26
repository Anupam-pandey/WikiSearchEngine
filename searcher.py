#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys  
import re
import timeit
import heapq

reload(sys)  
sys.setdefaultencoding('utf8')
from Stemmer import Stemmer
from collections import defaultdict,OrderedDict
stemmer=Stemmer("english")
start=0
stop=0
titledata=""
stopwordsdict = defaultdict(int)
tfdict=defaultdict(int)
docscoresdict = defaultdict(float)

secondarydict = defaultdict(list)
titledict = defaultdict(list)
docIDdict = defaultdict(list)
querydict = defaultdict(list)
key_doclistdict={}
wordIDidfdict = defaultdict(list)
scorelist=defaultdict(list)
doctfidfdict = defaultdict(list)

with open("IndexFolder/Title-ID.txt") as f:
	line= f.read().splitlines()
	for title in line:
		docIDinTitle=title.split('-')
		titledict[docIDinTitle[0]]=docIDinTitle[1]


with open("IndexFolder/SecondaryIndex.txt") as f:
	line= f.read().splitlines()
	for x in line:
		#print x
		documentmapper=x.split()
		rangetoptobottom=documentmapper[0]
		rangetoptobottomlist=rangetoptobottom.split('-')
		secondarydict[documentmapper[1]].append(rangetoptobottomlist[0])
		secondarydict[documentmapper[1]].append(rangetoptobottomlist[1])





with open("stopwords.txt") as f:
	line= f.read().split()
	for x in line:
		stopwordsdict[x]=1


def tokenize(data):
	tokens=re.findall("[\w]+",data)
	tokens=[key.strip().encode('utf-8') for key in tokens]
	return tokens

def getStemmedTokens(data):
	stemmedWords=[ stemmer.stemWord(key) for key in list(data) ]
	return stemmedWords


def getNonStopwords(data):
	data=[i for i in data.split() if stopwordsdict[i]!=1 and len(i)>3]
	return data


def createfile(IndexID):
	filename="Index"+str(IndexID)+".txt"
	return filename


def tfidfsummer(docpostdict,idfscore,key):
	for k,v in docpostdict.items():
		tf=v.split('_')[0]
		doctfidfdict[k]=float(tf)*float(idfscore)
	return doctfidfdict		


def parsewords(words,word):
	docIDdict = defaultdict(list)
	doclistdict=[]
	listdict={}

	postingline=words.split()
	flag=0
	key=tf=idf=-1
	for i in xrange(len(postingline)):
		if i==0:
			key=postingline[i].split('-')[0]
			if str(key)==str(word):
				idf=postingline[i].split('-')[1]
				docID_details=postingline[i].split('-')[2]
				docID=docID_details.split(':')[0]
				docID=docID.strip()
				tf=docID_details.split(':')[1]
				tf=tf.strip()
				listdict[docID]=float(tf)*float(idf)
				key_doclistdict[key]=listdict
				restdata=docID_details.split(':')[2]
				restdata=tf+'_'+restdata
				docIDdict[docID]=restdata
		elif str(key)==str(word):
				docID_details=postingline[i].split(':')
				docID=docID_details[0]
				docID=docID.strip()
				tf=docID_details[1]
				tf=tf.strip()
				listdict[docID]=float(tf)*float(idf)
				key_doclistdict[key]=listdict
				restdata=docID_details[2]
				restdata=tf+'_'+restdata
				docIDdict[docID]=restdata

	return key,key_doclistdict,idf,docIDdict








def getwordcontent(filename,word,size):
	with open("IndexFolder/"+filename) as f:
		line= f#.readline().splitlines()
		t=10
		global scorelist,wordIDidfdict,docIDdict
		try:
			for postingline in line:
				key=postingline.split('-',1)[0]
				if str(word)==str(key):
					key_doclistdict={}
					key,key_doclistdict,idf,docIDdict= parsewords(postingline,word)
					wordIDidfdict[word]=idf
					scorelist=tfidfsummer(docIDdict,idf,key)
			return key_doclistdict,scorelist,docIDdict,wordIDidfdict,key
		except:
			key_doclistdict={}
			return key_doclistdict,scorelist,docIDdict,wordIDidfdict,key
			pass		


def main():

	while True:
		try:
			IndexID=-1
			global querydict,start,stop
			global docscoresdict
			query=raw_input()
			query=str(query)
			query.lower()
			if query=="q":
				sys.exit(0)
			if re.search(r'[t|b|c|e|i]:',query):
				flag=1
				print query
			else:
				querylist=tokenize(query)
				stemmedquerylist=getNonStopwords(" ".join(querylist))
				stemmedquerylist=getStemmedTokens(stemmedquerylist)
				for word in stemmedquerylist:
					for k,v in secondarydict.items():
						if str(v[0])<=str(word) and str(v[1])>=str(word):
							IndexID=k

					filename=createfile(IndexID)
					key_doclistdict,scorelist,docIDdict,wordIDidfdict,key=getwordcontent(filename,word,len(stemmedquerylist))
				start = timeit.default_timer()
				if len(stemmedquerylist)==1:
					#scorelist=heapq.nlargest(10,scorelist.items(),key=scorelist.get)
					t=10
					if scorelist:
						scorelist=sorted(scorelist.items(), key=lambda kv: kv[1], reverse=True)
						for i,v in scorelist:
							print titledict[i]
							t-=1
							if(t==0):
								break;
					stop = timeit.default_timer()
					print "Time to execute : ",stop - start				
				else:
					for item in stemmedquerylist:
						t=10
						for k,v in key_doclistdict.items():
							if item==k:
								for ids,val in v.items():
									docscoresdict[ids]+=float(key_doclistdict[item][ids])
					if docscoresdict:
						docscoresdict2=sorted(docscoresdict.items(), key=lambda kv: kv[1], reverse=True)[:10]
						for i,v in docscoresdict2:
							print titledict[i]
							t-=1
							if(t==0):
								break;
					stop = timeit.default_timer()
					print "Time to execute : ",stop - start			
		except:
			print "No match"
			stop = timeit.default_timer()
			print "Time to execute : ",stop - start		




#print secondarydict

main()

#print "Time to execute : ",stop - start
#start = timeit.default_timer()






