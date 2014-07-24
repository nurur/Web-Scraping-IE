# This script scrapes the website 'ratemyprofessors.com'
# It extracts information about popularities of professors in various junior col.s  
# The website conatins four distinct pages:
# (http://www.ratemyprofessors.com/toplists/topLists.jsp)
# 1. 'Highest Rated', 2. 'Hottest', 3. 'Top Schools', 4. 'Fun Lists'
#
# Part 1 of the script scrapes the page called 'Highest Rated' 
# and extracts IDs of each of professor given by this site  
# Part 2 uses this information and scrapes individual page of each 
# 'Highest Rated' junior college professors 


# Load appropriate libraries
library(xlsx)



# List of years the site is rating proferssors  
list2012 <- readLines("http://www.ratemyprofessors.com/toplists/getxmlfromstatic.jsp?file=top100ProfessorsJrColl_2012.xml")
list2011 <- readLines("http://www.ratemyprofessors.com/toplists/getxmlfromstatic.jsp?file=top100ProfessorsJrColl_2011.xml")
list2010 <- readLines("http://www.ratemyprofessors.com/toplists/getxmlfromstatic.jsp?file=top100ProfessorsJrColl_2010.xml")
list2009 <- readLines("http://www.ratemyprofessors.com/toplists/getxmlfromstatic.jsp?file=top100ProfessorsJrColl_2009.xml")


#listHOT     <- readLines("http://www.ratemyprofessors.com/toplists/getxmlfromstatic.jsp?file=hotProfessors_2012.xml")
#listUNI_TOP <- readLines("http://www.ratemyprofessors.com/toplists/getxmlfromstatic.jsp?file=topSchoolsUniv_2012.xml")
#listJRC_TOP <- readLines("http://www.ratemyprofessors.com/toplists/getxmlfromstatic.jsp?file=topSchoolsJrColl_2012.xml")


listYEAR <- c(2012,2011,2010,2009)
listJRC  <- c(list2012, list2011, list2010, list2009)


# Part 1
# Scrape the 'Highest Rated' page for Junior College Professors 
pID <- matrix(nrow=4, ncol=25)

for (i in 1:length(listJRC)) {
# Professor's ID in the website
aID     <- unlist( strsplit(listJRC[i], "<tid>") )
bID     <- unlist( strsplit(aID,    "</tid>") )
pID[i, ]<- bID[seq(2,50,2)]

# Professor's Name
afName  <- unlist( strsplit(listJRC[i], "<tfname>") )
bfName  <- unlist( strsplit(afName, "</tfname>") )
alName  <- unlist( strsplit(listJRC, "<tlname>") )
blName  <- unlist( strsplit(alName, "</tlname>") )
pName   <- paste(bfName[seq(2,50,2)], blName[seq(2,50,2)])

# Professor's Department 
aDept   <- unlist( strsplit(listJRC[i], "<tdept>") )
bDept   <- unlist( strsplit(aDept,  "</tdept>") )
pDept   <- bDept[seq(2,50,2)]

# Professor's School
aSchool <- unlist( strsplit(listJRC[i], "<sname>") )
bSchool <- unlist( strsplit(aSchool,"</sname>") )
pSchool <- bSchool[seq(2,50,2)]

# Professor's State
aState  <- unlist( strsplit(listJRC[i],  "<state>") )
bState  <- unlist( strsplit(aState,  "</state>") )
pState  <- bState[seq(2,50,2)]

# Professor's Overall Rank 
aRank   <- unlist( strsplit(listJRC[i],  "<overallRank>") )
bRank   <- unlist( strsplit(aRank,   "</overallRank>") )
pRank   <- bRank[seq(2,50,2)]
}

# Create a data frame to save these information 
#dfJRC  <- data.frame(id=pID[1,], name=pName, dept=pDept, 
#	              school=pSchool, state=pState, rank=pRank)




# Print an empty line for decration purpose 
cat('', '\n')



# Part 2
# Scrape 'individual page' of each 'Highest Rated' Junior College Professors

# Create a data frame of 1 row by 9 cols 
df  <- data.frame(matrix(NA, nrow=1, ncol=9), stringsAsFactors=FALSE)

