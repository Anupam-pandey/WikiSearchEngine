#!/usr/bin/python
# -*- coding: utf-8 -*-
import heapq
import os
import xml.sax
import re
import sys  
import math  
reload(sys)
sys.setdefaultencoding('utf8')
import managedata
import timeit
from collections import defaultdict
import collections 
titleID=open("IndexFolder/Title-ID.txt",'w')
Index = defaultdict(list)
count = 0
countdoc = 0
offset = 0
countFile=0
class WikiParser( xml.sax.ContentHandler ):
  parentid=0


  def __init__(self):
    self.bufferId = ""
    self.bufferText = ""
    self.inTitle = False
    self.bufferTitle = ""
    self.inId=False
    self.inText=False     
    self.inPage = False
    self.EL={}
    self.title={}
    self.Index=defaultdict(list)
    self.Infobox={}
    self.catagory={}
    self.page={}

  # Call when an element starts

  def startElement(self, tag, attributes):
    if tag == "page":
      self.inPage=True
      global countdoc
      countdoc+=1

      self.catagory={}
      self.EL={}
      self.Info={}
    elif tag == "title":
      self.bufferTitle=""
      self.inTitle=True
    elif tag == "id" and WikiParser.parentid==0:
      WikiParser.parentid=1
      self.inId=True
      self.bufferId=""
    elif tag == "text":
      self.inText=True
      self.bufferText=""
      

  
    # Call when an elements ends
  def endElement(self, tag):
    self.CurrentData = tag
    if tag == "text":
      self.inText=False
    elif tag == "id" :
      #print self.bufferId
      self.inId=False
    elif tag == "title":

      self.inTitle=False
    elif tag == "page":
      global count,countFile
      global Index
      self.title=managedata.getTitle(str(managedata.normalize(self.bufferTitle.lower().replace(u'_',' '))))
      self.catagory,self.Infobox,self.page,self.EL= managedata.getCatagoryInfobox(str(managedata.normalize(self.bufferText.lower().replace(u'_',' '))))
      indexing(sys.argv[2],self.page,self.Infobox,self.catagory,self.title,self.EL,self.bufferId)
      try:
        titleID.write(self.bufferId+'-'+self.bufferTitle+'\n')
        WikiParser.parentid=0
        count+=1
        if count%30000==0:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
          print count
          Index=collections.OrderedDict(sorted(Index.items(), key=lambda t: t[0]))
          file = open("IndexFolder/"+sys.argv[2]+'_'+str(countFile)+".txt","w") 
          for k,v in Index.items():
              if(len(k)>3):
                d=k+' '+" ".join(v)+'\n'
                file.write(d)
          Index=defaultdict(list)
          countFile+=1
      except:
        pass    

      self.inPage=False
  def endDocument(self):
    titleID.close()
    print "doc ended"
    #file.close()


  # Call when a character is read
  def characters(self, content):
    if self.inId and WikiParser.parentid==1:
      self.bufferId=content     
    elif self.inTitle:
      self.bufferTitle+=content
    elif self.inText:
      self.bufferText+=content

 
offset=0
def indexing(filename,page,infobox,title,category,externallinks,ID):
  global Index
  global count
  Indexkey=list(set(page.keys()+title.keys()+infobox.keys()+category.keys()+externallinks.keys()))
  Indexvalue=""
  global offset

  for k in Indexkey:
    try:
      summ=0
      value=""
      if title[k]>=1:
        try:
          summ+=round(title[k]/float(len(title)),3)
          value+='t'+(str(round(title[k]/float(len(title)),3)))
        except:
          pass
      if(page[k]>=1):
        try:
          summ+=round(page[k]/float(len(page)),3)
          value+='b'+(str(round(page[k]/float(len(page)),3)))
        except:
          pass
      if(infobox[k]>=1):
        try:
          summ+=round(infobox[k]/float(len(infobox)),3)
          value+='i'+(str(round(infobox[k]/float(len(infobox)),3)))
        except:
          pass
      if(category[k]>=1):
        try:
          summ+=round(category[k]/float(len(category)),3)
          value+='c'+(str(round(category[k]/float(len(category)),3)))
        except:
          pass
      if(externallinks[k]>=1):
        try:
          summ+=round(externallinks[k]/float(len(externallinks)),3)
          value+='e'+(str(round(externallinks[k]/float(len(externallinks)),3)))
        except:
          pass
      value=str(ID)+':'+str(summ)+':'+value   
      Index[k].append(value)
    except:
      pass  
    
  #return Index

