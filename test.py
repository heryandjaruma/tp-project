import pandas as pd

df1 = pd.DataFrame({'A':[3,3,4,6], 'B':['a1','b1','c1','d1']})
df2 = pd.DataFrame({'A':[5,4,6,1], 'B':['a2','b2','c2','d2']})

dfff = pd.DataFrame()
for i in range(0,4):

    print(df1.iloc[i])
    print('\n')
    print(df2.iloc[i])
    input()


    dfx = pd.concat([df1.iloc[i].T, df2.iloc[i].T])
    dfff = pd.concat([dfff, dfx])
    
    
print(pd.concat([df1, df2]).sort_index(kind='merge'))