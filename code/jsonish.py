import os
import json
import pandas as pd



BIDS_DIR = '/Volumes/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS'
SOURCE_DIR = '/Volumes/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS/sourcedata'


# define functions


# iterate through BIDS directory and for each folder that starts with 'sub' check if all json files inside are larger than 1700 bytes, if not, add the json filepath to a list


import os

def check_jsons(BIDS_DIR):
    wrong_jsons = []
    scanned_dirs = set()
    subject_dirs = []

    # First, gather all subject directories
    for root, dirs, files in os.walk(BIDS_DIR, topdown=True):
        dirs[:] = [d for d in dirs if d.startswith('sub')]
        for dir in dirs:
            sub_dir_path = os.path.join(root, dir)
            subject_dirs.append(sub_dir_path)
        break  # Only scan the top-level directory

    # Now, scan each subject directory
    for sub_dir_path in subject_dirs:
        if sub_dir_path in scanned_dirs:
            print('already scanned', sub_dir_path)
            continue

        scanned_dirs.add(sub_dir_path)
        print('scanning', sub_dir_path)
        
        day_folders = ['day1pre', 'day1post', 'day2pre', 'day2post', 'ses-post']

        for day_folder in day_folders:
            func_path = os.path.join(sub_dir_path, day_folder, 'func')
            dwi_path = os.path.join(sub_dir_path, day_folder, 'dwi')

            # Check func folder for JSON files
            if os.path.exists(func_path):
                for func_file in os.listdir(func_path):
                    if func_file.endswith('.json') and os.path.getsize(os.path.join(func_path, func_file)) < 1700:
                        wrong_jsons.append(os.path.join(func_path, func_file))

            if os.path.exists(dwi_path):
                for dwi_file in os.listdir(dwi_path):
                    if dwi_file.endswith('.json') and os.path.getsize(os.path.join(dwi_path, dwi_file)) < 1700:
                        wrong_jsons.append(os.path.join(dwi_path, dwi_file))
        
        print('finished scanning', sub_dir_path)

    return wrong_jsons


wrong_jsons = check_jsons(BIDS_DIR)
print(wrong_jsons)



#using subject and session [8,9], image type [10], and task name [11], create a directory using SOURCE_DIR 

def create_src_dirs(wrong_jsons):
    for json_file in wrong_jsons:
        parts = json_file.split('/')
        sub = parts[8]
        ses = parts[9]
        img_type = parts[10]
        task = parts[11]
        new_dir = os.path.join(SOURCE_DIR, sub, ses, img_type, task)
       



# function to replace new json with the json files for corresponding subject and session on server
#/Shared/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS/sourcedata/sub-2002_ses-day1pre/scans/4-func_bold_task_rest_run_1/resources/DICOM/files

# function to create new job files for each new json file and add them to specified directory



#for all file paths in folders, create a .job file (in this directory /Volumes/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS/derivatives/Zak/job_files_08-22_slice-timing) using the following syntax:
'''
#!/bin/bash



#load dcm2niix module
module load dcm2niix

#run code where -b o only pulls data to construct json files
dcm2niix -f sub-2002 -b o -o /Shared/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS/derivatives/ [[path to dicom files]]


'''

for d in dicoms:
    with open(os.path.join('/Volumes/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS/derivatives/Zak/code/json_qc_s-24', d.split('/')[-1] + '.sh'), 'w') as f:
        f.write('''
#!/bin/bash



#load dcm2niix module
module load dcm2niix

#run code where -b o only pulls data to construct json files
dcm2niix -f d[8]-b o -o [[path to output location] [[path to dicom files]]
''')

   
                
