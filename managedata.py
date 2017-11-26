#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys  
import re
reload(sys)  
sys.setdefaultencoding('utf8')
from Stemmer import Stemmer
#from nltk.stem import SnowballStemmer
from collections import defaultdict,OrderedDict
#ps = SnowballStemmer('english')
stemmer=Stemmer("english")

titledata=""
stopwordsdict = defaultdict(int)


with open("stopwords.txt") as f:
	line= f.read().split()
	for x in line:
		stopwordsdict[x]=1


ELregex = re.compile(r'(==external links ==|== external links ==|==external links==|== external links==|== external  links ==)')
def tokenize(data):
	tokens=re.findall("[\w]+ ",data)
	tokens=[key.strip().encode('utf-8') for key in tokens]
	return tokens

def getStemmedTokens(data):
	words = tokenize(data)                                        #Stemming
	stemmedWords=[ stemmer.stemWord(key) for key in words ]
	return stemmedWords

# def getStemmedTokens(data):
# 	#data = unicode(data, errors='ignore')
# 	words = tokenize(data)
# 	words=[ps.stem(word) for word in words]
# 	return words

def getNonStopwords(data):
	data=[i for i in data.split() if stopwordsdict[i]!=1 and len(i)>3]
	return data




def getCatagoryInfobox(data):
	# data=data.replace(u'=',' ')
	# data=data.replace(u',',' ')
	# data=data.replace(u'!',' ')
	# data=data.replace(u"&lt;",' ')
	# data=data.replace(u"&quot;",' ' )
	# data=data.replace(u"&gt;",' ')
	# data=data.replace(u"&amp;",' ')
	# data=data.replace(u"&nbsp",' ')
	# data=data.replace(u'$',' ')
	# data=data.replace(u'^',' ')
	# data=data.replace(u'&',' ')
	# data=data.replace(u'@',' ')
	# data=data.replace(u'*',' ')
	# data=data.replace(u'#',' ')
	# data=data.replace(u"+",' ')
	# data=data.replace(u"-",' ')
	# data=data.replace(u".",' ')
	# data=data.replace(u"+",' ')
	# data=data.replace(u'|',' ')
	# data=data.replace(u";",' ')
	# data=data.replace(u'/',' ')
	# data=data.replace(u'?',' ')
	# data=data.replace(u'<',' ')
	# data=data.replace(u'>',' ')
	category=defaultdict(int)
	postlist=defaultdict(int)
	infobox = defaultdict(int)
	page= defaultdict(int)
	infotext=[]
	Externallinks=[]
	cattext=""
	PageText=""
	info=""
	catstr=""
	maindatacat=""
	cate=[]
	infotext=data.split("\n")
	n=len(infotext)
	for i in xrange(0,n):
		try:
			searchObj = ELregex.search(infotext[i])
			if "{{infobox" in infotext[i]:
				flag=0	
				temp=infotext[i].split('{{infobox')
				info+=" ".join(temp)
				while True:
					if '{{' in infotext[i]:
						flag+=infotext[i].count('{{')
					if '}}' in infotext[i]:
						flag-=infotext[i].count('}}')
					if flag<=0:
						break
					i+=1
					info+=infotext[i]+' '
				continue

			elif "{{ infobox" in infotext[i]:
				flag=0	
				temp=infotext[i].split('{{ infobox')
				info+=" ".join(temp)
				while True:
					if '{{' in infotext[i]:
						flag+=infotext[i].count('{{')
					if '}}' in infotext[i]:
						flag-=infotext[i].count('}}')
					if flag<=0:
						break
					i+=1
					info+=infotext[i]+' '
				continue
				
			elif "[[category" in infotext[i] or "[[:category" in infotext[i] :
				if "[[category" in infotext[i]:
					for x in infotext[i].split(' '):
						cate =x.split("[[category")[1:]
						#print cate
						if len(cate)>0:
							maindatacat+=" ".join(cate)
							# datacat=getNonStopwords(" ".join(cate))
							# datacat=getStemmedTokens(" ".join(datacat))

				if "[[:category" in infotext[i]:
					for x in infotext[i]:
						 	cate=x.split("[[:category")[1:]
						 	if len(cate)>0:
						 		for y in cate:
						 			cattext=y.split("]]")[0]
									maindatacat+=cattext
									# cattext=getNonStopwords(cattext)
									# cattext=getStemmedTokens(" ".join(cattext))
							#print datacat						
				
				
			elif searchObj is not None and (searchObj.group()) in infotext[i]:
				try :	
					while not ("* [" in infotext[i] or "* {" in infotext[i] or "*[" in infotext[i] or "*" in infotext[i]):
						#print infotext[i]
						i+=1	
					while True: 
						if "* [" in infotext[i] or "* {" in infotext[i] or "*[" in infotext[i] or "*" in infotext[i]:
							val=infotext[i].split(' ')
							val=val[2:]	
							for sd in val:
								Externallinks.append(sd)
						i+=1
						if (infotext[i]=="" and infotext[i+1].startswith("[[category") or infotext[i]=="" and infotext[i+1].startswith("{{")):
							break 
					# for k,v in postlist.items():
					# 	print k,v	
				except:
					pass 
			else:
				PageText+=infotext[i]+" "					
		except:
			pass	

