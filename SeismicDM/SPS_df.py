from .utils import *
# from .userInputs import temp_nffid
# from .userInputs import temp_nffid, ok_r, ok_x, ok_s

def T0_loadFix_SrcGeom(txt_file):
    df = txt2df(txt_file)
    df1 = df.iloc[:, 0:4]
    # case with w and double lines
    if 4<len(df.columns)<8:
        extra = df.iloc[:, 1]
        df = df.drop(df.columns[1], axis=1)
        df1 = df.iloc[:, 0:4]
    else:
        df2 = df.iloc[:, 4:]
        df1.append(df2,ignore_index=True)

    headers = ['FLDR', 'EAS', 'NOR', 'ELEV']  # FLDR: source numbering
    df1.columns = headers
    return df1


def T1_loadFix_RecGeom(txt_file):
    df = txt2df(txt_file)
    df1 = df.iloc[:, 0:4]
    if 4<len(df.columns)<8:
        extra = df.iloc[:, 1]
        df = df.drop(df.columns[1], axis=1)
        df1 = df.iloc[:, 0:4]
    else:
        df2 = df.iloc[:, 4:]
        df1.append(df2, ignore_index=True)
    headers = ['REC', 'EAS', 'NOR', 'ELEV']
    df1.columns = headers
    df1 = df1.astype(float) # added
    # df1['ok']= ok_r
    return df1


def T2_loadFix_Relation(txt_file):
    df = txt2df(txt_file)
    df = df.iloc[:, 0:8]
    headers = ['FLDR', 'SP', 'SPxLat', 'SPxLin', 'RPal', 'RPbl', 'ChnG', 'NCh']
    # SP : source identifier , RPal : rec begin group1 RPbl: rec begin group2
    df.columns = headers
    df = df.astype(float) # added
    # df['ok']= ok_x

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


