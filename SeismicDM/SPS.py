from .headers import (S_HEADER, R_HEADER, X_HEADER)
from .utils import *
from .paths_init import (SeismicDM_PATH,geom_PATH, segy_PATH)


def T0_loadFix_SrcGeom(txt_file):
    df = txt2df(txt_file)
    df1 = df.iloc[:, 0:4]
    df2 = df.iloc[:, 4:]
    df1.append(df2,ignore_index=True)
    headers = ['FLDR', 'EAS', 'NOR', 'ELEV']  # FLDR: source numbering
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
    df = df.iloc[:, 0:8]
    headers = ['FLDR', 'SP', 'SPxLat', 'SPxLin', 'RPal', 'RPbl', 'ChnG', 'NCh']
    # SP : source identifier , RPal : rec begin group1 RPbl: rec begin group2
    df.columns = headers
    return df


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

    def _load_geom(self, srctxt=None, rectxt=None, reltxt=None):
        SrcGeom = T0_loadFix_SrcGeom(srctxt)
        RecGeom = T1_loadFix_RecGeom(rectxt)
        RelGeom = T2_loadFix_Relation(reltxt)

        self.BuildGeomDB(SrcGeom, RecGeom, RelGeom)

    def BuildGeomDB(self, SrcGeom, RecGeom, RelGeom):
        """
        Create SPS structure from geometry inputs
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
            if not hasattr(krec_i, "__len__"):
                print('debug')
            for j in range(len(krec_i)):
                if self.X.rpoint[i][j] < min(self.R.point) or self.X.rpoint[i][j] > max(self.R.point):
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

        # Decimate SPS/S SPS/R to stations member in SPS/X
        # TODO: add
        # k = unique([sps.X.ksrc]);
        # sps.S = sps.S(k);
        # sps.nsrc = numel(sps.S);
        # k = unique([sps.X.KREC]);
        # sps.R = sps.R(k);
        # sps.nrec = numel(sps.R);

