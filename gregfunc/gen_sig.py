# arg 1 : total signal length
# arg 2 : injected signal length
# arg 3 : signal to noise ratio [dB]
# arg 4 : signal starting ratio : .5 = starts at half the total signal, .75 = starts at 3/4 of total signal
# arg 5 : signal type {(1)sine wave, (2)chirp, (3)BPSK, (4)BFSK, (5)normal noise}

import sys
import numpy as np
import math
import matplotlib.pyplot as plt

if len(sys.argv) != 7:
	print ("not enough arguments!!")
	# print "gen_sig.py generates signed 8-bit signals in .dat binary data file"
	# print "arg #1 : total signal length"
	# print "arg #2 : injected signal length"
	# print "arg #3 : signal to noise ratio [dB]"
	# print "arg #4 : signal starting ratio : .5 = starts at half the total signal, .75 = starts at 3/4 of total signal..."
	# print "arg #5 : signal type {(1)sine wave, (2)chirp, (3)BPSK, (4)BFSK, (5)normal noise}"
	# print "arg #6 : output file name [string]"
	# print ""
	# print "example : python gen_sig.py 1024 200 10 .1 2 ""signal.dat"""
	# print "generates a 1024 samples signal made of normal noise and a linear chirp"
	# print "starting at 10% of total signal length, SNR = +10dB, signal length = 200 samples"
	# print "in file ""signal.dat"""
	sys.exit()

nTotSam = int(sys.argv[1])
nSigSam = int(sys.argv[2])
dSNR = float(sys.argv[3])
nStartSam = int(np.round(float(sys.argv[4])*nTotSam))
SigChoice = int(sys.argv[5])

if nSigSam > nTotSam:
	print ("error : injected signal cannot be longer than total signal")
	sys.exit()

if (nStartSam + nSigSam - 1) > nTotSam:
	print ("error : artificial signal starting ratio must be <= " + str(float((nTotSam-nSigSam+1)/float(nTotSam))))
	sys.exit()

if SigChoice == 5:
	sigma = 100*pow(3+3*pow(10,dSNR/20.),-1)
else:
	sigma = 100*pow(3+pow(10,dSNR/20.),-1)

noise = np.random.normal(0,sigma,nTotSam)

sig = np.zeros(nTotSam)
if SigChoice == 1:	# pure carrier
	sig[nStartSam:nStartSam+nSigSam] = sigma*pow(10,dSNR/20)*np.sin(2*np.pi*(np.random.uniform()*np.arange(nSigSam) + np.random.uniform()))
elif SigChoice == 2:	# linear chirp
	sig[nStartSam:nStartSam+nSigSam] = sigma*pow(10,dSNR/20)*np.sin(2*np.pi*(np.random.uniform()*np.arange(nSigSam) + np.random.uniform()*pow(nSigSam,-1)/2*pow(np.arange(nSigSam),2) + np.random.uniform()))
elif SigChoice == 3:	# BPSK
	BR = int(np.round(np.random.uniform(1,nSigSam-1)))
	sigtmp = np.zeros(nSigSam)
	for nsym in range(int(np.floor(nSigSam/float(BR)))):
		sigtmp[nsym*BR:nsym*BR+BR] = (2*np.round(np.random.uniform(0,1))-1)
	sigtmp[nsym*BR+BR:nSigSam] = (2*np.round(np.random.uniform(0,1))-1)
	sig[nStartSam:nStartSam+nSigSam] = sigtmp*sigma*pow(10,dSNR/20)*np.sin(2*np.pi*(np.random.uniform()*np.arange(nSigSam) + np.random.uniform()))
elif SigChoice == 4:	# BFSK
	BR = int(np.round(np.random.uniform(1,nSigSam-1)))
	sigtmp = np.zeros(nSigSam)
	freqs = np.random.uniform(0,1,2)
	for nsym in range(int(np.floor(nSigSam/float(BR)))):
		sigtmp[nsym*BR:nsym*BR+BR] = freqs[int(np.round(np.random.uniform(0,1)))]
	sigtmp[nsym*BR+BR:nSigSam] = freqs[int(np.round(np.random.uniform(0,1)))]
	sig[nStartSam:nStartSam+nSigSam] = sigma*pow(10,dSNR/20)*np.sin(2*np.pi*(sigtmp*np.arange(nSigSam) + np.random.uniform()))
elif SigChoice == 5:	# normal noise
	sig[nStartSam:nStartSam+nSigSam] = np.random.normal(0,sigma*pow(10,dSNR/20),nSigSam)
else:
	print ("signal type not recognized")
	sys.exit()
	
totsig = noise + sig
totsig = totsig.astype(np.int8)

output_file = open(sys.argv[6],"wb")
np.save(output_file, totsig)
output_file.close()