def MergeIt(Indexname,totalfiles):
  try:
    fileIndexes=[0]*(totalfiles+1)
    filetopline={}
    global countdoc
    listoftoplines={}
    data=defaultdict(list)
    heap=[]
    IndexFile={}
    Secondary_Index=open("IndexFolder/SecondaryIndex.txt","w")
    start_key=""
    for i in xrange(totalfiles):
      filename=Indexname+str(i)+".txt"
      IndexFile[i]=open(filename,"r") 
      filetopline[i]=IndexFile[i].readline().strip()
      listoftoplines[i]=filetopline[i].split(' ',1)
      listoftoplines[i][0]=listoftoplines[i][0].strip()
      #print listoftoplines

      if listoftoplines[i][0] not in heap:
              heapq.heappush(heap, listoftoplines[i][0])
      fileIndexes[i]=1
    filecounter=0  
    counter=0
    while any(fileIndexes)==1:
      firstelement=heapq.nsmallest(1, heap)
      firstelement=" ".join(str(x) for x in firstelement)
      firstelement=firstelement.strip()
      heapq.heappop(heap)
      counter+=1
      tokens=20000  
      if counter%tokens==0:
        flag=0
        with open("IndexFolder/Index"+str(filecounter)+".txt","w") as file:
          for k in sorted(data.keys()):
              if flag==0:
                start_key=k
                flag=1
              df= round(math.log(countdoc/float(len(data[k]))),3)
              d=str(k)+'-'+str(df)+'-'+" ".join(data[k])+'\n'
              file.write(d)
        end_key=k        
        Secondary_Index.write(start_key+'-'+end_key+' '+str(filecounter)+'\n')
        #file.close()
        filecounter+=1
        data.clear()
      for x in xrange(totalfiles):
        if fileIndexes[x]:
          if listoftoplines[x][0]==firstelement:
            data[firstelement].extend(listoftoplines[x][1:])
            filetopline[x]=IndexFile[x].readline().strip()  
            if filetopline[x]=='':
              fileIndexes[x]=0
              IndexFile[x].close()
              os.remove(Indexname+str(x)+".txt")
            else:
              listoftoplines[x]=filetopline[x].split(' ',1)
              if listoftoplines[x][0] not in heap:
                  heapq.heappush(heap, listoftoplines[x][0])
    flag=0
    with open("IndexFolder/Index"+str(filecounter)+".txt","w") as file: 
      for k in sorted(data.keys()):
        if flag==0:
          start_key=k
          flag=1
        df= round(math.log(countdoc/float(len(data[k]))),3)
        d=str(k)+'-'+str(df)+'-'+" ".join(data[k])+'\n'
        file.write(d)
      end_key=k        
      Secondary_Index.write(start_key+'-'+end_key+' '+str(filecounter)+'\n')
      Secondary_Index.close()
    #file.close()
    data.clear()              
  except:
    pass  












    
def master():
  parser = xml.sax.make_parser()
  global Index,countFile,count
  # override the default ContextHandler
  Handler = WikiParser()
  parser.setContentHandler( Handler )

  parser.parse(sys.argv[1])
  Index=collections.OrderedDict(sorted(Index.items(), key=lambda t: t[0]))

  try:
    file = open("IndexFolder/"+sys.argv[2]+'_'+str(countFile)+".txt","w") 
    for k,v in Index.items():
        if(len(k)>3):
          d=k+' '+" ".join(v)+'\n'
          file.write(d)
    countFile+=1
    Index.clear()
    MergeIt("IndexFolder/"+sys.argv[2]+'_',countFile)
  except:  
    pass  
if ( __name__ == "__main__"):
  # create an XMLReader
 # global countFile
  start = timeit.default_timer()
  master()
  print countFile  
  stop = timeit.default_timer()
  print "Time to execute : ",stop - start
