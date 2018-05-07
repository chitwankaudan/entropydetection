import numpy as np
import pandas as pd
from subprocess import run, PIPE
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
from pathlib import Path

def plot_entropies(path, etype, needletype):
    #Groupby needle types and plot normalized entropies
    results = pd.read_csv(str(path) +'/' + etype + '_results.csv', index_col=0)
   
    plt.style.use('seaborn-deep')
    fig = plt.figure(figsize=(20, 15))
    ax1 = plt.subplot2grid((3,2), (0,0), colspan=2)
    ax2 = plt.subplot2grid((3,2), (1,0), colspan=2)
    ax3 = plt.subplot2grid((3,2), (2,0), colspan=1)
    ax4 = plt.subplot2grid((3,2), (2,1), colspan=1)

    needle = results[results.NeedleType == needletype]['norm_entropy']
    noise = results[results.NeedleType == 'noise']['norm_entropy']
    full_range=(needle.min(), max(noise.max(), needle.max()))
    overlap_range=(min(noise.min(), needle.min()), max(noise.max(), needle.max()))
    bins = int(np.sqrt(len(results)))

    ax1.hist(noise, bins=bins*10, color='orange', alpha=0.70, edgecolor='black', label='noise', range=full_range);
    ax1.hist(needle, bins=bins*10, alpha=0.70, edgecolor='black', label=needletype, range=full_range);
    ax1.legend(loc='upper left');
    ax1.set_title('Norm Entropy Full Range')

    ax2.hist(noise, bins=bins*5, color='orange', alpha=0.70, edgecolor='black', label='noise', range=overlap_range);
    ax2.hist(needle, bins=bins*5, alpha=0.70, edgecolor='black', label=needletype, range=overlap_range);
    ax2.legend(loc='upper left');
    ax2.set_title('Norm Entropy Overlap')

    ax3.hist(needle, bins=bins)
    ax3.set_title('Norm entropy ' + needletype)

    ax4.hist(noise, bins=bins, color='orange')
    ax4.set_title('Norm entropy noise')

    # fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    # results.groupby('NeedleType')['norm_entropy'].plot(kind='kde', ax=ax[0], legend=True)
    # ax[0].set_xlabel('normalized entropy [0-1]')
    # ax[0].set_title('KDE of sine and noise')

    # ax[1].hist(results.loc[results['NeedleType'] == 'sine', 'norm_entropy'], bins=50, color='g')
    # ax[1].set_xlabel('normalized entropy [0-1]')
    # ax[1].set_title('Entropy Distr. (Sine)')

    # ax[2].hist(results.loc[results['NeedleType'] == 'noise', 'norm_entropy'], bins=50, color='b')
    # ax[2].set_xlabel('normalized entropy [0-1]')
    # ax[2].set_title('Entropy Distr. (Noise)')
    dSNR = results['dSNR'].mean(skipna=True)
    title_str = str(dSNR) + 'db' + '_' + str(needle.count() + noise.count()) + 'haystacks'
    fig.suptitle(title_str)

    plt.savefig(str(path) + '/' + etype + '_' + needletype + '_plots.png')
    #plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= 'Runs desire entropy method over all files in haystacks/')
    parser.add_argument('etype', choices=["i", "j", "x", "a"], help= 'Use "j" for Jensen-Shannon exodivergence, "i" for Leidich exodivergence, or "x" for exoelasticity')
    parser.add_argument('NeedleType', choices=['sine', 'chirp', 'BPSK', 'BFSK', 'noise', 'normnoise'], help= 'Choose the NeedlType you would like to examine entropy for.')
    parser.add_argument('haystacks_path', type=str, help= 'Specify path to haystacks you want to scan')
    
    args = parser.parse_args()
    
    p = Path(args.haystacks_path)
    if p.exists():
        plot_entropies(p, args.etype, args.NeedleType)
    else:
        print(str(p) + 'does not exist. First create these haystacks using rand_hay.py')

