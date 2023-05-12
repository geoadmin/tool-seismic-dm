from .loadSegy import *
from .paths_init import (SeismicDM_PATH)


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


class Seis(object):
    def __init__(self, file=None, SPS = None, binary_header=None, trace_header=None, endianness='>'):

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
            self.traces = Traces()
            self._loadSegy()

    def _loadSegy(self):
        loadSegy(self)


    def _saveSeisDB(self,name = 'tempDB'):
        pd.to_pickle(self, SeismicDM_PATH+'/temp/' + name + '.pickle')

    def navmergesps(self):
        """
        Assign a survey acquisition geometry provided by a SPS database to seismic shot records provided as a seismic data structure (s)
        :return:
        """
        # TODO
        print('----')
