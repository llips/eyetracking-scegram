"""
Create histogram of average dwell time by category
"""
import pandas as pd
import matplotlib.pyplot as plt

from config import fname
from helpers import plot_diff


analysis_metrics = pd.read_csv(fname.analysis_metrics, sep="\t")

analysis_metrics = analysis_metrics[['SCENE', 'SUBJECT','BLOCK', 'index', 'TTFF', 'CATEGORY', 'DWELL_TIME', 'FIXATION_ROI_COUNT']]
analysis_metrics = analysis_metrics.sort_values(['index', 'SUBJECT','BLOCK'],ascending=[False,False, False]).reset_index(drop=True)
analysis_metrics[['TTFF_DIFF', 'DWELL_TIME_DIFF', 'FIXATION_ROI_DIFF']] = analysis_metrics.groupby(['SUBJECT', 'index'])[['TTFF', 'DWELL_TIME', 'FIXATION_ROI_COUNT']].diff(-1)


# plot diff ttff 
category = "CATEGORY"
variable = "TTFF_DIFF"
ylabel = "Difference in TTFF"

data = analysis_metrics.groupby([category]).mean()[variable][['CON', 'SEM', 'SYN', 'SEMSYN', 'EXSYN', 'EXSEMSYN']].reset_index()
plot_diff(data, category=category, variable=variable, ylabel=ylabel, ymin=-1, ymax=1, filename=fname.figure_difference(measurement=variable))

# Plot diff dwell time
category = "CATEGORY"
variable = "DWELL_TIME_DIFF"
ylabel = "Difference in Dwell Time"

data = analysis_metrics.groupby([category]).mean()[variable][['CON', 'SEM', 'SYN', 'SEMSYN', 'EXSYN', 'EXSEMSYN']].reset_index()
plot_diff(data, category=category, variable=variable, ylabel=ylabel, ymin=-1, ymax=1, filename=fname.figure_difference(measurement=variable))

#plot diff 
category = "CATEGORY"
variable = "FIXATION_ROI_DIFF"
ylabel = "Difference in #Fixations ROI"

data = analysis_metrics.groupby([category]).mean()[variable][['CON', 'SEM', 'SYN', 'SEMSYN', 'EXSYN', 'EXSEMSYN']].reset_index()
plot_diff(data, category=category, variable=variable, ylabel=ylabel, ymin=-1, ymax=1, filename=fname.figure_difference(measurement=variable))