"""
Overviews
"""

import pandas as pd
from argparse import ArgumentParser

from config import fname, subjects


parser = ArgumentParser(__doc__)
parser.add_argument('block', type=str, help='Experiment block to process [A|B]')
args = parser.parse_args()


analysis_metrics = pd.read_csv(fname.analysis_metrics, sep="\t")

# everything per subject & block
for subject in subjects:
    df = analysis_metrics[(analysis_metrics['SUBJECT']==0)&(analysis_metrics['BLOCK']==args.block)][['index', 'TTFF', 'DWELL_TIME', 'AVERAGE_FIXATION_ROI_DURATION', 'FIXATION_ROI_COUNT']]
    df = df.rename(columns={df.columns[0]:'SCENE'})
    df.round(3).to_csv(fname.overview_subject(block=args.block, subject=subject), index=True)

for variable in ['TTFF', 'DWELL_TIME', 'AVERAGE_FIXATION_ROI_DURATION', 'FIXATION_ROI_COUNT']:
    # min for every subject per block
    analysis_metrics['SUBJECT'] = analysis_metrics['SUBJECT'].astype('int64')
    df = pd.pivot_table(analysis_metrics[analysis_metrics['BLOCK']==args.block], index='SUBJECT', columns='CATEGORY', values=variable, aggfunc='min')
    df.loc['min'] = df.min()
    df.round(3).to_csv(fname.overview_min(block=args.block, variable=variable), index=True)

    # max for every subject per block
    analysis_metrics['SUBJECT'] = analysis_metrics['SUBJECT'].astype('int64')
    df = pd.pivot_table(analysis_metrics[analysis_metrics['BLOCK']==args.block], index='SUBJECT', columns='CATEGORY', values=variable, aggfunc='max')
    df.loc['max'] = df.max()
    df.round(3).to_csv(fname.overview_max(block=args.block, variable=variable), index=True)

    # mean for every subject per block
    analysis_metrics['SUBJECT'] = analysis_metrics['SUBJECT'].astype('int64')
    df = pd.pivot_table(analysis_metrics[analysis_metrics['BLOCK']==args.block], index='SUBJECT', columns='CATEGORY', values=variable, aggfunc='mean')
    df.loc['mean'] = df.mean()
    df.round(3).to_csv(fname.overview_mean(block=args.block, variable=variable), index=True)