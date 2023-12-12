from .loadSegy import *
from .snavmergesps_df import *
from obspy.io.segy.segy import _read_segy
from .headers import STH_keys, BINARY_FILE_HEADER_FORMAT, TRACE_HEADER_FORMAT
import matplotlib.pyplot as plt
import matplotlib as mpl



class ImportError(Exception):
    pass


class Fileheader(object):
    def __init__(self):
        self.nsam = None
        self.dform = None


class Traceheader(object):
    def __init__(self):
        self.ntr = None

class Traces(object):
    def __init__(self):
        self.headers = pd.DataFrame()
        self.data = pd.DataFrame()


class TRH(object): #TODO: do we need object
    def __init__(self):
        self.tr = []
    def Add(self, tra):
        self.tr.append(tra)


class tr(object): #TODO: do we need object
    def __init__(self, header, data):
        # for rh in TRACE_HEADER:
        #     setattr(self, rh, 0)
        self.header = header
        self.data = data


class Seis(object):
    def __init__(self, file=None, SPS = None, line = None, binary_header=None, trace_header=None, endianness='>'):

        if SPS is None:
            msg = """ No geometry to read""".strip()
            self.msg = msg
            raise ImportError(msg)
        elif file is None:
            msg = """ No file to read""".strip()
            self.msg = msg
            raise ImportError(msg)
        else:
            self.line = line
            self.sps = SPS
            self.nffid = self.sps.n_fldr
            self.file = file
            self.fileheader = Fileheader()
            self.traces = Traces()

            self._loadSegy()
            # self._reshape_thr()

            # self._navmergesps()

    def _loadSegy(self):
        loadSegy(self)


    def _saveSeisDB(self,name = 'tempDB', path=None):
        pd.to_pickle(self, path+'/temp/' + name + '.pkl')

    def _reshape_thr(self):
        T = TRH()
        [[t.header, t.data] for t in T.tr]
        d = self.traces.data
        for i in range(d.shape[0] - 1):
            d_init = self.traces.data.loc[i, :]
            d = np.concatenate(d_init, axis=0)
            d = np.reshape(d, (self.fileheader.nsam, self.fileheader.ntr))
            h = self.traces.headers.loc[i, :]
            T.Add(tr(h, d))
        self.THR = T


    def _navmergesps(self):
        # snavmergesps(self)
        snavmergesps_df(self)

class Segy_obspy(object):
    def __init__(self,file=None):
        Seis = _read_segy(file)
        file_header = Seis.binary_file_header
        trace_headers = Seis.traces
        self.obj = Seis
        head, tail = os.path.split(file)
        self.file = tail
        self.path = head
        self.ntr = len(Seis.traces)

        # load file header
        FH = {}
        FH_keys = [header[1] for header in BINARY_FILE_HEADER_FORMAT if header[2]]
        for key in FH_keys:
            FH[key] = file_header.__getattribute__(key)
        fileHeader_dataframe = pd.DataFrame(pd.Series(FH)).T
        self.file_header = fileHeader_dataframe

        # Load trace header
        STH = {}
        for key in STH_keys:
            STH[key] = np.hstack([t.header.__getattr__(key) for t in Seis.traces])
        Trace_dataframe = pd.DataFrame.from_dict(STH)
        self.trace_header = Trace_dataframe

        # load data
        d = [Seis.traces[tr].data for tr in range(len(Seis.traces))]
        self.data = pd.DataFrame(d).T
        self.sra = self.trace_header['sample_interval_in_ms_for_this_trace']

    def _visualize_segy_obspy_data(self, cut_up = 0, cut_low = None, invert_x = 0):
        fig, (ax) = plt.subplots()
        data = self.data
        if cut_low is not None:
            # data = self.data.iloc[0:cut,:]
            data = self.data.iloc[cut_up:cut_low,:]
        ax.imshow(data, norm=mpl.colors.CenteredNorm(), cmap='seismic', aspect='auto')  # good in sample
        if invert_x == 1:
            plt.gca().invert_xaxis()
        # extent = [0, len(self.data), 0, self.data * self.sra]
        # ax.imshow(self.data, cmap='seismic')  # good in sample
        ax.set_xlabel('traces')
        ax.set_ylabel('samples')
        ax.set_title(self.file)
        plt.show()

    def _visualize_segy_obspy_geom(self):
        r_coordinates = self.trace_header[['group_coordinate_x', 'group_coordinate_y']].values
        s_coordinates = self.trace_header[['source_coordinate_x', 'source_coordinate_y']].values
        rx, ry = r_coordinates[:, 0], r_coordinates[:, 1]
        sx, sy = s_coordinates[:, 0], s_coordinates[:, 1]
        fig, (ax) = plt.subplots()
        ax.plot(rx, ry, c='b', label='Receivers')
        ax.scatter(sx, sy, s=1, c='r', label='Shotpoints')
        ax.legend()
        ax.ticklabel_format(style='plain')
        ax.set_title(self.file)
        plt.show()


class Segy_proc(object): #TODO
    def __init__(self, nsam, ntr, nffid, file=None, encoding='cp500', endianness='big' ):
        self.file = file
        self.nsam = int(nsam)
        self.ntr = int(ntr)
        self.nffid = int(nffid)
        self.encoding = encoding
        self.endianness = endianness
        self.fileheader = Fileheader()
        self.traces = Traces()

