################################################
#Description: script to call cadence simulation
#             and run optimization of VFs
#Creation Date: 8/30/17
#Author: Yingqiu Cao (CC)
#Modification log
###############################################
import os
import helper

#####################################################################
#input arguments that should be loaded to the writeOcn.py file 
#specify the directory to save the charge pump simulation files
rundir="/work/yc923/ocean/autoCP"
seperator="/"
oceanFileName="start.ocn"

#initialize the parameters used in simulation
vinp=0.15 #peak voltage of the input ac signal
VF=[0.6,0.6,0.6,0.6,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.4]  #initial voltage of the floating gates of the diodes
stopTime=5000 #stop time of the transient simulation, in ns
startTime=stopTime-10  #start time to save the output transient signal
stepSize=0.1 #step size to sample the output waveform, in ns. By default, the operating freq is 1G Hz, a stepSize of 0.1 ns gives 10 data points per cycle
################################################


################################################
#
from bs import linearSearch
search=linearSearch(vinp,startTime,stopTime,stepSize,rundir,seperator,oceanFileName)

#vout=search.runSim(VF)
#print(vout)

#VOUT=search.runSim(list(VF))
#print(VOUT)

deltaV_low=0.2
deltaV_high=0.2
init_grid=0.1
stop_grid=0.02 #20mV
startStage=0
count=4


result=search.searchVF(VF,startStage,count,deltaV_low,deltaV_high,init_grid,stop_grid,rundir)

print("optiVF:",result[0],"maxVout:",result[1])

