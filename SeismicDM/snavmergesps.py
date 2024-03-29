from .userInputs import *
from .headers import TRACE_HEADER_ADDITIONAL
from .utils import *

def spsAssignGeomToTHR(s, KTR=0, gm=2):
    """
    transcribes source- and receiver-related
    information from a SPS database to seismic trace headers.
    :param s:
    :param ktr: Indices of traces to which geometry shall be assigned.
                This trace-subset must have the same FFID !
    :param gm: Operation mode. 0: does not assign geometry, 1: assign only source-point-related geometry
               2: assign source and receiver-related geometry
    :return:
    """
    s=0
    print('write function snavmergesps_df')
#     nx = s.SPS.nx
#
#     # Add non standard trace headers
#     for attribute in TRACE_HEADER_ADDITIONAL:
#         if hasattr(s.traces.headers, attribute[1]) == False:
#             s.traces.headers[attribute[1]] = np.array([0 for i in range(nx)])
#             # s.TRH[attribute[1]] = np.array([0 for i in range(ntr)])
#
#     #TODO : add PTCNUM
#
#     if KTR==0:
#         print('Geometry assigned to all indices')
#         if not temp_nffid:
#             KTR = [i for i in range(s.nffid)]
#         else:
#             KTR = [i for i in range(temp_nffid)]
#
#
#
#     ntrEdit = len(KTR)
#     checkt = []
#
#     for ktr in KTR:
#         ffid = s.traces.headers.fldr[ktr]
#
#         # Index of FFID-matching relation record
#         # must be a single index in expanded relation records
#         kx = findValueinObj(ffid, s.SPS.X, 'ffid')
#         # print('kx: ', kx)
#
#         if kx == None:
#             ntr = 0
#         else:
#             # .............................
#             # Index of matching SPS S record
#             ks =s.SPS.X[kx].ksrc
#             # print('matching SPS S : ks =', ks)
#
#             # Number of traces to edit
#             ntr = len(KTR)
#
#             ## Assign source-point related information
#             for i in range(ntr):
#                 lsc = 0  # optional input
#                 # np.warnings.filterwarnings('ignore')
#                 s.traces.headers.at[ktr, 'ep'] = s.SPS.S[ks].line * lsc*10 + s.SPS.S[ks].point * 10 + s.SPS.S[ks].index # sn same as ep?
#                 s.traces.headers.at[ktr, 'sx'] = s.SPS.S[ks].easting
#                 s.traces.headers.at[ktr, 'sy'] = s.SPS.S[ks].northing
#                 s.traces.headers.at[ktr, 'selev'] = s.SPS.S[ks].elevation
#                 s.traces.headers.at[ktr, 'sdepth'] = s.SPS.S[ks].depth
#                 s.traces.headers.at[ktr, 'swdep'] = s.SPS.S[ks].waterdepth
#                 s.traces.headers.at[ktr, 'sdel'] = s.SPS.S[ks].srd
#                 s.traces.headers.at[ktr, 'sut'] = s.SPS.S[ks].uht
#                 s.traces.headers.at[ktr, 'sstat'] = s.SPS.S[ks].stat
#                 # s.traces.headers['styp'][ktr[i]] = s.SPS.S[ks[i]].ptcnum  # TODO: add
#                 s.traces.headers.at[ktr, 'sline'] = s.SPS.S[ks].line
#                 s.traces.headers.at[ktr, 'spoint'] = s.SPS.S[ks].point
#                 s.traces.headers.at[ktr, 'sindex'] = s.SPS.S[ks].index
#                 s.traces.headers.at[ktr, 'spsks'] = ks
#                 s.traces.headers.at[ktr, 'spskx'] = kx
#                 s.traces.headers.at[ktr, 'ssp1'] = s.SPS.S[ks].spare1
#                 s.traces.headers.at[ktr, 'ssp2'] = s.SPS.S[ks].spare2
#
#             # Check source time stamp
#             ts = 24*3600 * s.traces.headers.day[ktr] +\
#                  3600 * s.traces.headers.hour[ktr] + 60 * s.traces.headers.minute[ktr] +\
#                  s.traces.headers.sec[ktr]
#             checkt = np.append(checkt, ts)
#             # if len(np.unique(ts)) < len(ts): print('Error : ts are not unique')
#
#             #  Assign receiver related geometry
#             # Indices of matching SPS R records
#             KR = s.SPS.X[kx].krec
#             # print('KR: ', KR)
#             chanR = s.SPS.X[kx].CHAN
#             # print('chanR: ', chanR)
#
#             # Channel number
#             CHAN = s.traces.headers.tracf[ktr]
#             # print('CHAN trace: ', CHAN)
#
#             ntr_assigned = 0
#             ntr_missing = 0
#
#             # Find matching channel in the seismic data
#             k = findx(CHAN, chanR)
#             if len(k)>0:
#                 k = k[0]
#             else:
#                 ntr_missing += 1
#                 k = None
#
#             if not (k is None) and k > temp_nffid : k = None #Todo: remove condition when all
#             if not (k is None):
#
#                 # # Loop over channels reported in the SPS database
#                 for j in range(len(KR)):
#                     # Index of trace at hand
#                     jtr = KTR[k]
#                     # Index of matching SPS-R-record
#                     kr = int(KR[j])
#                     if not (kr is None) and kr < temp_nffid: # Todo: remove condition when all
#
#                         # Effective receiver elevation
#                         gelev = s.SPS.R[kr].elevation - s.SPS.R[kr].depth
#
#                         # Assign receiver related geometry
#                         s.traces.headers.at[jtr, 'duse'] = 1
#                         s.traces.headers.at[jtr, 'cdpt'] = s.SPS.R[kr].line * lsc*10 + s.SPS.R[kr].point*10 + s.SPS.R[kr].index
#                         s.traces.headers.at[jtr, 'gx'] = s.SPS.R[kr].easting  # round in matlab
#                         s.traces.headers.at[jtr, 'gy'] = s.SPS.R[kr].northing  # round in matlab
#                         s.traces.headers.at[jtr, 'gelev'] = gelev  # round?
#                         s.traces.headers.at[jtr, 'gwdep'] = s.SPS.R[kr].waterdep
#                         s.traces.headers.at[jtr, 'gdel'] = s.SPS.R[kr].srd
#                         s.traces.headers.at[jtr, 'gut'] = s.SPS.R[kr].uht
#                         # # s.traces.headers.at[jtr, 'gstat'] = s.SPS.R[krstat # TODO: add
#                         # # s.traces.headers.at[jtr, 'tatyp'] = s.SPS.R[kr].ptcnum # TODO: add
#                         s.traces.headers.at[jtr, 'rline'] = s.SPS.R[kr].line
#                         s.traces.headers.at[jtr, 'rpoint'] = s.SPS.R[kr].point
#                         s.traces.headers.at[jtr, 'rindex'] = s.SPS.R[kr].index
#                         s.traces.headers.at[jtr, 'spskr'] = kr
#                         s.traces.headers.at[jtr, 'rsp1'] = s.SPS.R[kr].spare1
#                         s.traces.headers.at[jtr, 'rsp2'] = s.SPS.R[kr].spare2
#
#                         ntr_assigned += 1
#
#                         # Compute midpoint-related coordinates and offsets
#                 # Todo: fix mean with gx, gy
#                 cdpx = (s.traces.headers.sx[ktr] + s.traces.headers.gx[ktr]) / 2
#                 # print(s.traces.headers.sx[ktri],s.traces.headers.gx[ktri],  cdpx)
#                 cdpy = (s.traces.headers.sy[ktr] + s .traces.headers.gy[ktr]) / 2
#                 offs = np.sqrt((s.traces.headers.sx[ktr] - s.traces.headers.gx[ktr])**2 +
#                                (s.traces.headers.sy[ktr] - s.traces.headers.gy[ktr])**2)
#
#                 # Compute src-to-rec azimuth and dip
#                 # negative dips indicate src-pt at greater elevation than rec-pt
#                 dx = -(s.traces.headers.sx[ktr] - s.traces.headers.gx[ktr])
#                 dy = -(s.traces.headers.sy[ktr] - s.traces.headers.gy[ktr])
#                 dz = s.traces.headers.selev[ktr] - s.traces.headers.sdepth[ktr] - s.traces.headers.gelev[ktr]
#                 # azim, dip = azimuthdip(dx, dy, dz) # TODO : add function
#
#                 # Transcribe midpoint attributes to trace headers
#                 if s.traces.headers.duse[ktr] == 1 :
#                     s.traces.headers.at[ktr, 'cdpx'] = cdpx
#                     s.traces.headers.at[ktr, 'cdpy'] = cdpy
#                     s.traces.headers.at[ktr, 'offset'] = offs
# #             # s.traces.headers.azimuth[ktr, 'azimuth'] = azim[khi]
# #             # s.traces.headers.dip[ktr, 'dip'] = dip[khi]
# #
#     uniquet = np.unique(checkt)
#     if len(uniquet) < len(checkt) : print('Error : ts are not unique')

    return s


