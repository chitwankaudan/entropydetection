import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
from subprocess import run
from pathlib import Path

class GenHstacks:
    def __init__(self, n, dSNR, sigma, NeedleSize, HstackSize, NeedleType, out_path):
        self.n = n
        self.sigma = np.repeat(sigma, n)
        self.dSNR = np.repeat(dSNR, n)
        self.NeedleSize = NeedleSize
        self.HstackSize = HstackSize
        self.NeedleType = NeedleType
        self.out_path = out_path
    
    def build_hstack(self):
        #Initialize haystack w/ noise
        haystack = np.random.normal(0, self.sigma, size=(self.HstackSize, self.n))
        #Create info df to store basic haystack info
        info = pd.DataFrame()
        info['sigma'] = pd.Series(self.sigma)
        info['HstackSize'] = pd.Series(np.repeat(self.HstackSize, self.n))

        if self.NeedleType == 'noise':
            #add 'noise' as NeedleType
            info['NeedleType'] = pd.Series(np.repeat('noise', self.n))
        
        elif self.NeedleType == 'sine':
            #inject sinusodial and update haystack and info
            needle = self.create_sin()
            haystack, info = self.inject_needle(needle, haystack, info)
        else:
            pass

        self.save(haystack.astype(np.int8), info, self.out_path)

    def create_sin(self):
        #define time array (t)
        t = np.arange(self.NeedleSize).reshape(self.NeedleSize,1)
        #Randomly select save freq, phase. Compute amplitude.
        rand_freq = np.random.uniform(size=(1, self.n))
        rand_phase = np.repeat([np.random.uniform(size=self.n)], self.NeedleSize).reshape(self.n,self.NeedleSize).T
        amplitude = self.sigma*pow(10,self.dSNR/20)
        
        #Create the sinusodial needle
        needle = amplitude * np.sin(2*np.pi*((np.matmul(t, rand_freq) + rand_phase)))
        return needle

    def inject_needle(self, needle, noise, info):
        #Adding each signal at the correct place within in a zeros matrix
        LastStartRatio= (self.HstackSize - self.NeedleSize) / self.HstackSize
        StartRatio = np.random.uniform(0, LastStartRatio, size=self.n)
        StartSam = np.round((StartRatio * self.HstackSize)).astype(int)
        needle_mask = np.zeros((self.HstackSize, self.n))

        #Add needle each needle at its random start sample location in the zero array
        for i in np.arange(self.n):
            needle_mask[:,i][StartSam[i]:StartSam[i]+self.NeedleSize] = needle[:, i]
        
        #Add the needle to the haystack
        haystack = noise + needle_mask

        #Update info df with correct metadata
        info['dSNR'] = pd.Series(self.dSNR)
        info['NeedleSize'] = pd.Series(np.repeat(self.NeedleSize, self.n))
        info['NeedleType'] = pd.Series(np.repeat(self.NeedleType, self.n))
        info['StartSam'] = pd.Series(StartSam)
        return haystack, info
        
    def save(self, haystack, info, out_path):
        #Check if directory exits or create directory
        if out_path:
            p = Path(out_path)
            if p.exists():
                pass
            else:
                run(['mkdir','--', p])
        
        else:
            p = Path(str(self.dSNR[0]) + 'db_' + str(self.sigma[0]) + 'sigma_haystacks/')
            if p.exists():
                pass
            else:
                run(['mkdir','--', p])

        time = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        for i in np.arange(self.n):
            hstack_name = str(p) + '/' + time +'__' + str(i)
            np.save(hstack_name, haystack[:, i])
            info.iloc[i].to_csv(hstack_name + '.txt')    

def main():
    startTime = datetime.now()
    parser = argparse.ArgumentParser(description='creates many haystack ')
    parser.add_argument('n', type=int, help='# of haystack you want to generate (int)')
    parser.add_argument('NeedleType', choices=['sine', 'chirp', 'BPSK', 'BFSK', 'noise'], help='injected signal type {sine, chirp, BPSK, BFSK, noise}')
    parser.add_argument('--dSNR', type=float, help='# of samples each injected signal is (int)')
    parser.add_argument('--sigma', type=float, default=10.0, help='# variance of the noise; defaults to 10')
    parser.add_argument('--NeedleSize', type=int, default=250000, help='# of samples each injected signal is (int)')
    parser.add_argument('--HstackSize', type=int, default=1000000, help='# of total samples each signal (int)')
    parser.add_argument('--out_path', default=None, help='You can specify where to save haystacks')
    args = parser.parse_args()
    
    if args.NeedleType != 'noise' and not args.dSNR:
        parser.error('Please specify a SNR in db for your needle.')

    GenHstacks(args.n, args.dSNR, args.sigma, args.NeedleSize, args.HstackSize, args.NeedleType, args.out_path).build_hstack()
                
if __name__ == '__main__':
    main()
            
        