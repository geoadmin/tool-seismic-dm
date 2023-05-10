
import os
import utils
from user_inputs import (DB_seismik_path,Seismic_Datamanagement_path,
                         Srctxt, Rectxt, Reltxt,
                         line_name,srv)
from Seis_DM import *

print(os.getcwd())
#TODO: when Git repository ready, use relative path

# Get path to stored data
Geom_input_path = DB_seismik_path+line_name+'/02-NAVIGATION/'
Object_output_path = Seismic_Datamanagement_path+'Preprocessed_segy/'+line_name
segy_path = DB_seismik_path+line_name+'/04-DATA-RAW/'
segy_file = utils.get_file_in_folder(segy_path)

# Create geometry structure from s,r,x txt file
os.chdir(Geom_input_path)
sps = SPS(Srctxt, Rectxt, Reltxt, srv)

# Create SeisDB
os.chdir(segy_path)
SeisDB = Seis(segy_file, sps)


#-----------------

#TODO: get encoding, endianness and data format
# EBCDIC Text HEader Encoding
# Big Endian byte order
# IBM Float 32 bit sample format
# ---------------> fix values data


# Use Obspy to load segy
from segy2csv import *
# segy_file = '8403.SGY'
# data = segy_data(segy_path,segy_file)
# ObypyS = ObspySegyS(segy_path,segy_file)

# # Look at raw shots
# a=navmergesps(SeisDB)




