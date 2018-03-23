import numpy as np
import pandas as pd
from subprocess import run, PIPE
from glob import glob
import matplotlib as mpl
#mpl.use('agg')
import matplotlib.pyplot as plt
import argparse
from datetime import datetime

def run_scan(datafiles, txtfiles, etype, dSNR):
    #initialize empty results df
    results = pd.DataFrame()
    for data, txt in zip(datafiles, txtfiles):
        output = run(["agnentro/tmp/agnentroscan", etype, data, "10", "5000", "1", "3"], stdout=PIPE)
        m = pd.read_csv(txt, squeeze=True, header=None, index_col=0)
        # m = pd.read_csv(txt, header=None).T
        # m.columns = m.iloc[0]
        # m = m.reindex(m.index.drop(0))
        m['file_name'] = np.str(txt)
        m['entropy_hex'] = str(output.stdout[0:16])
        m['start_window'] = str(output.stdout[17:33])
        results = results.append(m)
    #compute normalized entropy (b/w 0-1)
    results = results.reset_index(drop=True)
    results['norm_entropy'] = [int(i[2:18], 16) for i in results['entropy_hex']]
    results['norm_entropy'] = results['norm_entropy'] / int('FFFFFFFFFFFFFFFF', 16)
    results.to_csv(str(dSNR) + 'db_haystacks/' + etype + '_results.txt')
    print('Completed Scan! Now working on plotting...')

def plot_entropies(results_file, etype, dSNR):
    #Groupby needle types and plot normalized entropies
    results = pd.read_csv(str(results_file), index_col=0)
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    results.groupby('NeedleType')['norm_entropy'].plot(kind='kde', ax=ax[0], legend=True)
    ax[0].set_xlabel('normalized entropy [0-1]')
    ax[0].set_title('KDE of sine and noise')

    ax[1].hist(results.loc[results['NeedleType'] == 'sine', 'norm_entropy'], bins=50, color='g')
    ax[1].set_xlabel('normalized entropy [0-1]')
    ax[1].set_title('Entropy Distr. (Sine)')

    ax[2].hist(results.loc[results['NeedleType'] == 'noise', 'norm_entropy'], bins=50, color='b')
    ax[2].set_xlabel('normalized entropy [0-1]')
    ax[2].set_title('Entropy Distr. (Noise)')

    title_str = str(results['dSNR'].mean()) + 'db' + '_' + str(results.shape[0]) + 'samples'
    fig.suptitle(title_str)

    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(str(dSNR) + 'db_haystacks/' + etype +'_eplots.png')
    plt.show()
    
# def plot_entropies(txtfiles):
#     #Concatenate all metadata into one big df
#     df_list = [pd.read_csv(file, index_col=0) for file in txtfiles]
#     big_df = pd.concat(df_list)
#     big_df.to_csv('haystacks/results.txt')
#     #Groupby NeedleType and plot relative entropies
#     fig, ax = plt.subplots(figsize=(8,6))
#     big_df.groupby('NeedleType')['entropy'].plot(kind='kde', ax=ax, legend=True)
#     plt.savefig('haystacks/eplots.png')
#     plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs desire entropy method over all files in haystacks/')
    parser.add_argument('E', choices=["i", "j", "x"], help=' Use "j" for Jensen-Shannon exodivergence, "i" for Leidich exodivergence, or "x" for exoelasticity')
    parser.add_argument('dSNR', type=float, help=' Specify dSNR so scan.py know which haystack to agnentropy on')
    args = parser.parse_args()
    
    startTime = datetime.now()
    all_dat = sorted(glob('./' + str(args.dSNR) + 'db_haystacks/*.dat'))
    all_txt = sorted(glob('./' + str(args.dSNR) + 'db_haystacks/*.txt'))
    run_scan(all_dat, all_txt, args.E, args.dSNR)
    plot_entropies(str(args.dSNR) + 'db_haystacks/' + args.E + '_results.txt', args.E, args.dSNR)
    print(datetime.now() - startTime)

