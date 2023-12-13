import os
import re
import numpy as np
import pandas as pd
import struct
from SeismicDM.SPS import *
import matplotlib.pyplot as plt

def OCR_check(line, path, fix,import_corrected_files, method=2):
# def OCR_check(line, path_rsx_files, path_rsx_files_corrected, fix,import_corrected_files, method=2):

    rsx_files = os.listdir(os.path.abspath(path+'BBL/'))
    # rsx_files = os.listdir(os.path.abspath(path_rsx_files))
    if fix == 1:
        for rs in rsx_files[:2]:
            fix_sr_file(path, rs, method)
        fix_log_file(path, rsx_files[2])

    rsx_files_corrected = os.listdir(os.path.abspath(path+'v2/'))
    # rsx_files_corrected = os.listdir(os.path.abspath(path_rsx_files_corrected))
    path_corrected = path+'v2/'
    if import_corrected_files == 1:
        sfile, rfile, xfile = T0_loadFix_SrcGeom(path_corrected+rsx_files_corrected[1]),\
            T1_loadFix_RecGeom(path_corrected+rsx_files_corrected[0]),\
            T2_loadFix_Relation(path_corrected + rsx_files_corrected[2])

        fig, [ax1, ax2, ax3] = plt.subplots(3)  # , sharex=True, sharey=True)
        ax1.scatter(sfile['EAS'], sfile['NOR'], s=2, color='blue')
        ax1.set_xlim(min(sfile['EAS']),max(sfile['EAS']))
        ax1.set_ylim(min(sfile['NOR']),max(sfile['NOR']))
        ax1.set_title('Sources coordinates')
        ax1.xaxis.set_major_locator(plt.MaxNLocator(5))
        ax1.yaxis.set_major_locator(plt.MaxNLocator(3))

        ax2.scatter(rfile['EAS'], rfile['NOR'], s=2, color='darkorange')
        ax2.set_title('Reciever coordinates')
        ax2.set_xlim(min(rfile['EAS']),max(rfile['EAS']))
        ax2.set_ylim(min(rfile['NOR']),max(rfile['NOR']))
        ax2.xaxis.set_major_locator(plt.MaxNLocator(5))
        ax2.yaxis.set_major_locator(plt.MaxNLocator(3))

        min_s_east, min_s_north = min(sfile['EAS']), min(sfile['NOR'])
        max_s_east, max_s_north = max(sfile['EAS']), max(sfile['NOR'])
        min_r_east, min_r_north = min(rfile['EAS']), min(rfile['NOR'])
        max_r_east, max_r_north = max(rfile['EAS']), max(rfile['NOR'])
        # print(min_s_east, min_s_north ,max_s_east, max_s_north,min_r_east, min_r_north,max_r_east, max_r_north)

        ax3.scatter(sfile['EAS'], sfile['NOR'], s=1, color='blue')
        ax3.scatter(rfile['EAS'], rfile['NOR'], s=0.5, color='darkorange')
        ax3.set_xlim(min(min_s_east,min_r_east),max(max_s_east,max_r_east))
        ax3.set_ylim(min(min_s_north,min_r_north), max(max_s_north,max_r_north))
        # print(max_s_north)

        ax3.xaxis.set_major_locator(plt.MaxNLocator(5))
        ax3.yaxis.set_major_locator(plt.MaxNLocator(3))
        ax3.set_title('Comparison')
        fig.suptitle('{}'.format(line), fontsize=16)
        # fig.autofmt_xdate()
        fig.tight_layout()
        plt.show()
    return

def check_offset(path):
    path_corrected = path+'v2/'
    rsx_files_corrected = os.listdir(os.path.abspath(path + 'v2/'))
    sfile, rfile, xfile = T0_loadFix_SrcGeom(path_corrected+rsx_files_corrected[1]),\
        T1_loadFix_RecGeom(path_corrected+rsx_files_corrected[0]),\
        T2_loadFix_Relation(path_corrected + rsx_files_corrected[2])
    d_sfile = [np.sqrt((sfile['EAS'][i+1]-sfile['EAS'][i])**2+(sfile['NOR'][i+1]-sfile['NOR'][i])**2) for i in range(len(sfile['EAS'])-1)]
    d = [sfile['EAS'][i+1]-sfile['EAS'][i] for i in range(len(sfile['EAS'])-1)]
    return sfile, rfile, xfile, d_sfile, d

def check_sps_import(sps):
    # check s point and x spoint
    no_match = []
    for pt in sps.X['spoint'].astype(int):
        if pt in sps.S['point'].values.astype(int):
            pass
        else:
            no_match.append(pt)
    print('no match x point {} in sources'.format(no_match))
    print('---------------------------------------------')
    print('\n')

    # step 1 : check ffid
    no_match=[]
    for fldr in sps.X['ffid']:
        if fldr in sps.S['fldr']:
            pass
        else:
            no_match.append(int(fldr))
    print('no match fldr {} in sources'.format(no_match))
    print('---------------------------------------------')
    print('\n')

    # step 2 : shotpoints numbers
    no_match = []
    for point in sps.S['point'].astype(int):
        if point in sps.R['point'].values.astype(int):
            pass
        else:
            no_match.append(point)
    print('no match source point {} in receivers'.format(no_match))
    print('---------------------------------------------')
    print('\n')

    # step 3 : check Zahl Kanalnummer


    return 0


def import_OCR_file(txt_file = None):
    try:
        # Try to load file without manual corrections
        df = T0_loadFix_SrcGeom(txt_file)
    except:
        # raise issue
        print('The txt file can not be imported. Please correct data in the file. ')
        df = 0
        # df = T0_loadFix_SrcGeom(txt_file[:-4]+'_corrected'+'.TXT')
    return df

