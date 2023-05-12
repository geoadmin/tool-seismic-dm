from SeismicDM.SPS import SPS
from SeismicDM.SEGY import Seis
from SeismicDM.paths_init import (SeismicDM_PATH, geom_PATH, segy_PATH)
from SeismicDM.user_inputs import srv, existingDB
from SeismicDM.utils import load_segy, load_geometry
from SeismicDM.visualization import plotWavelets
import pandas as pd


def createDB():
    Srctxt, Rectxt, Reltxt = load_geometry(geom_PATH)
    # Create geometry structure from s,r,x txt file
    sps = SPS(Srctxt, Rectxt, Reltxt, srv)
    segy_file = load_segy(segy_PATH)
    # Create SeisDB
    return Seis(segy_file, sps)


if __name__ == '__main__':
    if existingDB == 0:
        SeisDB = createDB()
        SeisDB._saveSeisDB('SeisDB')
    else:
        # Load DB if already exists
        SeisDB = pd.read_pickle(SeismicDM_PATH + '/temp/SeisDB_temp.pickle')

    # Test if download correct
    # plotWavelets(SeisDB)


