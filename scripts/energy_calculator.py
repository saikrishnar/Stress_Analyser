import wave
import wave,struct,numpy,numpy.fft
import scipy.signal#,matplotlib.pyplot


def read_wave(wavefilename):
    wav = wave.open(wavefilename,'r')
    fs = wav.getframerate() 
    sig = []
    stime = 0
    etime = 0
    wavnframes = wav.getnframes()
    sframe = int(stime * fs)                               #input is in seconds and so they are to be convereted
    wav.setpos(sframe)                                   #to frame count  
    eframe = int(etime * fs)
    if eframe == 0:
        eframe = wavnframes
    for i in range(sframe,eframe):                          #In wave format 2 bytes are used to represent one value
        hexv = wav.readframes(1)                          #readframes is an iterative function which reads 2 bytes
        sig.append(float(struct.unpack('h',hexv)[0]))
    wav.close()
    return numpy.array(sig,dtype='float'),fs

def movavg(sig,fs,wlent):
        '''
        The following function is a mathematical representation for
        a moving average. The input to the function is the signal and
        the window length in milli seconds.
        Following is the mathematical equation for the moving average.

        y[n] = 1/(2*N+1)sum(sig[i+n]) for i = -N to +N

        y[n], sig[n] are both discrete time signals

        sig is the signal and wlent is the window length in milli seconds
        '''
        wlent = 30
        wlenf = (wlent * fs)/1000
        window = numpy.array([1] * wlenf)
        avg = numpy.convolve(sig,window,mode='full')
        avg = avg[(window.size/2) - 1:avg.size - (window.size/2)]
        norm = numpy.convolve(window,numpy.array([1] * avg.size),mode='full')
        norm = norm[(window.size/2) - 1:norm.size - (window.size/2)]
        return numpy.divide(avg,norm)


def energy_calculator(sig,fs):
    zfse = 1.0 * sig * sig #squaring each of the samples: to find the ZFS energy.
    wlent = 30
    zfse_movavg = numpy.sqrt(movavg(zfse,fs,wlent)) #averaging across wlent window
    zfse_movavg = zfse_movavg/max(zfse_movavg) #normalzing
    avg_energy = sum(zfse_movavg)/zfse_movavg.size #average energy across all the window.
    return avg_energy


def main():
    wavepath = '../wav/'
    wavefilename = wavepath + 'output.wav' 
    sig,fs = read_wave(wavefilename)
    average_energy = energy_calculator(sig,fs)
    print average_energy

if __name__ == '__main__':
     main()
