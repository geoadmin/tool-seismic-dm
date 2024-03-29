import os
import re
import numpy as np
import pandas as pd
import struct
import xarray as xr
import pyvista as pv

# from .pathsInit import (SeismicDM_PATH, geom_PATH, segy_PATH)
# from .userInputs import srv




def load_geometry(geom_folder_path):
    files = os.listdir(os.path.abspath(geom_folder_path))
    geom_files = []
    for file in files:
        geom_files.append(file)
    try:
        # as R comes bevor S in the alphabet, we invert the order to have sources first
        return geom_files[1], geom_files[0], geom_files[2]
    except:
        print('Warning: {} is missing file(s)'.format(geom_folder_path))
        pass


def load_segy(segy_folder_path):
    files = os.listdir(os.path.abspath(segy_folder_path))
    for file in files:
        return file
    else:
        print('Warning: {} is empty'.format(segy_folder_path))
        return 0

def unpack_ibm_4byte(f):
    """
    From: ibm2ieee(ibm)
    https://stackoverflow.com/questions/7125890/python-unpack-ibm-32-bit-float-point

    Converts an IBM floating point number into IEEE format.
    :param: ibm - 32 bit unsigned integer: unpack('>L', f.read(4))
    """
    [int32] = struct.unpack(">L", f.read(4))
    if int32 == 0:
        return 0
    else:
        sign = int32 >> 31 & 0x01
        exponent = int32 >> 24 & 0x7f
        mantissa = (int32 & 0x00ffffff) / float(pow(2, 24))
        return (1 - 2 * sign) * mantissa * pow(16, exponent - 64)


def get_header(f, HEADER, endianness):
    dic = {}
    for ls in HEADER:
        b = int.from_bytes(f.read(ls[0]), byteorder=endianness)
        # TODO:   if ls[1] == 'trheadnam': chr(b)
        dic[ls[1]] = b
    header_df = pd.DataFrame.from_dict([dic])
    return header_df


def return_ascii_header(file_header):
    r = r"[^\d\s]+ \S+: \S+"  # good to match non-digit + str: + str
    attributes = re.findall(r, str(file_header))
    dic = {}
    for att in attributes:
        value = att.partition(':')[2]
        key = att.partition(':')[0]
        dic[key] = value

    df_file_header = pd.DataFrame.from_dict([dic])
    return df_file_header


def get_bytefactor_from_format(format_data_sample):
    # TODO: verify https://en.wikipedia.org/wiki/IBM_hexadecimal_floating-point
    if format_data_sample == 1: bytefactor = 4      # '4-Byte IMB floating point'
    if format_data_sample == 2: bytefactor = 4      # 4-byte two complement integer
    if format_data_sample == 3: bytefactor = 2      # 2-byte two complement integer
    if format_data_sample == 4: bytefactor = 4
    if format_data_sample == 5: bytefactor = 4      # np.float32 # 4-byte ieee floating-point
    if format_data_sample == 6: bytefactor = 8      # 8-byte ieee floating point
    if format_data_sample == 7: bytefactor = 3      # 3-byte two's complement integer
    if format_data_sample == 8: bytefactor = 1      # 1-byte two's complement integer
    if format_data_sample == 9: bytefactor = 8      # 8-byte two's complement integer
    if format_data_sample == 10: bytefactor = 4     # np.uint32      # 4-byte unsigned integer
    if format_data_sample == 11: bytefactor = 2     # np.uint16      # 2-byte unsigned integer
    if format_data_sample == 12: bytefactor = 8     # np.uint64      # 8-byte unsigned integer
    if format_data_sample == 15: bytefactor = 3     # np.uint24      # 3-byte unsigned integer
    if format_data_sample == 16: bytefactor = 1     # np.uint8       # 1-byte unsigned integer
    return bytefactor


def txt2df(txt_file):
    df = pd.read_csv(txt_file, comment='#', delimiter=" ", header=None, skipinitialspace=True)  # delimiter = "\t"
    return df


def get_index(serie1, serie2):
    idx = [i for (i, val) in enumerate(serie1) if serie1 in serie2]
    return idx


def findx(x_a, b):
    """
    Get index where element x_a is found in serie b
    """
    k = [i_b for i_b, x_b in enumerate(b) if x_b == x_a]
    return k


