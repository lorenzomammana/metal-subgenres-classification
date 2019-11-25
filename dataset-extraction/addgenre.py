import pandas as pd

lyrics = pd.read_csv('darklyrics.csv', index_col=0)
maband = pd.read_csv('ma-band.csv')

maband['band'] = maband.apply(lambda x: x['band'].lower().capitalize(), axis=1)
maband['country'] = maband.apply(lambda x: x['country'].lower(), axis=1)
lyrics['band'] = lyrics.apply(lambda x: x['band'].lower().capitalize(), axis=1)
lyrics['genre'] = ""

for band in lyrics['band'].unique():

    if len(band.split("(")) > 1:
        bname = band.split("(")[0].strip()
        country = band.split("(")[1].split(")")[0]
    else:
        bname = band
        country = "None"

    associated = maband[maband['band'] == bname]

    if len(associated) == 0:
        lyrics.loc[lyrics['band'] == bname, 'genre'] = "MISSING"
    if len(associated) == 1:
        lyrics.loc[lyrics['band'] == bname, 'genre'] = associated['genre'].iloc[0].replace(",", "|")
    if len(associated) > 1:
        if country == "None":
            lyrics.loc[lyrics['band'] == bname, 'genre'] = "MISSING"
            print(bname)
        else:
            genrecountry = associated[associated['country'] == country]['genre']

            if len(genrecountry) == 0:
                lyrics.loc[lyrics['band'] == bname, 'genre'] = "MISSING"
                print(bname)
            else:
                lyrics.loc[lyrics['band'] == bname, 'genre'] = genrecountry.iloc[0].replace(",", "|")

lyrics.to_csv('darklyrics2.csv', index=False)


