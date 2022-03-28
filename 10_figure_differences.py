"""
Create histogram of average dwell time by category
"""
import pandas as pd
import matplotlib.pyplot as plt

from config import fname


analysis_metrics = pd.read_csv(fname.analysis_metrics, sep="\t")

analysis_metrics = analysis_metrics[['SCENE', 'SUBJECT','BLOCK', 'index', 'TTFF', 'CATEGORY', 'DWELL_TIME', 'REENTERING_ROI_COUNT']]
analysis_metrics = analysis_metrics.sort_values(['index', 'SUBJECT','BLOCK'],ascending=[False,False, False]).reset_index(drop=True)
analysis_metrics[['TTFF_DIFF', 'DWELL_TIME_DIFF', 'REENTRIES_ROI_DIFF']] = analysis_metrics.groupby(['SUBJECT', 'index'])[['TTFF', 'DWELL_TIME', 'REENTERING_ROI_COUNT']].diff(-1)

# Save plots

ax1 = analysis_metrics.groupby(['CATEGORY']).mean()['TTFF_DIFF'][['CON', 'SEM', 'SYN', 'SEMSYN', 'EXSYN', 'EXSEMSYN']].plot(kind='bar', figsize=(10,6), fontsize=13, rot=0, title='TTFF Difference (Block B - Block A)', ylabel='TTFF', xlabel='Consistency Category', ylim=(-0.5, 0.5))
ax1.axhline(y=0, color='black', linestyle='-', lw=0.5)
ax1.get_figure().savefig(fname.figure_difference(measurement='TTFF'))
plt.close()

ax2 = analysis_metrics.groupby(['CATEGORY']).mean()['DWELL_TIME_DIFF'][['CON', 'SEM', 'SYN', 'SEMSYN', 'EXSYN', 'EXSEMSYN']].plot(kind='bar', figsize=(10,6), fontsize=13, rot=0, title='Dwell Time Difference (Block B - Block A)', ylabel='Dwell Time',
         xlabel='Consistency Category', ylim=(-0.8, 0.8))
ax2.axhline(y=0, color='black', linestyle='-', lw=0.5)         
ax2.get_figure().savefig(fname.figure_difference(measurement='DWELL_TIME'))
plt.close()

ax3 = analysis_metrics.groupby(['CATEGORY']).mean()['REENTRIES_ROI_DIFF'][['CON', 'SEM', 'SYN', 'SEMSYN', 'EXSYN', 'EXSEMSYN']].plot(kind='bar', figsize=(10,6), fontsize=13, rot=0, title='Reentries Roi Difference (Block B - Block A)', ylabel='Count',
         xlabel='Consistency Category', ylim=(-2, 2))
ax3.axhline(y=0, color='black', linestyle='-', lw=0.5)         
ax3.get_figure().savefig(fname.figure_difference(measurement='REENTRIES_ROI'))
plt.close()