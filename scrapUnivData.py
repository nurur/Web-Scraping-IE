#Extract information about various US colleges
# 
#Computational steps of the code:
#
#Part 1: Import relevant python modules  
#Part 2: Define the URL of the Site and Get the (clean) data as a long list  
#Part 3: Extract 1D data from the long list
#Part 4: Create pandas dataframe 
#Part 5: Save data in a csv file
#Part 6: Plot


#################################################################################
#Beginning of the program   
#
#Part 1: Import relevant python modules
import sys, csv
import urllib, urllib2
from bs4 import BeautifulSoup
import re
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl



#################################################################################
#Part 2: Define URL and create the Soup
page=['data', 'data/page+1', 'data/page+2', 'data/page+3', 'data/page+4', 'data/page+5', 'data/page+6',
      'data/page+7', 'data/page+8', 'data/page+9', 'data/page+10', 'data/page+11', 'data/page+12', 
      'data/page+13','data/page+14']
        
#Define an empty list. It collects all the data
dataList = []                                    

for num in range(len(page)):
    urlAddress="http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities/"+page[num]
    pageContent= urllib2.urlopen(urlAddress)
    
    print "URL of '" + page[num] + "' opens successfully"
                
    #Create soup using BeautifulSoup method of bs4
    print 'Creating the soup ... ... ... ... ... ... ... ....'
    soup       = BeautifulSoup(pageContent)
    
    #Use findAll method of BeautifulSoup to extract tables from the soup
    print 'Extracting data from the soup ... ... ... ... ....'
    table = soup.findAll('table') 
    #print len(table)
    
    print 'Adding data to the long list ... ... ... ... ... .'
    for tb in table:                                 #loop over tables
        rows = tb.findAll('tr', valign="top")
        for tr in rows:
            dataRow = []
            cells = tr.findAll('td')
            for td in cells:
                tmp = re.sub('[\s\n$#,]','', td.getText())
                tmp = re.sub('%(.+)?',  '', tmp)
                tmp = re.sub('in-state:\d+',  '', tmp)
                tmp = re.sub('out-of-state:', '', tmp)
                tmp = re.sub('N/A', '-9999', tmp)
                dataRow.append( tmp )        #append each cell to the dataRow list
            dataList.append(dataRow)         #append each dataRow list to dataList list
    print '                                                  '

#re.sub('[\$,]|%|%(.+)?', '', a)

#################################################################################
#Part 3: Extract 1D data for various plotting purposes
u = []
v = []
w = []
x = []
y = []

for i in range(0, len(dataList)):
    u.append(int(dataList[i][2]))    #tuition
    v.append(int(dataList[i][3]))    #enrolment
    w.append(float(dataList[i][4]))  #acceptance
    x.append(int(dataList[i][5]))    #retention
    y.append(int(dataList[i][6]))    #graduation


for i in range(0, len(u)):
    if (u[i] == -9999):
        u[i] = np.median(u)          #tuition
    if (v[i] == -9999):
        v[i] = np.median(v)          #enrolment
    if (w[i] == -9999.0):
        w[i] = np.median(w)          #acceptance
    if (x[i] == -9999):
        x[i] = np.median(x)          #retention
    if (y[i] == -9999):
        y[i] = np.median(y)          #graduation


#Convert graduation from percent in total number
#for i in range(len(y)):
#    y[i] = int(v[i]*y[i]/100.) 



#################################################################################
#Part 4: Create panadas dataframe
#fist create a dictionary  
pdict = {'tuition':u, 'enrollment':v, 'acceptance':w, 'retention':x, 'graduation':y}
#next pass the dictonary to the dataframe  
df    = pd.DataFrame(pdict)



#################################################################################
#Part 5: Save data frame as a csv file 
df.to_csv('scrapUnivData.csv')
#getDF=pd.read_csv('scrapUnivData.csv')
#print df


import MySQLdb as mdb
import pandas.io.sql as sql
#Get connect to dump the data in MySQL
con  = mdb.connect('localhost','root','mysql','mydata')

