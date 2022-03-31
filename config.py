"""
===========
Config file
===========

Configuration parameters for the study.
"""

import os
import getpass
from socket import getfqdn
from fnames import FileNames

###############################################################################
# Determine which user is running the scripts on which machine and set the path
# where the data is stored and how many CPU cores to use.

user = getpass.getuser()  # Username of the user running the scripts
host = getfqdn()  # Hostname of the machine running the scripts

# You want to add your machine to this list as well as the path to the data dir with the raw files and the path to the scegram database
if user == 'luis':
    data_dir = '/Users/luis/git/eyetracking-scegram/data'
    scegram_database = '/Users/luis/Documents/Universität/InformatikMaster/sem4/EyeTracking/semesterproject/SCEGRAM_Database'
    n_jobs = 10
else:
    raise RuntimeError('Running on an unknown system. Please add your system '
                       'configuration to the config.py file.')

# For BLAS to use the right amount of cores
os.environ['OMP_NUM_THREADS'] = str(n_jobs)


###############################################################################
# These are all the parameters that either:
#  1) Are used in more than one script
#  2) Need to be reported in the Methods section of the paper

# Subjects
subjects = [0,1,2,3,4,5]

# Experiment Blocks
blocks = ['A', 'B']

# Experiment Setup
display_resolution = (1920, 1080)
eye_tracker = None
sampling_frequency = None # 62 Hz
image_size = (1024, 768)
distance_user_display = None #57cm

###############################################################################
# Templates for filenames
#
# This part of the config file uses the FileNames class. It provides a small
# wrapper around string.format() to keep track of a list of filenames.
# See fnames.py for details on how this class works.
fname = FileNames()

# Some directories
fname.add('data_dir', data_dir)
fname.add('raw_data_dir', '{data_dir}/raw')
fname.add('fixed_data_dir', '{data_dir}/fixed')
fname.add('processed_data_dir', '{data_dir}/processed')
fname.add('figures_dir', './figures')
fname.add('figures_subject_block_dir', '{figures_dir}/sub-{subject}/block-{block}')
fname.add('tables_dir', './tables')

fname.add('raw_data_subject', '{raw_data_dir}/subject-{subject:d}.tsv')
fname.add('fixed_data_subject', '{fixed_data_dir}/subject-{subject:d}.tsv')
fname.add('processed_data_subject', '{processed_data_dir}/subject-{subject:d}.tsv')

# Trial sequences
fname.add('trial_sequences', '{data_dir}/trial_sequences.xlsx')

# SCEGRAM 
fname.add('scegram_data_dir', scegram_database)
fname.add('scegram_excel', '{scegram_data_dir}/SCEGRAM_Database_scenes_objects.xlsx')

# File containing TTFF, Dwell Time, etc. 
fname.add('analysis_metrics', '{tables_dir}/analysis_metrics.tsv')
fname.add('overview_subject', '{tables_dir}/overview_subject-{subject}_block-{block}.csv')
fname.add('overview_min', '{tables_dir}/overview_{variable}_min_block-{block}.csv')
fname.add('overview_max', '{tables_dir}/overview_{variable}_max_block-{block}.csv')
fname.add('overview_mean', '{tables_dir}/overview_{variable}_mean_block-{block}.csv')


# Averages per consistency category
fname.add('averages', '{tables_dir}/averages_block-{block}.tsv')

# Figures
fname.add('figure_ttff', '{figures_dir}/histogram_ttff_block-{block}.png')
fname.add('figure_dwell_time', '{figures_dir}/histogram_dwell_time_block-{block}.png')
fname.add('figure_reentries_roi', '{figures_dir}/histogram_reentries_roi_block-{block}.png')
fname.add('figure_fixation_roi_count', '{figures_dir}/histogram_fixation_roi_count_block-{block}.png')
fname.add('figure_first_fixation_duration_roi', '{figures_dir}/histogram_first_fixation_duration_roi_block-{block}.png')
fname.add('figure_average_fixation_duration_roi', '{figures_dir}/histogram_average_fixation_duration_roi_block-{block}.png')
fname.add('figure_difference', '{figures_dir}/histogram_difference-{measurement}.png')
fname.add('figure_cross_gazepoints_image', '{figures_subject_block_dir}/{image}_cross_gazepoints_subject-{subject}_block-{block}.png')
fname.add('figure_cross_fixations_image', '{figures_subject_block_dir}/{image}_cross_fixations_subject-{subject}_block-{block}.png')
fname.add('figure_stimulus_gazepoint_image', '{figures_subject_block_dir}/{image}_stimulus_gazepoints_subject-{subject}_block-{block}.png')
fname.add('figure_stimulus_fixations_image', '{figures_subject_block_dir}/{image}_stimulus_fixations_subject-{subject}_block-{block}.png')
fname.add('figure_stimulus_gazepoint_offset_image', '{figures_subject_block_dir}/{image}_stimulus_gazepoints_offset_subject-{subject}_block-{block}.png')
fname.add('figure_stimulus_fixations_offset_image', '{figures_subject_block_dir}/{image}_stimulus_fixations_offset_subject-{subject}_block-{block}.png')


# File produce by check_logs.py
fname.add('log_check', './log_check_sub{subject:d}.txt')

# File produced by check_system.py
fname.add('system_check', './system_check.txt')