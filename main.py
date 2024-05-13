import numpy as np
import uproot
import pandas as pd
import csv
import json
import matplotlib.pyplot as plt
import time
import random
import statistics
import glob


files_to_open = glob.glob('C:\\Users\\zalewski\\Desktop\\work\\data\\geo1\\*.root')

start_time = time.time()

# testing for one file
file = uproot.open('C:\\Users\\zalewski\\Desktop\\work\\data\\geo1\\cln_run01.root:cleaned')

# columns necessary for data interpretation
df = file.arrays(['SQX_L', 'SQY_L', 'CsI_L',
                  'SQX_R', 'SQY_R', 'CsI_R',
                  'F3', 'tdcF3', 'F5', 'tdcF5',
                  'nx1', 'ny1', 'nx2', 'ny2',
                  'x1', 'y1', 'x2', 'y2', 'trigger'], library="pd")

# read columns and corresponding calibration files paths
data = {}
with open('calibration_files.json', 'r') as parameters_file:
    data = json.load(parameters_file)

# read column + calibration path pair
for column, path in data.items():
    # open calibration parameters file for each detector
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        intercept, slope = zip(*(map(float, row) for row in reader))

        # perform calibration of each column with read parameters
        tmp_array = np.array(df[column].tolist())
        calibrated_array = (tmp_array + random.uniform(-0.5, 0.5)) * slope + intercept
        df[column] = calibrated_array.tolist()

print("--- %s seconds ---" % (time.time() - start_time))

# get numbers of strips with the highest energy
df['strip_X_L'] = [x.index(max(x)) for x in df['SQX_L']]
df['strip_Y_L'] = [x.index(max(x)) for x in df['SQY_L']]
df['strip_X_R'] = [x.index(max(x)) for x in df['SQX_R']]
df['strip_Y_R'] = [x.index(max(x)) for x in df['SQY_R']]
df['csi_L'] = [x.index(max(x)) for x in df['CsI_L']]
df['csi_R'] = [x.index(max(x)) for x in df['CsI_R']]

# get the highest energies
df['sqlde'] = [max(x) for x in df['SQX_L']]
df['sqrde'] = [max(x) for x in df['SQY_L']]
df['sqletot'] = [max(x) for x in df['CsI_L']]
df['sqretot'] = [max(x) for x in df['CsI_R']]


df['tF3'] = [statistics.mean(x) for x in df['tdcF3']]
df['tF5'] = [statistics.mean(x) for x in df['tdcF5']]
df['aF5'] = [statistics.mean(x) for x in df['F5']]
df['tof'] = df['tF5'] - df['tF3'] + 89.165

def get_wire_number(m_list, m_size):
    if (m_list[0:m_size] == list(range(m_list[0], m_list[0]+m_size))).all():
        return (m_list[0]+m_list[m_size-1])/2
    else:
        print('ERROR')
        return float('NaN')


MWPC_lists = {'MWPC_1_X': ['x1', 'nx1'],
              'MWPC_2_X': ['x2', 'nx2'],
              'MWPC_1_Y': ['y1', 'ny1'],
              'MWPC_2_Y': ['y2', 'ny2']}

for MWPC_ID, MWPC_input in MWPC_lists.items():
    hits_array = np.array(df[MWPC_input[0]].tolist())
    hit_ID_array = np.array(df[MWPC_input[1]].tolist())
    df[MWPC_ID] = [get_wire_number(x, y) for x, y in zip(hits_array, hit_ID_array)]

df = df.dropna()

df.drop(['SQX_L', 'SQY_L', 'CsI_L',
         'SQX_R', 'SQY_R', 'CsI_R',
         'tdcF3', 'tdcF5', 'F5', 'F3',
         'x1', 'nx1', 'x2', 'nx2',
         'y1', 'ny1', 'y2', 'ny2'], axis=1, inplace=True)

plt.scatter(df['sqretot'], df['sqrde'])
plt.show()

df.to_csv('C:\\Users\\zalewski\\Desktop\\work\\data\\geo1\\calibrated.csv')
