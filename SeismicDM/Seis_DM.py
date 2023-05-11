from .headers import (S_HEADER,R_HEADER,X_HEADER,
                     BINARY_FILE_HEADER,TRACE_HEADER)
from .utils import *
from .paths_init import geom_PATH, segy_PATH

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def T0_loadFix_SrcGeom(txt_file):
    df=txt2df(txt_file)
    df1=df.iloc[:,0:4]
    df2=df.iloc[:,4:]
    df1.append(df2,ignore_index=True)
    headers = ['FLDR','EAS','NOR','ELEV'] # FLDR: source numbering
    df1.columns = headers
    return df1

def T1_loadFix_RecGeom(txt_file):
    df = txt2df(txt_file)
    df1 = df.iloc[:, 0:4]
    df2 = df.iloc[:, 4:]
    df1.append(df2, ignore_index=True)
    headers = ['REC', 'EAS', 'NOR', 'ELEV']
    df1.columns = headers
    return df1

def T2_loadFix_Relation(txt_file):
    df = txt2df(txt_file)
    #TODO:Abklären ob df[9] ignoriert werden muss oder nicht
    df = df.iloc[:, 0:8]
    headers = ['FLDR','SP','SPxLat','SPxLin','RPal','RPbl','ChnG','NCh'] #SP : source identifier , RPal : rec begin group1 RPbl: rec begin group2
    df.columns = headers
    return df


class ImportError(Exception):
    pass


class S(object):
    def __init__(self):
        for sh in S_HEADER:
            setattr(self, sh, None)


class R(object):
    def __init__(self):
        for rh in R_HEADER:
            setattr(self, rh, None)


class X(object):
    def __init__(self):
        for xh in X_HEADER:
            setattr(self, xh, None)


class SPS(object):
    def __init__(self, srctxt=None, rectxt=None, reltxt=None, srv=None):
        self.srv = srv
        self.S = S()
        self.R = R()
        self.X = X()

        # load geometry if txt file found
        if None in [srctxt, rectxt, reltxt]:
            msg = """ One or more txt file missing"""
            raise FileNotFoundError(msg)
        else:
            self._load_geom(srctxt, rectxt, reltxt)

    def _load_geom(self,srctxt=None, rectxt=None, reltxt=None):
        SrcGeom = T0_loadFix_SrcGeom(srctxt)
        RecGeom = T1_loadFix_RecGeom(rectxt)
        RelGeom = T2_loadFix_Relation(reltxt)

        self.BuildGeomDB(SrcGeom, RecGeom, RelGeom)

    def BuildGeomDB(self, SrcGeom, RecGeom, RelGeom):
        """
        Create SPS structure from geometry inputs
        :param segy:
        :param srv:
        :param SrcGeom:
        :param RecGeom:
        :param RelGeom:
        :return:
        """
        print('Loading geometry ...')

        # Import source station records
        self.S.line = self.srv
        self.S.code = 'V1'
        self.S.spare1 = SrcGeom['FLDR']  # numbering source shots
        self.S.easting = SrcGeom['EAS']
        self.S.northing = SrcGeom['NOR']

        # Import receiver station records
        self.R.line = self.srv
        self.R.point = RecGeom['REC']
        self.R.index = 1
        self.R.easting = RecGeom['EAS']
        self.R.northing = RecGeom['NOR']
        self.R.elevation = RecGeom['ELEV']

        # Import relation records (only those yet reviewd)
        n_ffid = len(RelGeom['FLDR'])  # nbr total combinations source-receiver
        n_chan = RelGeom['NCh'].values  # nbr channel pro ffid
        n_rec = len(RelGeom['NCh'].values)  # nbr total recordings
        ok = np.arange(40)

        self.X.ffid = RelGeom['FLDR']
        self.X.sline = self.srv
        self.X.spoint = RelGeom['SP']  # Point identifier
        self.X.time = ok

        ksrc = find(self.S.spare1, self.X.ffid)  # ksrc= Index des SPS-S Datensatz zum SPS-X Datensatz.

        self.X.ksrc = ksrc
        if not hasattr(ksrc, "__len__"): print('debug')

        # source index
        unique, counts = np.unique(self.X.spoint.values, return_counts=True)  # ID shots and counts / ffid
        shots_dic = dict(zip(unique, counts))  # shot ID : nbr count/ID
        self.X.sindex = counts  # nbr repetition / shots ID : for every ffid get number shot repeted

        # copy source related information to source rec
        self.S.ts = np.arange(len(self.X.time))
        self.S.index = counts
        self.S.point = unique

        # TODO add
        # S(ksrc).ts = j;
        # S(ksrc).index = X(i).sindex;
        # S(ksrc).point = X(i).spoint;

        # channel and receiver related information
        self.X.nChan = RelGeom['NCh']
        self.X.CHAN = [np.arange(RelGeom['NCh'].values[i]) for i in range(n_rec)]  # from 0 to nCh-1
        self.X.rline = [np.ones((1, RelGeom['NCh'].values[i])) * self.srv for i in range(n_rec)]
        self.X.rpoint = [
            np.vstack((RelGeom['RPal'].values[i] + np.arange(60), RelGeom['RPbl'].values[i] + np.arange(60))).flatten()
            for i in range(n_rec)]
        self.X.rindex = [np.ones((1, RelGeom['NCh'].values[i])) for i in range(n_rec)]  # all ones

        # aux information (dummy)
        self.X.instr = [np.ones((1, RelGeom['NCh'].values[i])) for i in range(n_rec)]
        self.X.spar1 = [np.zeros((1, RelGeom['NCh'].values[i])) for i in range(n_rec)]
        self.X.spar2 = [np.zeros((1, RelGeom['NCh'].values[i])) for i in range(n_rec)]

        # find receiver indices
        self.X.krec = [[None for x in range(n_chan[i])] for i in range(n_ffid)]
        for i in range(n_ffid):
            krec_i = [i_R for x_r in self.X.rpoint[i] for i_R, x_R in enumerate(self.R.point) if x_r == x_R]
            if not hasattr(krec_i, "__len__"): print('debug')
            for j in range(len(krec_i)):
                if (self.X.rpoint[i][j] < min(self.R.point) or self.X.rpoint[i][j] > max(self.R.point)):
                    self.X.krec[i][j] = 0
                else:
                    self.X.krec[i][j] = krec_i[j]

        # drop void receiver stations
        k0 = []
        k0 = [np.append(k0, (i, j)) for i in range(n_ffid) for j in range(n_chan[i]) if self.X.krec[i][j] == 0]

        for e in k0:
            i, j = int(e[0]), int(e[1])
            self.X.CHAN[i] = np.delete(self.X.CHAN[i], j)
            self.X.rline[i] = np.delete(self.X.rline[i], j)
            self.X.rpoint[i] = np.delete(self.X.rpoint[i], j)
            self.X.rindex[i] = np.delete(self.X.rindex[i], j)
            self.X.instr[i] = np.delete(self.X.instr[i], j)
            self.X.krec[i] = np.delete(self.X.krec[i], j)
            self.X.spar1[i] = np.delete(self.X.spar1[i], j)
            self.X.spar2[i] = np.delete(self.X.spar2[i], j)

        # New n channel after drop
        self.X.nChan = [len(self.X.CHAN[i]) for i in range(n_ffid)]

        # Build SPS
        self.n_ffid = n_ffid
        self.nsrc = len(RecGeom['REC'])
        self.nrec = len(RecGeom['REC'])
        self.nx = n_ffid
