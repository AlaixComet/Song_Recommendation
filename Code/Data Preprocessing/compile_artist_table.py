#In[1]:
import os
import pandas as pd
import numpy as np

#In[2]:
def make_artist_table(base):
# Get file names

    files = [os.path.join(base,fn) for fn in os.listdir(base) if fn.endswith('.h5')]
    data = {'id':[], 'file':[], 'artist':[], 'title':[], 'artist_id':[], 'danceability':[], 'song_hotttnesss':[], 'year':[]}

    # Add artist and title data to dictionary
    for f in files:
        store = pd.HDFStore(f)
        print(store.keys())
        id = store.root.metadata.songs.cols.song_id[0]
        title = store.root.metadata.songs.cols.title[0]
        artist = store.root.metadata.songs.cols.artist_name[0]
        artist_id = store.root.metadata.songs.cols.artist_mbid[0]
        danceability = store.root.analysis.songs.cols.danceability[0]
        song_hotttnesss = store.root.metadata.songs.cols.song_hotttnesss[0]
        year = store.root.musicbrainz.songs.cols.year[0]
        data['id'].append(id.decode("utf-8"))
        data['file'].append(os.path.basename(f))
        data['title'].append(title.decode("utf-8"))
        data['artist'].append(artist.decode("utf-8"))
        data['artist_id'].append(artist_id.decode("utf-8"))
        data['danceability'].append(danceability.item())
        data['song_hotttnesss'].append(np.asscalar(song_hotttnesss))
        data['year'].append(np.asscalar(year))
        store.close()
    
    # Convert dictionary to pandas DataFrame
    df = pd.DataFrame.from_dict(data, orient='columns')
    df = df[['id', 'file', 'artist', 'artist_id', 'title', 'danceability', 'song_hotttnesss', 'year']]
    return df

#In[3]:
def findLyricsFromWeb(artist, title):
    import  urllib.request as urllib2
    import  urllib.error
    from bs4 import BeautifulSoup
    
    artist = artist.replace(' ','_')
    title = title.replace(' ','_')
    url = 'http://lyrics.wikia.com/wiki/'+artist+':'+title
    try :
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        soup.find('div', {'class':'special-categories'})
        english = soup.find('li', {'data-name':'Language/English'})
        if english :
            lyrics = soup.find('div', {'class':'lyricbox'}).text
            return(lyrics)
    except (urllib.error.HTTPError, UnicodeEncodeError) :
        pass

#In[4]:
base = 'Subset1/'
results = "ResultsSubset1/"

#In[5]:
df = make_artist_table(base)

#In[6]:
def writeFile(row, lyrics):
    with open(results+row['file'],'w',encoding = 'utf-8') as f :
        for r in row :
            f.write(str(r)+"\n")
        f.write(lyrics)

#In[7]:
import re

def adaptLyrics(lyrics):
    reg = re.compile(r'(\S)([A-Z])')
    result = reg.sub(r'\1<SEP>\2',lyrics)
    return result

lyrics = "Darling, I don't know muchBut I know I love you so muchMy life depends on your touchAnd my love is a river running soul deepWay down inside me, it's-a soul deepIt's too big to hide And it can't be deniedMy love is a river running soul deepI'll work myself to death for youJust to show I adore youNothing I wouldn't do for you'Cause my love is a river running soul deepWay down inside me, it's-a soul deepIt's too big to hide And it can't be deniedMy love is a river running soul deepAll I ever, ever hope to beDepends on your love for meBaby, believe meIf you should leave meI'd be nothing but an empty shellI know darn well, I can tell, nowI don't know muchBut I know I love you so muchMy life depends on your touchAnd my love is a river running soul deepWay down inside me, it's-a soul deepIt's too big to hide and it can't be deniedMy love is a river running soul deepMy love is a river running soul deepWay down inside me, it's-a soul deepMy love is a river running soul deepWay down inside me, it's-a soul deepWell, my love is a river running soul deepWay down inside me, it's-a soul deep"
adaptLyrics(lyrics)

# #In[8]:
# print(df.columns.values)
# for index, row in df.iterrows():
#     print(row)
#     artist = row['artist']
#     title =  row['title']
#     lyrics = (findLyricsFromWeb(artist, title))
#     if lyrics :
#         lyrics = adaptLyrics(lyrics.rstrip())
#         writeFile(row, lyrics)

#In[9]:
print()