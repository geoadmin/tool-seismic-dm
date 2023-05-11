import matplotlib.pyplot as plt
import numpy as np


def plot_wavelets(SeisDB):
    fig, (ax) = plt.subplots()
    for i in range(SeisDB.nffid):
        data_single_trace = np.array(SeisDB.traces.trace[i].data)
        max_trace = data_single_trace.max()
        len_trace = len(data_single_trace)
        if max_trace != 0:
            norm_d = data_single_trace/max_trace
            ax.plot(norm_d + i * np.ones(len_trace), linewidth=0.2)
        ax.set_ylabel('traces')
        ax.set_xlabel('samples')
