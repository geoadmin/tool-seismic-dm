import os
import numpy as np
import pandas as pd
import struct
# from obspy.io.segy.util import clibsegy
# from obspy.core.compatibility import from_buffer

def get_file_in_folder(folder_path):
    for file in os.listdir(folder_path):
        return file
    else:
        print('Warning: {} is empty'.format(folder_path))
        return 0

def get_header(f,HEADER,endianness):
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
    if format_data_sample == 1: bytefactor = 4  # '4-Byte IMB floating point' # TODO: verify https://en.wikipedia.org/wiki/IBM_hexadecimal_floating-point
    if format_data_sample == 2: bytefactor = 4       # 4-byte two complement integer
    if format_data_sample == 3: bytefactor = 2     # 2-byte two complement integer
    if format_data_sample == 4: bytefactor = 4
    if format_data_sample == 5: bytefactor = 4       #np.float32 # 4-byte ieee floating-point
    if format_data_sample == 6: bytefactor = 8       # 8-byte ieee floating point
    if format_data_sample == 7: bytefactor = 3    # 3-byte two's complement integer
    if format_data_sample == 8: bytefactor = 1       # 1-byte two's complement integer
    if format_data_sample == 9: bytefactor = 8       # 8-byte two's complement integer
    if format_data_sample == 10: bytefactor = 4       # np.uint32       # 4-byte unsigned integer
    if format_data_sample == 11: bytefactor = 2       # np.uint16       # 2-byte unsigned integer
    if format_data_sample == 12: bytefactor = 8     # np.uint64       # 8-byte unsigned integer
    if format_data_sample == 15: bytefactor = 3     # np.uint24      # 3-byte unsigned integer
    if format_data_sample == 16: bytefactor = 1      # np.uint8       # 1-byte unsigned integer
    return bytefactor

def txt2df(txt_file,shape=None):
    df=pd.read_csv(txt_file,comment='#',delimiter = " ", header=None) #delimiter = "\t"
    return df

def get_index(serie1,serie2):
    """

    :param serie1: reference serie
    :param serie2: serie with index repetition
    :return: idx from serie1
    """
    idx = [i for (i, val) in enumerate(serie1) if serie1 in serie2]
    return idx

def find(a,b):
    k = [i_a for i_b, x_b in enumerate(b) for i_a,x_a in enumerate(a) if x_a==x_b]
    return k

def flatten(l):
    return [item for sublist in l for item in sublist]

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


def unpack_ibm_notworking(f,size):
    """
    From Obspy:
    https://docs.obspy.org/_modules/obspy/io/segy/unpack.html#unpack_4byte_ibm
    """
    data = np.fromstring(f.read(size), dtype=np.int32)
    sign = np.bitwise_and(np.right_shift(data, 31), 0x01)
    exponent = np.bitwise_and(np.right_shift(data, 24), 0x7f)
    mantissa = np.bitwise_and(data, 0x00ffffff)
    # Force single precision.
    mantissa = np.require(mantissa, 'float32')
    mantissa /= 0x1000000
    sign *= -2.0
    sign += 1.0
    mantissa *= 16.0 ** (exponent - 64)
    mantissa *= sign
    return mantissa









