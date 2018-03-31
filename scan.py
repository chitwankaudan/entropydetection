import numpy as np
import pandas as pd
from subprocess import run, PIPE
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
from pathlib import Path

def run_scan(datafiles, txtfiles, etype, dSNR, path):
    #initialize empty results df
    results = pd.DataFrame()
    for data, txt in zip(datafiles, txtfiles):
        output = run(["agnentro/tmp/agnentroscan", etype, data, "10", "5000", "1", "3"], stdout=PIPE)
        m = pd.read_csv(txt, squeeze=True, header=None, index_col=0)
        m['file_name'] = np.str(txt)
        m['entropy_hex'] = str(output.stdout[0:16])
        m['start_window'] = str(output.stdout[17:33])
        results = results.append(m)
    #compute normalized entropy (b/w 0-1)
    results = results.reset_index(drop=True)
    results['norm_entropy'] = [int(i[2:18], 16) for i in results['entropy_hex']]
    results['norm_entropy'] = results['norm_entropy'] / int('FFFFFFFFFFFFFFFF', 16)
    results.to_csv(str(path) +'/' + etype + '_results.txt')
    print('Completed Scan! Now working on plotting...')

def plot_entropies(path, etype, dSNR):
    #Groupby needle types and plot normalized entropies
    results = pd.read_csv(str(path) +'/' + etype + '_results.txt', index_col=0)
   
    plt.style.use('seaborn-deep')
    fig = plt.figure(figsize=(20, 15))
    ax1 = plt.subplot2grid((3,2), (0,0), colspan=2)
    ax2 = plt.subplot2grid((3,2), (1,0), colspan=2)
    ax3 = plt.subplot2grid((3,2), (2,0), colspan=1)
    ax4 = plt.subplot2grid((3,2), (2,1), colspan=1)

    sin = results[results.NeedleType == 'sine']['norm_entropy']
    noise = results[results.NeedleType == 'noise']['norm_entropy']
    full_range=(sin.min(), max(noise.max(), sin.max()))
    overlap_range=(noise.min(), max(noise.max(), sin.max()))
    bins = int(np.sqrt(len(results)))

    ax1.hist(noise, bins=bins*10, color='orange', alpha=0.70, edgecolor='black', label='noise', range=full_range);
    ax1.hist(sin, bins=bins*10, alpha=0.70, edgecolor='black', label='sine', range=full_range);
    ax1.legend(loc='upper left');
    ax1.set_title('Norm Entropy Full Range')

    ax2.hist(noise, bins=bins*5, color='orange', alpha=0.70, edgecolor='black', label='noise', range=overlap_range);
    ax2.hist(sin, bins=bins*5, alpha=0.70, edgecolor='black', label='sine', range=overlap_range);
    ax2.legend(loc='upper left');
    ax2.set_title('Norm Entropy Overlap')

    ax3.hist(sin, bins=bins)
    ax3.set_title('Norm Entropy Sine')

    ax4.hist(noise, bins=bins, color='orange')
    ax4.set_title('Norm Entropy Noise')

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

    title_str = str(dSNR) + 'db' + '_' + str(sin.count() + noise.count()) + 'haystacks'
    fig.suptitle(title_str)

    fig.tight_layout(rect=[0, 0.03, 1, 0.97])

    plt.savefig(str(path) + '/' + etype + '_plots.png')
    #plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs desire entropy method over all files in haystacks/')
    parser.add_argument('E', choices=["i", "j", "x"], help=' Use "j" for Jensen-Shannon exodivergence, "i" for Leidich exodivergence, or "x" for exoelasticity')
    parser.add_argument('dSNR', type=float, help=' Specify dSNR so scan.py know which haystack to agnentropy on')
    parser.add_argument('--sigma', type=float, default=10.0, help=' Specify dSNR so scan.py know which haystack to agnentropy on')
    args = parser.parse_args()
    
    p = Path(str(args.dSNR) + 'db_' + str(args.sigma) + 'sigma_haystacks/')
    
    if p.exists():
        all_dat = sorted(p.glob('*.npy'))
        all_txt = sorted(p.glob('*.txt'))
        run_scan(all_dat, all_txt, args.E, args.dSNR, p)
        plot_entropies(p, args.E, args.dSNR)
    else:
        print(str(p) + 'does not exist. First create these haystacks using rand_hay.py')

