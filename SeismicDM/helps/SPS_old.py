import numpy as np
import pandas as pd

from SeismicDM.headers import (S_HEADER, R_HEADER, X_HEADER)
from SeismicDM.utils import *
from SeismicDM.userInputs import temp_nffid, ok_r, ok_x, ok_s
from SeismicDM.pathsInit import (SeismicDM_PATH, geom_PATH, segy_PATH)


def T0_loadFix_SrcGeom(txt_file):
    df = txt2df(txt_file)
    df1 = df.iloc[:, 0:4]
    df2 = df.iloc[:, 4:]
    df1.append(df2,ignore_index=True)
    headers = ['FLDR', 'EAS', 'NOR', 'ELEV']  # FLDR: source numbering
    df1.columns = headers
    df1['ok']= ok_s
    return df1


def T1_loadFix_RecGeom(txt_file):
    df = txt2df(txt_file)
    df1 = df.iloc[:, 0:4]
    df2 = df.iloc[:, 4:]
    df1.append(df2, ignore_index=True)
    headers = ['REC', 'EAS', 'NOR', 'ELEV']
    df1.columns = headers
    df1['ok']= ok_r

    return df1


def T2_loadFix_Relation(txt_file):
    df = txt2df(txt_file)
    df = df.iloc[:, 0:8]
    headers = ['FLDR', 'SP', 'SPxLat', 'SPxLin', 'RPal', 'RPbl', 'ChnG', 'NCh']
    # SP : source identifier , RPal : rec begin group1 RPbl: rec begin group2
    df.columns = headers
    df['ok']= ok_x

    return df


class Si(object):
    def __init__(self):
        for sh in S_HEADER:
            setattr(self, sh, 0)

class Ri(object):
    def __init__(self):
        for rh in R_HEADER:
            setattr(self, rh, 0)


class Xi(object):
    def __init__(self):
        for xh in X_HEADER:
            setattr(self, xh, [])


