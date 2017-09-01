#############################################
# Description: py script to write .ocn file
# for automatic charge pump simulation
# Creation Data: 8/28/17
# Author: Yingqiu Cao (CC)
# Modification log
# 8/30/17
#  -make this file a function, with the input arguments given by main.py
# 8/31/17
#  -deal with variable length of VF
############################################

import os
#import pdb

def generateOcn(dir,seperator,oceanFileName,vinp,VF,startTime,stopTime,stepSize):

	print 'generating "start.ocn" file ...'

	#VF0=VF[0]
	#VF1=VF[1]

	"""
	#########################################################
	#input arguments that should be loaded from the main file
	#specify the directory to save the charge pump simulation files
	dir="/work/yc923/ocean/autoCP"
	seperator="/"
	oceanFileName="start.ocn"

	#initialize the parameters used in simulation
	vinp=0.3 #peak voltage of the input ac signal
	VF0,VF1=0.3,0.3  #initial voltage of the floating gates of the diodes
	stopTime=20 #stop time of the transient simulation, in ns

	#########################################################
	"""

	#open up and write to the .ocn file
	oceanFilePath=seperator.join([dir,oceanFileName]) #note that join only takes one argument
	oceanFile=open(oceanFilePath,'w')

	#write descriptions into the .ocn file
	oceanFile.write(";setting up the environment\n")
	oceanFile.write(";specify circuit simulator\n")
	oceanFile.write("simulator('spectre)\n")

	oceanFile.write(";load the input netlist\n")
	#design("./ocean/cp1s/netlist")
	s='design("{0}/netlist")\n'.format(dir)
	oceanFile.write(s)

	#write the output command line to the .ocn file
	oceanFile.write("\n")
	oceanFile.write(";set up directory to save simulation results\n")
	s=dir+"/results"
	#check if the directory to save result exist, if not create the dir
	print(s)
	if not os.path.isdir(s):
		os.mkdir(s)

	s='outputDir="{0}/results"\n'.format(dir)
	#outputDir="./ocean/cp1s/results"
	oceanFile.write(s)
	#resultsDir(outputDir)
	oceanFile.write("resultDir(ourputDir)\n")


	#assign parameter values
	oceanFile.write("\n;assign parameter values\n")
	oceanFile.write(";the peak voltage of the input ac signal, in Volt\n")
	s='desVar("vinp" {0:.3f})\n'.format(vinp)
	#desVar("vinp" 0.3)
	oceanFile.write(s)
	oceanFile.write(";set initial value of the floating nodes\n")
	#ic("VF0" 0.3 "VF1" 0.3)
	#s='ic("VF0" {0:.3f} "VF1" {1:.3f})\n'.format(VF0,VF1)
	for i in range(len(VF)):
		s='ic("VF{0}" {1:.3f})\n'.format(str(i),VF[i])
		oceanFile.write(s)

	#set up transient simulation
	oceanFile.write("\n;set up transient simulation\n")
	oceanFile.write(';analysis(\'dc ?saveOppoint t ?oppoint "rawfile")\n')
	#analysis('tran ?stop 20n)
	s="analysis('tran ?stop {0:d}n ?errpreset \"moderate\")\n".format(stopTime)
	oceanFile.write(s)

	#set up save options
	oceanFile.write("set up save options\n")
	#delete the defalt save setting
	oceanFile.write("delete('save)\n")
	#save voltage of net VOUT
	oceanFile.write("save( 'v \"VOUT\")")

	#command line to run the simulation
	oceanFile.write("\n;actually run the simulation\n")
	oceanFile.write("run\n")

	#selecting simulation result
	oceanFile.write("\n;selecting simulation result\n")
	oceanFile.write("selectResults('tran)\n")

	#save simulation result to file
	oceanFile.write(";saving result to file\n")
	#;ocnPrint( ?output "/yc923/oceab/cp1s/results/vout" ?numberNotation 'scientific v("VOUT"))
	oceanFile.write(";specify the location of the outputfile\n")
	#outFile=strcat(outputDir "/vout")
	outFile=seperator.join([dir,"results/vout"])
	#check if the output file already exist
	if not os.path.exists(outFile):
		os.mknod(outFile) #create the output file if it doesn't exist
	#sample the output transient waveform
	#outSig=sample(v("VOUT") 0 20n "linear" 0.1n)
        oceanFile.write(";sample the output transient waveform\n")
	s='outSig=sample(v("VOUT") {0}n {1}n "linear" {2}n)\n'.format(startTime,stopTime,stepSize)
	oceanFile.write(s)
	#writing the sampled waveform to output
	s="ocnPrint( ?output \"{0}\" ?numberNotation 'scientific outSig))\n".format(outFile)
	oceanFile.write(s)


	#finish writing
	#close the .ocn file
	oceanFile.close()

	print('"start.ocn" file generated.')

#cmd = 'virtuoso -replay /work/yc923/ocean/cp1s/start.ocn'
#os.system( cmd )


