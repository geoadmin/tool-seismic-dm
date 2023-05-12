import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


def plot_wavelets(SeisDB):
    for i in range(5):  # TODO: change when ready to plot all nffid
        fig, ax = plt.subplots()
        ntraces_i = SeisDB.traces.headers['ntr'][i]
        for nt in range(ntraces_i):
            data_single_trace = SeisDB.traces.data[nt*i]
            max_trace = data_single_trace.max()
            len_trace = len(data_single_trace)
            if max_trace != 0:
                norm_d = data_single_trace/max_trace
                ax.plot(norm_d + nt * np.ones(len_trace), linewidth=0.2)
        ax.set_title('nffid'+str(i))
        ax.set_ylim(bottom=0)
        ax.set_ylabel('traces')
        ax.set_xlabel('samples')
        plt.show()
