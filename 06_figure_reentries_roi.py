"""
Create histogram of average dwell time by category
"""
import pandas as pd
from argparse import ArgumentParser

from config import fname
from helpers import plot


parser = ArgumentParser(__doc__)
parser.add_argument('block', type=str, help='Experiment block to process [A|B]')
args = parser.parse_args()

analysis_metrics = pd.read_csv(fname.analysis_metrics, sep="\t")

#analysis_metrics[analysis_metrics['BLOCK']==args.block].groupby('CATEGORY')['REENTERING_ROI_COUNT'].mean()[['CON', 'SEM', 'SYN', 'SEMSYN', 'EXSYN', 'EXSEMSYN']].plot(kind='bar', figsize=(10,6), fontsize=13, rot=0, title='Number of reentries in roi', ylabel='Count',
#         xlabel='Consistency Category', ylim=(0,5)).get_figure().savefig(fname.figure_reentries_roi(block=args.block))

category = "CATEGORY"
variable = "REENTERING_ROI_COUNT"
ylabel = "#Reentries ROI"

data = analysis_metrics[analysis_metrics['BLOCK']==args.block].groupby([category])[variable].mean()[['CON', 'SEM', 'SYN', 'SEMSYN', 'EXSYN', 'EXSEMSYN']].reset_index()
data_std = analysis_metrics[analysis_metrics['BLOCK']==args.block].groupby([category])[variable].std()[['CON', 'SEM', 'SYN', 'SEMSYN', 'EXSYN', 'EXSEMSYN']].reset_index()[variable]

plot(data, data_std, category=category, variable=variable, ylabel=ylabel, ymax=10, filename=fname.figure_reentries_roi(block=args.block))