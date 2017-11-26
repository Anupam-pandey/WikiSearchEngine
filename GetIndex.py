import os
import sys
import filehandler
from collections import defaultdict
reload(sys)

def sumlist(list1,list2):
	return [sum(x) for x in zip(list1, list2)]



def tf(word, words):
	return str(word)


# def n_containing(word, wordlist):
# 	return sum(1 for words in wordlist if word in words)

# def idf(word, wordlist):
# 	return math.log(len(wordlist) / (1 + n_containing(word, wordlist)))

# def tfidf(word, words, wordlist):
# 	return tf(word, words) * idf(word, wordlist)
cnt=0
offset=0
Index = defaultdict(list)
def indexing(filename,page,infobox,title,category,externallinks,ID):
	global Index

	Indexkey=list(set(page.keys()+title.keys()+infobox.keys()+category.keys()+externallinks.keys()))
	#k=oldk=next(iter(Indexkey))
	Indexvalue=""
	global cnt
	global offset
	#temp=[]
	#Indexlist=[0,0,0,0,0]
#	Index=dict(Counter(page)+Counter(infobox)+Counter(title)+Counter(category)+Counter(externallinks))
	for k in Indexkey:


		#print k
		# if str(k)==str(oldk):
		# 	temp.append(page[k])
		# 	temp.append(infobox[k])
		# 	temp.append(title[k])
		# 	temp.append(category[k])
		# 	temp.append(externallinks[k])
		# 	Indexlist=sumlist(Indexlist,temp)	
		# 	print Indexlist
		# 	oldk=k
		# 	Index[k]=Indexlist
		# 	continue
		# else:
		# 	Indexlist=[0,0,0,0,0]
		# 	temp=[]









#		value=str(cnt)+' '
		value="D:"+str(ID)+' '
		if title[k]>=1:
		#	print title[k], type(title[k])
			value+='t'+(str(title[k]))
		if(page[k]>=1):
			value+='b'+(str(page[k]))
		if(infobox[k]>=1):
			value+='i'+(tf(infobox[k],infobox))
		if(category[k]>=1):
			value+='c'+(tf(category[k],category))
		if(externallinks[k]>=1):
			value+='e'+(tf(externallinks[k],externallinks))
		Index[k].append(value)
		#print k,value
		
		cnt+=1
		# if cnt%5000==0:
	 #      print count
	 #      offset = writeIntoFile(sys.argv[2], index, dict_Id, countFile,offset)
	 #      index=defaultdict(list)
	 #      dict_Id={}
	 #      countFile+=1

		# for k,v in Index.items():
		# 	print k,v
	return Index

		# Writer(sortedIndex,cnt,"file",path)
	# for k,v in sortedIndex.items():
	# 	if(len(k)>3) and not str(k).isdigit() and not re.search(r'\d', str(k)) and len(v)>0 :#and hashset[k]!=1:
	# 		#if len(v)>0:
	# 		print k," ",v
			#pass

			#hashset[k]=1
				#d,l=sumlist(v)
			#else:
			#	pass
	#Index = defaultdict(list)

	# 	cnt+=1
	# 	if cnt==50:
	# 		break
		





# def Writer(Index,offset,filename,path):
# 	datatowrite=""
# 	for k,v in Index.items():
# 		datatowrite+=k +' '+" ".join(v)+'\n'
# 	print datatowrite
	

	



	#print page
