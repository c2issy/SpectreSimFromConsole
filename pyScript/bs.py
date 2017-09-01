#######################################################################
#Description: Using linear search to find the optimum VF for each stage
#Creation Date: 8/31/17
#Author: Yingqiu Cao (CC)
#Modification log:
#	9/1/17
#	 -add function searchVF 
######################################################################

import os
import copy
import writeOcn
import helper

class linearSearch:
	
	#python class constructor
	def __init__(self,vinp,startTime,stopTime,stepSize,rundir,seperator,oceanFileName):
		#define instance variables
		#self.VF=VF
		self.vinp=vinp
		self.startTime=startTime
		self.stopTime=stopTime
		self.stepSize=stepSize
		self.rundir=rundir
		self.seperator=seperator
		self.oceanFileName=oceanFileName

	
	#function: perform cadence spectre simulation for the given list of VF and vinp
	#return the DC output voltage
	def runSim(self,VF):
		#run cadence spectre simulation
		#generator "start.ocn" file
		writeOcn.generateOcn(self.rundir,self.seperator,self.oceanFileName,self.vinp,VF,self.startTime,self.stopTime,self.stepSize) 
		#save the current directory so that we can change back to it after simulation
		curDir=os.getcwd()
		os.chdir('/work/yc923/Cadence')  #change to a directory that has cds.lib and other start up files
		#the ocean command line to run spectre simulation
		cmd = 'virtuoso -nograph -replay "{0}/{1}"'.format(self.rundir,self.oceanFileName)
		#calling cadence
		os.system( cmd )
		#change the directory back
		os.chdir(curDir)

		#clean up the .log files before they prevent simulation
		if os.path.exists('/home/yc923/CDS.log'):
			os.remove('/home/yc923/CDS.log')
		if os.path.exists('/home/yc923/CDS.log.cdslck'):
			os.remove('/home/yc923/CDS.log.cdslck')
		#os.remove('/home/yc923/.ocean_history')


		#open the file that saves the transient simulation result of Vout
		outFile=self.rundir+"/results/vout"
		f=open(outFile,"rb+")
		#get vout
		vout=helper.readFromTail(f,int(1/self.stepSize)) #assuming the operating freq is 1G Hz
		#close the file
		f.close()

		#return the DC output voltage
		return vout




	#function:perform linear sweep of VF,for count number of diodes, starting from diode indexed n, with given grid size
	#save list of VF and the corresponding vout to a result file
	#return the optimum VF and the maximum vout achieved with VF
	#input argument:
	#	-VF:the list of threshold voltages selected in previous rounds
	#	-n:the index of the current Vth in the VF list
	#	-count: the number of VFs to be added to VF list
	#	-deltaV_low: the lower bound of the threshold voltage that VF can take, relavant to the initial VF
	#	-deltaV_high:the upper bound of the threshold voltage than VF can take
	#	-grid: the stepSize of the threshold voltage in the sweepi
	#	-optiVF: the list that saves the optimum values of VF that gives max Vout
	#	-maxVout:the max Vout found during the search
	#	-resultFile: the file to save the simulated VF and vout to
	def sweepVF(self,VF,n,count,deltaV_low,deltaV_high,grid,optiVF,maxVout,resultFile):
		#print("current VF is:", VF)
		size=len(VF)
		
		if count==0:
			#perform spectre simulation, and read the DC output vout
			vout=self.runSim(VF)
			#print("returned VF is:",VF) #for debug purpose, let me inspect the recursion
			#save VF and vout to result file
			curResultFile=resultFile+"_step{0}".format(str(grid))
			f=open(resultFile,"a")   #append VF and vout
			for i in range(len(VF)):
				s="{0} ".format(VF[i])
				f.write(s)
			s="{0.4f}\n".format(str(vout))
			f.write(s) 
			f.close()		
			#find the VF that gives maxVout	
			if (vout>maxVout[0]):
				maxVout[0]=vout
				optiVF[:]=[]
				for j in range(len(VF)):
					optiVF.append(VF[j])				
			#print("optiVF is",optiVF)
			return


		#count>0
		for i in range(int((deltaV_high+deltaV_low)/grid+0.000001)+1):
			#set VF[n]
			tmp=VF[n]
			VF[n]=VF[n]-deltaV_low+i*grid
			self.sweepVF(VF,n+1,count-1,deltaV_low,deltaV_high,grid,optiVF,maxVout,resultFile)
			VF[n]=tmp




	#function:perform linear sweep of VF,for count number of diodes, starting from diode indexed n
	#initially the grid size for sweep is init_grid
	#then the grid size shrinks by 2 in each iteration, until it becomes smaller than or equal to the stop_grid
	#save list of VF and the corresponding vout to a result file
	#return the optimum VF and the maximum vout achieved with VF
	#input argument:
	#	-VF:the list of threshold voltages selected in previous rounds
	#	-n:the index of the current Vth in the VF list
	#	-count: the number of VFs to be added to VF list
	#	-low: the lower bound of the threshold voltage that VF can take
	#	-high:the upper bound of the threshold voltage than VF can take
	#	-init_grid: the stepSize of the threshold voltage in the sweep,initial value
	#	-stop_grid: the stop value of the grid size
	#	-resultFile: the file to save the simulated VF and vout to
	
	#return values:
	#	-optiVF: the list that saves the optimum values of VF that gives max Vout
	#	-maxVout:the max Vout found during the search

	def searchVF(self,VF,n,count,deltaV_low,deltaV_high,init_grid,stop_grid,resultDir):
		optiVF=[]
		maxVout=[0]

		cur_grid=init_grid #cur_grid saves the grid size for current iteration
		while(cur_grid>=stop_grid):
			#file to save the simulation results of current iteration	
			resultFile=resultDir+"/results"+"/out_stage{0}to{1}_step{2}".format(str(n),str(n+count-1),str(cur_grid))
			#create a file to save the sim result
			helper.openNewFile(resultFile)
			#perform linear sweep for the current grid
			self.sweepVF(VF,n,count,deltaV_low,deltaV_high,cur_grid,optiVF,maxVout,resultFile)
			#update VF, deltaV_low and deltaV_high
			#set initial value of VF to the optimum value found in the coarse grid
			for i in range(len(optiVF)):
				VF[i]=optiVF[i]
			deltaV_low=cur_grid
			deltaV_high=cur_grid
			#shrink the grid size by 2 times
			cur_grid=cur_grid/2
		
		#return optiVF and maxVout
		return [optiVF,maxVout]
