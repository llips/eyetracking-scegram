import pandas as pd
from argparse import ArgumentParser, BooleanOptionalAction

from config import fname


parser = ArgumentParser(__doc__)
parser.add_argument('subject', type=int, help='Subject to process [1-6]')
parser.add_argument('--fix', default=False, action=BooleanOptionalAction)
args = parser.parse_args()
    
# Load raw data
raw_data_subject = pd.read_csv(fname.raw_data_subject(subject=args.subject), sep="\t")

# Make work copy
df = raw_data_subject.copy()

# Create temporary columns
df['USERX'] = df.apply(lambda row: '_'.join([str(row['USER']).split('_')[i] for i in [4,5]]) if len(str(row['USER']).split('_')) == 6 else None, axis=1)
df['USERY'] = df.apply(lambda row: '_'.join([str(row['USER']).split('_')[i] for i in [0,1,2,3]]) if len(str(row['USER']).split('_')) == 6 else None, axis=1)

default = ['FIXATION_ONSET_BLOCK_A', 'FIXATION_END_BLOCK_A', 'STIMULI_ONSET_BLOCK_A', 'STIMULI_END_BLOCK_A', 'FIXATION_ONSET_BLOCK_B', 'FIXATION_END_BLOCK_B', 'STIMULI_ONSET_BLOCK_B', 'STIMULI_END_BLOCK_B']

# Find missing logs
temp = df.groupby('USERX').agg({'USERY':lambda x: list(set(default)-set(list(x))) if list(set(default)-set(list(x))) else 0}).reset_index()
missing = temp[temp['USERY'] != 0]
m1 = missing.apply(lambda row: '_'.join([row.USERY[0], row.USERX]), axis=1)
m2 = missing.apply(lambda row: '_'.join([row.USERY[1], row.USERX]) if len(row.USERY) > 1 else 0, axis=1)
m2 = m2[m2 != 0]
missing = pd.concat([m1, m2])

# If True, adds missing logs right after FIXATION_END

if args.fix:
    for log in missing.values:
        # Replace duplicated log message (always taking the first)
        raw_data_subject['USER'] = raw_data_subject['USER'].where(~raw_data_subject.duplicated(subset=['USER']), other=-1)
        
        fixation_log = log.replace('STIMULI_ONSET', 'FIXATION_END')
        idx = raw_data_subject.USER.eq(fixation_log).idxmax()
        raw_data_subject['USER'].loc[idx+1] = log

    raw_data_subject.to_csv(fname.fixed_data_subject(subject=args.subject), sep="\t", index=False)


# Save
missing.to_csv(fname.log_check(subject=args.subject), index=False)