#
#         # Decimate SPS/S SPS/R to stations member in SPS/X
#         # TODO:
#         # k = unique([sps.X.ksrc]);
#         # sps.S = sps.S(k);
#         # sps.nsrc = numel(sps.S);
#         # k = unique([sps.X.KREC]);
#         # sps.R = sps.R(k);
#         # sps.nrec = numel(sps.R);


class Fileheader(object):
    def __init__(self):
        self.spare = None


class Traceheader(object):
    def __init__(self):
        self.spare = None


class Data(object):
    def __init__(self):
        self.spare = None


class Trace(object):
    def __init__(self):
        self.header = Traceheader()
        self.data = Data()


class Traces(object):
    def __init__(self,nffid=1):
        self.trace = [Trace() for n in range(nffid)]


class Seis(object):
    def __init__(self, file=None, SPS=None, binary_header=None, trace_header=None, endianness='>'):

        if SPS is None:
            msg = """ No geometry to read""".strip()
            raise ImportError(msg)
        elif file is None:
            msg = """ No file to read""".strip()
            raise ImportError(msg)
        else:
            self.SPS = SPS
            self.nffid = self.SPS.n_ffid
            self.file = file
            self.fileheader = Fileheader()
            self._read_encod()
            self._read_file_summary()
            self._read_file_header()
            self.traces = Traces(self.nffid)
            self._read_trace()
            # self._read_trace_obspy()
            # self.plot_sample_time_data()


    def _read_encod(self, header_encoding='cp500',endianness = 'big'):
        """
        Read encoding necessary for data extraction
        """
        self.endianness = endianness
        self.header_encoding = header_encoding
        self.trace_dtype = None

    def _read_file_summary(self):
        """
        Read textual file header (3200 bytes). Encoding in EBCDIC or ASCII.
        """
        # TODO: fehlt loc shot, record, reel, trace sequence
        # TODO: read all data after : to multiple space?
        # TODO: conditions for encoding
        try:
            with open(self.file, encoding=self.header_encoding) as f:  # 'rb for utf8
                # Textual file header
                file_sum = f.read(3200)
                self.file_summary = file_sum
        except:
            raise ImportError('File summary can not be read')

    def _read_file_header(self):
        """
        Read binary file header. (240 bytes after textual file header of 3200 bytes)
        """
        try:
            with open(self.file,'rb') as f:
                f.seek(3200) # jump to binary file header
                [setattr(self.fileheader,ls[1],int.from_bytes(f.read(ls[0]), byteorder=self.endianness))
                 for ls in BINARY_FILE_HEADER ]
        except:
            raise ImportError('File header can not be read')

    def _read_trace(self):
        """
        Fetch for each shot its header and data
        """
        # Get main information from segy:
        ntraces = self.fileheader.ntr
        nsamples = self.fileheader.nsam
        bytef = get_bytefactor_from_format(self.fileheader.dform)

        try:
            with open(self.file,'rb') as f:
                f.seek(3600)  # jump to end of trace file header
                for t in self.traces.trace:
                    [setattr(t.header, ls[1], int.from_bytes(f.read(ls[0]), byteorder=self.endianness))
                     for ls in TRACE_HEADER]
                    # TODO : verify import byte / data.encode for ibm needed
                    t.data = [unpack_ibm_4byte(f) for j in range(t.header.nstr)]
        except:
            raise ImportError('Traces can not be read')

    def _read_trace_obspy(self):
        from obspy.io.segy.segy import _read_segy
        Obj = _read_segy(self.file)
        obj_traces = Obj.traces
        self.obspy_data = obj_traces


    def navmergesps(self):
        """
        Assign a survey acquisition geometry provided by a SPS database to seismic shot records provided as a seismic data structure (s)
        :return:
        """
        # TODO
        print('----')

