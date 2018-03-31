import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from datetime import datetime

def rand_sig(n, sigma, dSNR, NeedleSize, HstackSize, NeedleType):
        #Create dSNR and sigma arrays
        arr_dSNR = np.repeat(dSNR, n)
        arr_sigma = np.repeat(sigma, n)
        
        #Initialize haystack w/ noise
        haystack = np.random.normal(0, arr_sigma, size=(HstackSize, n))

        #To generate just noise, output quantized haystacks and their powers
        metadata = pd.DataFrame()
        metadata['sigma'] = pd.Series(sigma)
        metadata['NeedleType'] = pd.Series(np.repeat(NeedleType, n))
        if NeedleType == 'noise':
                return haystack.astype(np.int8), metadata

        #Creating injected signal matrix
        w = np.arange(NeedleSize)
        w.shape
        w = w.reshape(NeedleSize,1)
        
        uni_mul = np.random.uniform(size=(1, n))
        uni_add = np.repeat([np.random.uniform(size=n)], NeedleSize).reshape(n,NeedleSize).T
        
        needle = sigma*pow(10,dSNR/20)*np.sin(2*np.pi*((np.matmul(w, uni_mul) + uni_add)))
        
        #Adding each signal at the correct place within the noise matrix
        LastStartR= (HstackSize-NeedleSize)/HstackSize
        StartR = np.random.uniform(0, LastStartR, size=n)
        StartSam = np.round((StartR*HstackSize).astype(float)).astype(int)
        
        for sig in np.arange(n):
            haystack[:,sig][StartSam[sig]:StartSam[sig]+NeedleSize] += needle[0:NeedleSize, sig]
        
        #Creating metadata dataframe to populate .txt file
        metadata = pd.DataFrame()
        metadata['sigma'] = pd.Series(sigma)
        metadata['dSNR'] = pd.Series(dSNR)
        metadata['HstackSize'] = pd.Series(np.repeat(HstackSize, n))
        metadata['NeedleSize'] = pd.Series(np.repeat(NeedleSize, n))
        metadata['NeedleType'] = pd.Series(np.repeat(NeedleType, n))
        metadata['StartSam'] = pd.Series(StartSam)

        #Return quantized haystacks and their metadata
        return haystack.astype(np.int8), metadata

if __name__ == '__main__':
        startTime = datetime.now()
        parser = argparse.ArgumentParser(
        description='creates many haystack ')
        parser.add_argument('n', type=int, default=10, help='# of haystack you want to generate (int)')
        parser.add_argument('dSNR', type=float, help='# of samples each injected signal is (int)')
        parser.add_argument('--sigma', type=float, default=10, help='# variance of the noise; defaults to 10')
        parser.add_argument('--NeedleSize', type=int, default=250000, help='# of samples each injected signal is (int)')
        parser.add_argument('--HstackSize', type=int, default=1000000, help='# of total samples each signal (int)')
        parser.add_argument('--NeedleType', choices=['sine', 'chirp', 'BPSK', 'BFSK', 'noise'], default='sine', help='injected signal type {sine, chirp, BPSK, BFSK, noise}')
        args = parser.parse_args()

        #Generate n random haystack and their corresponding metadata
        data = rand_sig(args.n, args.sigma, args.dSNR, args.NeedleSize, args.HstackSize, args.NeedleType)
        haystack = data[0]
        metadata = data[1]
        
        #Saving files
        time = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        for sig_index in np.arange(args.n):
                #save .dat file
                output_file = open('haystacks/'+ time +'__' + str(sig_index) + '.dat', "wb")
                np.save(output_file, haystack[:, sig_index])
                output_file.close()
                
                #saving .txt file
                metadata.iloc[sig_index].to_csv('haystacks/'+ time +'__' + str(sig_index) + '.txt')
        
        print(datetime.now() - startTime)