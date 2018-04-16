import numpy as np
import pandas as pd
from subprocess import run, PIPE
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
from pathlib import Path

def run_scan(datafiles, txtfiles, etype, geo, sweep, ranks, out_format, path):
    #initialize empty results df
    results = pd.DataFrame()
    for data, txt in zip(datafiles, txtfiles):
        output = run(["agnentro/tmp/agnentroscan", etype, data, str(geo), str(sweep), str(ranks), str(out_format)], stdout=PIPE)
        m = pd.read_csv(txt, squeeze=True, header=None, index_col=0)
        m['file_name'] = np.str(txt)
        m['entropy_hex'] = str(output.stdout[0:16])
        m['start_window'] = str(output.stdout[17:33])
        results = results.append(m)
    
    # Compute normalized entropy (b/w 0-1), add agnentroscan parameters to results df
    results = results.reset_index(drop=True)
    n = results.shape[0]
    results['norm_entropy'] = [int(i[2:18], 16) for i in results['entropy_hex']]
    results['norm_entropy'] = results['norm_entropy'] / int('FFFFFFFFFFFFFFFF', 16)
    results['geometry'] = np.repeat(geo, n)
    results['sweep size (bytes)'] = np.repeat(sweep, n)
    
    # Save results to output file
    output_file = Path(str(path) +'/' + etype + '_results.csv')
    if output_file.exists():
        old_results = pd.read_csv(str(output_file), index_col=0)
        results = pd.concat([old_results, results], axis=0, ignore_index=True)
    results.to_csv(str(output_file))
    print('Completed Scan! Checkout results in ', str(output_file))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= 'Runs desire entropy method over all files in haystacks/')
    parser.add_argument('etype', choices=["i", "j", "x"], help= 'Use "j" for Jensen-Shannon exodivergence, "i" for Leidich exodivergence, or "x" for exoelasticity')
    parser.add_argument('haystacks_path', type=str, help= 'Specify path to haystacks you want to scan')
    parser.add_argument('--geo', type=int, default=10, help= 'Specify geometry to control mask processing; see hex bitmap in tmp/agnentroscan --help')
    parser.add_argument('--sweep', default=5000, help= 'Specify sweep window size (in bytes)')
    parser.add_argument('--ranks', type=int, default=1, help= 'State desired number of output matches')
    parser.add_argument('--out_format', type=int, default=3, help= 'Specify output format; see hex bitmap in tmp/agnentroscan --help')
    args = parser.parse_args()
    
    p = Path(args.haystacks_path)

    if p.exists():
        all_dat = sorted(p.glob('*.npy'))
        all_txt = sorted(p.glob('*.txt'))
        run_scan(all_dat, all_txt, args.etype, args.geo, args.sweep, args.ranks, args.out_format, p)
        #plot_entropies(p, args.E, args.dSNR)
    else:
        print(str(p) + 'does not exist. First create these haystacks using rand_hay.py')