#	ni=len(infotext)		



	data=getNonStopwords(info)
	data=" ".join(data)
	data=getStemmedTokens(data)
	for word in data:
		try:
			infobox[word]+=1
		except KeyError:
			infobox[word]=1
	#np=len(PageText)
	#o=getN(np)
	maindatacat=getNonStopwords(maindatacat)
	maindatacat=getStemmedTokens(" ".join(maindatacat))

	for word in maindatacat:
		try:
			category[word]+=1
		except KeyError:
			category[word]=1
	#print PageText		
	# np=len(page)		
	#nl=len(Externallinks)		
	# PageText=PageText[0:np]
	data=getNonStopwords(PageText)
	data=getStemmedTokens(" ".join(data))
	for word in data:
		try:
			page[word]+=1
		except KeyError:
			page[word]=1
	text=getNonStopwords(" ".join(Externallinks))
	text=getStemmedTokens(" ".join(text))
	for word in text:
		try:
			postlist[word]+=1
		except KeyError:
			postlist[word]=1

	return category,infobox	,page,postlist
				
	
def normalize(x):
	x=re.sub(r'\b\w{1,3}\b', '', x)
	# x=x.replace(u'!',' ')
	# x=x.replace(u'$',' ')
	# x=x.replace(u'^',' ')
	# x=x.replace(u'&',' ')
	# x=x.replace(u'@',' ')
	# x=x.replace(u'*',' ')
	# x=x.replace(u'#',' ')
	# x=x.replace(u',',' ')
	# x=x.replace(u'"',' ')
	#x=x.replace(u'_',' ')
	# x=x.replace(u'(',' ')
	# x=x.replace(u')',' ')
	# x=x.replace(u'"',' ')
	# x=x.replace(u':',' ')
	# x=x.replace(u"'",' ')
	# x=x.replace(u"‘‘",' ')
	# x=x.replace(u"’’",' ')
	# x=x.replace(u"''",' ')
	# x=x.replace(u".",' ')
	# x=x.replace(u";",' ')
	# x=x.replace(u"+",' ')
	# x=x.replace(u"-",' ')
	# x=x.replace(u"[",' ')
	# x=x.replace(u"]",' ')
	# x=x.replace(u"&lt;",' ')
	# x=x.replace(u"{",' ')
	# x=x.replace(u"}",' ')
	# x=x.replace(u"&quot;",' ' )
	# x=x.replace(u"&gt;",' ')
	# x=x.replace(u'|',' ')
	# x=x.replace(u"&amp;",' ')
	# x=x.replace(u'&nbsp',' ')
	# x=x.replace(u'=',' ')
	# x=x.replace(u'/',' ')
	# x=x.replace(u'?',' ')
	# x=x.replace(u'<',' ')
	# x=x.replace(u'>',' ')

	return x


# def getExternalLinks3(data):
# 	Alllinks=data.split("== external links ==")
# 	Externallinks=[]
# 	n=len(Alllinks)
# 	if n>1:
# 		links=Alllinks[1];
# 		for x in links.split('\n'):
# 			if "* [" in x or "* {" in x or "*[" in x:
# 				val=x.split(' ')
# 				val=val[2:]
				
# 				for i in val:
# 					Externallinks.append(i)

# 	text=getNonStopwords(" ".join(Externallinks))
# 	text=getStemmedTokens(" ".join(text))				
# 	return text			

# def getExternalLinks2(data):
# 	Alllinks=data.split("==external links ==")
# 	Externallinks=[]
# 	n=len(Alllinks)
# 	if n>1:
# 		links=Alllinks[1];
# 		for x in links.split('\n'):
# 			if "* [" in x or "* {" in x or "*[" in x:
# 				val=x.split(' ')
# 				val=val[2:]
				
# 				for i in val:
# 					Externallinks.append(i)

# 	text=getNonStopwords(" ".join(Externallinks))
# 	text=getStemmedTokens(" ".join(text))				
# 	return text			

# def getExternalLinks(data):
# 	data2=data
# 	postlist=defaultdict(int)
# 	Alllinks=data.split("==external links==")
# 	Externallinks=[]
# 	n=len(Alllinks)
# 	if n>1:
# 		links=Alllinks[1];
# 		for x in links.split('\n'):
# 			if "* [" in x or "* {" in x or "*[" in x:
# 				val=x.split(' ')
# 				val=val[2:]
				
# 				for i in val:
# 					Externallinks.append(i)

# 	text=getNonStopwords(" ".join(Externallinks))
# 	text=getStemmedTokens(" ".join(text))
# 	text+=getExternalLinks2(data2)+getExternalLinks3(data2)

# 	for word in text:
# 		try:
# 			postlist[word]+=1
# 		except KeyError:
# 			postlist[word]=1

# 	# for k,v in postlist.items():
# 	# 	print k,v
# 	return postlist			


		


def getTitle(data):
	postlist=defaultdict(int)
	titledata=data
	data=getNonStopwords(data)
	data=getStemmedTokens(" ".join(data))
	for word in data:
		try:
			postlist[word]+=1
		except KeyError:
			postlist[word]=1
	return postlist

