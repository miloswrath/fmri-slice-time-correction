
import os
import json




BIDS_DIR = '/Shared/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS'
SOURCE_DIR = '/Shared/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS/sourcedata'
bad_subs = ['sub-2002']
'''
txt = open('/Shared/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS/derivatives/Zak/code/json_qc_s-24/bad_subs.txt', 'r')
bad_subs = txt.read().splitlines()
txt.close()
'''





BIDS_DIR = '/Shared/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS'
SOURCE_DIR = '/Shared/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS/sourcedata'

# for all subjects in bad_subs, enter the following directories and store the path to all json files
# in each directory, enter either func or dwi folders to look for jsons
dirs = ['ses-day1pre', 'ses-day1post', 'ses-day2pre', 'ses-day2post', 'ses-post']

jsons = []

for sub in bad_subs:
    #first enter the sub directory
    sub_dir = os.path.join(BIDS_DIR, sub)
    #then enter each directory in dirs
    for d in dirs:
        d_dir = os.path.join(sub_dir, d)
        #then enter either func or dwi, if they exist
        if os.path.exists(os.path.join(d_dir, 'func')):
            func_dir = os.path.join(d_dir, 'func')
            for file in os.listdir(func_dir):
                if file.endswith('.json'):
                    jsons.append(os.path.join(func_dir, file))
        if os.path.exists(os.path.join(d_dir, 'dwi')):
            dwi_dir = os.path.join(d_dir, 'dwi')
            for file in os.listdir(dwi_dir):
                if file.endswith('.json'):
                    jsons.append(os.path.join(dwi_dir, file))




# In SOURCE_DIR, go through all directories that start with subs in bad_subs
# in each directory, if has ses-day1pre, scan the following directory /scans and save path for folders that start with 4,5,6,7
#if directory has ses-day2pre, scan the following directory /scans and save path for folders that start with 4,5,6,7
# if directory has ses-day1post or day2post, scan the following directory /scans and save path for folders that start with 4,5,6
# if directory has ses-post, scan the following directory /scans and save path for folders that start with 4,5,6,7,10


folders = []

for sub in bad_subs:
    for d in os.listdir(SOURCE_DIR):
        if d.startswith(sub):
            if d == sub + '_ses-day1pre':
                d_dir = os.path.join(SOURCE_DIR, d)
                for s in os.listdir(os.path.join(d_dir, 'scans')):
                    if s.startswith('4-') or s.startswith('5-') or s.startswith('6-') or s.startswith('7-'):
                        folders.append(os.path.join(d_dir, 'scans', s))
            if d == sub + '_ses-day2pre':
                d_dir = os.path.join(SOURCE_DIR, d)
                for s in os.listdir(os.path.join(d_dir, 'scans')):
                    if s.startswith('4-') or s.startswith('5-') or s.startswith('6-') or s.startswith('7-'):
                        folders.append(os.path.join(d_dir, 'scans', s))
            if d == sub + '_ses-day1post' or d == sub + '_ses-day2post':
                d_dir = os.path.join(SOURCE_DIR, d)
                for s in os.listdir(os.path.join(d_dir, 'scans')):
                    if s.startswith('4-') or s.startswith('5-') or s.startswith('6-'):
                        folders.append(os.path.join(d_dir, 'scans', s))
            if d == sub + '_ses-post':
                d_dir = os.path.join(SOURCE_DIR, d)
                for s in os.listdir(os.path.join(d_dir, 'scans')):
                    if s.startswith('4-') or s.startswith('5-') or s.startswith('6-') or s.startswith('7-') or s.startswith('10-'):
                        folders.append(os.path.join(d_dir, 'scans', s))




# for each in folders add /resources/DICOM/files to the end of the path
dicoms = []
for f in folders:
    dicoms.append(os.path.join(f, 'resources/DICOM/files'))



# for each in dicoms, find the output path in the BIDS directory for that subject, session and scan

output_path = []

