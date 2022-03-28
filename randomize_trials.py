import random
import pandas as pd
from  config import fname

random.seed(0)


trial = pd.read_excel(fname.trial_sequences)

_trial = trial.copy()

for col in _trial:
    succesful = False
    while not succesful:
        # shuffle
        _shuffled = trial.copy()
        _shuffled[col] = _shuffled[col].sample(frac=1).values.copy()

        _splitted = _shuffled.copy()
        _splitted[col] = _splitted[col].str.split('_', 1, expand=True)[1].copy()
        
        # check for three consecutive same categories 
        last = None
        count = 0

        _splitted['diff'] = (_splitted[col] != _splitted[col].shift(1)).cumsum()
        #_trial['diff'] = (_trial[col] != _trial[col].shift(1)).cumsum()
        max_consecutive = max(_splitted.groupby('diff').count().max().values)


        if max_consecutive < 3:
            succesful = True
            trial[col] = _shuffled[col]


trial.to_excel('randomized_trial_sequences.xlsx', index=False)