import pandas
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

#add the music datasets
triplets_file = 'https://static.turi.com/datasets/millionsong/10000.txt'
songs_metadata_file = 'https://static.turi.com/datasets/millionsong/song_data.csv'

#load the datasets using Pandas Library
song_df_1 = pandas.read_table(triplets_file, header=None)
song_df_1.columns = ['user_id', 'song_id', 'listen_count']
song_df_2 = pandas.read_csv(songs_metadata_file)
#Merge the tables and drop the duplicate tables
song_df = pandas.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on="song_id", how="left")
song_df.head()
#print(len(song_df))

#As the dataset has over a million rows, we take a subset of the data.
#Subset size = 10K
song_df = song_df.head(10000)

#Merge the title and artist_name columns to make a single column
song_df['song'] = song_df['title'].map(str) + " : " + song_df['artist_name']

#Most popular songs in the dataset
song_grouped = song_df.groupby(['song']).agg({'listen_count': 'count'}).reset_index()
grouped_sum = song_grouped['listen_count'].sum()
song_grouped['percentage']  = song_grouped['listen_count'].div(grouped_sum)*100
song_grouped.sort_values(['listen_count', 'song'], ascending = [0,1])

#unique users
users = song_df['user_id'].unique()
#print(len(users))

#uniquw songs
songs = song_df['song'].unique()
#print(len(songs))

#Cross-evaluation - 5 Fold
#Dividing the data into train and test

train_data, test_data = train_test_split(song_df, test_size=0.20, random_state=0)
print(train_data.head(5))
