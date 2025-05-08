import numpy as np

def function_sinc(k, numtaps):
    n = k - (numtaps - 1) / 2
    return  np.sin(np.pi * n) / (np.pi * n)

def function_sinc_lowpass(k, cutoff, numtaps, fs):
    n = k - (numtaps - 1) / 2
    fc = cutoff / fs  # 正規化截止頻率
    if n == 0:
        return cutoff
    else:
        return np.sin(2 * np.pi * fc * n) / (np.pi * n)

def function_sinc_highpass(k, cutoff, numtaps, fs):
    n = k - (numtaps - 1) / 2
    if n == 0:
        return cutoff
    
    h_high = function_sinc_lowpass(k, cutoff, numtaps, fs)
    return function_sinc(k, numtaps) - h_high

def function_sinc_bandpass(k, cutoff_low, cutoff_high, numtaps, fs):
    n = k - (numtaps - 1) / 2
    if n == 0:
        return cutoff_high - cutoff_low
    
    h_high = function_sinc_lowpass(k, cutoff_high, numtaps, fs)
    h_low = function_sinc_lowpass(k, cutoff_low, numtaps, fs)
    return h_high - h_low

def function_sinc_bandptop(k, cutoff_low, cutoff_high, numtaps, fs):
    n = k - (numtaps - 1) / 2
    if n == 0:
        return cutoff_high - cutoff_low
    
    h_high = function_sinc_highpass(k, cutoff_high, numtaps, fs)
    h_low = function_sinc_lowpass(k, cutoff_low, numtaps, fs)
    return  h_high + h_low

class FIR_Design:
    def __init__():
        pass
    
    def Order(numtaps, cutoff, *, filter_type=None, fs=None):
        
        if filter_type == None or fs == None:
            raise ValueError("argument error.")
        
        b = []
        match filter_type:
            case 'lowpass':
                b = [function_sinc_lowpass(i, cutoff, numtaps, fs) for i in range(numtaps)]
                
            case 'highpass':
                b = [function_sinc_highpass(i, cutoff, numtaps, fs) for i in range(numtaps)]
                
            case 'bandpass':
                if not isinstance(cutoff, (list, tuple)) or len(cutoff) != 2:
                    raise ValueError("bandpass cutoff should be (low, high)")
                
                cutoff_low, cutoff_high = cutoff
                b = [function_sinc_bandpass(i, cutoff_low, cutoff_high, numtaps, fs) for i in range(numtaps)]
                
            case 'bandstop':
                if not isinstance(cutoff, (list, tuple)) or len(cutoff) != 2:
                    raise ValueError("bandpass cutoff should be (low, high)")
                
                cutoff_low, cutoff_high = cutoff
                b = [function_sinc_bandptop(i, cutoff_low, cutoff_high, numtaps, fs) for i in range(numtaps)]
                
            case _:
                raise NotImplementedError(f"Filter type '{filter_type}' not supported.")
            
        return b

    

