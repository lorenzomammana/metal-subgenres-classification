import pandas as pd


maband = pd.read_csv('ma-band.csv', index_col=0)

maband.drop('Status', axis=1, inplace=True)

maband['NameLink'] = maband.apply(lambda x: x['NameLink'].split(">")[1].split("<")[0], axis=1)

maband.to_csv('ma-band2.csv', index=False)