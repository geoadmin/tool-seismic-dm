import os

from SeismicDM.Seis_DM import SPS, Seis
from SeismicDM.paths_init import (geom_PATH,segy_PATH)
from SeismicDM.user_inputs import srv
from SeismicDM.utils import load_segy, load_geometry
from SeismicDM.visualization import plot_wavelets


if __name__ == '__main__':
    # Create geometry structure from s,r,x txt file
    Srctxt, Rectxt, Reltxt = load_geometry(geom_PATH)
    sps = SPS(Srctxt, Rectxt, Reltxt, srv)
    # Create SeisDB
    segy_file = load_segy(segy_PATH)
    SeisDB = Seis(segy_file, sps)

    #-----------------
    #TODO: encoding, endianness and data format
    # EBCDIC Text Header Encoding
    # Big Endian byte order
    # IBM Float 32 bit sample format

    # Look at raw shots
    # plot_wavelets(SeisDB)
    # a=SeisDB.navmergesps()