for d in dicoms:    

    # get the subject and session
    sub = d.split('/')[-6].split('_')[0]
    ses = d.split('/')[-6].split('_')[1]
    scan = d.split('/')[-4]


    #if scan contains func, then output path is /func
    #if scan contains breathold, output path is /func
    #if scan contains dwi, then output path is /dwi

    if 'func' in scan or 'breathhold' in scan:
        output_path.append(os.path.join(BIDS_DIR, sub, ses, 'func'))
    if 'dwi' in scan:
        output_path.append(os.path.join(BIDS_DIR, sub, ses, 'dwi'))
    



# wait for user to press enter to start dcm2niix conversion
def pause_for_user():
    if os.getenv('INTERACTIVE_MODE', 'false') == 'true':
        print("Ready to start dcm2niix conversion. Press Enter to continue...")
        input()

# Example usage
pause_for_user()





#run dcm2niix on each dicom folder and save the output to the corresponding output path, when each subject is done, copy all jsons to a new directory with the subject name as the directory name
#split the dicom path to get the subject and scan


for i in range(len(dicoms)):
    #if a dwi file is found, name it according
    if 'dwi' in dicoms[i]:
        print('running' + dicoms[i].split('/')[-6].split('_')[0] + ' ' + dicoms[i].split('/')[-6].split('_')[1] + ' ' + dicoms[i].split('/')[-4])
        os.system('dcm2niix -f ' + dicoms[i].split('/')[-6].split('_')[0] + '_' + dicoms[i].split('/')[-6].split('_')[1] + '_' + 'dwi' + ' -b o -o ' + output_path[i] + ' ' + dicoms[i])
        print('subject ' + dicoms[i].split('/')[-6].split('_')[0] + ' session, ' + dicoms[i].split('/')[-6].split('_')[1] + ' scan, ' + dicoms[i].split('/')[-4] + ' done')
    elif 'breathhold' in dicoms[i]:
        print('running' + dicoms[i].split('/')[-6].split('_')[0] + ' ' + dicoms[i].split('/')[-6].split('_')[1] + ' ' + dicoms[i].split('/')[-4])
        os.system('dcm2niix -f ' + dicoms[i].split('/')[-6].split('_')[0] + '_' + dicoms[i].split('/')[-6].split('_')[1] + '_' + 'task-' + dicoms[i].split('/')[11].split('_')[-1] + ' -b o -o ' + output_path[i] + ' ' + dicoms[i])
        print('subject ' + dicoms[i].split('/')[-6].split('_')[0] + ' session, ' + dicoms[i].split('/')[-6].split('_')[1] + ' scan, ' + dicoms[i].split('/')[-4] + ' done')

    else:
        print('running' + dicoms[i].split('/')[-6].split('_')[0] + ' ' + dicoms[i].split('/')[-6].split('_')[1] + ' ' + dicoms[i].split('/')[-4])
        os.system('dcm2niix -f ' + dicoms[i].split('/')[-6].split('_')[0] + '_' + dicoms[i].split('/')[-6].split('_')[1] + '_' + 'task-' + dicoms[i].split('/')[11].split('_')[3] + '_' + dicoms[i].split('/')[11].split('_')[-2] + '-' + dicoms[i].split('/')[11].split('_')[-1] + ' -b o -o ' + output_path[i] + ' ' + dicoms[i])
        print('subject ' + dicoms[i].split('/')[-6].split('_')[0] + ' session, ' + dicoms[i].split('/')[-6].split('_')[1] + ' scan, ' + dicoms[i].split('/')[-4] + ' done')
    #save file with log of terminal output
    
       


# copy jsons from jsons into new directory with subject name as the directory name 
NEW_JSON_DIR = '/Shared/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS/derivatives/Zak/code/json_qc_s-24'
for j in jsons:
    sub = j.split('/')[8]
    new_dir = os.path.join(NEW_JSON_DIR, sub)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    os.system('cp ' + j + ' ' + new_dir)


##perform datacheck and wait for user permission to move on
def pause_for_user2():
    if os.getenv('INTERACTIVE_MODE', 'false') == 'true':
        print('Datacheck needed. Check ' + NEW_JSON_DIR + ' and ' + BIDS_DIR + ', Then Press Enter to continue...')
        input()

# Example usage
pause_for_user2()




#remove all jsons in jsons from the BIDS directory
for j in jsons:
    os.system('rm ' + j)




