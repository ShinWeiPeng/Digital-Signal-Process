import numpy as np
import matplotlib.pyplot as plt
from read_acc_csv import ReadAccCsv
from cwt_setting import CWT_Setting
from numpy.fft import fft, fftshift, fftfreq
import pywt
from dialog import InputNumber
    
ACC_X = 0
ACC_Y = 1
ACC_Z = 2
ACC_MAX = 3

def run_analysis():
    csv_data = ReadAccCsv.Read()
    
    if csv_data == None:
        return None
    
    # Pre-allocate X and Xm arrays with the correct shape
    # num_samples = len(csv_data[ReadAccCsv.Keys[ACC_X]])  # Assuming the data length is the same for all axes
    # X = np.empty((num_samples, 3), dtype=np.complex128)  # Each column corresponds to an axis
    # Xm = np.empty((num_samples, 3), dtype=np.complex128)  # Same shape for magnitude

    # t = np.linspace(0, num_samples * period_sample, num_samples)  # 時間軸
    # f = fftshift(fftfreq(num_samples, period_sample))

    # for axis in range(ACC_X, ACC_MAX):
    #     print(f"FFT {axis} Axis")
    #     X[:, axis] = fftshift(fft(csv_data[ReadAccCsv.Keys[axis]]))  # Store FFT result for this axis
    #     Xm[:, axis] = np.abs(X[:, axis])  # Store magnitude of FFT result


    fig, ax = plt.subplots(3, 3, figsize=(12, 8), sharex='col', sharey='col')
    fig.canvas.manager.set_window_title(f"{csv_data['FileName']} Analysis")

    DISPLAY_COL_RAW = 0
    DISPLAY_COL_SPECTRUM = 1
    DISPLAY_COL_SPECTROGRAM = 2

    for axis_raw in range(ACC_X, 3):
        num_samples = len(csv_data[ReadAccCsv.Keys[axis_raw]])  # Assuming the data length is the same for all axes
        t = np.linspace(0, num_samples * period_sample, num_samples)  # 時間軸
        f = fftshift(fftfreq(num_samples, period_sample))
        
        X = fftshift(fft(csv_data[ReadAccCsv.Keys[axis_raw]]))  # Store FFT result for this axis
        Xm = np.abs(X)  # Store magnitude of FFT result
        
        ax[axis_raw, DISPLAY_COL_RAW].plot(t, csv_data[ReadAccCsv.Keys[axis_raw]])
        ax[axis_raw, DISPLAY_COL_RAW].set_xlabel('Time (s)')
        ax[axis_raw, DISPLAY_COL_RAW].set_ylabel('g')
        ax[axis_raw, DISPLAY_COL_RAW].grid()
        ax[axis_raw, DISPLAY_COL_RAW].set_title(f"{ReadAccCsv.Keys[axis_raw]} Raw Data")

        ax[axis_raw, DISPLAY_COL_SPECTRUM].plot(f, Xm)
        ax[axis_raw, DISPLAY_COL_SPECTRUM].set_xlabel('Frequency (Hz)')
        ax[axis_raw, DISPLAY_COL_SPECTRUM].set_ylabel('Magnitude')
        ax[axis_raw, DISPLAY_COL_SPECTRUM].set_xlim(left=0)
        ax[axis_raw, DISPLAY_COL_SPECTRUM].grid()
        ax[axis_raw, DISPLAY_COL_SPECTRUM].set_title(f"{ReadAccCsv.Keys[axis_raw]} Spectrum")

        # 小波轉換 (CWT)
        cwt_matrix, frequencies = pywt.cwt(csv_data[ReadAccCsv.Keys[axis_raw]], CWT_Setting.Scales, CWT_Setting.WaveletName, sampling_period=period_sample)
        
        # 時頻圖 (Scalogram)
        ax[axis_raw, DISPLAY_COL_SPECTROGRAM].contourf(t, frequencies, np.abs(cwt_matrix))
        ax[axis_raw, DISPLAY_COL_SPECTROGRAM].set_xlabel('Time (s)')
        ax[axis_raw, DISPLAY_COL_SPECTROGRAM].set_ylabel('Frequency (Hz)')
        ax[axis_raw, DISPLAY_COL_SPECTROGRAM].set_title(f"{ReadAccCsv.Keys[axis_raw]} Spectrogram")

    print(f"{csv_data['FileName']} Analysis Finish")
    fig.tight_layout()
    return True

print("Accel Spectrogram Analysis")

freq_sample = InputNumber("Plesase enter your sample frequency: ")
if freq_sample == None or freq_sample <= 0:
    quit()

period_sample = 1 / freq_sample

CWT_Setting.ChoiceDialog()

while run_analysis() != None:
    continue

plt.show()