class SPS_df(object):
    def __init__(self, geom_datafolder=None, srctxt=None, rectxt=None, reltxt=None, srv=None, temp_nffid=None):
        self.srv = srv
        if self.srv:
            self.srv = int(self.srv)
        else:
            self.srv = 1

        # load geometry if txt file found
        if None in [srctxt, rectxt, reltxt]:
            msg = """ One or more txt file missing"""
            raise FileNotFoundError(msg)
        else:
            sg, rg, xg = self._load_geom(geom_datafolder, srctxt, rectxt, reltxt)
            self.S = pd.DataFrame()
            self.R = pd.DataFrame()
            self.X = pd.DataFrame()
            self.BuildGeomDB(sg, rg, xg)


    def _load_geom(self, geom_datafolder, srctxt, rectxt, reltxt):
        os.chdir(geom_datafolder)
        SrcGeom = T0_loadFix_SrcGeom(srctxt)
        RecGeom = T1_loadFix_RecGeom(rectxt)
        RelGeom = T2_loadFix_Relation(reltxt)
        self.n_fldr = len(RelGeom['FLDR'])
        return SrcGeom, RecGeom, RelGeom

    def BuildGeomDB(self, SrcGeom, RecGeom, RelGeom):
        """
        Create SPS structure from geometry inputs
        """
        print('Loading geometry ...')

        ok = np.arange(len(RelGeom['FLDR']))

        # line-specific parameters
        line = self.srv     # line number
        chanIncr = 1        # channel numbering, increment
        recIncr = 1         # rec station ID, increment
        srcIdx = 1          # constant source index
        recIdx = 1          # constant receiver index
        srcPt0 = 0          # value to add to SP numbers of SF to match SP numbers in XF
        recPt0 = 0          # ..dto rec points
        sfFFID = True       # Switch: s files provides FFIDs (rather than SP-IDs)
        srcCode = 'V'       # source code (vibrotor, unspec)


        # RELATION STATION RECORDS
        self.X = pd.DataFrame(columns=['ffid','sline','spoint', 'sindex', 'SPxLat', 'SPxLin','ksrc',
                                       'time','nChan','CHAN',
                                       'rline', 'rpoint', 'rindex','instr',
                                       'spar1','spar2','krec'])
        self.X['ffid'] = RelGeom['FLDR']                        # FFID, record number
        # shot station identification
        self.X['sline'] = self.srv
        self.X['spoint'] = RelGeom['SP']                        # Point identifier

        # shot location offset
        self.X['SPxLat'] = RelGeom['SPxLat']                    # lateral offset [m]
        self.X['SPxLin'] = RelGeom['SPxLin']                    # inline offset [m]

        self.X['CHAN'] = self.X['CHAN'].astype(object)
        self.X['rline'] = self.X['rline'].astype(object)
        self.X['rpoint'] = self.X['rpoint'].astype(object)
        self.X['rindex'] = self.X['rindex'].astype(object)
        self.X['instr'] = self.X['instr'].astype(object)
        self.X['spar1'] = self.X['spar1'].astype(object)
        self.X['spar2'] = self.X['spar2'].astype(object)
        self.X['krec'] = self.X['krec'].astype(object)

        # SOURCES STATION RECORDS
        ## TODO: change order fields
        self.S['fldr'] = SrcGeom['FLDR']
        self.S['line'] = np.ones(len(SrcGeom['FLDR']))*self.srv # FIX FLDR length
        self.S['spare1'] = SrcGeom['FLDR']
        self.S['easting'] = SrcGeom['EAS']
        self.S['northing'] = SrcGeom['NOR']
        self.S['elevation'] = SrcGeom['ELEV']
        self.S['code'] = ['V1' for _ in range(len(SrcGeom['FLDR']))]

        # RECIEVER STATION RECORDS
        self.R['line'] = np.ones(len(RecGeom['REC']))*self.srv
        self.R['point'] = RecGeom['REC']
        self.R['index'] = 1
        self.R['easting'] = RecGeom['EAS']
        self.R['northing'] = RecGeom['NOR']
        self.R['elevation'] = RecGeom['ELEV']
        self.R['code'] = ['G' for _ in range(len(RecGeom['REC']))]


        for i in range(len(ok)):
            j = ok[i]

            # increment source index in case of double spoint instance
            Spoint = RelGeom['SP'][j]
            self.X.at[i,'sindex'] = srcIdx + len(findx(int(Spoint), self.X['spoint'][:j]))

            # check for unique ffid
            nbr_ffid = findx(int(self.X['ffid'][j]), self.X['ffid'])
            if len(nbr_ffid)>1:
                print('----- Non-unique FFID. FFID: {}'.format(self.X['ffid'][j]))


            # number of channels
            self.X.at[i, 'nChan'] = int(RelGeom['NCh'][j])
            nch_j = int(RelGeom['NCh'][j])

            # channel numbering -- 4 stations not recording around SP
            # layout A: rec stations before SP
            chanLast = RelGeom['ChnG'][j]
            chanFirst = 1
            ChanA = np.arange(chanFirst,chanLast, chanIncr).astype(int) # chanFirst: in python, last = last-1
            # layout B: rec stations after SP
            chanFirst = RelGeom['ChnG'][j]
            chanLast = self.X['nChan'][j]
            ChanB = np.arange(chanFirst,chanLast, chanIncr).astype(int)

            # assign channel numbers
            self.X.at[i, 'CHAN'] = np.concatenate((ChanA, ChanB), axis=0) # [ChanA, ChanB], axis=0 keeps ","

            # receiver point identification, layout A
            recFirst = RelGeom['RPal'][j] - len(ChanA) #TODO: verify !! angepasst
            recLast = RelGeom['RPal'][j]
            recA = np.arange(recFirst, recLast, chanIncr)
            # receiver point identification, layout A
            recFirst = RelGeom['RPbl'][j]
            recLast = RelGeom['RPbl'][j] + len(ChanB)
            recB = np.arange(recFirst, recLast, chanIncr)
            # assign receiver point identification
            self.X.at[i, 'rpoint'] = np.concatenate((recA, recB), axis=0) # [recA, recB]

            # receiver stations identification
            self.X.at[i, 'rline'] = np.ones((1, self.X['nChan'][j])) * self.srv
            self.X.at[i, 'rindex'] = np.ones((1, self.X['nChan'][j]))  # all one assuming receivers do not move

            # check for matching ffid in X records
            if sfFFID:
                k = findx(SrcGeom['FLDR'][j], self.X['ffid'])
                if len(k)==1:
                    self.S.at[i,'point'] = self.X['spoint'][k[0]]
                    self.S.at[i,'index'] = self.X['sindex'][k[0]]
                else:
                    print('----- no FFID-match for {} in X records'.format(SrcGeom['FLDR'][j]))
            else:
                self.S.at[i, 'point'] = SrcGeom['FLDR'][j] + srcPt0
                self.S.at[i, 'index'] = srcIdx

            # check for unique records
            #TODO: -------------------------

            # spare1 = [self.S['spare1'][n] for n in range(len(ok))]
            # ksrc = findx(int(SrcGeom['FLDR'][j]), spare1)  #TODO: à l'envers??  # ksrc= Index des SPS-S Datensatz zum SPS-X Datensatz.
            # ksrc = ksrc[0] if len(ksrc) == 1 else None
            #
            # self.X.at[i, 'ksrc'] = ksrc
            # self.X.at[i, 'time'] = j
            #
            #
            # # copy source related information to source rec
            # self.S.at[ksrc, 'ts'] = self.X.loc[i, 'time']
            # self.S.at[ksrc, 'index'] = self.X.loc[i, 'sindex']
            # self.S.at[ksrc, 'point'] = self.X.loc[i, 'spoint']
            # ## seems ok until here ------------------------------------------------
            #
            #
            #
            # #
            #
            # # TODO : OLD X.rpoint struct
            # # self.X.at[i, 'rpoint'] = np.asarray([RelGeom['RPal'][j] + np.linspace(0,59,60),
            # #                              RelGeom['RPbl'][j] + np.linspace(0,59,60)]).flatten()
            #
            # # aux information (dummy)
            # self.X.at[i, 'instr'] = np.ones((1, nch_j))
            # self.X.at[i, 'spar1'] = np.zeros((1, nch_j))
            # self.X.at[i, 'spar2'] = np.zeros((1, nch_j))
            #
            # # find receiver indices
            # self.X.at[i, 'krec'] = np.zeros(self.X.at[i,'nChan'])
            # for jr in range(int(self.X.at[i,'nChan'])):
            #     if self.X.at[i, 'rpoint'][jr] < np.min(RecGeom['REC']) or self.X.at[i, 'rpoint'][jr] > np.max(RecGeom['REC']):
            #         self.X.at[i, 'krec'][jr] = None
            #     else:
            #         # krec = findx(int(self.X.at[i, 'rpoint'][jr]), RecGeom['REC'].values)
            #         krec = findx(int(self.X.at[i, 'rpoint'][jr]), self.R.point)
            #         krec = krec[0] if len(krec) == 1 else None
            #         self.X.at[i, 'krec'][jr] = krec

            # drop void receiver stations
            # k0 = np.where(np.isnan(self.X.at[i, 'krec']))
            #
            # self.X.at[i, 'CHAN'] = np.delete(self.X.at[i, 'CHAN'], k0)
            # self.X.at[i, 'rline'] = np.delete(self.X.at[i, 'rline'], k0)
            # self.X.at[i, 'rpoint'] = np.delete( self.X.at[i, 'rpoint'] , k0)
            # self.X.at[i, 'rindex'] = np.delete(self.X.at[i, 'rindex'], k0)
            # self.X.at[i, 'instr'] = np.delete(self.X.at[i, 'instr'], k0)
            # self.X.at[i, 'krec'] = np.delete(self.X.at[i, 'krec'], k0)
            # self.X.at[i, 'spar1'] = np.delete(self.X.at[i, 'spar1'], k0)
            # self.X.at[i, 'spar2'] = np.delete(self.X.at[i, 'spar2'], k0)
            #
            # # New n channel after drop
            # self.X.at[i, 'nChan'] = len(self.X.at[i, 'CHAN'])

        # Build SPS
        # Decimate SPS/S SPS/R to stations member in SPS/X
        # k = np.unique(self.X['ksrc'])
        # ksrc = [self.X[i].ksrc for i in range(len(ok))]
        # k = np.unique(ksrc)
        #
        # self.S = [ self.S[ki] for ki in k]
        # self.R = [ self.R[ki] for ki in k]
        # self.X = [ self.X[ki] for ki in k]

        self.nsrc = len(self.S)
        self.nrec = len(self.R)
        self.nx = len(self.X)
