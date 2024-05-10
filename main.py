import numpy as np
import uproot

file = uproot.open("C:\\Users\\zalewski\\Desktop\\work\\data\\geo1\\cln_run01.root:cleaned")
# print(file.keys())
df = file.arrays(['SQX_L', 'SQY_L', 'CsI_L',
                  'SQX_R', 'SQY_R', 'CsI_R',
                  'F3', 'tdcF3', 'F5', 'tdcF5',
                  'nx1', 'ny1', 'nx2', 'ny2',
                  'x1', 'y1', 'x2', 'y2', 'trigger'], library="pd")

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

df.drop(['SQX_L', 'SQY_L', 'CsI_L',
         'SQX_R', 'SQY_R', 'CsI_R'], axis=1, inplace=True)
