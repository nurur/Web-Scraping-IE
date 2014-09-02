# Author : Nurur Rahman
#
# This script scrapes the web-site 'industrialfansdirect.com' using Python
# It extracts information about various categories and types 
# of fans used in home and commercial buildings   
#
# The web-site contains three distinct types of pages:
# 1. Fan category -> Models 
# 2. Fan category -> Sub-categories -> Models 
# 3. Fan category -> Sub-categories -> Sub-sub-categories -> Models 
#
# This script focuses on scraping the second type 
# Writing scripts for the other pages are simple extensions of the current script
#
#
# The output of the script:
#
# fan_Bathroom-fans.py.xlsx 
# fan_Circulating.py.xlsx 
# fan_Duct-inline.py.xlsx  
# fan_Explosion-proof.py.xlsx 
# fan_Fire-safety.py.xlsx 
# fan_Roof-exhaust.py.xlsx
# fan_Supply-fans.py.xlsx   
# fan_Wall-ventilation.py.xlsx
# fan_Whole-house.py.xlsx
#
#
#
#################################################################################
#Part 1: Import relevant python modules  
import sys, csv
import urllib, urllib2
from bs4 import BeautifulSoup
import pandas
from pandas import *
import re
#Part 1 ends

#################################################################################
#Part 2: Define global variables 
#number of column to be created using the web data 
colNum  = 9 
rowNum  = [] 
colName = ['Category', 'Type', 'Model', 'Brand', 'Build', 'Shipment',
           'Warehouse', 'MSRP', 'DiscountPrice']
#Part 2 ends

#################################################################################
#Part 3: Define a function to write xlsx file

def writeXlsxFile(dfList, fanCatelog, fanType):
    # fanCatelog : the name of the fan catelog 
    # fanType    : the list of fan types 
    replace = lambda f: f.group(1).upper()
    catName = re.sub('\A([a-z])', replace, fanCatelog)

    fileName= ''.join(['fan_', catName, '.py', '.xlsx'])
    writer = ExcelWriter(fileName)

    for n, df in enumerate(dfList):
        df.to_excel(writer, sheet_name=fanType[n], index=False)
    writer.save()
#Part 3 ends

#################################################################################
#Part 4: Define URL and create the soup
# Main webpage 
mainURL= 'http://www.industrialfansdirect.com/'

# Fan category -> Models 
# Two loops 
#fanCat <- c('ceiling','air-curtain','evaporative-cooling',
#	     'mancoolers','portable-cooling','air-movers', 
#	     'confined-space', 'high-velocity')


# Fan category -> Sub-categories -> Models 
# Three loops 
fanCat = ['circulating','duct-inline','wall-ventilation', \
          'explosion-proof','roof-exhaust', 'bathroom-fans', \
          'supply-fans','fire-safety','whole-house']


#Total number of fan categories (The bigger loop variable)
d1 = len(fanCat)

print ' '

