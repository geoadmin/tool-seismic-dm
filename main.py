from SeismicDM.DB import Seis
from SeismicDM.SPS import *
from SeismicDM.visualization import *

if __name__ == '__main__':
    # %% REPROCESSING TEST
    SeismicDM_PATH = os.getcwd()

    # User imputs
    import_existing_sps = 1
    import_existing_segy = 1

    # # 0. Set path
    geom_PATH = Data_PATH + folder + '02-GEOMETRIE/' + line + '/'
    segy_PATH = Data_PATH + folder + '04-DATA-RAW/' + line + '/'  # read ersten file from folderE

    # 1. Import Geometry : Loadfix + Builddatabase
    if import_existing_sps == 0:
        Srctxt, Rectxt, Reltxt = load_geometry(geom_PATH)
        s = T0_loadFix_SrcGeom(geom_PATH+Srctxt)
        r = T1_loadFix_RecGeom(geom_PATH+Rectxt)
        x = T2_loadFix_Relation(geom_PATH+Reltxt)
        # sps = SPS_df(geom_PATH,Srctxt, Rectxt, Reltxt, srv = Srctxt[-11:-7],temp_nffid=80)
        sps = SPS_df(geom_PATH,Srctxt, Rectxt, Reltxt, srv = Srctxt[-11:-7])
        sps._saveSPS(name='tempSPS', path= SeismicDM_PATH)
    else:
        sps = pd.read_pickle(SeismicDM_PATH + '/temp/tempSPS.pkl')

    # 2. import RAW SEGY
    if import_existing_segy==0:
        segy_file = load_segy(segy_PATH)
        segy = os.path.join(segy_PATH, segy_file)
        SeisDB = Seis(segy, sps, line)
        SeisDB._saveSeisDB(name= 'tempSeisDB', path=SeismicDM_PATH)
    else:
        SeisDB = pd.read_pickle(SeismicDM_PATH+'/temp/SeisDB.pkl')

    # 3. create THR
    SeisDB._navmergesps()



