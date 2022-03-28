"""
Definition of dodo tasks
"""

from config import fname, subjects, blocks


DOIT_CONFIG = {'default_tasks': ['check_logs', 'preprocess', 'analyse', 'averages', 'figure_ttff', 'figure_dwell_time', 'figure_reentries_roi', 'figure_fixation_count_roi', 'figure_first_fixation_duration_roi', 'figure_average_fixation_duration_roi']}


def task_check():
    """
    Check the system dependencies.
    """
    return dict(
        file_dep=['check_system.py'],
        targets=[fname.system_check],
        actions=['python check_system.py']
    )

def task_check_logs():
    """
    Check the logs of the eyetracker
    """
    for subject in subjects:
        yield dict(
            name=f'subject-{subject:d}',
            file_dep=[fname.raw_data_subject(subject=subject)
                  for subject in subjects] + ['00_check_logs.py'],
            targets=[fname.fixed_data_subject(subject=subject)],
            actions=[f'python 00_check_logs.py {subject} --fix'],
        )

def task_preprocess():
    """
    Preprocess the raw eye tracking data
    """
    for subject in subjects:
        yield dict(
            name=f'subject-{subject:d}',
            file_dep=[fname.fixed_data_subject(subject=subject)
                  for subject in subjects] + ['01_preprocessing.py'],
            targets=[fname.processed_data_subject(subject=subject)],
            actions=[f'python 01_preprocessing.py {subject}'],
        )

def task_analyse():
    """
    Compute analytic metrics
    """
    return dict(
        file_dep=[fname.processed_data_subject(subject=subject)
                  for subject in subjects] + ['02_analysis.py'],
        targets=[fname.analysis_metrics],
        actions=['python 02_analysis.py'],
    )

# def task_analyse():
#     """
#     Compute analytic metrics
#     """
#     for subject in subjects:
#         yield dict(
#             name=f'subject-{subject:d}',
#             file_dep=['02_analysis.py'],
#             targets=[fname.analysis_metrics(subject=subject)],
#             actions=[f'python 02_analysis.py {subject}'],
#         )


def task_averages():
    """
    Compute averages of analytic metrics over all subjects
    """

    for block in blocks:
        yield dict(
            name = f'average-block-{block}',
            file_dep=[fname.analysis_metrics, '03_averages.py'],
            targets=[fname.averages(block=block)],
            actions=[f'python 03_averages.py {block}'],
        )

def task_figure_ttff():
    """
    Figure of average time to first fixation grouped by category
    """
    for block in blocks:
        yield dict(
            name = f'ttff-block-{block}',
            file_dep=[fname.analysis_metrics, '04_figure_ttff.py'],
            targets=[fname.figure_ttff(block=block)],
            actions=[f'python 04_figure_ttff.py {block}'],
        )

def task_figure_dwell_time():
    """
    Figure of average dwell time grouped by category
    """
    for block in blocks:
        yield dict(
            name = f'dwell_time-block-{block}',
            file_dep=[fname.analysis_metrics, '05_figure_dwell_time.py'],
            targets=[fname.figure_dwell_time(block=block)],
            actions=[f'python 05_figure_dwell_time.py {block}'],
    )

def task_figure_reentries_roi():
    """
    Figure of average reentries into roi by category
    """
    for block in blocks:
        yield dict(
            name = f'reentries-block-{block}',
            file_dep=[fname.analysis_metrics, '06_figure_reentries_roi.py'],
            targets=[fname.figure_reentries_roi(block=block)],
            actions=[f'python 06_figure_reentries_roi.py {block}'],
    )

def task_figure_fixation_count_roi():
    """
    Figure of average fixation count in roi by category
    """
    for block in blocks:
        yield dict(
            name = f'fixation_count-block-{block}',
            file_dep=[fname.analysis_metrics, '07_figure_fixation_count.py'],
            targets=[fname.figure_fixation_roi_count(block=block)],
            actions=[f'python 07_figure_fixation_count.py {block}'],
    )

def task_figure_first_fixation_duration_roi():
    """
    Figure of first fixation duration in roi by category
    """
    for block in blocks:
        yield dict(
            name = f'first_fixation_duration-block-{block}',
            file_dep=[fname.analysis_metrics, '08_figure_first_fixation_duration.py'],
            targets=[fname.figure_first_fixation_duration_roi(block=block)],
            actions=[f'python 08_figure_first_fixation_duration.py {block}'],
    )

def task_figure_average_fixation_duration_roi():
    """
    Figure of average fixation duration in roi by category
    """
    for block in blocks:
        yield dict(
            name = f'average_fixation_duration-block-{block}',
            file_dep=[fname.analysis_metrics, '09_figure_average_fixation_duration.py'],
            targets=[fname.figure_average_fixation_duration_roi(block=block)],
            actions=[f'python 09_figure_average_fixation_duration.py {block}'],
    )