import numpy as np
import pandas as pd
from subprocess import run, PIPE
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
from pathlib import Path
 
def create_haystacks(n, dSNRs, NeedleType, NeedleSize):
    dSNR_levels = dSNRs
    #Create haystacks with needles
    for dSNR in dSNR_levels:
        run(['python', 'rand_hay.py', str(n), str(NeedleType), '--dSNR', str(dSNR), '--NeedleSize', str(NeedleSize), '--out_path', 'sweepsize_test/'])
    #Create empty haystacks
    run(['python', 'rand_hay.py', str(n), 'noise', '--out_path', 'sweepsize_test/'])
    
def sweep_sizes(etype):
    sweeps = [2**10, 2**11, 2**12, 2**13, 2**15, 2**16, 2**17, 2**18, 2**19, 1000000]
    for window in sweeps:
        run(['python', 'scan.py', etype, 'sweepsize_test', '--sweep', str(window)])
    print('Ran scan on on exponentially decreasing window sizes. Check out results in sweepsize_test/')

def plot_mc(etype, dSNRs):
    results = pd.read_csv('sweepsize_test/' + etype + '_results.csv', index_col=0)
    
    num_plots = len(dSNRs) + 1

    plt.style.use('seaborn')
    fig, ax = plt.subplots(num_plots, 1, figsize=(10, 20))
    fig.subplots_adjust(hspace=0.4)

    for dSNR, plot in zip(dSNRs, ax):
        results[results['dSNR'] == dSNR].boxplot(column='norm_entropy', by='sweep size (bytes)', ax=plot)
        plot.set_title(str(dSNR) + ' db')
    results[results['dSNR'].isnull()].boxplot(column='norm_entropy', by='sweep size (bytes)', ax=ax[4]);
    
    fig.suptitle('Normalized Entropy Across Different Sweep Sizes')
    fig.tight_layout()
    fig.subplots_adjust(top=.95)
    plt.savefig('sweepsize_test/' + etype + '_' + '_plot.png')
    #plt.show()

    print('Completed plotting. Check out plots in sweepsize_test/')
        
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= 'Runs monte carlo simulation to find optimal sweep size at various db levels.')
    parser.add_argument('--n', type=int, default=10, help= 'specify how many haystacks you want to test at each dSNR level')
    parser.add_argument('--NeedleSize', type=int, default=250000, help='# of samples each injected signal is as an int (i.e. --NeedleSize 250000)')
    parser.add_argument('--NeedleType', choices=['sine', 'chirp', 'BPSK', 'BFSK', 'noise'], default='sine', help='injected signal type {sine, chirp, BPSK, BFSK, noise}')
    parser.add_argument('--etype', choices=["i", "j", "e"], default="i", help='Specifiy Entropy type. Use "j" for Jensen-Shannon exodivergence, "i" for Leidich exodivergence, or "x" for exoelasticity')
    parser.add_argument('--dSNRs', nargs=argparse.REMAINDER, default = [-20, -10, 0.5, 5.0], help= 'List which dSNRs you want to test as floats (i.e. --dSNRs 5.0 10.0 ...')
    args = parser.parse_args()
    
    #create_haystacks(args.n, args.dSNRs, args.NeedleType, args.NeedleSize)
    #sweep_sizes(args.etype)
    plot_mc(args.etype, args.dSNRs)

