#Save plot as a pdf file 
pdf('scrapUnivData.pdf')


#Multiplot Option 
par(mfrow=c(3,2))


#Read the data 
a  = read.table(file="scrapUnivData.csv", header=TRUE, sep=",")
accep=a[,2]
enrol=a[,3]
gradu=a[,4]
rente=a[,5]
tuiti=a[,6]



hist(enrol, nclass=25, col="blue", lwd=3, probability=TRUE, 
     xlab='Number of Enrollment',
     ylab='Norm. Freq.', 
     main='Distribution of Enrollment at the Top Univ.s',
     cex.axis=0.8, cex.main=0.8, cex.lab=0.8)


plot(enrol,gradu,      
     xlab='Number of Enrollment',
     ylab='Number of Graduation', 
     main='Enrollment vs. Graduation at the Top Univ.s',
     cex.axis=0.8, cex.main=0.8, cex.lab=0.8, 
     pch=1, cex=0.75, col='red')


boxplot(enrol,      
     ylab='Number of Enrollment',
     main='Distribution of Enrollment Only',
     cex.axis=0.8, cex.main=0.8, cex.lab=0.8,
     col='green')


boxplot(gradu, horizontal=TRUE, 
     xlab='Number of Graduation', 
     main='Distribution of Graduation only',
     cex.axis=0.8, cex.main=0.8, cex.lab=0.8, 
     col='yellow')



plot(enrol,gradu,    
     xlim=c(0,42000), ylim=c(0,42000),   
     xlab='Number of Enrollment',
     ylab='Number of Graduation', 
     main='Enrollment vs. Graduation at the Top Univ.s',
     cex.axis=0.8, cex.main=0.8, cex.lab=0.8, 
     pch=1, cex=0.75, col='red')

abline( lm(gradu~enrol) )



#Return output to the terminal
dev.off()
