import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


def plotWavelets(SeisDB, idx = None):
    print('wavelet')
    if idx ==  None:
        for nffid_i in range(3):  # TODO: change when ready to plot all nffid
            fig, ax = plt.subplots()
            nch_i = SeisDB.fileheader.ntr
            for nt in range(nch_i):
                data_single_trace = SeisDB.traces.data[nt*nffid_i]
                max_trace = data_single_trace.max()
                len_trace = len(data_single_trace)
                if max_trace != 0:
                    norm_d = data_single_trace/max_trace
                    ax.plot(norm_d + nt * np.ones(len_trace), linewidth=0.2)
            ax.set_title('line: ' + str(SeisDB.line) + ' nffi '+str(nffid_i))
            ax.set_ylim(bottom=0)
            ax.set_ylabel('traces')
            ax.set_xlabel('samples')
            plt.show()
    else:
        fig, ax = plt.subplots()
        nch_i = SeisDB.fileheader.ntr
        for nt in range(nch_i):
            data_single_trace = SeisDB.traces.data[nt*idx]
            max_trace = data_single_trace.max()
            len_trace = len(data_single_trace)
            if max_trace != 0:
                norm_d = data_single_trace/max_trace
                ax.plot(norm_d + nt * np.ones(len_trace), linewidth=0.2)
        ax.set_title('line: ' + str(SeisDB.line) + ' nffid'+str(idx))
        ax.set_ylim(bottom=0)
        ax.set_ylabel('traces')
        ax.set_xlabel('samples')
        plt.show()
def plot_aquisition_geom(SeisDB):
    fig = plt.figure()
    idx = 1
    plt.scatter(SeisDB.sps.S.easting, SeisDB.sps.S.northing, s=5, marker='x', c='blue',
                label=SeisDB.line + ': Sources location')
    plt.scatter(SeisDB.sps.R.easting, SeisDB.sps.R.northing, s=5, marker='+', c='orange',
                label=SeisDB.line+ ': Receiver location')
    plt.xlabel('Easting')
    plt.ylabel('Northing')
    plt.title('Aquisition Geometry Line {}'.format(SeisDB.line))
    plt.legend()
    plt.show()

def plotFFID(SeisDB, n):
    print('Plot ffid')
    fig, (ax) = plt.subplots()
    # TODO: transform sample in time - import sra
    data = SeisDB.THR.tr[n].data
    ax.imshow(data.T, cmap='seismic')  # good in sample
    ax.set_xlabel('traces')
    ax.set_ylabel('samples')
    #     ax.plot(data[idx_tr]/max(data[idx_tr])) # scaling and shift
    plt.show()


def plotImshow(SeisDB):
    print('Plot imshow')
    fig, (ax) = plt.subplots()
    # TODO: transform sample in time - import sra
    data = SeisDB.traces.data
    sra = 0.4000 #SeisDB.fileheader.
    extent = [0, len(data), 0, data * sra]
    ax.imshow(data.T, cmap='seismic')  # good in sample
    ax.set_xlabel('traces')
    ax.set_ylabel('samples')
    #     ax.plot(data[idx_tr]/max(data[idx_tr])) # scaling and shift
    plt.show()

def plot_Geom_src_rec_cdp(SeisDB):
    """obsolete"""
    fig, ax = plt.subplots()
    sx = SeisDB.traces.headers.sx[SeisDB.traces.headers.sx != 0]
    sy = SeisDB.traces.headers.sy[SeisDB.traces.headers.sy != 0]
    gx = SeisDB.traces.headers.gx[SeisDB.traces.headers.gx != 0]
    gy = SeisDB.traces.headers.gy[SeisDB.traces.headers.gy != 0]
    cdpx = SeisDB.traces.headers.cdpx[SeisDB.traces.headers.cdpx > 560000]
    # cdpx = SeisDB.traces.headers.cdpx[SeisDB.traces.headers.cdpx > 560000]
    cdpy = SeisDB.traces.headers.cdpy[SeisDB.traces.headers.cdpy > 160000]
    # cdpy = SeisDB.traces.headers.cdpy[SeisDB.traces.headers.cdpy > 160000]
    ax.scatter(sx, sy, c='r')
    ax.scatter(gx, gy, c='b')
    ax.scatter(cdpx, cdpy, c='g')
    plt.show()

