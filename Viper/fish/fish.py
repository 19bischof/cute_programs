import csv
from i_menu import i_menu
import pathlib

rows = []
with open("fish.csv",encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    col_i = 0
    for row in csv_reader:
        if col_i == 0:
            column_heads = row
            col_i += 1
        else:
            rows.append(row)
            # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            col_i += 1
    print(f'Processed {col_i} lines.')
for i in range(len(rows)):
    rows[i].pop(0)
column_heads.pop(0)
column_values = []
for col_i in range(len(rows[0])):
    column_values.append([])
    for row_i in range(len(rows)):
        if not rows[row_i][col_i] in column_values[col_i]:
            column_values[col_i].append(rows[row_i][col_i])
print(column_values)

def filter(chosen):
    count = 0
    for (real,possible) in zip(chosen,column_values):
        if real:
            assert real in possible
    assert len(chosen) == len(rows[0])
    for row in rows:
        count += 1
        for i in range(len(row)):
            if not chosen[i]:
                continue
            if row[i] != chosen[i]:
                count -= 1
                break
    return count
def get_distribution(chosen):
    for (real,possible) in zip(chosen,column_values):
        if real:
            assert real in possible
    lod = []
    for column_i in range(len(column_heads)):
        dick = {key:0 for key in column_values[column_i]}
        for row in rows:
            able = True
            for i in range(len(row)):
                if not chosen[i]:
                    continue
                if row[i] != chosen[i]:
                    able = False
            if not able:
                continue
            dick[row[column_i]] += 1
        lot = sum(dick.values())
        new_dick = {}
        for key,value in dick.items():
            new_dick[key] = f"{value} ({value/lot*100:.1f}%)"
        lod.append(new_dick)
    return lod
# print(filter(choice))
res = [None,None,None,None,None,None,None,None,None]
m = i_menu(options=column_values,header=column_heads)
value = len(rows)
while True:
    m.result = f"Search results: {value} ({value/len(rows)*100:.1f}%)"
    lod = get_distribution(res)
    m.distros = lod
    res = m.loop()
    value = filter(res)