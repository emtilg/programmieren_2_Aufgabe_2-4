import pandas as pd

def find_peaks(series, threshold, respacing_factor=5):
    """
    A function to find the peaks in a series
    Args:
        - series (pd.Series): The series to find the peaks in
        - threshold (float): The threshold for the peaks
        - respacing_factor (int): The factor to respace the series
    Returns:
        - peaks (list): A list of the indices of the peaks
    """
    # Respace the series
    series = series.iloc[::respacing_factor]
    
    # Filter the series
    series = series[series>threshold]


    peaks = []
    last = 0
    current = 0
    next = 0

    for index, row in series.items():
        last = current
        current = next
        next = row

        if last < current and current > next and current > threshold:
            peaks.append(index-respacing_factor)

    return peaks

#df = pd.read_csv(r'data/ekg_data/01_Ruhe.txt', sep='\t', header=None, names=['EKG in mV','Time in ms',])

#peaks = find_peaks(df["EKG in mV"].copy(), 340, 5)

#peaks[0:5]

#print(peaks[0:5])

def add_peaks_true_false(link):
    df = pd.read_csv(link, sep='\t', header=None, names=['EKG in mV','Time in ms',])

    peaks = find_peaks(df["EKG in mV"].copy(), 340, 5)
    
    df["is_peak"] = df.index.isin(peaks)
    return df

print(add_peaks_true_false('data/ekg_data/01_Ruhe.txt')[319:500])