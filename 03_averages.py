"""
Compute the averages per category
"""

import pandas as pd
from argparse import ArgumentParser

from config import fname


parser = ArgumentParser(__doc__)
parser.add_argument('block', type=str, help='Experiment block to process [A|B]')
args = parser.parse_args()


analysis_metrics = pd.read_csv(fname.analysis_metrics, sep="\t")

averages = analysis_metrics[analysis_metrics['BLOCK']==args.block].groupby('CATEGORY').mean()[['DWELL_TIME', 'TTFF', 'REENTERING_ROI_COUNT', 'STIMULUS_DURATION']]

averages.to_csv(fname.averages(block=args.block), sep="\t", index=True)