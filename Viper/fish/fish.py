import csv
from i_menu import i_menu
from colored import fg,attr
red = fg('red')
reset = attr('reset')
rows = []
try:
    csv_file_handle = open("fish.csv", encoding="utf-8")
except FileNotFoundError:
    print(red+"ERROR: "+ reset + "No 'fish.csv' file in directory!")
    quit()
with csv_file_handle:
    csv_reader = csv.reader(csv_file_handle, delimiter=',')
    col_i = 0
    for row in csv_reader:
        if col_i == 0:
            column_heads = row
            col_i += 1
        else:
            for cell in row:
                if not cell:
                    cell = "" #still False but now is a string and type uniform
            rows.append(row)
            col_i += 1
for i in range(len(rows)):
    rows[i].pop(0)
column_heads.pop(0)#because first column is time of entry (useless)
column_values = []
for col_i in range(len(rows[0])):
    column_values.append([])
    for row_i in range(len(rows)):
        if not rows[row_i][col_i] in column_values[col_i]:
            column_values[col_i].append(rows[row_i][col_i])


def filter(chosen):
    """Counts how many rows match the chosen pattern"""
    count = 0
    for (real, possible) in zip(chosen, column_values):
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
    """for eachpage, show the distribution of all rows that match chosen patter on the current page options,
    so that the sum of all options are equal to all entries that match the chosen pattern"""
    for (real, possible) in zip(chosen, column_values):
        if real:
            assert real in possible
    lod = [] #list of dicts. Each dict is on page or one column with each key a option and 
    #the value the number of rows that match chosen pattern and have selected that option

    for column_i in range(len(column_heads)):
        dick = {key: 0 for key in column_values[column_i]}
        for row in rows:
            able = True # a row matches the chosen pattern in this column
            for i in range(len(row)):
                if chosen[i] is None:
                    continue
                if row[i] != chosen[i]:
                    able = False #somewhere the row doesn't match the chosen pattern anymore
            if not able:
                continue
            dick[row[column_i]] += 1
        lot = sum(dick.values())
        new_dick = {}
        for key, value in dick.items():
            new_dick[key] = f"{value} ({value/lot*100:.1f}%)"
        lod.append(new_dick)
    return lod


res = [None for _ in range(len(rows))] #what has been selected (the chosen pattern)
m = i_menu(options=column_values, header=column_heads)
value = len(rows)
while True:
    m.result = f"Search results: {value} ({value/len(rows)*100:.1f}%)"
    lod = get_distribution(res) #list of dicts, one dict per page, one key for each option
    m.distros = lod #unnecessary but readable?
    res = m.loop()#user input loop until user presses enter to choose option
    value = filter(res) # count the rows matching new pattern
