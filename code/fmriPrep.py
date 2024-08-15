import os 
import sys


#Creates four lists of paths to job scripts for each session
#Checks to see if there are any json files that end in a, b, or c and renames them to remove the letter (this can occur if the json file is created before deleting the previous file)

#bad_subs is a list of subject numbers that need to be fixed

JOB_SCRIPTS_DIR = '/path/to/job/scripts'
BIDS_DIR = '/path/to/BIDS'


def search_jsons(BIDS_DIR):
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

    return jsons

def rename_files(jsons):
    for file_path in jsons:
        directory, file_name = os.path.split(file_path)
        name, ext = os.path.splitext(file_name)

        if name[-1] in ['a', 'b', 'c']:
            new_name = name[:-1] + ext
            new_path = os.path.join(directory, new_name)
            os.rename(file_path, new_path)
            print(f'Renamed: {file_path} to {new_path}')
        else:
            print(f'No change: {file_path}')
    return jsons


def find_job_scripts(bad_subs):
    job_scripts = []
    dirs = [
        os.path.join(JOB_SCRIPTS_DIR, 'day1pre'),
        os.path.join(JOB_SCRIPTS_DIR, 'day1post'),
        os.path.join(JOB_SCRIPTS_DIR, 'day2pre'),
        os.path.join(JOB_SCRIPTS_DIR, 'day2post'),
        os.path.join(JOB_SCRIPTS_DIR, 'post')
    ]
    for sub in bad_subs:
        for d in dirs:
            #for each dir in the job scripts directory, check if there is a .job file that contains the subhect number
            for f in os.listdir(d):
                if sub in f:
                    job_scripts.append(os.path.join(d, f))
    
    return job_scripts


#split the job scripts into four lists by session
def split_job_scripts(job_scripts):
    job_scripts1 = []
    job_scripts2 = []
    job_scripts3 = []
    job_scripts4 = []
    
    for script in job_scripts:
        if 'day1pre' in script:
            job_scripts1.append(script)
        elif 'day1post' in script:
            job_scripts2.append(script)
        elif 'day2pre' in script:
            job_scripts3.append(script)
        elif 'day2post' in script:
            job_scripts4.append(script)
    return job_scripts1, job_scripts2, job_scripts3, job_scripts4



#create .txt files for each list of job scripts
def create_txt_files(job_scripts1, job_scripts2, job_scripts3, job_scripts4):
    with open('job_scripts1.txt', 'w') as f:
        for item in job_scripts1:
            f.write("%s\n" % item)
    with open('job_scripts2.txt', 'w') as f:
        for item in job_scripts2:
            f.write("%s\n" % item)
    with open('job_scripts3.txt', 'w') as f:
        for item in job_scripts3:
            f.write("%s\n" % item)
    with open('job_scripts4.txt', 'w') as f:
        for item in job_scripts4:
            f.write("%s\n" % item)

    return 'job_scripts1.txt', 'job_scripts2.txt', 'job_scripts3.txt', 'job_scripts4.txt'





