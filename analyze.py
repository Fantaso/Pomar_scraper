import pandas as pd

# name of the table headers
col_names = ['cedula','genre','city','name','last_name','phone','birthday','email',\
            'email_alt','city_attend','experience','cata','degustacion','course',\
            'visit','event','ninguna','date_found']
# read file, has no headers names, add the col names and the table is comma ',' separated
table = pd.read_table('database_pomar3.txt', header = None, names = col_names, sep = ',')

# print table
# print(table.head())
print(table)
