import numpy as np
import uproot
import pandas as pd
import csv
import json


# testing for one file
file = uproot.open("C:\\Users\\zalewski\\Desktop\\work\\data\\geo1\\cln_run01.root:cleaned")
# print(file.keys())
df = file.arrays(['SQX_L', 'SQY_L', 'CsI_L',
                  'SQX_R', 'SQY_R', 'CsI_R',
                  'F3', 'tdcF3', 'F5', 'tdcF5',
                  'nx1', 'ny1', 'nx2', 'ny2',
                  'x1', 'y1', 'x2', 'y2', 'trigger'], library="pd")

data = {}
with open('calibration_files.csv', 'r') as fp:
    data = json.load(fp)

# read column + calibration path pair
for column, path in data.items():
    slope = []
    intercept = []
    pixel_number = 0
    # open calibration parameters file for each detector
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        # read calibration parameters for each pixel
        for row in reader:
            slope.append(float(row[0]))
            intercept.append(float(row[1]))
            df[column] = df[column].apply(lambda x: slope[pixel_number] * x + intercept[pixel_number])
            pixel_number += 1






df['strip_X_L'] = df['SQX_L'].apply(lambda x: np.argmax(x))
df['strip_Y_L'] = df['SQY_L'].apply(lambda x: np.argmax(x))
df['strip_X_R'] = df['SQX_R'].apply(lambda x: np.argmax(x))
df['strip_X_R'] = df['SQX_R'].apply(lambda x: np.argmax(x))
df['csi_L'] = df['CsI_L'].apply(lambda x: np.argmax(x))
df['csi_R'] = df['CsI_R'].apply(lambda x: np.argmax(x))

df['sqlde'] = df['SQX_L'].apply(lambda x: np.max(x))
df['sqrde'] = df['SQX_R'].apply(lambda x: np.max(x))
df['sqletot'] = df['CsI_L'].apply(lambda x: np.max(x))
df['sqretot'] = df['CsI_R'].apply(lambda x: np.max(x))

df['tF3'] = df['tdcF3'].apply(lambda x: np.mean(x))
df['tF5'] = df['tdcF5'].apply(lambda x: np.mean(x))
df['aF5'] = df['F5'].apply(lambda x: np.mean(x))

df.drop(['SQX_L', 'SQY_L', 'CsI_L',
         'SQX_R', 'SQY_R', 'CsI_R',
         'tdcF3', 'tdcF5', 'F5', 'F3'], axis=1, inplace=True)