def find(xa, b):
    """
    Get index where elements xa are found in serie b
    """
    # k = [i_b for x_a in a for i_b, x_b in enumerate(b) if x_b == x_a]
    if isinstance(xa,(int, np.integer)):
        ki = np.asarray([int(i_b) for i_b, x_b in enumerate(b) if x_b == xa])
        if len(ki) == 1:
            return int(ki[0])
        elif len(ki)>1 :
            # print('index non unique')
            return int(ki[0])
        else:
            print('No index match in {} for {}:'.format(b,ki))
            pass

def intersect_mtlb(a, b):
    """
    https://stackoverflow.com/questions/45637778/how-to-find-intersect-indexes-and-values-in-python
    """
    a1, ia = np.unique(a, return_index=True)
    b1, ib = np.unique(b, return_index=True)
    aux = np.concatenate((a1, b1))
    aux.sort()
    c = aux[:-1][aux[1:] == aux[:-1]]
    return c

def ismember(A, B):
# https://stackoverflow.com/questions/25923027/matlab-ismember-function-in-python
  return [1 if (i == B) else 0 for i in A]


def spsfindsrc(sps, line, point, sindex):
    """
    % Author: Andreas Hoelker
    This function returns teh SPS-S index of a source station (or indices of multiple stations) given line, point and index numbers or easting/northing coordinates.
    Optionally also returns teh indices of the matching SPS-X records.
    :param sps: SPS data structure
    :param line: Source line number(s)
    :param point: Source point number(s)
    :param sindex: Source index. Default is all indices
    :return: ks: Index of teh SPS.S record(s) matching the source line/point/index or eas/nor range. Empoty array if no match is found.
             kx: Indices of matching relation records. Empty array, if no matches are found or if the SPS structure contains no relation records.
                 If expanded relation records are available, the original relation records are ignored.
    """

    # ===============================================
    # Search for point data assuming eas/nor :
    # Note: eas/nor input requires 1x2 arrays.
    # Note: If eas/nor is outside eas/nor value range in data, line/point input is assumed.
    ks = []
    if hasattr(line, "__len__") and hasattr(point, "__len__"):
        print('function spsfindptxy not existing yet')
        pass
        # ks = spsfindptxy(sps.S, [min(line) max(line)], [min(point) max(point)])
        # #TODO: function spsfindptxy

    # ===============================================
    # Search point data by line/point
    # Note: for each sps.S.line/point, find its position in line/point Array
    if not ks:
        k1 = findx(line, sps.S.line)
        k2 = findx(point, sps.S.point)
        ks = intersect_mtlb(k1, k2)
        len_ks = len(ks)
        if len(ks) > 1: ks = ks[sindex-1]
        else: ks = int(ks)

    # NOTE MATLAB: k1 = find(ismember([sps.S.line], line));
    # find gibt Vektor zurück mit Indizes jedes Elements ungleich null im Array.
    # ismember(A,B) gibt Vektor zurück mit 1 if element in A auch in B, 0 sonst
    # intersect(A,B) returns data common to A and B, with no repetitions and C in sorted order.

    return ks

    # ===============================================
    # Search relation records -- OPTIONAL #TODO: fix
    # kx = []
    # SL = sps.X['sline']
    # SP = sps.X['spoint']
    # try:
    #     SI = sps.X['sindex']
    # except:
    #     SI = sps.X['sptidx']
    #
    # # for j in range(len(sps.S['line'])):
    # k1 = findx(sps.S['line'][ks], SL)
    # k2 = findx(sps.S['point'][ks], SP)
    # kxi = intersect_mtlb(k1, k2)
    # print(kxi)
    # kx = np.append(kx, kxi)
    # return ks, kx

def spsfindrec(sps, line, point, rindex):
    """
    % Author: Andreas Hoelker
    :param sps:
    :param line:
    :param point:
    :param index:
    :return:
    """

    # ===============================================
    # Search for point data assuming eas/nor :
    # Note: eas/nor input requires 1x2 arrays.
    # Note: If eas/nor is outside eas/nor value range in data, line/point input is assumed.
    kr = []
    if hasattr(line, "__len__") and hasattr(point, "__len__"):
        print('function spsfindptxy not existing yet')
        pass
        # kr = spsfindptxy(sps.R, [min(line) max(line)], [min(point) max(point)])
        # #TODO: function spsfindptxy

    # ===============================================
    # Search point data by line/point
    # Note: for each sps.R.line/point, find its position in line/point Array
    if not kr:
        k1 = findx(line, sps.R.line)
        k2 = findx(point, sps.R.point)
        kr = intersect_mtlb(k1, k2)
        if len(kr) > 1:
            kr = kr[rindex - 1]
        elif kr or kr == 0:
            kr = int(kr)
        else:
            kr = None

    # ===============================================
    # Search relation records -- OPTIONAL #TODO: not done yet
    return kr

