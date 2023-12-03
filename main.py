import tracemalloc
import sys
import time
from matplotlib import pyplot as plt

from bwt import create_burrows_wheeler_transform
from Fmindex import Fmindex
from FileReader import FileReader
from WaveletTree import WaveletTree
import pandas as pd

def read_file(file_path):
    try:
        file_reader = FileReader(file_path)
        if not file_reader.is_read():
            raise IOError("File reading failed.")
        return file_reader.get_text() + "$"
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit()

def measure_bwt_memory_usage(bwt):
    tracemalloc.start()
    BWTcurrent, BWTpeak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return BWTpeak / (1024 * 1024)

def create_and_measure_wavelet_tree(bwt, block_size):
    tracemalloc.start()
    start_time = time.time_ns()
    wavelet_tree = WaveletTree([char for char in bwt], block_size)
    end_time = time.time_ns()
    creation_time_ns = (end_time - start_time) / 1000000
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_memory_mb = peak / (1024 * 1024)
    return wavelet_tree, creation_time_ns, peak_memory_mb

def pattern_matching(fmindex, wavelet_tree, pattern, bwt_length):
    start_time = time.time_ns()
    match_count = fmindex.match(pattern, wavelet_tree, bwt_length)
    end_time = time.time_ns()
    matching_time = (end_time - start_time) / 1000000
    return matching_time, match_count

def plot_results(block_sizes, wt_creation_times, space_usages, pattern_matching_times):
    plt.figure(1)
    plt.scatter(block_sizes, wt_creation_times, color='blue', label='Creation Time')
    plt.ylabel('Wavelet Tree Creation Time (ms)')
    plt.xlabel('Block Size')

    plt.figure(2)
    plt.plot(block_sizes, space_usages, 'o-', color='blue', label='Memory Usage')
    plt.ylabel('Memory Usage (MB)')
    plt.xlabel('Block Size')
                
    plt.figure(3)
    plt.plot(block_sizes, pattern_matching_times, 'o-', color='blue', label='Pattern Matching Time')
    plt.ylabel('Pattern Matching Time (ms)')
    plt.xlabel('Block Size')

    plt.show()

def main(file, pattern):
    text = read_file(file)
    bwt, _ = create_burrows_wheeler_transform(text)
    fmindex = Fmindex(bwt)
    peak_memory_usage_bwt = measure_bwt_memory_usage(bwt)
    print(f"BWT Memory Peak (MB): {peak_memory_usage_bwt}")

    block_sizes = [2 ** i for i in range(1, 10)]
    wt_creation_times, space_usages, pattern_matching_times = [], [], []
    data = []
    for block_size in block_sizes:
        wavelet_tree, creation_time_ms, peak_memory_mb = create_and_measure_wavelet_tree(bwt, block_size)
        matching_time, match_count = pattern_matching(fmindex, wavelet_tree, pattern, len(text))
        wt_creation_times.append(creation_time_ms)
        space_usages.append(peak_memory_mb)
        pattern_matching_times.append(matching_time)
        data.append([block_size, creation_time_ms, peak_memory_mb, matching_time])
        print(f"Pattern: {pattern}, Count: {match_count}, Time: {matching_time}ms")

    df = pd.DataFrame(data, columns=["Block Size", "Creation Time (ms)", "Memory Usage (MB)", "Pattern Matching Time (ms)"])
    plot_results(block_sizes, wt_creation_times, space_usages, pattern_matching_times)
    return df

if __name__ == "__main__":
    df = main("./english.txt", "hurricane")
    print(df)