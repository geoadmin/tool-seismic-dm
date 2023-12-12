from SeismicDM.DB import Seis
from SeismicDM.SPS_df import *
from SeismicDM.visualization import *

def createDB():
    Srctxt, Rectxt, Reltxt = load_geometry(geom_PATH)
    # Create geometry structure from s,r,x txt file
    sps = SPS_df(Srctxt, Rectxt, Reltxt, srv)
    segy_file = load_segy(segy_PATH)
    # Create SeisDB
    return Seis(segy_file, sps)


if __name__ == '__main__':
    # %% REPROCESSING TEST
    SeismicDM_PATH = os.getcwd()

    # # 0. Set path
    folder = '2D-Seismik-Dritter/LEAG84_Bund_K1/'
    line = 'LEAG8403'
    Data_PATH = '//adb.intra.admin.ch/SWISSTOPO$/Appl/DATA/PROD/lg/_DatMngt/03_PreProd/02_Seis/'
    geom_PATH = Data_PATH + folder + '02-GEOMETRIE/' + line + '/'
    segy_PATH = Data_PATH + folder + '04-DATA-RAW/' + line + '/'  # read ersten file from folderE

    # 1. Import Geometry : Loadfix + Builddatabase
    Srctxt, Rectxt, Reltxt = load_geometry(geom_PATH)
    s = T0_loadFix_SrcGeom(geom_PATH+Srctxt)
    r = T1_loadFix_RecGeom(geom_PATH+Rectxt)
    x = T2_loadFix_Relation(geom_PATH+Reltxt)
    # sps = SPS_df(geom_PATH,Srctxt, Rectxt, Reltxt, srv = Srctxt[-11:-7],temp_nffid=80)
    sps = SPS_df(geom_PATH,Srctxt, Rectxt, Reltxt, srv = Srctxt[-11:-7])

    # 2. import RAW SEGY
    segy_file = load_segy(segy_PATH)
    segy = os.path.join(segy_PATH, segy_file)
    SeisDB = Seis(segy, sps, line)

    # plotFFID(SeisDB, 4)


    # # plotImshow(SeisDB)



    # -----------------------------------------------------------------------------------------------

    # %% Path to data
    # Dir = '//adb.intra.admin.ch/SWISSTOPO$/Appl/DATA/PROD/lg/_DatMngt/03_PreProd/02_Seis/2D-Seismik-Bund/'
    # find_files_segy(Dir)

    # path_surveys_bund = pd.read_csv('//adb.intra.admin.ch/SWISSTOPO$/Appl/DATA/PROD/lg/01_PRODUKTION/Geophysik/2DSeis_Layer/Seismische_Sektionen/00_Daten/path_surveys_bund.csv')
    # line = 'LEAG8408'
    # for i in range(len(path_surveys_bund['surveys_lines'])):
    #     # print(path_segys_raw['path_windows'][i])
    #     if line in path_surveys_bund['surveys_lines'][i]:
    #         segy_PATH = path_surveys_bund['surveys_lines'][i]+'/04-Data-Raw/'
    #         segy_GEOM = path_surveys_bund['surveys_lines'][i]+'/02-Geometrie/'

    #%% segy PROCESSED test
    # os.chdir(r"C:\SeismicDM")
    # SeismicDM_PATH = os.getcwd()
    # Dir2 = '//adb.intra.admin.ch/SWISSTOPO$/Appl/DATA/PROD/lg/_restricted/_DatMngt_3D/02_Prod/02_Seis/Magglingen3D/20 - DataDeliveries/3D_PTSM&MTDM_20231102/'
    # file2 = Dir2 + 'MACOLIN2D_pstm_03_pp2.sgy'

    # from SeismicDM.DB import Segy_obspy

    # 0. Create object
    # S = Segy_obspy(file2)
    # 1. Plot geometry
    # S._visualize_segy_obspy_geom()
    # 3. Plot data
    # S._visualize_segy_obspy_data(invert_x=1)  # norm=mpl.colors.CenteredNorm() for normalization / cut possible

    #-----------------------------------------------------------------------------------------------------------------
    # S._visualize_segy_obspy_data(cut_up=1000, cut_low=2000, invert_x = 1)
    # # file2 = Dir2 + 'MACOLIN2D_pstm_01_pp2.sgy'
    # # os.chdir(r"M:/Appl/DATA/PROD/lg/01_PRODUKTION/Geophysik/2DSeis_Layer/Seismische_Sektionen/utils/Nav_export_from_segy")
    # # ProjectPath = os.getcwd()
    # # Dir = '//adb.intra.admin.ch/SWISSTOPO$/Appl/DATA/PROD/lg/01_PRODUKTION/Geophysik/2DSeis_Layer/Seismische_Sektionen/utils/TESTs/segys/'
    # # file = Dir + '2021_11_26_ENERGEO_LACOTE2D_Line_01_Final_PSDM_FullStack.sgy'
    # # Dir3 = '//adb.intra.admin.ch/SWISSTOPO$/Appl/DATA/PROD/lg/01_PRODUKTION/Geophysik/DB-Seismik/SEAGLEAG8307/05-DATA-PROCESSED/'
    # # file3 = Dir3 + 'SEAGLEAG8307_stk-p.sgy'




    #### OCR_check
    # from SeismicDM.OCR_check import *
    # line = 'SEAG8403'
    # path = 'M:/Appl/DATA/PROD/lg/01_PRODUKTION/Geophysik/Seismic_Reprocessing/13_Geometrie_batch2/' + line + '/'
    # # path = 'M:/Appl/DATA/PROD/lg/01_PRODUKTION/Geophysik/Seismic_Reprocessing/12_Geometrie_batch1/Intern_test_20231113/' + line + '/'
    # # fix = 1
    # # # method = 2
    # # import_corrected_files = 0
    # # OCR_check(line,path, fix,import_corrected_files)
    # Srctxt, Rectxt, Reltxt = load_geometry(path+'v2/')
    # # PATH = path+'v2/'
    # s = T0_loadFix_SrcGeom(path+'v2/'+Srctxt)
    # r = T1_loadFix_RecGeom(path+'v2/'+Rectxt)
    # x = T2_loadFix_Relation(path+'v2/'+Reltxt)
    # OCR_check(line, path, fix, method, import_corrected_files)
    #endregion

    ## GIS seismischen Sektionen
    # from SeismicDM.SeisLinMapGeoAdmin import *
    # if GIS_seismischen_Linien ==1:
    # Seismische_Linien = SeisLin()
    # # run_test(

    # --------------------------------
    #%% REPROCESSING TEST
    # SeismicDM_PATH = os.getcwd()
    #
    # folder = '2D-Seismik-Dritter/LEAG84__Bund_K1/'
    # line = 'LEAG8403'
    #
    # Data_PATH = '//adb.intra.admin.ch/SWISSTOPO$/Appl/DATA/PROD/lg/_DatMngt/03_PreProd/02_Seis/'
    # Geom_PATH = Data_PATH + folder + '02-GEOMETRIE/' + line + '/'
    # segy_PATH = Data_PATH + folder + '04-DATA-RAW/'  # read ersten file from folder
    #
    # # Import Geometry
    # Srctxt, Rectxt, Reltxt = load_geometry(geom_PATH)


    # geom_PATH = os.path.join(SeismicDM_PATH, folder, '02-NAVIGATION')
    # segy_PATH = os.path.join(SeismicDM_PATH, folder, '04-DATA-RAW')


    # line = ['LEAG8408', 'PSBR9005', 'SADH8401']
    # folder = ['LEAG84__K1/LEAG8408', 'PSBR90__K1/PSBR900501', 'SADH84__K1/SADH8401']
    #
    # ## LOAD GEOM
    # temp_nffid = 42
    # sps = []
    # i = 0
    # for line_i in line:
    #     srv = int(line_i[-4:])
    #     geom_PATH = Data_PATH + '2D-Seismik-Bund/' + folder[i] + '/02-GEOMETRIE/SPS/'
    #     Srctxt, Rectxt, Reltxt = load_geometry(geom_PATH)
    #     files = os.listdir(os.path.abspath(geom_PATH))
    #     sps_i = SPS_df(geom_PATH, Srctxt, Rectxt, Reltxt, srv, temp_nffid)
    #     sps.append(sps_i)
    #     i += 1
    #
    # ## Choose line from list
    # idx = 0
    #
    # ## LOAD RAW SEGY
    # segy_PATH = Data_PATH + '2D-Seismik-Bund/' + folder[idx] + '/04-DATA-RAW/'  # read ersten file from folder
    # segy_file = load_segy(segy_PATH)
    # segy = os.path.join(segy_PATH, segy_file)
    # SeisDB = Seis(segy, sps[idx], line[idx])
    #
    # plotImshow(SeisDB)
    # --------------------------------------------------------------------------------------------

    # Srctxt, Rectxt, Reltxt = load_geometry(geom_PATH)
    # sps = SPS_df(geom_PATH, Srctxt, Rectxt, Reltxt, srv, temp_nffid)

    # # # plot geom 3D
    # # from SeismicDM.utils import read_raster
    # # filename = 'C:/SeismicDM/Testdata/Testdata2/swissalti3d_9005.tif'
    # # tif_files = 'C:/SeismicDM/Testdata/Testdata2/tif_files'
    # # p = pv.Plotter()
    # # for tif_file in os.listdir(tif_files):
    # #     mesh = read_raster(tif_files + '/' + tif_file)
    # #     p.add_mesh(mesh)
    # #     contours = mesh.contour()
    # # points_R = np.vstack((sps.R.easting + 2000000, sps.R.northing + 1000000, sps.R.elevation)).T
    # # point_cloud = pv.PolyData(points_R)
    # # point_cloud["elevation"] = sps.R.elevation
    # # p.add_mesh(point_cloud, color='maroon', point_size=5.0, render_points_as_spheres=True)
    # # p.show_grid()
    # # p.show()
    # segy_file = load_segy(segy_PATH)
    # segy = os.path.join(segy_PATH,segy_file)
    # SeisDB = Seis(segy, sps, line)
    # # plot_Geom_src_rec(SeisDB)
    # # plotWavelets(SeisDB)

    # if existingDB == 0:
    #     SeisDB = createDB()
    #     SeisDB._saveSeisDB('SeisDB')
    #     SeisDB = pd.read_pickle(SeismicDM_PATH + '/temp/SeisDB.pkl')
    # else:
    #     # Load DB if already exists
    #     print('Import pkl')
    #     SeisDB = pd.read_pickle(SeismicDM_PATH+'/temp/SeisDB.pkl')

    # # Test if download correct
    # # plotWavelets(SeisDB)
    #
    # # ASSIGN GEOM - can be called in class when finished
    # SeisDB._navmergesps()
    # # # TODO: fix styp and do azimuthdip function
    # plot_Geom_src_rec(SeisDB)
    # plotWavelets(SeisDB)

