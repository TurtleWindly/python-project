import pandas as pd

data = {
    'Name': ['Shravan', 'Jeetu', 'Ram', 'Jeetu', 'Shravan', 'Ram'],
    'Subject': ['DSA', 'DSA', 'DSA', 'DBMS', 'DBMS', 'DBMS'],
    'Score': [85, 90, 75, 80, 88, 82],
    'Grade': ['A', 'A', 'B', 'B', 'A', 'B']
}

df = pd.DataFrame(data)
print(df)

# Creating a pivot table with multiple columns
pivot_table = df.pivot_table(index='Name',
                             columns='Subject',
                             values=['Score', 'Grade'],
                             aggfunc={'Score': 'mean', 'Grade': 'first'})

print(pivot_table)