import sys
import numpy as np
import math
import matplotlib.pyplot as plt

input_file = open(sys.argv[1],"rb")
signal = np.fromfile(input_file,dtype = 'int8')
input_file.close()

energy = np.mean(np.power(signal,2))
print str(energy)