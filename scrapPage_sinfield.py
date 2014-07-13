#Extract informztion from the webpage of Seinfeld case study
#
#
#Computational steps of the code:
#
#Part 1: Import relevant python modules  
#
#Part 2: Define the URL of Seinology web site
#
#Part 3: Parse the data fetched from Seinology web site following the procedure 
#        of the web author 
#        Save the data in a file for later use in the code 
#
#Part 4: Get the page souce of the Wikitionary English Frequency List of TV scripts
#Note  : The page has been downloaded manually, trimmed and fed into the main code 
#        The html format of the page source is named as "htmlFreqList.doc" and
#        saved in the working dictionary  
#
#        Read through the page source and Extract (clean) data as a long list  
#        Transfer data from the list to a 2D Table 
#       
#        The web author save the content of the English Frequency List
#        In this code this was avoided by holding the data in the 2D Table 
#        and then transfer it to a dictionary called 'sranks'
#
#Part 5: Compare the frequency of words reported in the wikitionary to those 
#        obtained from the Sienfeld scripts 
#        Save the 2D Table in a csv file



#################################################################################
#Beginning of the program   
#
#Part 1: Import relevant python modules
import sys
import urllib, urllib2
from bs4 import BeautifulSoup 
#Part 1 ends



#################################################################################
#Part 2: This section pulls data from the Seinology web site and save it in a file
#
#Set the maximum depth of the Python interpreter stack to limit=2000
sys.setrecursionlimit(2000) 

#Open a file to write and append the contents of the scripts 
f = open("data1.txt","a")
f.truncate()

print '                             '
#Define a function to use the scripts  
#Exception handling (try and except) implemented
def getStuff(script): 
    try:                            
        #Load the content from the url into a BeautifulSoup object
        urlAddress = urllib2.urlopen("http://www.seinology.com/scripts/script-" + script + ".shtml")
        urlContent = urlAddress.read()
        soup       = BeautifulSoup(urlContent)

        #Navigate the soup and find url content with <p> tag
        p = soup.findAll("p") 
        #scripts are inside the 4th <p> in the document
        f.write(str(p[3]))          

        print "Done with script " + script
    except:
        print "Unable to open script " + script


#Looping through the scripts
#Append everything to the file 'data1.txt'
print 'Getting data from Seinology web site ... .... ...'

lownums = ["01","02","03","04","05","06","07","08","09"] 

for num in lownums:
    getStuff(num)

for i in range(10,177):
    getStuff(str(i))

f.close()
#Part 2 ends




#################################################################################
#Part 3 : This section parse the fetched data 
#
#The baic idea is to select only dialogue lines, then split every word, remove 
#punctuation, and count the number of times each word occurs following the 
#dictionary data structure

#Open the data file that was created earlier 
f = open("data1.txt","r")
 
#Look at dialogue lines which always have a colon and pass it in the string 
#Create an empty string 
text = ""
for line in f:
  if ':' in line:
    text = text + line
 
f.close()
 

#Create a list of punctuation marks which might be present in each line of the text 
punctuationMarks = ['!',',','.',':','"','?','-',';','(',')','[',']','\\','/']

#Create an empty dictionary 
dict = {}

#Split the text and create a list of strings called 'words' 
words = text.lower().split()
#print len(text), len(words)

#Loop through each of the elements of the 'words' list 
for word in words:
 
  for mark in punctuationMarks:
    if mark in word:
      word = word.replace(mark,"")
 
  if word in dict:
    dict[word] += 1
  else:
    dict[word] = 1
 

#Create a file to store the count of individual word, 
#and the number of times each word appear in the list  
f = open("counts.txt","w")
f.truncate()
 
for word, count in dict.items():
  f.write(word + "\t" + str(count) + "\n")
 
f.close()
#Part 3 ends 



#################################################################################
#Part 4: Wikitionary English frequency List based off of TV scripts
#
#Create the soup from the Wikitionary page source 
print 'Creating the soup from the Wikitionary page source ... ....'
soup   = BeautifulSoup( open('./htmlFreqList.doc') )
tables = soup.findAll('table') 

#print 'Creating the long list ... ... ... ... ...'
data = []                            #define an empty list
for tb in tables:                    #loop over tables
    rows = tb.findAll('tr')
    i=0
    for tr in rows:
        cells = tr.findAll('td')
        for td in cells:
            data.append( str(td.getText()) )  #append each cell to the data list

cNum   = 3                                    #number of columns in the Frequency List 
rNum   = int(len(data)/cNum)-1                #number of rows excluing the column header
array2D= [cNum*[0] for x in range(rNum)]      #2D Array

data2 = data[3:]                              #exclude the column header (first row)
k=0
for d1 in range(rNum):
    for d2 in range(cNum):
        array2D[d1][d2]= data2[k]
        k = k + 1
#Part 4 ends



#################################################################################
#Part 5: This section compare the frequency of words reported in the wikitionary 
#to those obtained from the Sienfeld scripts 
#
#Create an empty dictionary and transfer word and their frequencies from Sienfed 
#scripts to this dictionary
sranks = {}
for d1 in range(rNum):
        word = array2D[d1][1]
        value= array2D[d1][2]
        sranks[word] = value
        

#The data file 'counts.txt' created in part 3 has been modify to remove blanks and 
#some stray HTML. The file has been re-named as 'eranks.txt'
f = open("eranks.txt","r") 
eranks = {}

for line in f:
  pair = line.split()
  word = pair[0]
  value = pair[1]
  eranks[word] = value
 
f.close()
 

print 'Creating the final data file compare.txt ... ... ...' 
f = open("compare.txt","w")
f.write("Word\tSRank\tERank\n")
for word, count in sranks.items():
  if word in eranks:
    f.write(word + "\t" + str(count) + "\t" + str(eranks[word]) + "\n")
 
f.close()
#Part 5 ends


#End of the program
