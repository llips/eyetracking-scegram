"""
Preprocess raw data
"""

import pandas as pd
from argparse import ArgumentParser

from config import fname
from helpers import fill_between


parser = ArgumentParser(__doc__)
parser.add_argument('subject', type=int, help='Subject to process [1-6]')
args = parser.parse_args()
    
# Load fixed data
fixed_data_subject = pd.read_csv(fname.fixed_data_subject(subject=args.subject), sep="\t")

# Make work copy and drop columns
processed_data_subject = fixed_data_subject.copy()[['TIME','BPOGX', 'BPOGY', 'USER']]

# Replace duplicated log message (always taking the first)
processed_data_subject['USER'] = processed_data_subject['USER'].where(~fixed_data_subject.duplicated(subset=['USER']), other=-1)

# Create columns based on log messages
processed_data_subject['TYPE'] = processed_data_subject.apply(lambda row: str(row['USER']).split('_')[0] +'_'+ str(row['USER']).split('_')[1] if len(str(row['USER']).split('_')) == 6 else None, axis=1)
processed_data_subject['BLOCK'] = processed_data_subject.apply(lambda row: str(row['USER']).split('_')[3] if len(str(row['USER']).split('_')) == 6 else None, axis=1)
processed_data_subject['SCENE'] = processed_data_subject.apply(lambda row: str(row['USER']).split('_')[4] if len(str(row['USER']).split('_')) == 6 else None, axis=1)
processed_data_subject['CATEGORY'] = processed_data_subject.apply(lambda row: str(row['USER']).split('_')[5] if len(str(row['USER']).split('_')) == 6 else None, axis=1)

# Add additional information to each eyetracking sample
for i in ['FIXATION', 'STIMULI']:
    fill_between(processed_data_subject, 'TYPE', 'TYPE', i+'_ONSET', i+'_END', i)
    fill_between(processed_data_subject, 'TYPE', 'BLOCK', i+'_ONSET', i+'_END')
    fill_between(processed_data_subject, 'TYPE', 'SCENE', i+'_ONSET', i+'_END')
    fill_between(processed_data_subject, 'TYPE', 'CATEGORY', i+'_ONSET', i+'_END')

# Move column becaus of visual appearance
temp_column = processed_data_subject.pop('USER')
processed_data_subject = pd.concat([processed_data_subject, temp_column], 1)

# Save processed data
processed_data_subject.to_csv(fname.processed_data_subject(subject=args.subject), sep="\t", index=False)