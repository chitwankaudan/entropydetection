import numpy as np
import pandas as pd
from subprocess import run, PIPE
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
from pathlib import Path

p = Path('train_zorb/')
all_dat = sorted(p.glob('*.npy'))

for file in all_dat:
	run((["agnentro/tmp/agnentrozorb", "1", "2", "guassian.zrb", file]))
