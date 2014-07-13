Web-Scraping-IE
===============

Web scraping is used to obtain structured and unstructured data from 
the web and convert the data into structured format for various data 
mining purposes. This task belongs to a data mining techniques named 
information extraction (IE). 

This repo contains python codes for extracting various types of data 
(tabular, non-tabular, plain text etc.) from from various web pages. 
The R codes to perform the exactly same tasks will be added soon.
 

The upcoming source codes will contain information extraction tricks 
from the following pages:

1. http://www.fec.gov/finance/disclosure/srssea.shtml : This page 
creates a table as an output but the tricky part is that the table 
is created dynamically which can not book-marked. The existing codes 
in this repo can not be used to extract this dynamic table because 
they lack necessary tricks. This is a work in progress.   
 

2. http://www.ratemyprofessors.com/toplists/topLists.jsp : This page 
does not show data in the tabluar form at all! I want to scrap the 
page and want to create a table where each row will contain the name 
of the profressor and various attributes promoted in this webpage 
such as quality, helpfulness, clarity, easiness, and hotness. My plan 
is to use the data for hierarchical regression study. The hierarchical 
regression assesses teh significance of the inclusion or exclusion of 
an attribute in a given model. This is work in progress.
 


  