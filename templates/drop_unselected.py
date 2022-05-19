uselected = [
%unselectedCols%
]
for col in uselected:
    if col in train.columns:
        train = train.drop(col, 1)
    if col in test.columns:
        test = test.drop(col, 1)
train.head()