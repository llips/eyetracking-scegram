"""
Helper Functions
"""

import numpy as np
import matplotlib.pyplot as plt

# Returns true if in given ROI
def is_in_roi(x, y, roi_x, roi_y, roi_width, roi_height):
    """
    Returns true if in region of interest and false if not
    """
    return ((x >= roi_x and x <= roi_x + roi_width) and (y >= roi_y and y <= roi_y + roi_height))


def fill_between(df, search_column, change_column, start_str, end_str, fill_str=None):
    """
    TODO: Description
    """
    starts = list(df[df[search_column] == start_str].index)
    ends = list(df[df[search_column] == end_str].index)

    boundaries = list(zip(starts, ends))

    for (s,e) in boundaries:
        fill_str_ = df[change_column].loc[s] if fill_str == None else fill_str
        df[change_column].loc[list(range(s+1,e))] = fill_str_

    return df


def px_to_deg(distance, size_in_px, px_density):
    """
    Convertion from px to degree
    """
    size_in_mm = size_in_px / px_density
    return np.degrees(np.arctan2(size_in_mm, distance))


def I_DT(samples, disp_t, dur_t):
    
    reached_the_end=False
    win_start=0
    win_end=dur_t
    fixation=[]
    no_fixation=[]
    
    while not reached_the_end:
        d=get_dispersion(get_samples(win_start,win_end,samples))
        if d > disp_t:
            no_fixation.append((win_start,win_end))
            win_start+=1
            win_end+=1
            if win_end>=len(samples[0])-1:
                reached_the_end=True
                break
                
            continue
        else:
            while d <= disp_t:
                win_end+=1              
                d=get_dispersion(get_samples(win_start,win_end,samples))
                if win_end>=len(samples[0])-1:
                    reached_the_end=True
                    win_end = len(samples[0])
                    break
            no_fixation.append((win_end-1,win_end-1))
            fixation.append((win_start,win_end-1))
            win_start=win_end
            win_end+=dur_t
        
    return fixation, no_fixation

        
def get_dispersion(smpls):
    return (max(smpls[0])-min(smpls[0]))+(max(smpls[1])-min(smpls[1]))


def get_samples(start,end,smpls):
    s=np.array(smpls)[:, start:end]
    return s


def plot(data, data_std, category, variable, ylabel, ymax, filename):
    labels = data[category]
    values = data[variable]

    colors = plt.get_cmap("tab10").colors
    plt.rc('font', size=30)
    plt.rc('xtick', top=False, bottom=False, labelbottom=False)
    plt.rc('figure', figsize=(20,10))

    value = [v for v in values]
    yerr = data_std

    bars = plt.bar(x = labels, height = values, color = colors, yerr=yerr, capsize=15)

    for p in plt.gca().patches:
        plt.gca().annotate(
            f"{(p.get_height()):.1f}", 
            (p.get_x() + p.get_width() / 2., p.get_height() + 1.1*data_std.max()), 
            ha = 'center', va = 'center', 
            xytext = (0, 9), 
            textcoords = 'offset points'
        )

    patches = list(bars)
    legend_labels = [l for l in labels]

    plt.legend(patches, legend_labels, bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.ylabel(ylabel, labelpad=40)
    plt.ylim(0, ymax)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()