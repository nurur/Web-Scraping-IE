# This script scapes The Geroge Washington University webpage for course info
# Computer Science and Economics Dept for Spring and Fall of 2013 and 2014
# The script produces a bar graph showing the number of 'open' and 'closed' 
# courses 


# Get HTML document using RCurl package 
# Parse using XML package 
# Load packages
packages = c("RCurl","XML","plyr","ggplot2", "highlight")
lapply( packages, library, character.only=TRUE )



# Main URL
mainURL    <- "http://my.gwu.edu/mod/pws/courses.cfm"
# Additional parameter to be used in the complete URL
pageNUMBER <- c("1","2","3","4","5")
# Year and Term Name (spring=01, fall=03)
termNAME   <- c("201301", "201303", "201401", "201403")  
# Course Name
subjNAME   <- c("CSCI", "ECON") 


# Loop over the sequential links of the web page
for (i in 1:length(pageNUMBER)) {
    # Provide complete URL 
    # get HTML page source using "RCurl getForm()" function
    html.src <- getForm(mainURL,campId="1",termId=termNAME[1],subjId=subjNAME[1], 
                        pageNum=pageNUMBER[i])

    # Parse HTML document for R representation using "XML htmlParse()" function  
    html.docs <- htmlParse(html.src)

    # Get tables from HTML document as a 'list of data frames'
    html.tabs <- readHTMLTable(html.docs, header=FALSE, stringsAsFactors=FALSE)

    # Find the total number of tables
    length(html.tabs)

    # Check all tables 
    cat('\n')
    cat('Showing Tables from page', i, '\n')
    #str(html.tabs, max.level=1)


    # Select appropriate tables from the list of tables in 'html.tab' 
    # First, get the number of data frames inside table 'html.tab' 
    dfTot <- length(html.tabs)
    cat('Total number of data frames in the list of page', i, 'is', dfTot, '\n')

    # Second, run through the list of data frames to find appropriate data frames 
    # These data frames are the 'courses' offered 
    indTab <- vector();                 # empty vector of index of data frames  
    k <- 1;                             # loop index for empty vector

    # Third, loop over the list
    for (j in 7:dfTot){ 
    	dd <- html.tabs[[j]] 
    	cn <- length(colnames(dd))      # number of columns
    	   if (cn == 11){
       	      indTab[k] <- j
       	      k <- k+1
       	   }
        }

   # Finally, print indices on the screen
   cat('Indices of appropriate data frames: ', indTab, '\n')
   cat('\n')

   # Total numbe of indices 
   indLen <- length(indTab)

   # Create empty data frame with appropriate rows and cols (create only once)  
   # Assign names of the columns 
   if(i == 1){
   	# Get appropriate column names and numbers from the relevant table
	# Here I am interested in first 10 columns
	colNum  <- 10
   	# Get column names from the relevant table 
   	colName <- as.vector(apply( html.tabs[[6]][1,1:colNum], 2, paste, collapse=''))

   	# df  <- data.frame(matrix(NA, nrow=1, ncol=colNum, dimnames=list(c(), colName)))
   	# Assign Names of the cols 
   	df        <- data.frame( matrix(NA, nrow=1, ncol=colNum), stringsAsFactors=FALSE)
   	names(df) <- colName
   	df        <- df[-1, ] 
   	}

   # Clean approprite data frames 
   for (i in 1:indLen) {
       tab <- html.tabs[[ indTab[i] ]][1, 1:colNum]

       tmp <- data.frame(lapply(tab, 
             FUN <- function(x) (gsub("\t", "", as.character(x), fixed=TRUE))), 
	     stringsAsFactors=FALSE)

       names(tmp)  <- colName                    #Push the names of the columns 
       tmp$SUBJECT <- gsub("\n \n\n\n", " ", tmp$SUBJECT)  #Clean the column once again

       df <- rbind(df, tmp)                      #Build the final data frame 
       } 

} #Loop over the links ends



# Plot
# Convert STATUS as a factor for plotting purpose.
df$STATUS = as.factor(df$STATUS)
plot(df$STATUS)