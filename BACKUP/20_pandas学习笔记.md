# [pandas学习笔记](https://github.com/chaleaoch/gitblog/issues/20)


Table of Contents
=================



\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
```
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import pandas as pd
import numpy as n

dates = pd.date_range("20200101", periods=6)


# %%
df = pd.DataFrame(np.random.randn(6,4), index = dates,columns=list('ABCD'))
df


# %%
df.head(3)


# %%
df.tail(3)


# %%
df.index


# %%
df.columns


# %%
df.describe()


# %%
df.sort_values(by="B",ascending=False)


# %%
df.A


# %%
df[0:3]


# %%
import pandas as pd
import numpy as np
pd.DataFrame([1,2,3,4,5,6])


# %%
data = [['xiaoming', 10],['BOB', 12],['laochen', 13]]
pd.DataFrame(data, columns=['username', 'age'])


# %%
data = {
    'username':['小黑','小白','小陈'],
    'income':[1000,2000,3000]
}
pd.DataFrame(data, columns=['username', 'income'], index=[1,2,3])
pd.DataFrame(data, index=[1,2,3])


# %%
data = {
    'one':pd.Series([1,2,3],index=['a','b','c']),
    'two':pd.Series([1,2,3,4],index=['a','b','c','d']),
}
df = pd.DataFrame(data)
df


# %%
df['one']


# %%
df['three'] = pd.Series([4,5,6,7], index=['a','b','c','d'])
df


# %%
df['four'] = df['one'] + df['three']
df


# %%
del df['four']
df.pop('two')
df


# %%
df.loc['c']


# %%
df.iloc[0]


# %%
df[0:2]


# %%
df2 = pd.DataFrame([[2,5],[5,6]], columns=['one','three'])
df.append(df2)


# %%
df2


# %%
df2.drop(0)


# %%
list(df.index)
df


# %%
df['router_name'] = list(df.index)
df


# %%
d = {
    "name":pd.Series(['小明','小黑','小红']),
    "age":pd.Series([12,16,18]),
    "score":pd.Series([98,99,45]),
}
df = pd.DataFrame(d)
df


# %%
df.sum(axis=1) # pandas 1 代表行 0 代表列 默认是列


# %%
dict(df.sum(axis=0))


# %%
df.mean()


# %%
df.max()


# %%
df.describe(include='int')


# %%
df = pd.DataFrame({
    "a":pd.date_range(start='2020-01-01', periods=5, freq="D"),
    "b":[1,2,3,4,5],
    'c':[0.1,0.2,0.3,0.4,0.5]
})
df


# %%
df.reindex(index=[0,2,4], columns=['a','b','d'])


# %%
df.reindex(index=[0,5,6], columns=['a','b','c'])


# %%
df.reindex(index=[0,5,6], columns=['a','b','c'],method="ffill")


# %%
df.rename(columns={'c':'g','d':'e'})


# %%
df = pd.DataFrame({
    "date":pd.date_range(start='2020-01-01', periods=7, freq="D"),
    "a":np.linspace(0,6,7,dtype=int),
    'b':np.random.rand(7),
    'c':np.random.choice(['Low','Medium','High',7]).tolist(),
    'd':np.random.normal(100,10,size=(7)).tolist(),
})
df


# %%
for col in df: # 按列迭代
    print(col)


# %%
for col,value in df.iteritems(): # 按列迭代
    print(col)
    print(value)


# %%
for key ,value in df.iterrows():
    print(key)
    print(value)


# %%
for row in df.itertuples():
    print(row)


# %%
df = pd.DataFrame(np.random.randn(8,4), index=['a','b','c','d','e','f','g','h'], columns=['A','B','C','D'])
df


# %%
df.loc[:,['A','B']]


# %%
df.loc['a':'e']


# %%
df.loc['a':'e','B':'D']


# %%
df.loc['a']>1


# %%
df.loc[:,'A']>1


# %%
df.loc[:,df.loc['a']>0]


# %%
df.iloc[1:3,1:3]


# %%
df.A


# %%
df = pd.DataFrame(np.random.randn(10,4))
df


# %%
df.rolling(window=3).mean()


# %%
df.expanding(min_periods=3).mean()


# %%
df = pd.DataFrame(np.random.randn(10,4), index=pd.date_range('2020-01-01', periods=10), columns=['A','B','C','D'])
df


# %%
df.rolling(window=3).aggregate(np.sum)


# %%
r = df.rolling(window=3)
r[['A','B']].aggregate([np.max,np.min])


# %%
df.rolling(window=3).max()


# %%
df.max(axis=1)


# %%
r[["A","B"]].aggregate({"A":np.min,"B":np.max})


# %%
df = pd.DataFrame(np.random.randn(5,3), index=['a','c','e','f','h'], columns=['one','two','three'])
df


# %%
df.reindex(columns = ["one"])


# %%
df = df.reset_index()
df


# %%
df.reindex()


# %%
df = pd.DataFrame({
    'user':['小明','小黑','小黄','小李'],
    'gender':['男','女','女','男'],
    'score':[12,34,56,78],
})
df


# %%
df.groupby('gender').groups


# %%
grouped = df.groupby('gender')
for name, group in grouped:
    print(name)
    print(group)


# %%
grouped.get_group('男')


# %%
grouped.get_group('男')['score'].agg(np.mean)


# %%
grouped.get_group('男').agg(np.mean)


# %%
df['star'] = pd.Series([5,7,4,3])
df


# %%
grouped = df.groupby('gender')
grouped[['score','star']].agg({'score':np.mean,'star':np.sum})


# %%
df.groupby('gender').filter(lambda x:x['score'].mean()>90)


# %%
yuwen = pd.DataFrame({
    'id':[1,2,3,4,5,6],
    'name':['小明','小敏','小红','小黑','小王','大王'],
    'yuwenScore':[12,34,56,78,99,66]
})
shuxue = pd.DataFrame({
    'id':[1,2,3,4,5,6],
    'name':['小明','小敏','小红','小黑','小王','小王8'],
    'shuxueScore':[99,45,31,56,56,100]
})
pd.merge(yuwen,shuxue,on='id')


# %%
pd.merge(yuwen,shuxue,on=['id','name'])


# %%
pd.merge(yuwen,shuxue,on=['id','name'],how='right')


# %%
pd.merge(yuwen,shuxue,on=['id','name'],how='outer')


# %%
one = pd.DataFrame({
    'name':['alex','xm','xh','lc','ll'],
    'subject':['python','java','go','js','html'],
    'score':[11,22,33,44,55],
})
two = pd.DataFrame({
    'name2':['alex','xm2','xh2','lc2','ll2'],
    'subject':['python','java2','go2','js2','html2'],
    'score':[11,222,333,444,555],
})


# %%
pd.concat([one,two],ignore_index=True)


# %%
pd.concat([one,two])


# %%
pd.concat([one,two],axis=1)



```