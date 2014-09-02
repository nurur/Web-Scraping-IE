# Author: Nurur Rahman
#
# Web Scraping using base package readLines() function 
# Parsing is done with regular expression 
#
#
# This script scrapes the web-site 'industrialfansdirect.com' using R
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
# fan_Bathroom-fans.R.xlsx 
# fan_Circulating.R.xlsx 
# fan_Duct-inline.R.xlsx  
# fan_Explosion-proof.R.xlsx 
# fan_Fire-safety.R.xlsx 
# fan_Roof-exhaust.R.xlsx
# fan_Supply-fans.R.xlsx   
# fan_Wall-ventilation.R.xlsx
# fan_Whole-house.R.xlsx
#
#
#
#### Load appropriate libraries 
lapply( c("xlsx"), library, character.only=TRUE )


#### Main webpage 
mainURL <- 'http://www.industrialfansdirect.com/'

# Fan category -> Models 
# Two loops 
#fanCat <- c('ceiling','air-curtain','evaporative-cooling',
#	     'mancoolers','portable-cooling','air-movers', 
#	     'confined-space', 'high-velocity')


#### Fan category -> Sub-categories -> Models 
## Three loops 
fanCat  <- c('circulating', 'duct-inline', 'wall-ventilation', 
	     'explosion-proof','roof-exhaust', 'bathroom-fans', 
	     'supply-fans','fire-safety','whole-house')


# Define an empty data frame for a given fan type 
# colName: fanCat,fanType,Model,Brand,Build,Shipment,Warehouse,MSRP,DisPrice
colNum  <- 9     
rowName <- c()
colName <- c('Category','Type','Model','Brand','Build','Shipment',
	     'Warehouse','MSRP','DiscountPrice')


d1      <- length(fanCat)

#### Loop over fan categories 
for (i in 1:d1) {
    list1 <- readLines( paste0(mainURL, fanCat[i], '.html') )
    pattern <- '<option value=\"[(A-Z)-]+\\d*\"'
    x <- grep(pattern, list1, value=TRUE)
    x <- gsub('["]>.*','', x)
    a <- gsub('[^(A-Z0-9)-]+', '', x)
    
    y <- grep('<option value=\"[(A-Z)-]+\\d*\"', list1, value=TRUE)
    y <- gsub('<.*["]>','', y)
    fanType <- gsub('<.*', '', y)


    # Define an empty list for a given fan category 
    myList <- list()

    typePage <- paste0(mainURL, a, '.html')
    d2 <- length(a)

    cat('\n')
    cat('--------------------------------------------', '\n')
    cat('Fan Type: ', fanCat[i], '\n')
    cat('Printing various types of', fanCat[i], '\n')
    cat('--------------------------------------------', '\n')
    cat('\n') 


    #### Loop over types (sub-categories)
    for (j in 1:d2){    	
   	list2   <- readLines( typePage[j] )
    	pattern <- '.*<b style="font.*>[(A-Z0-9)*].*>'
    	b <- grep(pattern, list2, value=TRUE)
	b <- gsub('<.*>', '', gsub('(<.*\".*\">)*', '', b))
    	

	d3 <- length(b)
	if (d3 !=0 ){
	modelPage <- paste0(mainURL, a[j], '/', b, '.html')

	cat('', '\n')
   	cat('Fan Type: ', fanType[j], '\n')
   	cat('Printing various models of', fanType[j], '\n')
	cat('', '\n')

	# Define an empty data frame for a given fan type 
	df <- data.frame(matrix(NA, nrow=1, ncol=colNum, 
	                 dimnames =list(rowName, colName) ))



    	#### Loop over models (sub-sub-categories)
    	for (k in 1:d3){
    	list3 <- readLines( modelPage[k] )

        # Model 
    	x1 <- grep('<b style=.*>Model', list3, value=T)
    	x1 <- unlist(strsplit(unlist(strsplit(x1, '</b>')), '>Model:'))[2]
    	x1 <- str_trim(x1)

	# Brand
     	 n <- grep('Brand', list3)
    	x2 <- grep('[a-z0-9]', list3[n+1], value=T)  
    	x2 <- gsub('[^A-Za-z]', '', x2)
	if (length(x2) == 0){ x2 = 'Unknown'}

	# Build Time 
       	 n <- grep('Build Time', list3)
        x3 <- grep('[a-z0-9]', list3[n+1], value=T)  
        x3 <-  str_trim( gsub('<!.*', '', x3) )
	if (length(x3) == 0){ x3 = 'Unknown'}

	# Shipping Method 
     	 n <- grep('Ships By:', list3)
    	x4 <- grep('[a-z0-9]', list3[n+1], value=T)
    	x4 <- str_trim( gsub('<br>', '', x4) )
	if (length(x4) == 0){ x4 = 'Unknown'}

	# Location of warehouse
	 n <- grep('Warehouse', list3)
	x5 <- grep('<b.*>', list3[n+1], value=T)
   	x5 <- str_trim( gsub('<br>', '', x5) )
	if (length(x5) == 0){ x5 = 'Unknown'}

	# Maximum retail price
     	x6 <- grep('MSRP', list3, value=T)
	x6 <- str_trim( gsub('[<bsr>:/A-Z:$]*', '', x6) )
	x6 <- as.numeric(x6)	

	# Discounted price
    	x7 <- grep('<b style.*>Only.*', list3, value=T)
    	x7 <- unlist(strsplit( gsub('[^$0-9.]+', '', x7), '[$]'))[2]
	x7 <- as.numeric(x7)	

	#cat(k, x1, x2, x3, x4, x5, x6, x7, '\n')

	# Create temporary data frame 
	tdf <- data.frame(X1=fanCat[i], fanType[j], x1, x2, x3, x4, x5, x6, x7)
	# Adjust the column names of tdf
	names(tdf) <- names(df)
	# Bind the row of tdf with df
	df  <- rbind(df, tdf)
    	} #Loop over fan models 


	# Pass the data frame to the myList
	myList[[j]] = df[-1, ]
	} #End of if statement 

	# There is a sub-sub-sub category. 
	else{   # Create a data frame of only one row
		myList[[j]] = data.frame(0)
		print ('There is a sub-sub-sub category!')
	     }
 	   #End of else statement 

    } #Loop over fan types 


    # Save data frames of myList in a work book
    # Define the name of the workbook
    workBook <- createWorkbook( type="xlsx" )

    # Capitalize the first letter of fan category
    # Using Perl=TRUE style replacement  
    category <- gsub('\\b([a-z])', '\\U\\1', fanCat[i], perl=T) 


    # Loop over the number of data frames
    for (ft in 1:d2) { 
    	myTable <- myList[[ft]]  
	if( nrow(myTable) > 1 ){
	    sheetName <- createSheet(workBook, sheetName=fanType[ft])
	    addDataFrame(myTable, sheet=sheetName, row.names=F,
	    	         startRow=1, startColumn=1)
	saveWorkbook( workBook, paste0('fan_',category,'.R','.xlsx') )
     	}
     }


} #Loop over fan categories
