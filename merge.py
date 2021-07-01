import pandas as pd


merged = pd.read_excel('./download/savedrecs.xls')
print(len(merged))

for i in range(1,25):
    ##### to be modified
    tmp = pd.read_excel('./download/savedrecs ('+str(i)+').xls')
    print(i)
    merged = pd.concat([merged, tmp])

merged.to_csv(r'./output.csv', index=None, encoding='utf_8_sig')