#If for the first time you create a table, then the following 'if_exists=replace' works
#sql.write_frame(df, name='scrapUnivData', con=con,  if_exists='replace', flavor='mysql')

#However, the approach 'if_exists=replace' does not work if you run your code 2nd time 
#and want to rewrite the table!
#
#The suggestion is 
#Create the table first and then  use the following two seperate commands
#sql.uquery("DELETE FROM scrapUnivData", con)
#sql.write_frame(df, name='scrapUnivData', con=con, if_exists='append', flavor='mysql')
#
#Putting all together
#sql.write_frame(df, name='scrapUnivData', con=con, 
#                if_exists='replace', flavor='mysql')
sql.uquery("DELETE FROM scrapUnivData", con)
sql.write_frame(df, name='scrapUnivData', con=con,  
                if_exists='append', flavor='mysql')

#Close connection 
con.close()


#Get connected to fetch the data from MySQL
con = mdb.connect('localhost','root','mysql','mydata')
df2 = sql.read_frame('select * from scrapUnivData', con)
#Close connection 
con.close()
#Check whether the dataframe has been fecthed correctly
print len(df2.index)
print df2.columns




#################################################################################
#Part 6: Plot
#Figure 1
plt.figure(1)   
plt.subplot(221)
pl.hist(v, 25, normed=1, histtype='stepfilled')
plt.xlabel('Enrollment', fontsize=10, color='red')
plt.ylabel('Norm Freq.', fontsize=10, color='red')
pl.tick_params(axis='y', which='major', labelsize=8)
pl.tick_params(axis='x', which='major', labelsize=6)


#X-Y plot: Enrollment vs Graduation
plt.subplot(222)
plt.plot(v, y, 'r.')
plt.xlabel('Enrollment', fontsize=10, color='red')
plt.ylabel('Graduation (in % of Enrollment)', fontsize=10, color='red')
pl.tick_params(axis='y', which='major', labelsize=8)
pl.tick_params(axis='x', which='major', labelsize=6)
#plt.setp(ax.get_yticklabels(), fontsize=8)
#plt.setp(ax.get_xticklabels(), fontsize=6)



#Box plot of Enrollment 
plt.subplot(223)
plt.boxplot(v, notch=False, sym='+', vert=True, whis=1.5,
        positions=None, widths=None, patch_artist=False,
        bootstrap=None, usermedians=None, conf_intervals=None)
plt.ylabel('Enrollment', fontsize=10, color='red')
pl.tick_params(axis='y', which='major', labelsize=8)
pl.tick_params(axis='x', which='major', labelsize=8)


#Box plot of Graduation 
plt.subplot(224)
plt.boxplot(y, notch=0, sym='+', vert=False, whis=1.5,
        positions=None, widths=None, patch_artist=False,
        bootstrap=None, usermedians=None, conf_intervals=None)
plt.xlabel('Graduation (in % of Enrollment)', fontsize=10, color='red')
pl.tick_params(axis='y', which='major', labelsize=8)
pl.tick_params(axis='x', which='major', labelsize=8)



#Figure 2
#Linear Regression plot
plt.figure(2)

b1 = np.array([[0]*2 for i in range(len(v))])
for i in range(len(v)):
    b1[i][0] = v[i]
    b1[i][1] = y[i]


b2 = b1[:,0].reshape(-1,1)
b0 = np.ones( (len(v),1) )
X = np.concatenate((b0, b2), axis=1)
Y = b1[:,1].T


#Obtain the vector of parameters 
w     = np.linalg.lstsq(X,Y)

line = np.zeros( (len(v),1) )
for i in range(len(v)):
    line[i] = w[0][0] + w[0][1]*v[i]

plt.plot(v,line, 'r-', v, y,'o')
plt.axis([0, 80000, 0, 100])
plt.xlabel('Enrollment', fontsize=12, color='red')
plt.ylabel('Graduation (in % of Enrollment)', fontsize=12, color='red')
pl.tick_params(axis='y', which='major', labelsize=10)
pl.tick_params(axis='x', which='major', labelsize=10)
   
plt.show()

