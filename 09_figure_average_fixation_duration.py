"""
Create histogram of average fixation duration in roi by category
"""
import pandas as pd
from argparse import ArgumentParser

from config import fname
from helpers import plot


parser = ArgumentParser(__doc__)
parser.add_argument('block', type=str, help='Experiment block to process [A|B]')
args = parser.parse_args()

analysis_metrics = pd.read_csv(fname.analysis_metrics, sep="\t")

category = "CATEGORY"
variable = "AVERAGE_FIXATION_ROI_DURATION"
ylabel = "Average Fixation Duration"

data = analysis_metrics[analysis_metrics['BLOCK']==args.block].groupby([category])[variable].mean()[['CON', 'SEM', 'SYN', 'SEMSYN', 'EXSYN', 'EXSEMSYN']].reset_index()
data_std = analysis_metrics[analysis_metrics['BLOCK']==args.block].groupby([category])[variable].std()[['CON', 'SEM', 'SYN', 'SEMSYN', 'EXSYN', 'EXSEMSYN']].reset_index()[variable]

plot(data, data_std, category=category, variable=variable, ylabel=ylabel, ymax=3, filename=fname.figure_average_fixation_duration_roi(block=args.block))