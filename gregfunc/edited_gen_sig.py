# arg 1 : total signal length
# arg 2 : injected signal length
# arg 3 : signal to noise ratio [dB]
# arg 4 : signal starting ratio : .5 = starts at half the total signal, .75 = starts at 3/4 of total signal
# arg 5 : signal type {(1)sine wave, (2)chirp, (3)BPSK, (4)BFSK, (5)normal noise}

import sys
import numpy as np
import math
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(
	description='gen_sig.py generates signed 8-bit signals in .dat binary data file')
parser.add_argument('nTotSam', nargs=1, type=int, help='# of samples in total signal')
parser.add_argument('nSigSam', nargs=1, type=int, help='# of samples in injected signal')
parser.add_argument('dSNR', nargs=1, type=float, help='signal to noise raito [dB]')
parser.add_argument('StartRatio', nargs=1, type=int, help='injected signal starting ratio (i.e. .5 = starts at half the total signal)')
parser.add_argument('SigChoice', nargs=1, choices=[1, 2, 3, 4, 5], help='injected signal type {(1)sine wave, (2)chirp, (3)BPSK, (4)BFSK, (5)normal noise}')
parser.add_argument('output', nargs=1, help='name of output file')
args = parser.parse_args()

def gen_signal(nTotSam, nSigSam, dSNR, nStartRatio, SigChoice):
    	'''
		Creates a signal...(add dsecription)
		'''
	#Checking to make sure signal length and start ratio make sense
	if nSigSam > nTotSam:
		raise (ValueError"error : injected signal cannot be longer than total signal")
	if (nStartSam + nSigSam - 1) > nTotSam:
		raise ValueError ("error : artificial signal starting ratio must be <= " 
			+ str(float((nTotSam-nSigSam+1)/float(nTotSam))))	
	
	nStartSam = int(np.round(float(args.StartRatio)*nTotSam))
	
	#Defining variance guassian noise
	if SigChoice == 5:
		sigma = 100*pow(3+3*pow(10,dSNR/20.),-1)
	else:
		sigma = 100*pow(3+pow(10,dSNR/20.),-1)
	#Generating guassian noise 
	noise = np.random.normal(0,sigma,nTotSam)

	#Generating signal
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
	else:	# normal noise
		sig[nStartSam:nStartSam+nSigSam] = np.random.normal(0,sigma*pow(10,dSNR/20),nSigSam)
	#Adding together noise and signal at injection sample
	totsig = noise + sig
	totsig = totsig.astype(np.int8)


if __name__ == '__main__':
    	signal = gen_signal(args.nTotSam, args.nSigSam,
			args.dSNR, args.nStartRatio, args.SigChoice)
		#saving signal array 
		output_file = open(args.output,"wb")
		signal.tofile(output_file)
		output_file.close()