class SPS(object):
    def __init__(self, srctxt=None, rectxt=None, reltxt=None, srv=None):
        self.srv = srv


        # load geometry if txt file found
        if None in [srctxt, rectxt, reltxt]:
            msg = """ One or more txt file missing"""
            raise FileNotFoundError(msg)
        else:
            sg, rg, xg = self._load_geom(srctxt, rectxt, reltxt)
            self.S = [Si() for i in range(self.n_fldr)]
            self.R = [Ri() for i in range(self.n_fldr)]
            self.X = [Xi() for i in range(self.n_fldr)]
            self.BuildGeomDB(sg, rg, xg)


    def _load_geom(self, srctxt=None, rectxt=None, reltxt=None):
        SrcGeom = T0_loadFix_SrcGeom(srctxt)
        RecGeom = T1_loadFix_RecGeom(rectxt)
        RelGeom = T2_loadFix_Relation(reltxt)
        self.n_fldr = len(SrcGeom['FLDR'])
        return SrcGeom, RecGeom, RelGeom



    def BuildGeomDB(self, SrcGeom, RecGeom, RelGeom):
        """
        Create SPS structure from geometry inputs
        """
        print('Loading geometry ...')

        ok = np.arange(temp_nffid)  #Todo remove when all data

        # import relation records
        for i in range(len(ok)):
            j = ok[i]

            # Import source station records
            self.S[i].line = self.srv
            self.S[i].code = 'V1'
            self.S[i].spare1 = SrcGeom['FLDR'][j]
            self.S[i].easting = SrcGeom['EAS'][j]
            self.S[i].northing = SrcGeom['NOR'][j]

            # Import receiver station records
            self.R[i].line = self.srv
            self.R[i].point = RecGeom['REC'][j]
            self.R[i].index = 1
            self.R[i].easting = RecGeom['EAS'][j]
            self.R[i].northing = RecGeom['NOR'][j]
            self.R[i].elevation = RecGeom['ELEV'][j]

        for i in range(len(ok)):
            j = ok[i]

            spare1 = [self.S[n].spare1 for n in range(len(ok))]
            ksrc = findx(SrcGeom['FLDR'][j], spare1)  # ksrc= Index des SPS-S Datensatz zum SPS-X Datensatz.
            ksrc = ksrc[0] if len(ksrc) == 1 else None
            # ksrc  = ksrc if np.isscalar(ksrc) else print('ksrc not a scalar')

            self.X[i].ffid =RelGeom['FLDR'][j]
            self.X[i].sline = self.srv
            self.X[i].spoint = RelGeom['SP'][j]  # Point identifier
            self.X[i].ksrc = ksrc
            self.X[i].time = j

            # Source index
            Spoint = RelGeom['SP']
            # self.X[i].sindex = len(findx(self.X[i].spoint, Spoint))
            self.X[i].sindex = findIdxCount(self.X, 'spoint', i, Spoint)


            # # copy source related information to source rec
            self.S[ksrc].ts = self.X[i].time
            self.S[ksrc].index = self.X[i].sindex
            self.S[ksrc].point = self.X[i].spoint
        #
        # n_rec = len(RelGeom['NCh'].values)  # nbr total recordings
        # n_chan = np.asarray(RelGeom['NCh'])  # nbr channel pro ffid
        #
            # channel and receiver related information
            self.X[i].nChan = RelGeom['NCh'][j]
            self.X[i].CHAN = np.arange(0,RelGeom['NCh'][j])
            self.X[i].rline = np.ones((1, RelGeom['NCh'][j])) * self.srv

            # TODO : verify X.rpoint struct
            self.X[i].rpoint = np.asarray([RelGeom['RPal'][j] + np.linspace(0,59,60),
                                         RelGeom['RPbl'][j] + np.linspace(0,59,60)]).flatten()
            self.X[i].rindex = np.ones((1, RelGeom['NCh'][j]))  # all one assuming receivers do not move

            # aux information (dummy)
            self.X[i].instr = np.ones((1, RelGeom['NCh'][j]))
            self.X[i].spar1 = np.zeros((1, RelGeom['NCh'][j]))
            self.X[i].spar2 = np.zeros((1, RelGeom['NCh'][j]))

            # find receiver indices
            self.X[i].krec = np.zeros(self.X[i].nChan)
            for jr in range(int(self.X[i].nChan)):
                if self.X[i].rpoint[jr] < np.min(RecGeom['REC']) or self.X[i].rpoint[jr] > np.max(RecGeom['REC']):
                    self.X[i].krec[jr] = None
                else:
                    krec = findx(self.X[i].rpoint[jr], RecGeom['REC'].values)
                    # ksrc = ksrc if np.isscalar(ksrc) else None
                    krec = krec[0] if len(krec) == 1 else None
                    self.X[i].krec[jr] = krec

            # drop void receiver stations
            k0 = np.where(np.isnan(self.X[i].krec))

            self.X[i].CHAN = np.delete(self.X[i].CHAN, k0)
            self.X[i].rline = np.delete(self.X[i].rline, k0)
            self.X[i].rpoint = np.delete(self.X[i].rpoint, k0)
            self.X[i].rindex = np.delete(self.X[i].rindex, k0)
            self.X[i].instr = np.delete(self.X[i].instr, k0)
            self.X[i].krec = np.delete(self.X[i].krec, k0)
            self.X[i].spar1 = np.delete(self.X[i].spar1, k0)
            self.X[i].spar2 = np.delete(self.X[i].spar2, k0)

            # New n channel after drop
            self.X[i].nChan = len(self.X[i].CHAN)

        # Build SPS
        # Decimate SPS/S SPS/R to stations member in SPS/X
        ksrc = [self.X[i].ksrc for i in range(len(ok))]
        k = np.unique(ksrc)

        self.S = [ self.S[ki] for ki in k]
        self.R = [ self.R[ki] for ki in k]
        self.X = [ self.X[ki] for ki in k]

        self.nsrc = len(self.S)
        self.nrec = len(self.R)
        self.nx = len(self.X)