def fix_sr_file(path, file_to_fix, method = 2 ):
    # create name for new file
    # new_txt_file = path + file_to_fix[:-4]+'_v1'+'.TXT'
    new_txt_file = path + 'v1/'+ file_to_fix[:10]+'_v1'+'.TXT'
    old_txt_file = path + 'BBL/' + file_to_fix
    # open new file for writing
    fnew = open(new_txt_file, "w+")
    # open existing file for reading
    with open(old_txt_file, 'r') as ft:
        for line in ft:
            # identify headers. If more than 2 letters in line -> line identified as header
            total_letters_line = len(re.findall('[A-z]', line))
            if total_letters_line > 3 :
                continue
            # for each word in line, check if good structure ex. ID, Coordinate, height
            pointer=0
            nfields = len(line.split())

            for word in line.split():
                # Replace , by .
                word = word.replace(',', '.')
                word = word.replace('..', '.')
                word = word.replace(':', '.')
                if nfields == 4:
                    ## WORKING with columns ids
                    if pointer == 0:
                        word = fix_id(word)
                        fnew.write(word + ' ')
                    if pointer == 1:
                        word = fix_coordinate(word)
                        fnew.write(word + ' ')
                    if pointer == 2:
                        word = fix_coordinate(word)
                        fnew.write(word + ' ')
                    if pointer == 3:
                        word = fix_hoehe(word)
                        fnew.write(word + '')
                        fnew.write('\n')
                    pointer+=1
                elif nfields == 8:
                    ## WORKING with columns ids
                    if pointer == 0 or pointer == 4:
                        word = fix_id(word)
                        fnew.write(word + ' ')
                    if pointer == 1 or pointer == 5:
                        word = fix_coordinate(word)
                        fnew.write(word + ' ')
                    if pointer == 2 or pointer == 6:
                        word = fix_coordinate(word)
                        fnew.write(word + ' ')
                    if pointer == 3 or pointer == 7:
                        word = fix_hoehe(word)
                        fnew.write(word + '')
                        fnew.write('\n')
                    pointer+=1
                elif nfields == 10:
                    ## WORKING with columns ids
                    if pointer == 0 or pointer == 5:
                        word = fix_id(word)
                        fnew.write(word + ' ')
                    if pointer == 1 or pointer == 6:
                        word = fix_letter(word)
                        fnew.write(word + ' ')
                    if pointer == 2 or pointer == 7:
                        word = fix_coordinate(word)
                        fnew.write(word + ' ')
                    if pointer == 3 or pointer == 8:
                        word = fix_coordinate(word)
                        fnew.write(word + ' ')
                    if pointer == 4:
                        word = fix_hoehe(word)
                        fnew.write(word + '')
                        fnew.write('\n')
                    if pointer == 9:
                        word = fix_hoehe(word)
                        fnew.write(word + '')
                        fnew.write('\n')
                    pointer+=1
                else:
                    if pointer == nfields-1:
                        word = check_number(word)
                        fnew.write(word + '')
                        fnew.write('\n')
                    else:
                        word = check_number(word)
                        fnew.write(word + ' ')
                    pointer += 1
    fnew.close()
    ft.close()
    return


def fix_log_file(path, file_to_fix):
    # create name for new file
    # new_txt_file = path + file_to_fix[:-4]+'_v1'+'.TXT'
    new_txt_file = path + 'v1/'+ file_to_fix[:10]+'_v1'+'.TXT'
    old_txt_file = path + file_to_fix
    old_txt_file = path + 'BBL/' + file_to_fix
    # open new file for writing
    fnew = open(new_txt_file, "w+")
    # open existing file for reading
    with open(old_txt_file, 'r') as ft:
        for line in ft:
            # identify headers. If more than 2 letters in line -> line identified as header
            total_letters_line = len(re.findall('[A-z]', line))
            if total_letters_line > 2 :
                continue
            # for each word in line, check if good structure ex. ID, Coordinate, height
            pointer=0
            for word in line.split():
                if pointer < 7 :
                    word = check_number(word)
                    fnew.write(word + ' ')
                if pointer ==7 :
                    # word = fix_id(word)
                    word = check_number(word)
                    fnew.write(word+'')
                    fnew.write('\n')

                pointer+=1

        fnew.close()
        ft.close()
    return

def is_number(s):
    try:
        float(s)  # for int, long and float
        return True
    except:
        return False

def check_number(word):
    if is_number(word)==True:
        word = word
    elif word[0].isupper():
        word = word
    else:
        word = word + ' ---issue---'
    return word

def fix_id(word):
    # check if ID is a number
    if word.isnumeric():
        word = word
    elif word[0] =='-':
        word = word
    else:
        word = word + ' ---issue ID---'
    return word

def fix_letter(word):
    # check if ID is an uppercase
    if word[0].isupper():
        word = word
    else:
        word = word + ' ---issue Uppercase---'
    return word
def fix_coordinate(word):
    # check if coordinates are xxxxxx.x
    # Note: LV03
    # TODO: manage LV95 coordintes
    word = word.replace('-', '.')
    if len(word) != 8:
        word = word + ' --- issue LEN COOR---'
    return word

def fix_hoehe(word):
    # check if hoehe number
    # if word.contains("."):
    try:
        # word = float(word)
        if word[:3].isnumeric() or word[:2].isnumeric():
            word = word
        else:
            word = word + '--- LEN issue HOEHE ---'
    except:
        word = word + '--- issue HOEHE ---'
    return word

def fix_end_line(word):
    # check if hoehe number
    if word.isnumeric() and len(word)<5:
        word = word
    elif len(word)>5:
        word = ' --- issue hohe---'
    else:
        word = word + '--- issue NUMMER ---'
    return word

