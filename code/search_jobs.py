import os 
import sys

#scan the job scripts directory and create a list of the paths to all job scripts that contain the subject number in bad_subs

def search_jobs(JOBS_DIR, bad_subs):
    jobs = []
    for sub in bad_subs:
        for file in os.listdir(JOBS_DIR):
            if sub in file:
                jobs.append(os.path.join(JOBS_DIR, file))

    return jobs

bad_subs = []
with open('bad_subs.txt', 'r') as f:
    for line in f:
        bad_subs.append(line.strip())

JOBS_DIR = '/Volumes/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS/derivatives/code/fmriprep_v22.0.2/job_scripts/day2pre'
jobs = search_jobs(JOBS_DIR, bad_subs)

print(jobs)

#save jobs to a text file 
with open('bad_jobs.txt', 'w') as f:
    for job in jobs:
        f.write(job + '\n')