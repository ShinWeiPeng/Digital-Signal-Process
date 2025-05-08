import numpy as np
import matplotlib.pyplot as plt
from read_acc_csv import ReadAccCsv
import scipy.signal as signal
from dialog import InputNumber

BANDPASS_FREQUENCY_TORRANCE = 8
HIGHPASS_FREQUENCY_TORRANCE = 1
RIPPLE_LINEAR = 0.02

def highpass_filter(data, fs, cut=5):
    nyq = 0.5 * fs  # 奈奎斯特頻率
    if cut <= HIGHPASS_FREQUENCY_TORRANCE:
        ws = 1 / nyq
    else:
        ws = (cut - HIGHPASS_FREQUENCY_TORRANCE) / nyq
        
    wp = cut / nyq
    
    rp = 20 * np.log10(1 + RIPPLE_LINEAR)
    rs = 20 * np.log10(RIPPLE_LINEAR)
    
    n, wn = signal.ellipord(wp, ws, rp, abs(rs))
    b, a = signal.ellip(n, rp, abs(rs), wn, 'highpass')
    print(f"IIR Filter Order = {n}")

    w, H = signal.freqz(b, a)
    
    phase = np.degrees(np.angle(H))
    magnitude = abs(H)
    freqs = w / np.pi * (fs / 2)  # 轉換為 Hz

    # plt.subplots()
    # plt.plot(freqs, magnitude, '-')
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Magnitude')
    return signal.filtfilt(b, a, data)

# 設定 bandpass 濾波器：5~300 Hz
def bandpass_filter(data, fs, lowcut=5, highcut=300):
    nyq = 0.5 * fs  # 奈奎斯特頻率
    if lowcut <= BANDPASS_FREQUENCY_TORRANCE:
        ws_low = 1 / nyq
    else:
        ws_low = (lowcut - BANDPASS_FREQUENCY_TORRANCE) / nyq
        
    wp_low = (lowcut + BANDPASS_FREQUENCY_TORRANCE) / nyq
    wp_high = (highcut - BANDPASS_FREQUENCY_TORRANCE) / nyq
    ws_high = (highcut + BANDPASS_FREQUENCY_TORRANCE) / nyq
    
    rp = 20 * np.log10(1 + RIPPLE_LINEAR)
    rs = 20 * np.log10(RIPPLE_LINEAR)
    
    n, wn = signal.ellipord([wp_low, wp_high], [ws_low, ws_high], rp, abs(rs))
    b, a = signal.ellip(n, rp, abs(rs), wn, 'bandpass')
    print(f"IIR Filter Order = {n}")

    w, H = signal.freqz(b, a)
    
    phase = np.degrees(np.angle(H))
    magnitude = abs(H)
    freqs = w / np.pi * (fs / 2)  # 轉換為 Hz

    # plt.subplots()
    # plt.plot(freqs, magnitude, '-')
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Magnitude')
    return signal.filtfilt(b, a, data)

