import numpy as np
import pandas as pd
from .userInputs import temp_nffid
from .headers import (BINARY_FILE_HEADER, TRACE_HEADER)
from .utils import *


def loadSegy(Object):

    # TODO : read encoding -- function
    Object.header_encoding = 'cp500' # textual file
    Object.endianness = 'big' # Object.fileheader.endia : get endianness there

    # Read textual file header (3200 bytes). Encoding in EBCDIC or ASCII.
    try:
        with open(Object.file, encoding=Object.header_encoding) as f:  # 'rb for utf8
            # Textual file header
            dic = {}
            for n in range(int(3200 / 80)):
                key = f.read(3)
                value = f.read(77)
                dic[key] = value
            Object.textual_header = pd.DataFrame.from_dict([dic]).T
    except:
        raise ImportError('File summary can not be read')

    # Read binary file header. (240 bytes after textual file header of 3200 bytes)
    try:
        with open(Object.file, 'rb') as f:
            f.seek(3200)  # jump to binary file header
            [setattr(Object.fileheader, ls[1], int.from_bytes(f.read(ls[0]), byteorder=Object.endianness))
             for ls in BINARY_FILE_HEADER]
    except:
        raise ImportError('File header can not be read')

    # TODO : read format -- function
    Object.dform = Object.fileheader.dform
    
    # Fetch for each shot its header and data
    try:
        with open(Object.file, 'rb') as f:
            f.seek(3600)  # jump to end of trace file header
            df_h = pd.DataFrame(columns=[ls[1] for ls in TRACE_HEADER])
            df_d = pd.DataFrame(columns=[i for i in range(Object.fileheader.nsam)])  # nvr columns = nsamples
            # for n in range(self.nffid):
            for n in range(temp_nffid):  # TODO: change when ready to store entire DB
                for i in range(Object.fileheader.ntr):
                    df_h.loc[n] = np.asarray([int.from_bytes(f.read(ls[0]), byteorder=Object.endianness)
                                            for ls in TRACE_HEADER])
                    df_d.loc[n * i] = np.array([unpack_ibm_4byte(f) for le in range(df_h['ns'][n])])
            Object.traces.headers = df_h
            Object.traces.data = df_d.T  # invert dataframe to have row as traces
    except:
        raise ImportError('Traces can not be read')
