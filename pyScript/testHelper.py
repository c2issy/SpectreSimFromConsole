################################################33
#Description: script to test the helper module
#Creation Data: 8/30/17
#Author: Yingqiu Cao (CC)
#Modification log


##test code for readFromTail function
file=open("vout","rb+") #open the file 
import helper
result=helper.readFromTail(file,2) #read the last n lines from the file
print(result)