def run_shock_detect(period_sample=0.001):
    csv_data = ReadAccCsv.Read()

    if csv_data == None:
        return None
    
    shock1_kernel = np.array([0, 5, -5, 5, -5, 0])
    shock2_kernel = np.array([0, 1, -1, 1, -1, 0])
    # average_shock_kernel = shock1_kernel / np.sum(shock1_kernel)
    filter_kernel = np.ones(15)
    filter_kernel = filter_kernel / np.sum(filter_kernel)


    fig, ax = plt.subplots(3, 3, figsize=(12, 8), sharex='all', sharey='col')
    fig.canvas.manager.set_window_title(f"{csv_data['FileName']} convolution")

    DISPLAY_COL_RAW = 0
    DISPLAY_COL_SHOCK1 = 1
    DISPLAY_COL_SHOCK2 = 2
    DISPLAY_COL_SHOCK3 = 3

    for axis_raw in range(0, 3):
        num_samples = len(csv_data[ReadAccCsv.Keys[axis_raw]])  # Assuming the data length is the same for all axes
        t = np.linspace(0, num_samples * period_sample, num_samples)  # 時間軸
        # t = np.linspace(0, num_samples, num_samples)  # 時間軸
        highpass_data = highpass_filter(csv_data[ReadAccCsv.Keys[axis_raw]], freq_sample, 300)
        average_data = np.convolve(highpass_data, filter_kernel , 'same')
        shock1_result = np.convolve(average_data, shock1_kernel[::-1], mode='same')
        shock2_result = np.convolve(average_data, shock2_kernel[::-1], mode='same')

        # print(f"Raw data length: {len(csv_data[ReadAccCsv.Keys[axis_raw]])}")
        # print(f"Filtered data length: {len(average_data)}")
        # print(f"Time axis length: {len(t)}")
        # print(f"Convolution data length: {len(shock1_result)}")
        # print(f"Filtered data : {average_data}")
        
        ax[axis_raw, DISPLAY_COL_RAW].plot(t, csv_data[ReadAccCsv.Keys[axis_raw]])
        ax[axis_raw, DISPLAY_COL_RAW].set_xlabel('Time (s)')
        ax[axis_raw, DISPLAY_COL_RAW].set_ylabel('g')
        ax[axis_raw, DISPLAY_COL_RAW].grid()
        ax[axis_raw, DISPLAY_COL_RAW].set_title(f"{ReadAccCsv.Keys[axis_raw]} Raw Data")

        ax[axis_raw, DISPLAY_COL_SHOCK1].plot(t, average_data, '-', label = 'average')
        ax[axis_raw, DISPLAY_COL_SHOCK1].plot(t, shock1_result, '-', label = 'shokc1')
        ax[axis_raw, DISPLAY_COL_SHOCK1].set_xlabel('Time (s)')
        ax[axis_raw, DISPLAY_COL_SHOCK1].set_ylabel('g')
        ax[axis_raw, DISPLAY_COL_SHOCK1].grid()
        ax[axis_raw, DISPLAY_COL_SHOCK1].legend()
        ax[axis_raw, DISPLAY_COL_SHOCK1].set_title(f"{ReadAccCsv.Keys[axis_raw]} average vs shokc1")
        
        ax[axis_raw, DISPLAY_COL_SHOCK2].plot(t, average_data, '-', label = 'average')
        ax[axis_raw, DISPLAY_COL_SHOCK2].plot(t, shock2_result, '-', label = 'shokc2')
        ax[axis_raw, DISPLAY_COL_SHOCK2].set_xlabel('Time (s)')
        ax[axis_raw, DISPLAY_COL_SHOCK2].set_ylabel('g')
        ax[axis_raw, DISPLAY_COL_SHOCK2].grid()
        ax[axis_raw, DISPLAY_COL_SHOCK2].legend()
        ax[axis_raw, DISPLAY_COL_SHOCK2].set_title(f"{ReadAccCsv.Keys[axis_raw]} average vs shokc2")
        
        # ax[axis_raw, DISPLAY_COL_SHOCK3].plot(t, average_data, '-', label = 'average')
        # ax[axis_raw, DISPLAY_COL_SHOCK3].plot(t, shock3_result, '-', label = 'shokc3')
        # ax[axis_raw, DISPLAY_COL_SHOCK3].set_xlabel('Time (s)')
        # ax[axis_raw, DISPLAY_COL_SHOCK3].set_ylabel('g')
        # ax[axis_raw, DISPLAY_COL_SHOCK3].grid()
        # ax[axis_raw, DISPLAY_COL_SHOCK3].legend()
        # ax[axis_raw, DISPLAY_COL_SHOCK3].set_title(f"{ReadAccCsv.Keys[axis_raw]} average vs shokc3")
        
        print(f"{csv_data['FileName']} Analysis Finish")
        fig.tight_layout()

    return True

print("Accel Convolution")
freq_sample = InputNumber("Plesase enter your sample frequency: ")
if freq_sample == None:
    quit()
    
period_sample = 1 / freq_sample

while run_shock_detect(period_sample) != None:
    continue
    
print(f"Finish")
plt.show()
