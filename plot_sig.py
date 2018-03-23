import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import signal
import argparse

mpl.rcParams['agg.path.chunksize'] = 10000

parser = argparse.ArgumentParser(
	description='plots histogram, spectrogram and timeseries of signal provided')
parser.add_argument('file', nargs=1, help='name of file with signal array')
parser.add_argument('--save', action="store_true", help='add --save flag to save plots as pdf')
args = parser.parse_args()

#loads binary file
output_file = open(sys.argv[1],"rb")
totsig = np.load(output_file)
output_file.close()

#plots signal
fig, axs = plt.subplots(ncols=3, figsize=[15, 5])

fig.subplots_adjust(wspace=.25)
axs[0].hist(totsig, bins=50)
axs[0].set_ylabel('Count')

freq, time, Sxx = signal.spectrogram(totsig)
axs[1].pcolormesh(time, freq, Sxx)
axs[1].set_xlabel('Time')
axs[1].set_ylabel('Frequency[Hz]')

axs[2].plot(totsig)
axs[2].set_xlabel('Time')
axs[2].set_ylabel('Amplitude')

fig.suptitle(str(sys.argv[1]))
fig.tight_layout(rect=[0, 0.03, 1, 0.95])

#if desired, saves plot to pdf with same name as the .dat file
if args.save:
    plt.savefig(str(sys.argv[1])[:-3] + 'pdf' )
    print('Plot saved!')

plt.show()
    
