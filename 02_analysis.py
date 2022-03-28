"""
Compute time to first fixation, dwell time, number of fixations and number of re-entering (each with respect to the ROI of the respective scene) for a subject
"""

import pandas as pd
from argparse import ArgumentParser

from config import fname, subjects, blocks,  display_resolution, image_size
from helpers import is_in_roi, I_DT


# parser = ArgumentParser(__doc__)
# parser.add_argument('subject', type=int, help='Subject to process [1-6]')
# args = parser.parse_args()

scegram_scenes_objects = pd.read_excel(fname.scegram_excel)
#trial_sequences = pd.read_excel(fname.trial_sequences) 

analysis_metrics_list = []
for subject in subjects:
    # Load subject data
    processed_data_subject = pd.read_csv(fname.processed_data_subject(subject=subject), sep="\t")

    for block in blocks:
        block_data = processed_data_subject[processed_data_subject['BLOCK'] == block]
       
        # get the shown images from the log messages
        showed_images = [str(i).lstrip(f'STIMULI_ONSET_BLOCK_{block}') for i in list(processed_data_subject['USER'][processed_data_subject['USER'].str.startswith(f'STIMULI_ONSET_BLOCK_{block}', na = False)])]

        # create empty dataframe for the analysis metrics
        analysis_metrics_subject = pd.DataFrame(index=showed_images)

        # iterate over shown images 
        for image in showed_images:
            # select image information from scegram
            image_information = scegram_scenes_objects[scegram_scenes_objects['sce_file_name'] == f"Scene{image}.png"]

            # eye tracking data from stimulus onset till offset
            fixcross_start_idx = processed_data_subject.USER.where(processed_data_subject.USER==f"FIXATION_ONSET_BLOCK_{block}_{image}").first_valid_index()
            fixcross_start_time = processed_data_subject.TIME.iloc[fixcross_start_idx]

            fixcross_end_idx = processed_data_subject.USER.where(processed_data_subject.USER==f"FIXATION_END_BLOCK_{block}_{image}").first_valid_index()
            fixcross_end_time = processed_data_subject.TIME.iloc[fixcross_end_idx]

            # eye tracking data from stimulus onset till offset
            start_idx = processed_data_subject.USER.where(processed_data_subject.USER==f"STIMULI_ONSET_BLOCK_{block}_{image}").first_valid_index()
            start_time = processed_data_subject.TIME.iloc[start_idx]

            end_idx = processed_data_subject.USER.where(processed_data_subject.USER==f"STIMULI_END_BLOCK_{block}_{image}").first_valid_index()
            end_time = processed_data_subject.TIME.iloc[end_idx]

            data_image = processed_data_subject.copy()[((processed_data_subject['TIME'] >= start_time) & (processed_data_subject['TIME'] <= end_time))]


            fixations, _ = I_DT([data_image['BPOGX'], data_image['BPOGY']], 0.2, 10)

            fixations_list = []
            for (fs, fe) in fixations:
                start_time_fixation = data_image.TIME.iloc[fs]
                end_time_fixation = data_image.TIME.iloc[fe]
                data_fixation = data_image.copy()[((data_image['TIME'] >= start_time_fixation) & (data_image['TIME'] <= end_time_fixation))]
                row = pd.DataFrame([[start_time_fixation, end_time_fixation, end_time_fixation - start_time_fixation, data_fixation.mean().BPOGX, data_fixation.mean().BPOGY]], columns=('START', 'END', 'DURATION', 'X', 'Y'))
                fixations_list.append(row)

            fixations_data = pd.concat(fixations_list).reset_index()

            # region of interest
            x = image_information['obj_x_center'].item()
            y = image_information['obj_y_center'].item()
            width = image_information['obj_width'].item()
            height = image_information['obj_height'].item()

            res_x = display_resolution[0]
            res_y = display_resolution[1]

            offset_x = (res_x - image_size[0]) / 2
            offset_y = res_y - (res_y - image_size[1]) / 2

           # data_image['ROI'] = data_image.apply(lambda row: is_in_roi(row['BPOGX']*res_x, res_y-row['BPOGY']*res_y, x+offset_x-width/2, offset_y-y+-height/2, width, height), axis=1)
            fixations_data['ROI'] = fixations_data.apply(lambda row: is_in_roi(row['X']*res_x, res_y-row['Y']*res_y, x+offset_x-width/2, offset_y-y+-height/2, width, height), axis=1)


            # Get type and scene
            scene = image.split('_')[0]
            category = image.split('_')[1]

            # compute time to first fixation on roi
            # first_fixation_idx = data_image['ROI'].idxmax()
            # first_fixation_time = data_image.TIME.loc[first_fixation_idx]
            # time_to_first_fixation = first_fixation_time - start_time

            first_fixation_idx = fixations_data['ROI'].idxmax()
            first_fixation_time = fixations_data.START.loc[first_fixation_idx]
            time_to_first_fixation = first_fixation_time - fixations_data.START.loc[0]

            # compute the dwell time on roi
            # groups = data_image.groupby((data_image['ROI'].shift() != data_image['ROI']).cumsum())
            # dwell_time = 0
            # for name, group in groups:
            #     if group.ROI.sum() != 0:
            #         dwell_time += group['TIME'].iloc[-1] - group['TIME'].iloc[0]

            group_sum = fixations_data.groupby('ROI').sum()
            dwell_time = group_sum['DURATION'][True] if True in group_sum.index else 0


            # compute number of reentrys of roi
            #reentering_roi_count = data_image['ROI'][data_image['ROI'].astype(int).diff() == 1].count()
            reentering_roi_count = fixations_data['ROI'][fixations_data['ROI'].astype(int).diff() == 1].count()

            # number of fixations in roi
            fixation_count_roi = fixations_data.ROI.sum()

            # first fixation duration roi
            first_fixation_duration_roi = fixations_data.iloc[fixations_data.ROI.idxmax()].DURATION

            # average fixation duration roi
            group_mean = fixations_data.groupby('ROI').mean()
            average_fixation_duration_roi = group_mean.DURATION[True] if True in group_mean.index else 0

            # Add metrics to data frame
            analysis_metrics_subject.loc[image, 'SUBJECT'] = int(subject)
            analysis_metrics_subject.loc[image, 'BLOCK'] = block
            #analysis_metrics_subject.loc[image, 'SCENE'] = scene
            analysis_metrics_subject.loc[image, 'OBJECT'] = image_information['obj_name'].item() 
            analysis_metrics_subject.loc[image, 'SCENE'] = image_information['sce_category'].item()
            analysis_metrics_subject.loc[image, 'CATEGORY'] = category
            analysis_metrics_subject.loc[image, 'TTFF'] = time_to_first_fixation
            analysis_metrics_subject.loc[image, 'DWELL_TIME'] = dwell_time
            analysis_metrics_subject.loc[image, 'REENTERING_ROI_COUNT'] = reentering_roi_count
            analysis_metrics_subject.loc[image, 'FIXATION_ROI_COUNT'] = fixation_count_roi
            analysis_metrics_subject.loc[image, 'FIRST_FIXATION_ROI_DURATION'] = first_fixation_duration_roi
            analysis_metrics_subject.loc[image, 'AVERAGE_FIXATION_ROI_DURATION'] = average_fixation_duration_roi
            analysis_metrics_subject.loc[image, 'FIXATION_CROSS_DURATION'] = fixcross_end_time - fixcross_start_time
            analysis_metrics_subject.loc[image, 'STIMULUS_DURATION'] = end_time - start_time


        # add to list
        analysis_metrics_list.append(analysis_metrics_subject)

# Combine subject data
analysis_metrics = pd.concat(analysis_metrics_list).reset_index()

# Save processed data
analysis_metrics.to_csv(fname.analysis_metrics, sep="\t", index=False)