#Loop over individual fan category 
for cat in range(0,d1):
    try:
        urlAddress = mainURL + fanCat[cat] + ".html"

        #Read the page content of the URL 
        #Use urlopen module of urllib package to read the page 
        pageContent= urllib.urlopen(urlAddress).read()
        print '--------------------------------------------------'
        print "URL opens successfully"
        print 'Now reading the web site of ', fanCat[cat], 'fans'
    except:
        print "Error: Unable to open URL!"

    #Part 4a: Create soup using BeautifulSoup method of bs4
    print 'Creating the soup ... ... ... ... ... .... ... ...'
    soup       = BeautifulSoup(pageContent)

    #Use findAll method to extract relevant tags from the soup
    print 'Extracting data from the soup ... ... ... ... ....'
    list1 = soup.findAll('option')


    # Collect information about various 'fan types'    
    a=[]; fanType=[]
    for item in range(len(list1)):
        pattern = '[A-Z]+\-[(A-Z)-]+\\d*'
        x = re.search( pattern, str( list1[item]) )
        y = re.sub( '<.*["]>', '', str( list1[item]) )
        y = re.sub('<.*>', '', y)
        if (x != None):
            a.append( x.group(0) )
            fanType.append( y )


    # Define an empty list for a given 'fan category' 
    myList = []

    d2 = len(a)
    typePage = ["".join([mainURL,a[type],".html"]) for type in range(d2)]

    print ''
    print 'Fan Category: ', fanCat[cat]
    print 'Printing various types of', fanCat[cat]
    print '--------------------------------------------------'
    print ''

    # Loop over types (sub-categories)
    for j in range(d2):
        urlTypes   = typePage[j]
        pageContent= urllib.urlopen(urlTypes).read()
        soup       = BeautifulSoup(pageContent)
        #Use findAll method to extract relevant tags from the soup
        list2   = soup.findAll('b') 

        pattern = '.*<b style="font.*>[(A-Z0-9)*].*>'
        b = [re.search(pattern, str(list2[x])) for x in range(len(list2))]
        b = [b[x].group() for x in range(len(b)) if b[x] != None]
        b = [re.sub('(<.*\".*\">)*', '', b[x]) for x in range(len(b))] 
        b = [re.sub('<.*>', '', b[x]) for x in range(len(b))]
        

        # The length of d3 
        # With the current style of code it gives 0 for case 3 written above
        # The following 'if' statement is a check for that 
        d3 = len(b)
        if (d3 != 0):

            modelPage = ["".join([mainURL,a[j],'/',b[model],".html"]) for model in range(d3)]

            print ''
            print 'Fan Type: ', fanType[j]
            print 'Printing various models of', fanType[j]
            print ''

            #Empty data frame 
            df = DataFrame( columns=colName )
    

            # Loop over models (sub-sub categories)
            for k in range(d3):
                urlModels  = modelPage[k]
                pageContent= urllib.urlopen(urlModels).read()
                soup       = BeautifulSoup(pageContent)
                #Use get_text method to extract relevant tags from the soup
                list3 = soup.get_text()
        
                # Model
                #x1 =[re.search('(<b style=.*Model:.*)',str(list3[x])) for x in range(len(list3))]
                #x1 = [x1[i].group(0) for i in range(len(x1)) if x1[i]!=None]
                #x1 = re.sub('<.*>', '', re.sub('<.*["]>','', x1[0]))
                #x1=(x1.split(':')[1]).strip()
                x1 = re.search('Model:\s[\w-]+', list3) 
                x1 = x1.group()
                if x1==None: 
                    x1 = 'Unknown'
                else:
                    x1 = (str(x1).split(':'))[1]
                    x1 =  x1.strip()
      
                # Brand
                x2 = re.search('Brand:\r(\w)+', list3)
                if x2==None: 
                    x2 = 'Unknown'
                else:
                    x2 = x2.group()
                    x2 = (str(x2).split('\r'))[1]
        
                # Build Time 
                x3 = re.search('Build Time:\r[\w\s?]+[\s]{2}', list3)
                if x3==None: 
                    x3 = 'Unknown'
                else:
                    x3 = x3.group()
                    x3 = (str(x3).split('\r'))[1]

                # Shipping Method
                x4 = re.search('Ships By:\r[\w\s?]+\s', list3) 
                if x4==None: 
                    x4 = 'Unknown'
                else:
                    x4 = x4.group()
                    x4 = (str(x4).split('\r'))[1]

                # Warehouse 
                x5 = re.search('Warehouse:\r[\w\s?]+\s', list3)
                if x5==None: 
                    x5 = 'Unknown'
                else:
                    x5 = x5.group()
                    x5 = (str(x5).split('\r'))[1]

                # Maximum retail price
                xx = re.search('MSRP:\s[\$\d,.]+[\w\s]+[\$\d,.]+', list3)
                xx = xx.group()
                xx = str(xx).split('Only')
                x6 = (xx[0].strip()).split('MSRP:')
                x6 = x6[1].strip()
                x6 = float( re.sub(r'[$,]', '', x6) )

                # Discouncted price 
                x7 = xx[1].strip()
                x7 = float( re.sub(r'[$,]', '', x7) )
        
                # Create a dict with model's information   
                tdf = {colName[0]: [fanCat[0]], \
                       colName[1]: [fanType[j]],\
                       colName[2]: [x1],\
                       colName[3]: [x2],\
                       colName[4]: [x3],\
                       colName[5]: [x4],\
                       colName[6]: [x5],\
                       colName[7]: [x6],\
                       colName[8]: [x7]}
        
                # Append the model to the data frame 
                df = df.append( DataFrame(tdf, columns=colName) ) 

            # Append data frame to the list
            myList.append(df)
        else: 
            print 'There is a sub-sub-sub category!'

    # Write the list fo data frame to a Excel file   
    writeXlsxFile(myList, fanCat[cat], fanType)
