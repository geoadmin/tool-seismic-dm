import pandas as pd
import numpy as np
from .userInputs import *
from .headers import TRACE_HEADER_ADDITIONAL
from .utils import find

def spsAssignGeomToTHR(S, ktr=0, gm=2):
    """
    transcribes source- and receiver-related
    information from a SPS database to seismic trace headers.
    :param S:
    :param ktr: Indices of traces to which geometry shall be assigned.
                This trace-subset must must have the same FFID !
    :param gm: Operation mode. 0: does not assign geometry, 1: assign only source-point-related geometry
               2: assign source and receiver-related geometry
    :return:
    """

    if temp_nffid:
        print('use temp nffid') # TODO: remove this temp nffid for final data
        ntr = temp_nffid
    else:
        ntr = S.nffid

    # Add non standard trace headers
    for attribute in TRACE_HEADER_ADDITIONAL:
        if hasattr(S.traces.headers, attribute[1]) == False:
            S.traces.headers[attribute[1]] = np.array([0 for i in range(ntr)])

    # # Check for numeric station type ID in field PTCNUM?
    # # TODO: ergänzen
    #
    # if ktr==0:
    #     print('Geometry assigned to all indeces')
    #     ktr = [ i for i in range(S.nffid)]
    #
    # if gm ==2:
    #
    #     ntrEdit = len(ktr)
    #
    #     ffid = pd.unique(S.traces.ffid(ktr))
    #
    #     # Index of FFID-matching relation record
    #     # must be a singel index in expanded relation records
    #     kx = find(S.SPS.X.ffid, ffid)
    # else:
    #     print('Operation mode not processed here')
    
    return S


def snavmergesps(S):
    """
    Assign a survey acquisition geometry provided by a SPS database to
    a seismic shot records provided as a seismic data structure (s)
    """
    # TODO : finish

    # ASSIGIN GEOMETRY TO SEISMIC TRACES
    ffid = S.traces.headers['ffid']
    uffid = pd.unique(ffid)
    nffid = len(uffid)
    trid = S.traces.headers['trid']

    # Set default values for header variables to be modified
    S = spsAssignGeomToTHR(S)



