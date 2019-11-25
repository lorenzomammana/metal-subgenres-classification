import pandas as pd

lyrics = pd.read_csv('darklyrics.csv')

bandalbumcountry = pd.read_csv('bandalbum.csv')

for row in bandalbumcountry.itertuples(index=True, name='Pandas'):
    band = getattr(row, 'band')
    album = getattr(row, 'album')
    country = getattr(row, 'country')

    newname = band + " (" + country.lower().capitalize() + ")"

    lyrics.loc[(lyrics['band'] == band) & (lyrics['album'] == album), 'band'] = newname

lyrics.to_csv('darklyrics2.csv')
