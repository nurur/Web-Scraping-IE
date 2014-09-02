WebScraping-IE
===============

Web scraping is a data mining techniques which falls under the hood 
of information extraction (IE). This method is used to obtain both 
structured and unstructured data from the web. If the scrapped data 
is unstructured it is then converted to structured format for various 
data mining purposes. 

This repo contains python codes for extracting various types of data 
(tabular, non-tabular, plain text etc.) from from various web pages. 
The R codes to perform the exactly same tasks will be added soon.
 
The upcoming source codes will contain information extraction tricks 
from the following page:

1. http://www.fec.gov/finance/disclosure/srssea.shtml : This page 
creates a table as an output but the tricky part is that the table 
is created dynamically which can not book-marked. The existing codes 
in this repo can not be used to extract this dynamic table because 
they lack necessary tricks. This is a work in progress.   
 



Note 1:

The attribute hotness of a professor (www.ratemyprofessors.com) in 
ratingsJRC_prof.xlsx and ratingsUNI_prof.xlsx files:

hotness = 3: Strong    (hotness >= 20)

hotness = 2: Spicy     (hotness >= 10  and hotness < 20)

hotness = 1: Seasoned  (hotness > 1 and hotness < 10)

hotness = 0: Savory    (hotness = 0) 