# def create_shp(SeisDB, path4saving, name_shp_saved):
#     # import arcpy
#     # Define spatial reference. Get the spatial reference CH1903+ LV95 through WKID
#     sr = arcpy.SpatialReference(2056)
#
#     r_coordinates = SeisDB.sps.R[['easting', 'northing']].values
#     s_coordinates = SeisDB.sps.S[['easting', 'northing']].values
#
#     # r_coordinates as <class 'list'>
#     r_coordinates = r_coordinates.tolist()
#     s_coordinates = s_coordinates.tolist()
#
#     features_receivers = []
#     features_receivers.append(
#         arcpy.Polyline(
#             arcpy.Array([arcpy.Point(*coords) for coords in r_coordinates]), sr))
#     arcpy.CopyFeatures_management(features_receivers, path4saving + 'receivers_' + name_shp_saved)
#     features_sources = []
#     features_sources.append(
#         arcpy.Multipoint(
#             arcpy.Array([arcpy.Point(*coords) for coords in s_coordinates]), sr))
#     arcpy.CopyFeatures_management(features_sources, path4saving + 'sources_' + name_shp_saved)
#
#     return 0

def findValueinObj(bi, Obj, att):
    obji = [getattr(Obj[i], att) for i in range(len(Obj))]
    if bi in obji:
        idi = obji.index(bi)
    else:
        idi = None
    return idi


def findValuesinObj(b, Obj, att):
    idx = []
    obji = [getattr(Obj[i], att) for i in range(len(Obj))]
    for bi in b:
        try:
            idi = obji.index(bi)
        except:
            idi = None
        idx = np.append(idx, idi)
    return idx


def findIdxCount(Obj, att, i, b): #, att, l, b):
    """
    Get value repetition of x_a in serie b
    """
    x_a = getattr(Obj[i], att)
    cnt = [i_b for i_b, x_b in enumerate(b) if x_b == x_a]
    a = get_attr_until_idx(Obj, att, np.arange(0,i))
    occ = a.count(x_a)
    return occ

def findIdxCountUntilValue(value, b, idx):  # , att, l, b):
    #TODO: verify if correct
    """
    Get value repetition of x_a in serie b
    """
    x_a = value
    cnt = [i_b for i_b, x_b in enumerate(b[:idx]) if x_b == x_a]
    return len(cnt)

    # ki = [ki+1 for cnt in list_idx if cnt in list_idx]
    # a = get_attr_idx(Obj, att, np.arange(0,i))
    # cnt = [i_b for i_b, x_b in enumerate(b) if x_b == x_a]
    # if cnt >1:
    #     ki+= 1
    # else
    #     ki = 1
    # print(cnt)
    # return ki

def get_attr_until_idx(Obj, att, idx):
    a = [getattr(Obj[idx[i]], att) for i in idx]
    return a

def flatten(el):
    return [item for sublist in el for item in sublist]

def azimuthdip(dx, dy, dz):
    azimuth = 0
    dip = 0

    # TODO: function azimuth dip
    return azimuth, dip

def read_raster(filename):
    """
    Helpful: https://github.com/pyvista/pyvista-support/issues/205
    """
    # Read in data
    data = xr.open_rasterio(filename)
    values = np.asarray(data)
    nans = values == data.nodatavals
    if np.any(nans):
        values[nans] = np.nan

    # Make mesh
    xx, yy = np.meshgrid(data['x'], data['y'])
    zz = values.reshape(xx.shape) # will make z comp
    mesh = pv.StructuredGrid(xx,yy,zz)
    mesh['data'] = values.ravel(order='F')
    return mesh

def find_files_segy(Dir):
    for root, dirs, files in os.walk(Dir,topdown=True):
        for file in files:
            if file.endswith(".segy") or file.endswith(".sgy"):
                # print(os.path.join(root, file))
                # surveys_lines = root.split("/")[-1]
                print(file)

    # print(os.walk(Dir).next()[1])