def snavmergesps(S, vFFID = None, verbose = None):
    """
    @author: Andreas Hoelker
    Assign a survey acquisition geometry provided by a SPS database to
    a seismic shot records provided as a seismic data structure (s)

    :param S: a seismic data structure. Required trace headers are:
              FLDR:     Shot identification, corresponding to FFID in SPS data
              TraceF:   Channel numbers, corresponding to channels in SPS data
              TRID:     Trace identification code, where:
                        1 indicates production seismic traces
                        >1 auxillary traces
                        0 void traces.
              SPS:      SPS database, with shot, receiver station records and relation records

    :runtime parameters:
              verbose=true  Switch: Progress/data reporting on/off
              vFFID:    Nummeric array holding a listing of void FFIDs,
                        i.e. FFIDs ocrruing in S but not to be assigned geometry
                        Typically these are the FFIDS of the daily tests
              xysc=10   Scaling factor applicable to X/Y coordinates prior to writing them into trace headers.
                        Coordinates will be rounded to integers after scaling. Default is 10.
              zsc=10    Scaling factor applicable to elevation and depth prior to writing them into trace headers.
                        Elevation will be rounded to integers after scaling. Default is 10.
              tsc=1     Scaling factor applicable to times (uphole, static shift) prior to writing them into trace head.
                        Times will be rounded to integers after scaling. Default is 1.
              lsc = *   Factor to scale line numbers when combining with point station numbers: line*LSC+station.
                        * the default is auto-determined
              ttol=2    Tolerance [s] when comparing shot time stamps from the SPS data and seismic data.
              check=true    Switch: Check consistency of SPS database. true= check, false= skip test

    :return: S= Seismic data structure, copy of input S, acquisition geometry added to headers

    """
    # TODO : finish
    print('snavmergesps')

    # ================================================
    # RUNTIME PARAMETERS
    #todo: implement

    # ================================================
    # COUNT FFID & TRACES
    #todo: implement

    # List of FFID and TRIDs per trace
    FFID = S.traces.headers['fldr']
    TRID = S.traces.headers['trid']
    #     FFID = S.traces.fldr[j]
    #     TRID = S.traces.trid[j]
    # exlude uniques : UFFID = pd.unique(FFID) + exclude

    # Set of unique FFIDs ( not excluding void-FFIDs)
    uFFID = pd.unique(FFID)

    # FFID counts
    nFFID = len(uFFID)
    if vFFID:
        nFFIDvoid = len(vFFID)
        nFFIDprod = nFFID - nFFIDvoid

    #Trace counts
    ntrTotal = len(FFID)
    k1 = np.where(ismember(FFID,vFFID)==0)
    k2 = TRID.index[TRID ==1] #k2 = sum(TRID == 1)
    k3 = TRID.index[TRID >1]
    ntrVoid = ntrTotal - len(k1)
    ntrProd = len(intersect_mtlb(k1,k2))
    ntrAux = len(intersect_mtlb(k1,k3))

    # Report
    if verbose:
        print('\n')
        print('Number of FFIDs: {}'.format(nFFID))
        print('Number of production FFIDs: {}'.format(nFFIDprod))
        print('Number of void FFIDs: {}'.format(nFFIDvoid))
        print('\n')
        print('Number of traces: {}'.format(ntrTotal))
        print('Number of seis. prod. data: {}'.format(ntrProd))
        print('Number of ass. void-FFIDs: {}'.format(ntrVoid))
        print('\n')


    # ================================================
    # NUMBER OF STATIONS, TRACES, etc
    nS = S.sps.S.shape[0]
    nR = S.sps.R.shape[0]
    nX = S.sps.X.shape[0]

    # Number of traces in SPS relation records
    ntrSPS = sum(S.sps.X['nChan'])

    # Number of traces in the seismic data
    # ntrSeis = sum(S.ntr)
    # print(ntrSeis)

    #
    # ================================================
    # ASSIGIN GEOMETRY TO SEISMIC TRACES



    # Counter of production ffid in data not being assigned
    # a geometry because there is no matching ffid in SPS
    nLack = 0

    # Loop over ffids in seismic data
    print('create spsAssignGeomToTHR')

    # for j in range(len(ffid)):
        # Assign shot-related SPS data to aux traces

        # Assign full geometry to production traces
    # S = spsAssignGeomToTHR_df(S)
    #
    #
    #     # Count FFID not assigned a geometry
    # nlack += 1




