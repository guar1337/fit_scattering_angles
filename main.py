import numpy as np
import uproot
import pandas as pd
import csv
import json
import matplotlib.pyplot as plt
import time
import random
import statistics


start_time = time.time()

# testing for one file
file = uproot.open("C:\\Users\\zalewski\\Desktop\\work\\data\\geo1\\cln_run01.root:cleaned")

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
    slope = []
    intercept = []
    # open calibration parameters file for each detector
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        # read calibration parameters for each pixel
        for row in reader:
            intercept.append(float(row[0]))
            slope.append(float(row[1]))

        # perform calibration of each column with read parameters
        tmp_array = np.array(df[column].tolist())
        calibrated_array = (tmp_array + random.uniform(-0.5, 0.5)) * slope + intercept
        df[column] = calibrated_array.tolist()

print("--- %s seconds ---" % (time.time() - start_time))

# get numbers of strips with the highest energy
df['strip_X_L'] = [x.index(max(x)) for x in df['SQX_L']]
df['strip_Y_L'] = [x.index(max(x)) for x in df['SQY_L']]
df['strip_X_R'] = [x.index(max(x)) for x in df['SQX_R']]
df['strip_X_R'] = [x.index(max(x)) for x in df['SQY_R']]
df['csi_L'] = [x.index(max(x)) for x in df['CsI_L']]
df['csi_R'] = [x.index(max(x)) for x in df['CsI_R']]

# get the highest energies
df['sqlde'] = [max(x) for x in df['SQX_L']]
df['sqrde'] = [max(x) for x in df['SQY_L']]
df['sqletot'] = [max(x) for x in df['CsI_L']]
df['sqretot'] = [max(x) for x in df['CsI_R']]



plt.scatter(df['sqletot'], df['sqlde'])
plt.show()

df['tF3'] = [statistics.mean(x) for x in df['tdcF3']]
df['tF5'] = [statistics.mean(x) for x in df['tdcF5']]
df['aF5'] = [statistics.mean(x) for x in df['F5']]



df.drop(['SQX_L', 'SQY_L', 'CsI_L',
         'SQX_R', 'SQY_R', 'CsI_R',
         'tdcF3', 'tdcF5', 'F5', 'F3'], axis=1, inplace=True)
