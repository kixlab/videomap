import pygsheets
import pandas as pd
# authorization
gc = pygsheets.authorize(
    service_file='./videomap-taxonomy-f38ec095e98c.json')

# Create empty dataframe
df = pd.DataFrame()

# Create a column
df['name'] = ['John', 'Steve', 'Sarah']

# open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('PY to Gsheet Test')

# select the first sheet
wks = sh[0]

# update the first sheet with
wks.set_dataframe(df, (1, 1))
