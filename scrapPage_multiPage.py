#Extract information about various courses (GWU course listing)
#
#
#Computational steps of the code:
#
#Part 1: Import relevant python modules  
#Part 2: Define global variables 
#Part 3: Define the list of keywords identifying various Departments  
#Part 4: Begin loop over individual departments of GWU 
#        4a. Create the Soup
#        4b. Get (clean) data as a long list from each individual web site 
#        4c. Transfer Data from list to a 2D Table 
#        4d. Save the 2D table in a csv file



#################################################################################
#Beginning of the program   
#
#Part 1: Import relevant python modules  
import sys, csv
import urllib, urllib2
from bs4 import BeautifulSoup
#Part 1 ends



#################################################################################
#Part 2: Define global variables 
#number of cells to be read from the web table
cNum     = 8            
#number of cells that needs to be discard from the total number of cells in the web table
#negative sign to indicate discarding from the back of the list contains the total number 
#of cells this number is used in Get Data Part 1 of the code  
cNumback = -3      #A pythonic feature

#Part 2 ends


#################################################################################
#Part 3: Define URL and create the Soup
subID=["ACA",  "ACCY", "AMST",  "ANAT",  "ANTH", "APSC", \
       "ARAB", "AH",   "FA",    "ASTR",  "BIOC", "BISC", \
       "BMSC", "BIOS", "BADM" , "CHEM" , "CHIN", "CE",   \
       "CLAS", "CPS" , "CCAS" , "COMM" , "CSCI", "CNSL", \
       "CPED", "DNSC", "EALL",  "ECON",  "EDUC", "ECE",  \
       "EHS",  "ENGL", "EAP",   "EMSE",  "ENRP", "EPID", \
       "EXSC", "FILM", "FINA",  "FORS",  "FREN", "GEOG", \
       "GEOL", "GER",  "SEHD",  "GREK",  "HSCI", "HLWL", \
       "HSML", "HEBR", "HIST",  "HOMP",  "HONR", "HDEV", \
       "HOL",  "HMSR", "IMMU",  "ISTM",  "IDIS", "INTD", \
       "IAFF", "IBUS", "ITAL",  "JAPN",  "JSTD", "KOR",  \
       "LATN", "LSPA", "LING",  "MGT",   "MKTG", "MBAD", \
       "MATH", "MAE",  "MICR",  "MMED",  "MSTD", "MUS",  \
       "NSC",  "ORSC", "PATH",  "PSTD",  "PERS", "PHAR", \
       "PHIL", "PT",   "PA",    "PHYS",  "PHYL", "PMGT", \
       "PPSY", "PSC",  "PORT",  "PSMB",  "PSYD", "PSYC", \
       "PUBH", "PPPA", "REL",   "RESV",  "PHHS", "SEAS", \
       "SMPA", "SLAV", "SOC",   "SONO",  "SPAN", "SPED", \
       "SPHR", "STAT", "SMPP",  "SUST",  "TRDA", "TSTD", \
       "TURK", "UW",   "WLP",   "WSTU",  "YDSH"]


#Total number of subjects offered by GWU (The bigger loop variable)
subTOT = len(subID)

print '                                    '
#Part 4: Begin loop over individual subjects
for sub in range(subTOT):
    try:
        urlAddress = "http://my.gwu.edu/mod/pws/courses.cfm?campId=1&termId=201303&subjId=" + subID[sub]

        #Read the page content of the URL 
        #Use urlopen module of urllib package to read the page 
        pageContent= urllib.urlopen(urlAddress).read()
        print "URL opens successfully"
        print sub, ': Now reading the web site of ', subID[sub], ' Department'
    except:
        print "Error: Unable to open URL!"


    #Part 4a: Create soup using BeautifulSoup method of bs4
    print 'Creating the soup ... ... ... ... ... .... ... ...'
    soup       = BeautifulSoup(pageContent)

    #Use findAll method of BeautifulSoup to extract tables from the soup
    print 'Extracting data from the soup ... ... ... ... ....'
    table = soup.findAll('table') 
 
    #Part 4a ends


    #################################################################################
    #Part 4b: Get Data as a long list from the relevant table
    #Rows and Cells are within the table
    #For a given Row, Use findAll module to extract the Cells 
    #
    print 'Creating a long list containing the data ... ... .'
    data = []                                        #define an empty list
    for tb in table:                                 #loop over tables
        rows = tb.findAll('tr', {"align" : "center"}, {"class" : "tableRow2Font"})
        for tr in rows:
            cells = tr.findAll('td')
            for td in cells[:cNumback]:              #discard cell numbers from the back 
                data.append( str(td.getText()) )     #append each cell to the data list
 
    #Part 4b ends


    #################################################################################
    #Part 4c: Get the correct number of rows that need to be saved
    #Transfer Data from list to a 2D Table
    #Create a 2d Table with 8 Cells and relevant number of cells given by rNum  

    rNum = int(len(data)/cNum/3)

    array2D= [ cNum*[0] for x in range(rNum)]

    #Transfer Data list to the Table array 
    k=0
    for d1 in range(rNum):
        for d2 in range(cNum):
            array2D[d1][d2]= data[k]
            k = k + 1

    #Part 4c ends

    #re.sub(r"\n|\t", "", a)
    #re.sub(r"\n[\t]*", "", a)  #\n\n\t
    #re.sub(r"\W", "", a)       #white space 
    #for d1 in range(1,rNum):
    #    array2D[d1][2] = re.sub(r"\n|\t", "", array2D[d1][2])
    #    array2D[d1][5] = re.sub(r"\s",    "", array2D[d1][5])
    #    array2D[d1][6] = re.sub(r"^\s",   "", array2D[d1][6])
    #################################################################################
    #Part 4d: Save Table in a csv file
    print 'Writing data from the 2D array to the csv file ...' 
    outfile   = open('problem.2.'+subID[sub]+'.csv', 'w')
    writerObj = csv.writer(outfile, dialect='excel')

    for row in array2D:
        writerObj.writerow(row)

    outfile.close()
    print '                                                  '
    #Part 4d ends


#End of the Program