# Loop over the years 
for (i in 1:length(listJRC) ) {

    # Loop over the professors 
    for (j in 1:length(pID[1,]) ) { 
    	nameList <- readLines( paste0('http://www.ratemyprofessors.com/ShowRatings.jsp?tid=', pID[i,j]), n=500)

    	#### Name of the professors
    	pattName <- '^.*<h2 id="profName".*>(.*)</h2>$'
    	x <- nameList[ grep(pattName, nameList, ignore.case = T) ]
 

	# Fill the data frame only if the ShowRatings exists
    	if (length(x) != 0) {
    	name <- gsub('</h2>', '',gsub('&nbsp;', ' ', gsub('<h2.*[=\\\"]>', '', x) ) )              #method 1
    	#name<- unlist(strsplit(unlist( strsplit((strsplit(x, '>')[[1]][2]), '<'))[1], '&nbsp;'))  #method 2

    	#### Information about the professors
    	pattInfo <- c('<li>School:', '<li>Department:', '<li>Location:')
    	info    <- seq(1,3)
    	for (k in 1:3){
    	    y   <- nameList[ grep(pattInfo[k], nameList, ignore.case = T) ]
	    tmp <- gsub('<li.*[=\\\"]>', '', y)
	    info[k] <- gsub('<.*', '', tmp)
	    }

    	#### Various Attributes of the professors
    	pattRate <- '^.*<li class="tTip" id=.* *.*>.*$'
    	z <- nameList[ grep(pattRate, nameList, ignore.case = T) ]

    	## Attribute 1: Quality
    	a  <- unlist( strsplit(z[1], 'strong') )
    	quality  <- gsub('[></]', '', a[2])
    	#a[3] <- gsub('><span>', '', unlist(strsplit(a[3], '</span>.*')))

    	## Attribute 2: Helpfulness
    	b  <- unlist( strsplit(z[2], 'strong') )
    	help  <- gsub('[></]', '', b[2])
    	#b[3] <- gsub('><span>', '', unlist(strsplit(b[3], '</span>.*')))

    	## Attribute 3: Clarity
    	c  <- unlist( strsplit(z[3], 'strong') )
    	clarity  <- gsub('[></]', '', c[2])
    	#c[3] <- gsub('><span>', '', unlist(strsplit(c[3], '</span>.*')))

    	## Attribute 4: Easiness
    	d  <- unlist( strsplit(z[4], 'strong') )
    	easy  <- gsub('[></]', '', d[2])
    	#d[3] <- gsub('><span>', '', unlist(strsplit(d[3], '</span>.*')))

    	## Attribute 5: Hotness		      
    	pattHot <- 'var status='
    	hot <- nameList[ grep(pattHot, nameList, ignore.case = T) ]	
    	hot <- gsub('[a-z =;]', '', hot)

    	## Rescale Hotness
    	if (hot >= 20) {hot = 3}  
    	else if (hot >= 10 & hot < 20) {hot = 2}  
    	else if (hot >= 1 & hot < 10) {hot = 1} 	 
    	else {hotness= 0} 	 


    	#### Create a temporary 1 row by 8 col data frame 
    	tmp <- data.frame(X1=name, X2=info[1], X3=info[2], X4=info[3],
                          X5=as.numeric(quality), 
			  X6=as.numeric(help), 
			  X7=as.numeric(clarity), 
			  X8=as.numeric(easy), 
			  X9=as.integer(hot), 
		      	  stringsAsFactors=FALSE)

        #### Combine the 'tmp' data frame with the existing 'df' data frame row-wise  
    	df <- rbind(df, tmp)
    	}


    	#### Print a wanring if the rating page of the professor is removed
    	else {
    	cat('Rating page of',pName[i],listYEAR[i],'has been removed!','\n')
    	} 

   } #End of the loop over the number of professors

} #End of the loop over the yers 



# Print an empty line for decration purpose 
cat('', '\n')


## Clean the data frame (i.e., remove the first row which contains 'NA') 
df <- df[-1, ]

## Assign appropriate names to the columns of the data frame    
colName   <- c('Name', 'School', 'Department', 'Location', 'Quality',  
               'Helfulness', 'Clarity', 'Easiness', 'Hotness')
names(df) <- colName


# Write the data frame as an Excel file
write.xlsx(df, 'ratingsJRC_prof.xlsx', sheetName='1', row.names=F, append=F)  


