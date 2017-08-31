################################################
#Description: script to call cadence simulation
#             and run optimization of VFs
#Creation Date: 8/30/17
#Author: Yingqiu Cao (CC)
#Modification log
###############################################
import os

#####################################################################
#input arguments that should be loaded to the writeOcn.py file 
#specify the directory to save the charge pump simulation files
rundir="/work/yc923/ocean/autoCP"
seperator="/"
oceanFileName="start.ocn"

#initialize the parameters used in simulation
vinp=0.3 #peak voltage of the input ac signal
VF=[0.30,0.30]  #initial voltage of the floating gates of the diodes
stopTime=10 #stop time of the transient simulation, in ns
stepSize=0.1 #step size to sample the output waveform, in ns. By default, the operating freq is 1G Hz, a stepSize of 0.1 ns gives 10 data points per cycle
################################################


###########################################
#run cadence spectre simulation
########################################
#generator "start.ocn" file
import writeOcn
writeOcn.generateOcn(rundir,seperator,oceanFileName,vinp,VF,stopTime,stepSize) 
#save the current directory so that we can change back to it after simulation
curDir=os.getcwd()
os.chdir('/work/yc923/Cadence')  #change to a directory that has cds.lib and other start up files
#the ocean command line to run spectre simulation
cmd = 'virtuoso -nograph -replay "{0}/{1}"'.format(rundir,oceanFileName)
#calling cadence
os.system( cmd )
#change the directory back
os.chdir(curDir)
