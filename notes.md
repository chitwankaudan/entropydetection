Right now we fix amplitude, 
Want to control:
(1) signal type, (2) number of samples in the signal, (3) total number of samples including surrounding noise, (4) amplitude of the signal, and (5) sigma of the noise before adding the signal

current approach: 
- fix nSigSam, nTotSam
- randomly select start ratio from U(0, (nTotSam-nSigSam)/nTotSam)
- randomly select SNR from ??
    SNR = A^2 / sigma^2
    0 - 
    -128 to 127

floating point perciison 64 bits can we use 128 (quad preicison)

    min # of bits to model guassian noise
        16 bits is what comes out of the digitizer
        8 bits per dim
        ERF/C = tail residue integral; unstable, requires high precision
            how many itmes u should hit 0 and FF

        write down a function that visualizes data, lower limit visually still follow a guassian curve

txt with arguments
linear scoring system (in seti demo) % of overlap

window size 

OR??
- randomly select sigma of noise ??
- randomly select amplitude 

how many bits are necesary for assuming data is guassian
quantized 
16 bits --> 3 bits
sigma shouldnt be lower than 5 
qunt
range of SNR: 
translate start ratio --> starting bit to guage accuracy of results


single dish radio --> energy dist time, freq
intrafermeter array also energy as space
    - localize sources; take out airplanes
    - can ignore signals from horizon

pick up time/freq of each detection
- list of detections (starts and stops)
    most interference happens are same frequency, periodic/24 hour period
    ? 
    data fusion: identify local interference

    do they all need to be on the same clock? time shift



    1 T hardrive
    ? What is Seti's AI 


given SNR
# detection 
# non detection
p