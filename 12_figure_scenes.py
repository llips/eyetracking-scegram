import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from argparse import ArgumentParser

from config import fname, subjects, blocks, display_resolution, image_size
from helpers import I_DT


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

        # load images
        imgs = {i: mpimg.imread(f"{fname.scegram_data_dir}/01scenes/01object_present/Scene{i}.png") for i in showed_images}

        # create empty dataframe for the analysis metrics
        analysis_metrics_subject = pd.DataFrame(index=showed_images)

        # iterate over shown images 
        for image in showed_images:
            # select image information from scegram
            image_information = scegram_scenes_objects[scegram_scenes_objects['sce_file_name'] == f"Scene{image}.png"]

            # eye tracking data from stimulus onset till offset
            start_idx = processed_data_subject.USER.where(processed_data_subject.USER==f"STIMULI_ONSET_BLOCK_{block}_{image}").first_valid_index()
            start_time = processed_data_subject.TIME.iloc[start_idx]

            end_idx = processed_data_subject.USER.where(processed_data_subject.USER==f"STIMULI_END_BLOCK_{block}_{image}").first_valid_index()
            end_time = processed_data_subject.TIME.iloc[end_idx]

            data_image = processed_data_subject.copy()[((processed_data_subject['TIME'] >= start_time) & (processed_data_subject['TIME'] <= end_time))]


            # compute fixations
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


            # plotting gazepoints
            fig, ax = plt.subplots()
            ax.plot(data_image['BPOGX']*1920 , 1080-data_image['BPOGY']*1080, 'x-', color='yellow', zorder=1, alpha=0.25)
            ax.imshow(imgs[image], extent=[448, 1472, 156, 924])
            rectangle = plt.Rectangle((x+448-width/2, 924-y+-height/2), width, height, ec="red", fc="none", alpha=0.5, zorder=3)
            ax.add_patch(rectangle)
            ax.set_title(image, fontsize=10)
            fig.savefig(fname.figure_stimulus_gazepoint_image(image=image, subject=subject, block=block))
            plt.close()


            # plotting fixations
            fig, ax = plt.subplots()
            ax.plot((fixations_data['X'])*1920 , 1080-(fixations_data['Y'])*1080, 'x-', color='yellow', zorder=1, alpha=0.5)
            ax.imshow(imgs[image], extent=[448, 1472, 156, 924])
            rectangle = plt.Rectangle((x+448-width/2, 924-y+-height/2), width, height, ec="red", fc="none", alpha=0.5, zorder=3)
            ax.add_patch(rectangle)
            ax.set_title(image, fontsize=10)
            fig.savefig(fname.figure_stimulus_fixations_image(image=image, subject=subject, block=block))
            plt.close()