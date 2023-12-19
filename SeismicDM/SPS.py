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

    def _saveSPS(self, name='tempSPS', path=None):
        pd.to_pickle(self, path + '/temp/' + name + '.pkl')


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
                # raise ValueError('Non-unique FFID')
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
            chanLast = self.X['nChan'][j]+1 # chanlast: in python, last = last-1
            ChanB = np.arange(chanFirst,chanLast, chanIncr).astype(int)

            # assign channel numbers
            self.X.at[i, 'CHAN'] = np.concatenate((ChanA, ChanB), axis=0) # [ChanA, ChanB], axis=0 keeps ","

            # receiver point identification, layout A
            recFirst = RelGeom['RPal'][j] - len(ChanA) #TODO: verify !! angepasst
            recLast = RelGeom['RPal'][j]
            recA = np.arange(recFirst, recLast, chanIncr)
            # receiver point identification, layout A
            recFirst = RelGeom['RPbl'][j]
            recLast = RelGeom['RPbl'][j] + len(ChanB) #TODO: verify !! angepasst
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
            # if not (isempty(find(([S.point] + i * [S.index]) == (s.point + i * s.index)))) # MATLAB : what is i??

            # check for unique records
            # if ismember(r.point, [R.point])  # matlab
            if self.R['point'][j] in self.R['point'][:j]:
                print('Non-unique R-point')

            self.nsrc = len(self.S)
            self.nrec = len(self.R)
            self.nx = len(self.X)

        # COMPILE SPS DB
        # complete relation record #TODO: why two loops and not only one in matlab? if lenth X varies?
        for j in range(self.nx):

            # source record index
            # sps.X(j).ksrc = spsfindsrc(sps, sps.X(j).sline, sps.X(j).spoint, sps.X(j).sindex);

            self.X.at[j, 'ksrc'] = spsfindsrc(self, self.X['sline'][j], self.X['spoint'][j], self.X['sindex'][j])
            if not self.X.at[j, 'ksrc'] and self.X.at[j, 'ksrc'] != 0:
                print('No matching source point')

            # receiver record indices
            # non-existing recs are assigned KREC = 0
            # self.X.at[j,'krec'] = np.zeros((1, self.X['nChan'][j]))
            self.X.at[j,'krec'] = np.zeros(self.X['nChan'][j])

            for jr in range(self.X['nChan'][j]):
                # a = self.X['rindex'][j][0, jr]
                k = spsfindrec(self, self.X['rline'][j][0, jr], self.X['rpoint'][j][jr], self.X['rindex'][j][0, jr])
                self.X.at[j,'krec'][jr] = k

            # Drop X records without R equivalent
            # k0 = findx(0, self.X['krec'][j])
            # k0 = np.where(np.isnan(self.X['krec'][j])) # find where nan are!
            k0 = np.where(np.isnan(self.X.at[j, 'krec'])) # find where nan instead of 0
            k0 = k0[0]
            # print('{} Rec of d {} stations dropped from X{}'.format(len(k0)-1,self.X['nChan'][j], j))

            # aux information (dummy)
            self.X.at[i, 'instr'] = np.ones((1, self.X['nChan'][j]))
            self.X.at[i, 'spar1'] = np.zeros((1, self.X['nChan'][j]))
            self.X.at[i, 'spar2'] = np.zeros((1,self.X['nChan'][j]))

            if len(k0) > 0 :
                # drop void receiver stations
                self.X.at[j, 'CHAN'] = np.delete(self.X.at[j, 'CHAN'], k0)
                self.X.at[j, 'rline'] = np.delete(self.X.at[j, 'rline'], k0)
                self.X.at[j, 'rpoint'] = np.delete( self.X.at[j, 'rpoint'], k0)
                self.X.at[j, 'rindex'] = np.delete(self.X.at[j, 'rindex'], k0)
                # self.X.at[j, 'instr'] = np.delete(self.X.at[j, 'instr'], k0) # todo: fix dimensions
                self.X.at[j, 'krec'] = np.delete(self.X.at[j, 'krec'], k0)
                # self.X.at[j, 'spar1'] = np.delete(self.X.at[j, 'spar1'], k0)
                # self.X.at[j, 'spar2'] = np.delete(self.X.at[j, 'spar2'], k0)

            # New n channel after drop
            self.X.at[j, 'nChan'] = len(self.X.at[j, 'CHAN'])

            #TODO: spsreport




        # Build SPS
        # Decimate SPS/S SPS/R to stations member in SPS/X
        # k = np.unique(self.X['ksrc'])
        # ksrc = [self.X[i].ksrc for i in range(len(ok))]
        # k = np.unique(ksrc)
        #
        # self.S = [ self.S[ki] for ki in k]
        # self.R = [ self.R[ki] for ki in k]
        # self.X = [ self.X[ki] for ki in k]


