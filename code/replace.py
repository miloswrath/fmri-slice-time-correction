import os 
import sys
import shutil

path = '/Volumes/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS/derivatives/Zak/code/json_qc_s-24'
BIDS_DIR = '/Volumes/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS'

#/Volumes/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS/derivatives/Zak/code/json_qc_s-24/sub-2103/ses-post_task-rest_run-2_bolda.json

# scan all subject directories [sub-2002, sub-2003, ...]
# for each json file ends with the letter a, save the path to a list

def get_json_files(path):
    json_files = []
    for dirss in os.listdir(path):
        if dirss.startswith('sub-'):
            for dirsss_path, dirs, files in os.walk(os.path.join(path, dirss)):
                for file in files:
                    if file.endswith('a.json'):
                        json_files.append(os.path.join(dirsss_path, file))
    return json_files




def copy_to_BIDS_and_remove_a(jsons):
    # for each json file in the list, copy the file into the correct folder in BIDS directory and remove the letter a from the end of the file name
    for j in jsons:
        split = j.split('/')
        sub = split[-2]
        ses = split[-1].split('_')[1]
        if 'dwi' in split[-1]:
            scan = 'dwi'
        else:
            scan = 'func'
        #last element of split without the last letter
        new_name = split[-1][:-6]+'.json'
        new_path = os.path.join(BIDS_DIR, sub, ses, scan, new_name)
        shutil.copy(j, new_path)


import os

def remove_if_a_or_not_bold(path):
    dir_list = os.listdir(path)
    bad_subs = []
    
    # Read subs from text file and save to bad_subs
    with open('./bad_subs.txt', 'r') as f:
        for line in f:
            bad_subs.append(line.strip())
        
    dirs = ['ses-day1pre', 'ses-day1post', 'ses-day2pre', 'ses-day2post', 'ses-post']
    for sub in dir_list:
    
        sub_path = os.path.join(path, sub)
        print(sub_path)
        if not os.path.isdir(sub_path):
            print(sub_path + 'is not a directory')
            continue
        for dirr in dirs:
            dirr_path = os.path.join(sub_path, dirr)
            print('scanning' + dirr_path)
            if not os.path.isdir(dirr_path):
                print(dirr_path + 'is not a directory')
                continue
            for dirsss in os.listdir(dirr_path):
                dirsss_path = os.path.join(dirr_path, dirsss)
                if dirsss == 'dwi':
                    print('scanning' )
                    for file in os.listdir(dirsss_path):
                        filepath = os.path.join(dirsss_path, file)
                        if os.path.isfile(filepath) and file.endswith('a.json'):
                            #remove the a from the file name
                            new_name = file[:-6]+'.json'
                            os.rename(os.path.join(dirsss_path, file), os.path.join(dirsss_path, new_name))
                            print('renamed:' + os.path.join(dirsss_path, file) + ' to ' + os.path.join(dirsss_path, new_name))
                elif dirsss == 'func':
                    for file in os.listdir(dirsss_path): 
                        filepath = os.path.join(dirsss_path, file) 
                        if os.path.isfile(filepath) and file.endswith('a.json'):
                            #remove the a from the file name
                            new_name = file[:-6]+'.json'
                            os.rename(os.path.join(dirsss_path, file), os.path.join(dirsss_path, new_name))
                            print('renamed:' + os.path.join(dirsss_path, file) + ' to ' + os.path.join(dirsss_path, new_name))
                        elif os.path.isfile(filepath) and 'bold' not in file:
                            #add bold to the file name
                            new_name = file[:-5]+'_bold.json'
                            os.rename(os.path.join(dirsss_path, file), os.path.join(dirsss_path, new_name))
                            print('renamed:' + os.path.join(dirsss_path, file) + ' to ' + os.path.join(dirsss_path, new_name))
                        else:
                            continue
                else:
                    continue
    return None




remove_if_a_or_not_bold(BIDS_DIR)