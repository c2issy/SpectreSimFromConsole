#########################################
#Description: helper functions
#Creation Date: 8/30/17
#Author: Yingqiu Cao (CC)
#Modification log
########################################
import os


#read n lines from the last of the file
#extract the 2nd colume of data (V data)
#return the average of the nlines V data
def readFromTail(file,nlines):
	#strip the first 3 lines, because they're either empty or title
	for i in range(3):
		file.readline()

	#try reading the first line to figure out the bytes in each line
	first_line=file.readline()
	bytes_per_line=len(first_line)
	#print(first_line+"\n"+str(bytes_per_line))
	
	average=0 #the average of the nlines's V data

	for i in range(1,nlines+1):
		#move to the ith line from the end of the file
		file.seek(-i*bytes_per_line,2)  #f.seek(offset, fromWhere). fromWhere can be 0 for beginning of the file, 1 for current position, or 2 for end of file
		#read the ith line from the tail of the file
		cur_line=file.readline()
	        	
		#strip the first char which is " "	
		cur_list=list(cur_line.split('      '))   #by default the seperator is 6 spaces
		#print('cur_list is', cur_list)
		#print(cur_list[1])
		#cur_list[1] is the 2nd colume of data (V data)
		#convert from string to float
		this_voltage=float(cur_list[1])	
		average+=this_voltage

	return average/nlines



#check if the resultFile exist
#if so, clear it's previous contents
#if not, create the file
def openNewFile(resultFile):
	if not os.path.exists(resultFile):
		os.mknod(resultFile)
	#clear the outputfile
	else:
		f=open(resultFile,'w')
		f.close()


